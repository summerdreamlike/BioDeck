from flask import Flask, render_template, request, jsonify, Response, session
from flask_cors import CORS  # 添加CORS支持
import os
import json
import logging
from biology_qa import BiologyQASystem
from config import Config
from database import Database
import uuid
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 确保临时目录存在
Config.ensure_temp_dir()

app = Flask(__name__)
# 配置CORS，允许所有来源的请求
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"]
    }
})
app.secret_key = os.urandom(24)  # 用于session加密

# 创建生物问答系统实例和数据库实例
biology_qa = None
db = Database()

# 对话历史记录
conversation_history = {}

def initialize_biology_qa():
    global biology_qa
    if biology_qa is None:
        try:
            api_key = Config.get_api_key()
            if not api_key:
                raise ValueError("API密钥未设置")
            biology_qa = BiologyQASystem(api_key=api_key)
            logger.info("生物问答系统初始化成功")
        except Exception as e:
            logger.error(f"初始化生物问答系统失败: {str(e)}")
            raise

@app.route('/')
def index():
    # 确保每个访问者都有一个唯一的会话ID
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        question = data.get('question', '')
        session_id = data.get('session_id', 'default')
        
        if not question:
            return jsonify({'error': '问题不能为空'}), 400
            
        # 记录开始时间
        start_time = time.time()
        
        # 从数据库获取历史记录
        history = db.get_history(session_id)
        
        # 处理问题
        answer = biology_qa.ask(question, history)
        
        # 记录结束时间
        end_time = time.time()
        response_time = end_time - start_time
        logger.info(f"问题处理时间: {response_time:.2f}秒")
        
        # 保存到数据库
        db.add_message(session_id, 'user', question)
        db.add_message(session_id, 'assistant', answer)
        
        return jsonify({
            'answer': answer,
            'response_time': response_time
        })
        
    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    try:
        data = request.get_json()
        session_id = data.get('session_id', '')
        db.clear_history(session_id)
        return jsonify({"message": "历史记录已清除"})
    except Exception as e:
        logger.error(f"清除历史记录失败: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        session_id = request.args.get('session_id', 'default')
        history = db.get_history(session_id)
        return jsonify({"history": history})
    except Exception as e:
        logger.error(f"获取历史记录失败: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    global biology_qa
    
    # 确保biology_qa已初始化
    if biology_qa is None:
        try:
            api_key = Config.get_api_key()
            if not api_key:
                app.logger.error("API密钥未设置")
                return jsonify({"error": "API密钥未设置，请设置MOONSHOT_API_KEY环境变量"}), 401
            biology_qa = BiologyQASystem(api_key=api_key)
            app.logger.info("生物问答系统初始化成功")
        except Exception as e:
            app.logger.error(f"初始化生物问答系统失败: {str(e)}")
            return jsonify({"error": f"初始化生物问答系统失败: {str(e)}"}), 500
    
    if 'image' not in request.files:
        app.logger.error("未上传图片文件")
        return jsonify({"error": "未上传图片"}), 400
        
    image = request.files['image']
    question = request.form.get('question', '请解答这个生物学问题')
    session_id = request.form.get('session_id', str(uuid.uuid4()))
    stream = request.form.get('stream', 'false').lower() == 'true'
    
    if image.filename == '':
        app.logger.error("图片文件名为空")
        return jsonify({"error": "未选择图片"}), 400
    
    # 检查图片格式和大小
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    file_ext = image.filename.rsplit('.', 1)[1].lower() if '.' in image.filename else ''
    if file_ext not in allowed_extensions:
        app.logger.error(f"不支持的图片格式: {file_ext}")
        return jsonify({"error": f"不支持的图片格式，仅支持: {', '.join(allowed_extensions)}"}), 400
    
    # 检查文件大小（限制为10MB）
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes
    image.seek(0, os.SEEK_END)
    file_size = image.tell()
    image.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        app.logger.error(f"图片大小超过限制: {file_size} bytes")
        return jsonify({"error": "图片大小超过限制（最大10MB）"}), 400
    
    try:
        # 使用Config类的方法确保临时目录存在
        temp_dir = Config.ensure_temp_dir()
        app.logger.info(f"临时目录路径: {temp_dir}")
            
        # 使用唯一文件名保存上传的图片
        temp_filename = f"{uuid.uuid4()}.{file_ext}"
        temp_path = os.path.join(temp_dir, temp_filename)
        app.logger.info(f"保存图片到临时文件: {temp_path}")
        
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
            # 保存文件
            image.save(temp_path)
            # 验证文件是否成功保存
            if not os.path.exists(temp_path):
                raise Exception("文件保存失败，文件不存在")
            app.logger.info(f"图片保存成功，大小: {os.path.getsize(temp_path)} bytes")
            
            try:
                if stream:
                    def generate():
                        try:
                            for chunk in biology_qa.process_image_biology_question_stream(temp_path, question):
                                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                        finally:
                            # 在生成器完成后删除文件
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                    
                    return Response(generate(), mimetype='text/event-stream')
                else:
                    answer = biology_qa.process_image_biology_question(temp_path, question)
                    # 保存到数据库，移除[图片问题]前缀
                    db.add_message(session_id, 'user', question if question else '请解答这个生物学问题')
                    db.add_message(session_id, 'assistant', answer)
                    
                    # 删除临时文件
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    
                    return jsonify({"answer": answer})
            except Exception as e:
                app.logger.error(f"处理图片问题时出错: {str(e)}")
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                raise
        except Exception as e:
            app.logger.error(f"保存或处理图片时出错: {str(e)}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise
    except Exception as e:
        return jsonify({"error": f"处理图片时出错: {str(e)}"}), 500


if __name__ == '__main__':
    try:
        initialize_biology_qa()
        logger.info("可用的API端点:")
        logger.info("  POST /api/ask - 提问接口")
        logger.info("  POST /api/clear-history - 清除历史记录")
        logger.info("  POST /api/upload-image - 上传图片解题")
        logger.info(f"启动服务器: http://127.0.0.1:5000")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f"启动服务器失败: {str(e)}")