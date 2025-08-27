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
            return f"细胞膜主要由磷脂双分子层与蛋白质构成，具有选择透过性。{tips}"
        if any(keyword in question for keyword in ['DNA', '遗传', '基因']):
            return f"遗传信息通常以DNA为载体，通过复制与表达传递性状。{tips}"
        if any(keyword in question for keyword in ['生态', '食物链', '群落']):
            return f"生态系统由生产者、消费者与分解者构成，能量沿食物链传递并逐级递减。{tips}"
        return f"问题已收到：{question}\n依据已知生物学常识进行概括：请聚焦关键概念与因果机制。{tips}"


ai_service = AiService()


