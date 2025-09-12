from .base import BaseModel
from datetime import datetime
import sqlite3


class LevelRecord(BaseModel):
    """学生闯关记录模型
    字段：
      - id: 主键
      - student_id: 学生用户ID（关联 users.id）
      - level_name: 关卡名称
      - is_success: 本次记录是否成功（0/1）
      - failure_count: 累计失败次数（与该关卡相关）
      - last_attempt_time: 最近一次尝试时间
      - created_at: 记录创建时间
    约束：
      - (student_id, level_name) 唯一，用于追踪同一学生在同一关卡的累计信息
    """

    @classmethod
    def get_db(cls):
        from .base import DATABASE
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def ensure_tables(cls):
        """确保 level_records 表存在，并建立必要索引与唯一约束"""
        conn = cls.get_db()
        cur = conn.cursor()

        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS level_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                level_name TEXT NOT NULL,
                is_success INTEGER NOT NULL DEFAULT 0,
                failure_count INTEGER NOT NULL DEFAULT 0,
                last_attempt_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(student_id, level_name)
            )
            '''
        )

        # 索引
        cur.execute('CREATE INDEX IF NOT EXISTS idx_level_records_student ON level_records(student_id)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_level_records_level ON level_records(level_name)')

        conn.commit()
        conn.close()

    # ===== 基础查询方法 =====
    @classmethod
    def get_student_level_records(cls, student_id: int):
        """获取某学生的全部关卡记录"""
        conn = cls.get_db()
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM level_records WHERE student_id = ? ORDER BY last_attempt_time DESC',
            (student_id,)
        )
        rows = cur.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @classmethod
    def get_level_record(cls, student_id: int, level_name: str):
        """获取某学生某关卡的记录（不存在则返回 None）"""
        conn = cls.get_db()
        cur = conn.cursor()
        cur.execute(
            'SELECT * FROM level_records WHERE student_id = ? AND level_name = ? LIMIT 1',
            (student_id, level_name)
        )
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None

    # ===== 写入/更新方法 =====
    @classmethod
    def upsert_level_attempt(cls, student_id: int, level_name: str, is_success: bool):
        """记录一次闯关（成功或失败），并更新累计失败次数与最近尝试时间。
        成功：is_success=1 -> failure_count 保持不变
        失败：is_success=0 -> failure_count += 1
        若记录不存在则插入初始记录。
        返回最新记录 dict。
        """
        conn = cls.get_db()
        cur = conn.cursor()

        # 读取现有记录
        cur.execute(
            'SELECT id, failure_count FROM level_records WHERE student_id = ? AND level_name = ? LIMIT 1',
            (student_id, level_name)
        )
        row = cur.fetchone()

        now_str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        fail_inc = 0 if is_success else 1

        if row:
            # 更新
            new_failure_count = int(row['failure_count'] or 0) + fail_inc
            cur.execute(
                '''
                UPDATE level_records
                SET is_success = ?,
                    failure_count = ?,
                    last_attempt_time = ?
                WHERE id = ?
                ''',
                (1 if is_success else 0, new_failure_count, now_str, row['id'])
            )
        else:
            # 插入
            cur.execute(
                '''
                INSERT INTO level_records (student_id, level_name, is_success, failure_count, last_attempt_time)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (student_id, level_name, 1 if is_success else 0, fail_inc, now_str)
            )

        conn.commit()

        # 返回最新记录
        cur.execute(
            'SELECT * FROM level_records WHERE student_id = ? AND level_name = ? LIMIT 1',
            (student_id, level_name)
        )
        latest = cur.fetchone()
        conn.close()
        return dict(latest) if latest else None

    @classmethod
    def get_failure_counts_by_student(cls, student_id: int):
        """返回该学生各关卡失败次数映射：{ level_name: failure_count }"""
        conn = cls.get_db()
        cur = conn.cursor()
        cur.execute(
            'SELECT level_name, failure_count FROM level_records WHERE student_id = ?',
            (student_id,)
        )
        rows = cur.fetchall()
        conn.close()
        return {row['level_name']: int(row['failure_count'] or 0) for row in rows} 