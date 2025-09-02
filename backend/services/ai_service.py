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


ai_service = AiService()


