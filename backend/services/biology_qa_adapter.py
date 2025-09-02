import os
import json
import base64
import requests
from functools import lru_cache


class BiologyQAAdapter:
    """
    轻量适配器：对接生物AI问答核心。实际模型调用请在此实现。

    环境变量：
      - MOONSHOT_API_KEY: 参考项目使用的 API Key 名称
    """

    def __init__(self):
        self.api_key = os.environ.get('MOONSHOT_API_KEY') or self._load_key_from_file()
        self.model = os.environ.get('BIO_QA_MODEL', 'moonshot-v1-32k')
        self.vision_model = os.environ.get('BIO_QA_VISION_MODEL', 'moonshot-v1-32k-vision')
        self.endpoint = os.environ.get('BIO_QA_ENDPOINT', 'https://api.moonshot.cn/v1/chat/completions')

    @property
    def ready(self) -> bool:
        return bool(self.api_key)

    def _load_key_from_file(self) -> str:
        candidates = [
            os.path.join(os.path.dirname(__file__), '.bio_api_key'),
            os.path.join(os.path.dirname(os.path.dirname(__file__)), '.bio_api_key'),
        ]
        for p in candidates:
            if os.path.exists(p):
                try:
                    with open(p, 'r', encoding='utf-8') as f:
                        key = f.read().strip()
                        if key:
                            return key
                except Exception:
                    pass
        return ''

    @lru_cache(maxsize=512)
    def _load_kb(self):
        # 可选知识库，放在项目根或 backend/services/ 下
        candidates = [
            os.path.join(os.path.dirname(os.path.dirname(__file__)), 'biology_knowledge_base.json'),
            os.path.join(os.path.dirname(__file__), 'biology_knowledge_base.json'),
        ]
        for p in candidates:
            if os.path.exists(p):
                try:
                    with open(p, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception:
                    pass
        return { 'questions': [] }

    def _build_prompt(self, question: str, history: list) -> str:
        kb = self._load_kb()
        # 简化：附带前2个相似问答（朴素包含判断）
        sims = []
        qlow = question.lower()
        for item in kb.get('questions', [])[:100]:
            if any(w and w in item.get('question','').lower() for w in qlow.split()[:3]):
                sims.append(item)
            if len(sims) >= 2:
                break
        parts = [
            '你是一位经验丰富的高中生物老师，专门负责线上教学。你采用费曼学习法来引导学生学习，即用简单易懂的语言解释复杂概念，通过提问和引导帮助学生自己发现答案。',
            '',
            '你的教学风格：',
            '1. 亲切友好，像朋友一样与学生交流',
            '2. 使用生动的比喻和日常生活中的例子',
            '3. 鼓励学生思考，不直接给出答案，而是引导他们自己得出结论',
            '4. 分步骤解释，确保每个概念都理解透彻',
            '5. 经常使用"你觉得呢？"、"想想看"等引导性语言',
            '6. 用简单的话说复杂的事，避免过于学术化的表达'
        ]
        if sims:
            parts.append('以下是相关示例以供参考：')
            for s in sims:
                parts.append(f"问题：{s.get('question','')}")
                if s.get('answer'):
                    parts.append(f"解答：{s['answer']}")
                if s.get('explanation'):
                    parts.append(f"解释：{s['explanation']}")
        if history:
            parts.append('已知对话要点：')
            for h in history[-4:]:
                parts.append(f"{h.get('role','user')}: {h.get('content','')}")
        parts.append(f"现在的问题：{question}")
        parts.append('请以生物老师的身份，用费曼学习法来回答这个问题。记住要亲切、引导性强，帮助学生真正理解概念。')
        return '\n'.join(parts)

    def _call_llm(self, system_prompt: str, user_content):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': self.model,
            'messages': [
                { 'role': 'system', 'content': system_prompt },
                { 'role': 'user', 'content': user_content }
            ],
            'temperature': 0.7,
            'max_tokens': 1000
        }
        r = requests.post(self.endpoint, headers=headers, json=payload, timeout=45)
        if r.status_code == 200:
            data = r.json()
            return data['choices'][0]['message']['content']
        return f'模型调用失败：{r.status_code} {r.text[:200]}'

    def ask(self, question: str, history: list) -> str:
        if not self.ready:
            return '未配置模型 API Key（MOONSHOT_API_KEY），已使用内置示例回答。'
        system_prompt = '你是一位经验丰富的高中生物老师，专门负责线上教学。你采用费曼学习法来引导学生学习，用简单易懂的语言解释复杂概念，通过提问和引导帮助学生自己发现答案。你的语气亲切友好，像朋友一样与学生交流。回答时要分点罗列，使用数字编号（1. 2. 3. 等），让回答结构清晰易懂。采用渐进式问答方式：不要一次性说完所有内容，而是分步骤引导学生思考，每个回答只讲1-2个要点，然后通过提问引导学生继续探索。回答内容要包含：先肯定学生的提问，用简单的话解释核心概念，举一个生活中的例子，引导学生思考相关问题，鼓励学生提出更多问题。但不要使用" 肯定学生的提问："这样的提示语，直接自然地表达内容。'
        prompt = self._build_prompt(question, history)
        return self._call_llm(system_prompt, prompt)

    def process_image(self, image_path: str, question: str) -> str:
        if not self.ready:
            return '未配置模型 API Key（MOONSHOT_API_KEY），图片问答不可用。'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        with open(image_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
        user_content = [
            { 'type': 'image_url', 'image_url': { 'url': f'data:image/png;base64,{b64}' } },
            { 'type': 'text', 'text': f'这是一个生物学问题：{question}。请以生物老师的身份，用费曼学习法来解答这个问题。用简单易懂的语言解释，举生活中的例子，并引导学生思考。' }
        ]
        payload = {
            'model': self.vision_model,
            'messages': [
                { 'role': 'system', 'content': '你是一位经验丰富的高中生物老师，专门负责线上教学。你采用费曼学习法来引导学生学习，用简单易懂的语言解释复杂概念。当看到生物学相关的图片时，你会用亲切友好的语气，通过生动的比喻和引导性问题来帮助学生理解图片中的生物学概念。回答时要分点罗列，使用数字编号（1. 2. 3. 等），让回答结构清晰易懂。采用渐进式问答方式：不要一次性说完所有内容，而是分步骤引导学生思考，每个回答只讲1-2个要点，然后通过提问引导学生继续探索。回答内容要包含：先肯定学生的提问，用简单的话解释核心概念，举一个生活中的例子，引导学生思考相关问题，鼓励学生提出更多问题。但不要使用"1. 肯定学生的提问："这样的提示语，直接自然地表达内容。' },
                { 'role': 'user', 'content': user_content }
            ],
            'temperature': 0.7,
            'max_tokens': 1000
        }
        r = requests.post(self.endpoint, headers=headers, json=payload, timeout=60)
        if r.status_code == 200:
            data = r.json()
            return data['choices'][0]['message']['content']
        return f'视觉模型调用失败：{r.status_code} {r.text[:200]}'


