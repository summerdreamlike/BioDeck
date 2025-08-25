import sqlite3
import os

# 数据库路径
DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')

# 基础模型类
class BaseModel:
    @classmethod
    def get_db(cls):
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    
    @staticmethod
    def dict_from_row(row):
        return {key: row[key] for key in row.keys()} if row else None 