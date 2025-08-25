import os
import re
import base64
import logging
from openai import OpenAI
from config import Config
import json
from typing import List, Dict, Any
import httpx
import time
from functools import lru_cache

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BiologyQASystem:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.Client(timeout=30.0)
        self.knowledge_base = self._load_knowledge_base()
        self.cache = {}
        self.cache_timeout = 3600  # 缓存1小时
        logger.info(f"初始化生物问答系统，使用模型: moonshot-v1-32k")
        
    def _load_knowledge_base(self) -> Dict[str, Any]:
        try:
            # 使用根目录下的biology_knowledge_base.json
            knowledge_base_path = 'biology_knowledge_base.json'
            logger.info(f"尝试加载生物知识库: {knowledge_base_path}")
            with open(knowledge_base_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info("生物知识库加载成功")
                return data
        except Exception as e:
            logger.error(f"加载生物知识库失败: {str(e)}")
            return {"questions": []}
            
    @lru_cache(maxsize=1000)
    def _find_similar_problems(self, question: str) -> List[Dict[str, Any]]:
        """在知识库中查找相似问题，使用缓存和更高效的相似度计算"""
        try:
            # 预处理问题文本
            question = question.lower().strip()
            question_words = set(question.split())
            
            # 计算相似度并排序
            similar_problems = []
            for problem in self.knowledge_base.get("questions", []):
                problem_text = problem["question"].lower()
                problem_words = set(problem_text.split())
                
                # 计算Jaccard相似度
                intersection = len(question_words & problem_words)
                union = len(question_words | problem_words)
                similarity = intersection / union if union > 0 else 0
                
                # 如果相似度大于阈值，添加到结果中
                if similarity > 0.3:  # 设置相似度阈值
                    similar_problems.append((similarity, problem))
            
            # 按相似度排序并返回前2个
            similar_problems.sort(key=lambda x: x[0], reverse=True)
            return [p[1] for p in similar_problems[:2]]
            
        except Exception as e:
            logger.error(f"查找相似问题时出错: {str(e)}")
            return []
        
    def ask(self, question: str, history: List[Dict[str, str]] = None) -> str:
        """处理生物学问题"""
        try:
            # 检查缓存
            current_time = time.time()
            if question in self.cache:
                cached_answer, timestamp = self.cache[question]
                if current_time - timestamp < self.cache_timeout:
                    logger.info("使用缓存回答")
                    return cached_answer
            
            # 在知识库中查找相似问题
            similar_problems = self._find_similar_problems(question)
            
            # 构建提示
            prompt = self._build_prompt(question, similar_problems, history)
            
            # 调用API
            response = self._call_api(prompt)
            
            # 更新缓存
            self.cache[question] = (response, current_time)
            
            return response
            
        except Exception as e:
            logger.error(f"处理问题失败: {str(e)}")
            return f"抱歉，处理问题时出现错误：{str(e)}"
            
    def _build_prompt(self, question: str, similar_problems: List[Dict[str, Any]], history: List[Dict[str, str]] = None) -> str:
        """构建提示"""
        prompt = "你是一个专业的高中生物学老师，请回答以下生物学问题。\n\n"
        
        # 添加相似问题的解答
        if similar_problems:
            prompt += "以下是一些相关的示例：\n"
            for problem in similar_problems:
                prompt += f"问题：{problem['question']}\n"
                prompt += f"解答：{problem['answer']}\n"
                prompt += f"解释：{problem['explanation']}\n\n"
                
        prompt += f"现在请回答这个问题：{question}\n"
        prompt += "请给出详细的解答步骤和解释，包括相关的生物学概念和原理。"
        
        return prompt
        
    def _call_api(self, prompt: str) -> str:
        """调用API"""
        try:
            response = self.client.post(
                "https://api.moonshot.cn/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "moonshot-v1-32k",
                    "messages": [
                        {"role": "system", "content": "你是一个专业的高中生物学老师，擅长解答各种生物学问题，包括细胞生物学、遗传学、生态学、进化论等。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000  # 减少token数量
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                logger.error(f"API调用失败: {response.status_code} - {response.text}")
                return "抱歉，API调用失败，请稍后重试。"
                
        except Exception as e:
            logger.error(f"API调用异常: {str(e)}")
            return f"抱歉，API调用异常：{str(e)}"
            
    def clear_history(self):
        """清除历史记录"""
        self.client = httpx.Client(timeout=30.0)
    
    def is_biology_question(self, query):
        """
        判断是否为生物学问题
        :param query: 用户输入的问题
        :return: 布尔值，表示是否为生物学问题
        """
        # 生物学问题的特征模式
        biology_patterns = [
            r'\b(细胞|组织|器官|系统|生物体)\b',  # 生物结构层次
            r'\b(蛋白质|核酸|糖类|脂质|酶)\b',  # 生物分子
            r'\b(基因|DNA|RNA|染色体|遗传)\b',  # 遗传学
            r'\b(细胞分裂|有丝分裂|减数分裂|受精)\b',  # 细胞过程
            r'\b(光合作用|呼吸作用|新陈代谢)\b',  # 代谢过程
            r'\b(生态系统|种群|群落|生物圈)\b',  # 生态学
            r'\b(进化|自然选择|适应|变异)\b',  # 进化论
            r'\b(植物|动物|微生物|真菌)\b',  # 生物分类
            r'\b(激素|神经|免疫|消化)\b',  # 生理学
            r'\b(实验|观察|显微镜|培养)\b',  # 实验方法
            r'\b(疾病|病毒|细菌|感染)\b',  # 病理学
            r'\b(环境|污染|保护|可持续发展)\b',  # 环境生物学
        ]
        
        for pattern in biology_patterns:
            if re.search(pattern, query):
                return True
        return False
    
    def format_biology_response(self, response):
        """
        格式化生物学回答，确保专业术语正确显示
        :param response: 原始回答
        :return: 格式化后的回答
        """
        # 检测常见的生物学术语并格式化
        # 替换常见的生物学符号和术语
        replacements = {
            # 化学分子式
            r'\bH2O\b': r'H₂O',  # 水分子
            r'\bCO2\b': r'CO₂',  # 二氧化碳
            r'\bO2\b': r'O₂',  # 氧气
            r'\bN2\b': r'N₂',  # 氮气
            r'\bCH4\b': r'CH₄',  # 甲烷
            r'\bNH3\b': r'NH₃',  # 氨气
            
            # 生物学术语
            r'\bDNA\b': r'**DNA**',  # DNA
            r'\bRNA\b': r'**RNA**',  # RNA
            r'\bATP\b': r'**ATP**',  # ATP
            r'\bADP\b': r'**ADP**',  # ADP
            r'\bNAD\b': r'**NAD**',  # NAD
            r'\bNADP\b': r'**NADP**',  # NADP
            
            # 希腊字母
            r'\b(alpha|α)\b': r'α',  # alpha
            r'\b(beta|β)\b': r'β',  # beta
            r'\b(gamma|γ)\b': r'γ',  # gamma
            r'\b(delta|δ)\b': r'δ',  # delta
            
            # 化学符号
            r'\bH\+\b': r'H⁺',  # 氢离子
            r'\bOH-\b': r'OH⁻',  # 氢氧根离子
            r'\bNa\+\b': r'Na⁺',  # 钠离子
            r'\bK\+\b': r'K⁺',  # 钾离子
            r'\bCa\+\+': r'Ca²⁺',  # 钙离子
            r'\bCl-\b': r'Cl⁻',  # 氯离子
            
            # 生物学过程
            r'\b(光合作用)\b': r'**光合作用**',
            r'\b(呼吸作用)\b': r'**呼吸作用**',
            r'\b(细胞分裂)\b': r'**细胞分裂**',
            r'\b(有丝分裂)\b': r'**有丝分裂**',
            r'\b(减数分裂)\b': r'**减数分裂**',
            r'\b(基因表达)\b': r'**基因表达**',
            r'\b(蛋白质合成)\b': r'**蛋白质合成**',
            
            # 生物学结构
            r'\b(细胞膜)\b': r'**细胞膜**',
            r'\b(细胞核)\b': r'**细胞核**',
            r'\b(线粒体)\b': r'**线粒体**',
            r'\b(叶绿体)\b': r'**叶绿体**',
            r'\b(内质网)\b': r'**内质网**',
            r'\b(高尔基体)\b': r'**高尔基体**',
            r'\b(溶酶体)\b': r'**溶酶体**',
            r'\b(核糖体)\b': r'**核糖体**',
        }
        
        formatted_response = response
        for pattern, replacement in replacements.items():
            formatted_response = re.sub(pattern, replacement, formatted_response, flags=re.IGNORECASE)
            
        return formatted_response
    
    def process_image_biology_question(self, image_path, question):
        """
        处理图像中的生物学问题（如实验图片、结构图等）
        :param image_path: 图像路径
        :param question: 附加问题描述
        :return: 回答
        """
        if not os.path.exists(image_path):
            error_msg = f"图像文件不存在: {image_path}"
            logger.error(error_msg)
            return error_msg
            
        try:
            # 检查文件大小
            file_size = os.path.getsize(image_path)
            if file_size == 0:
                error_msg = "图像文件为空"
                logger.error(error_msg)
                return error_msg
                
            logger.info(f"开始处理图像，文件大小: {file_size} 字节")
            
            # 获取文件扩展名
            file_ext = os.path.splitext(image_path)[1].lower()
            mime_type = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif'
            }.get(file_ext)
            
            if not mime_type:
                error_msg = f"不支持的图像格式: {file_ext}"
                logger.error(error_msg)
                return error_msg
            
            # 对图片进行base64编码
            try:
                with open(image_path, 'rb') as f:
                    img_base = base64.b64encode(f.read()).decode('utf-8')
                logger.info("图像base64编码成功")
            except Exception as e:
                error_msg = f"图像编码失败: {str(e)}"
                logger.error(error_msg)
                return error_msg
            
            # 使用配置中的视觉模型
            vision_model = Config.VISION_MODEL
            logger.info(f"使用视觉模型: {vision_model}")
            
            # 构建系统提示，增强生物学问题解答能力
            system_prompt = "你是一个专业的生物学问答助手，擅长解答图像中的生物学问题。请提供详细的解答步骤和准确的答案。对于复杂的生物学问题，请尽可能展示完整的分析过程。"
            
            try:
                response = self.client.post(
                    "https://api.moonshot.cn/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": vision_model,
                        "messages": [
                            {
                                "role": "system",
                                "content": system_prompt
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:{mime_type};base64,{img_base}"
                                        }
                                    },
                                    {
                                        "type": "text",
                                        "text": f"这是一个生物学问题，请解答：{question}。请提供详细的解答步骤和分析过程。"
                                    }
                                ]
                            }
                        ],
                        "temperature": 0.7,
                        "max_tokens": 1000
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result["choices"][0]["message"]["content"]
                    logger.info("成功获取模型响应")
                else:
                    error_msg = f"API调用失败: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    return error_msg
                
            except Exception as e:
                error_msg = f"调用视觉模型API失败: {str(e)}"
                logger.error(error_msg)
                return error_msg
            
            if not answer:
                error_msg = "模型返回的答案为空"
                logger.error(error_msg)
                return error_msg
            
            # 如果是生物学问题，格式化回答
            try:
                formatted_answer = self.format_biology_response(answer)
                logger.info("答案格式化成功")
                return formatted_answer
            except Exception as e:
                error_msg = f"格式化答案失败: {str(e)}"
                logger.error(error_msg)
                return error_msg
                
        except Exception as e:
            error_msg = f"处理图像时出错: {str(e)}"
            logger.error(error_msg)
            return error_msg
    
    def process_question(self, question):
        """
        处理生物学问题
        :param question: 问题文本
        :return: 回答
        """
        try:
            # 使用配置中的模型
            model = Config.DEFAULT_MODEL
            logger.info(f"使用模型: {model}")
            
            # 构建系统提示，增强生物学问题解答能力
            system_prompt = "你是一个专业的生物学问答助手，擅长解答生物学问题。请提供详细的解答步骤和准确的答案。对于复杂的生物学问题，请尽可能展示完整的分析过程。"
            
            response = self.client.chat.completions.create(
                model=model, 
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )
            
            if not response.choices:
                return "抱歉，无法获取回答。"
                
            answer = response.choices[0].message.content
            
            # 如果是生物学问题，格式化回答
            formatted_answer = self.format_biology_response(answer)
            
            return formatted_answer
        except Exception as e:
            logger.error(f"处理问题时出错: {str(e)}")
            return f"处理问题时出错: {str(e)}"
    
    def process_question_stream(self, question):
        """
        流式处理生物学问题
        :param question: 问题文本
        :return: 生成器，产生回答的各个部分
        """
        try:
            # 使用配置中的模型
            model = Config.DEFAULT_MODEL
            logger.info(f"使用流式模型: {model}")
            
            # 构建系统提示，增强生物学问题解答能力
            system_prompt = "你是一个专业的生物学问答助手，擅长解答生物学问题。请提供详细的解答步骤和准确的答案。对于复杂的生物学问题，请尽可能展示完整的分析过程。请分点作答，使答案更加清晰。"
            
            response = self.client.chat.completions.create(
                model=model, 
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                stream=True
            )
            
            current_chunk = ""
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    current_chunk += content
                    
                    # 当遇到段落结束符或句子结束符时，发送当前块
                    if content.endswith('\n\n') or content.endswith('。') or content.endswith('：'):
                        yield current_chunk
                        current_chunk = ""
            
            # 发送最后一块（如果有）
            if current_chunk:
                yield current_chunk
                
        except Exception as e:
            logger.error(f"流式处理问题时出错: {str(e)}")
            yield f"处理问题时出错: {str(e)}"
    
    def process_image_biology_question_stream(self, image_path, question):
        """
        流式处理图像中的生物学问题
        :param image_path: 图像路径
        :param question: 附加问题描述
        :return: 生成器，产生回答的各个部分
        """
        if not os.path.exists(image_path):
            error_msg = f"图像文件不存在: {image_path}"
            logger.error(error_msg)
            yield error_msg
            return
            
        try:
            # 检查文件大小
            file_size = os.path.getsize(image_path)
            if file_size == 0:
                error_msg = "图像文件为空"
                logger.error(error_msg)
                yield error_msg
                return
                
            logger.info(f"开始流式处理图像，文件大小: {file_size} 字节")
            
            # 获取文件扩展名
            file_ext = os.path.splitext(image_path)[1].lower()
            mime_type = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif'
            }.get(file_ext)
            
            if not mime_type:
                error_msg = f"不支持的图像格式: {file_ext}"
                logger.error(error_msg)
                yield error_msg
                return
            
            # 对图片进行base64编码
            try:
                with open(image_path, 'rb') as f:
                    img_base = base64.b64encode(f.read()).decode('utf-8')
                logger.info("图像base64编码成功")
            except Exception as e:
                error_msg = f"图像编码失败: {str(e)}"
                logger.error(error_msg)
                yield error_msg
                return
            
            # 使用配置中的视觉模型
            vision_model = Config.VISION_MODEL
            logger.info(f"使用流式视觉模型: {vision_model}")
            
            # 构建系统提示，增强生物学问题解答能力
            system_prompt = "你是一个专业的生物学问答助手，擅长解答图像中的生物学问题。请提供详细的解答步骤和准确的答案。对于复杂的生物学问题，请尽可能展示完整的分析过程。请分点作答，使答案更加清晰。"
            
            try:
                response = self.client.chat.completions.create(
                    model=vision_model, 
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{mime_type};base64,{img_base}"
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": f"这是一个生物学问题，请解答：{question}。请提供详细的解答步骤和分析过程，并分点作答。"
                                }
                            ]
                        }
                    ],
                    stream=True
                )
                logger.info("成功获取流式模型响应")
            except Exception as e:
                error_msg = f"调用视觉模型API失败: {str(e)}"
                logger.error(error_msg)
                yield error_msg
                return
            
            current_chunk = ""
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    current_chunk += content
                    
                    # 当遇到段落结束符或句子结束符时，发送当前块
                    if content.endswith('\n\n') or content.endswith('。') or content.endswith('：'):
                        yield current_chunk
                        current_chunk = ""
            
            # 发送最后一块（如果有）
            if current_chunk:
                yield current_chunk
                
        except Exception as e:
            error_msg = f"流式处理图像时出错: {str(e)}"
            logger.error(error_msg)
            yield error_msg

# 使用示例
if __name__ == "__main__":
    # 创建生物问答系统实例
    biology_qa = BiologyQASystem()
    
    # 标准问答示例
    print("=== 标准问答示例 ===")
    question = "什么是细胞呼吸？"
    print(f"问题: {question}")
    answer = biology_qa.ask(question)
    print(f"回答: {answer}\n")
    
    # 连续对话示例
    print("=== 连续对话示例 ===")
    follow_up = "细胞呼吸的三个阶段是什么？"
    print(f"问题: {follow_up}")
    answer = biology_qa.ask(follow_up)
    print(f"回答: {answer}\n")
    
    # 流式回答示例（在实际应用中可能需要异步处理）
    print("=== 流式回答示例 ===")
    question = "解释光合作用的过程"
    print(f"问题: {question}")
    print("回答开始流式输出...")
    for partial_response in biology_qa.ask(question, stream=True):
        # 在实际应用中，这里可以逐步更新UI显示
        pass
    print("流式回答完成\n")
    
    # 清除历史
    biology_qa.clear_history() 