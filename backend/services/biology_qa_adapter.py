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
            '你是一名专业的高中生物老师，请条理清晰地回答问题，必要时分点作答。',
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
        parts.append('请给出准确、简练、条理清晰的回答，并强调关键概念与因果机制。')
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
        system_prompt = '你是生物学问答助手。'
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
            { 'type': 'text', 'text': f'这是一个生物学问题，请解答：{question}。请分点作答。' }
        ]
        payload = {
            'model': self.vision_model,
            'messages': [
                { 'role': 'system', 'content': '你是生物学图像问答助手。' },
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


