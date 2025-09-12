import os
import sqlite3
from datetime import datetime


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')


class AiService:
    def __init__(self):
        self._ensure_tables()

    def _get_conn(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def _ensure_tables(self):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS ai_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )'''
        )
        conn.commit()
        conn.close()

    def add_message(self, session_id: str, role: str, content: str):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO ai_messages (session_id, role, content, created_at) VALUES (?, ?, ?, ?)',
            (session_id, role, content, datetime.utcnow().isoformat())
        )
        conn.commit()
        conn.close()

    def get_history(self, session_id: str):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('SELECT role, content, created_at FROM ai_messages WHERE session_id = ? ORDER BY id ASC', (session_id,))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def clear_history(self, session_id: str):
        conn = self._get_conn()
        cur = conn.cursor()
        cur.execute('DELETE FROM ai_messages WHERE session_id = ?', (session_id,))
        conn.commit()
        conn.close()

    def answer(self, question: str, history: list):
        # 占位实现：根据问题和上下文返回一个简洁的示例回答
        # 后续可接入真正的大模型或参考项目 BiologyQASystem
        tips = '（示例回答，可在后端接入真实模型）'
        if any(keyword in question for keyword in ['细胞', '膜', '细胞膜']):
            return f"很好的问题！让我来为你解释一下细胞膜：\n\n1. 细胞膜就像我们家的门一样，它控制着什么东西能进进出出\n2. 想象一下，细胞膜是由两层脂肪分子组成的，就像三明治一样\n\n你觉得为什么细胞需要这样的保护呢？{tips}"
        if any(keyword in question for keyword in ['DNA', '遗传', '基因']):
            return f"哇，你问到了生命最神奇的部分！让我来为你解释：\n\n1. DNA就像一本生命的说明书，它告诉我们的身体怎么工作\n2. 想象一下，DNA就像一串长长的密码，每个基因就像书中的一个章节\n\n你有没有想过，为什么你和父母长得像呢？{tips}"
        if any(keyword in question for keyword in ['生态', '食物链', '群落']):
            return f"太棒了！让我来为你解释生态系统：\n\n1. 生态系统就像一个大社区，每个生物都有自己的工作\n2. 植物就像工厂，制造食物；动物就像消费者，吃这些食物\n\n想想看，如果其中一环断了，会发生什么呢？{tips}"
        return f"很好的问题！{question}\n\n让我用简单的话来解释一下：\n\n1. 在生物学中，我们经常要关注几个关键点\n2. 这个概念是什么？它怎么工作？为什么重要？\n\n你觉得这个问题的核心是什么呢？{tips}"

    # ===== 新增：结构化回答与 Mermaid 知识图谱 =====
    def generate_structured_answer(self, question: str, base_answer: str) -> str:
        """
        将基础回答包装为「预习 / 学习 / 复习」三段，并在末尾追加 Mermaid 知识图谱代码块。
        注：前端当前未内置 Mermaid 渲染器，此处先返回 markdown 文本，便于前端后续增强。
        """
        preview = self._build_preview_section(question)
        learning = self._build_learning_section(base_answer)
        review = self._build_review_section(question)
        mermaid = self._build_mermaid_graph(question, base_answer)

        parts = []
        parts.append(f"### 预习\n{preview}")
        parts.append(f"### 学习\n{learning}")
        parts.append(f"### 复习\n{review}")
        parts.append("### 知识图谱\n```mermaid\n" + mermaid + "\n```")
        return "\n\n".join(parts).strip()

    def _build_preview_section(self, question: str) -> str:
        return (
            "1. 学习目标：明确本节要理解的核心概念与基本原理。\n"
            "2. 先导问题：" + (question.strip() or "本节的核心问题是什么？") + "\n"
            "3. 关键词：提取2-4个相关术语，为后续学习做铺垫。"
        )

    def _build_learning_section(self, base_answer: str) -> str:
        base_answer = (base_answer or '').strip()
        if not base_answer:
            base_answer = "本节将围绕核心概念进行讲解，并通过生活实例帮助理解。"
        return (
            "1. 核心讲解：\n" + base_answer + "\n\n"
            "2. 机制与过程：用1-2句话描述关键机制或步骤。\n\n"
            "3. 生活化例子：联系真实情景加深理解。"
        )

    def _build_review_section(self, question: str) -> str:
        return (
            "1. 自测题：用自己的话回答——" + (question.strip() or "本节的核心问题是什么？") + "\n"
            "2. 易错点：区分概念边界，避免混淆。\n"
            "3. 拓展：可延伸到的相关主题或更高阶问题。"
        )

    def _build_mermaid_graph(self, question: str, base_answer: str) -> str:
        q = (question or '').strip()
        text = (base_answer or '')

        # 规则化的简单主题识别
        if any(k in q for k in ['细胞膜', '细胞', '膜']):
            return "\n".join([
                "graph TD",
                "A[细胞膜] --> B[磷脂双分子层]",
                "A --> C[膜蛋白]",
                "C --> D[物质转运]",
                "C --> E[信号传导]",
                "B --> F[流动镶嵌模型]"
            ])
        if any(k in q for k in ['DNA', '基因', '遗传']):
            return "\n".join([
                "graph TD",
                "A[DNA] --> B[复制]",
                "A --> C[转录]",
                "C --> D[翻译]",
                "D --> E[蛋白质]",
                "A --> F[遗传信息]"
            ])
        if any(k in q for k in ['生态', '食物链', '群落', '生态系统']):
            return "\n".join([
                "graph TD",
                "A[生态系统] --> B[生产者]",
                "A --> C[消费者]",
                "A --> D[分解者]",
                "B --> E[能量输入]",
                "B --> F[食物链]",
                "F --> G[能量流动]"
            ])
        # 默认通用知识图谱
        return "\n".join([
            "graph TD",
            "A[问题] --> B[核心概念]",
            "B --> C[关键机制]",
            "B --> D[实例与应用]",
            "C --> E[常见误区]",
            "D --> F[拓展与延伸]"
        ])


ai_service = AiService()


