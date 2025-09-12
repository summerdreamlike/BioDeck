from flask import request, jsonify
from ..api import api
from services.ai_service import ai_service
from services.biology_qa_adapter import BiologyQAAdapter
import os
import tempfile

adapter = BiologyQAAdapter()


@api.route('/ai/ask', methods=['POST'])
def ai_ask():
    try:
        payload = request.get_json(force=True)
        question = payload.get('question', '').strip()
        session_id = payload.get('session_id', 'default')
        if not question:
            return jsonify({'error': '问题不能为空'}), 400
        history = ai_service.get_history(session_id)
        # 优先走真实模型适配器
        if adapter.ready:
            base_answer = adapter.ask(question, history)
        else:
            base_answer = ai_service.answer(question, history)
        # 生成结构化答案（预习/学习/复习 + Mermaid）
        answer = ai_service.generate_structured_answer(question, base_answer)
        ai_service.add_message(session_id, 'user', question)
        ai_service.add_message(session_id, 'assistant', answer)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/ai/history', methods=['GET'])
def ai_history():
    try:
        session_id = request.args.get('session_id', 'default')
        history = ai_service.get_history(session_id)
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/ai/clear-history', methods=['POST'])
def ai_clear_history():
    try:
        payload = request.get_json(silent=True) or {}
        session_id = payload.get('session_id', 'default')
        ai_service.clear_history(session_id)
        return jsonify({'message': '历史记录已清除'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api.route('/ai/upload-image', methods=['POST'])
def ai_upload_image():
    if not adapter.ready:
        return jsonify({'error': '未配置模型 API Key（MOONSHOT_API_KEY）'}), 501
    if 'image' not in request.files:
        return jsonify({'error': '未上传图片'}), 400
    image = request.files['image']
    question = request.form.get('question', '请解答这个生物学问题')
    session_id = request.form.get('session_id', 'default')
    # 保存到临时文件
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        image.save(tf.name)
        tmp_path = tf.name
    try:
        base_answer = adapter.process_image(tmp_path, question)
        answer = ai_service.generate_structured_answer(question, base_answer)
        # 记录到会话历史
        ai_service.add_message(session_id, 'user', f'图片问答：{question}')
        ai_service.add_message(session_id, 'assistant', answer)
        return jsonify({'answer': answer})
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass


