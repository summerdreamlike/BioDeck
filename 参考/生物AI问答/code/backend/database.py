import sqlite3
import json
from datetime import datetime
import os

class Database:
    def __init__(self, db_path='chat_history.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # 创建对话历史表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def add_message(self, session_id, role, content):
        """添加新消息到历史记录"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO chat_history (session_id, role, content) VALUES (?, ?, ?)',
                (session_id, role, content)
            )
            conn.commit()
    
    def get_history(self, session_id, limit=50):
        """获取指定会话的历史记录"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT role, content, timestamp FROM chat_history WHERE session_id = ? ORDER BY timestamp DESC LIMIT ?',
                (session_id, limit)
            )
            return [{'role': row[0], 'content': row[1], 'timestamp': row[2]} for row in cursor.fetchall()]
    
    def clear_history(self, session_id=None):
        """清除历史记录"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if session_id:
                cursor.execute('DELETE FROM chat_history WHERE session_id = ?', (session_id,))
            else:
                cursor.execute('DELETE FROM chat_history')
            conn.commit()
    
    def get_session_ids(self):
        """获取所有会话ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT session_id FROM chat_history')
            return [row[0] for row in cursor.fetchall()] 