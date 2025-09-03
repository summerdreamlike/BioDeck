from .base import BaseModel
from datetime import datetime, date
import sqlite3

class DailyCheckin(BaseModel):
    @classmethod
    def get_db(cls):
        from .base import DATABASE
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    
    @classmethod
    def ensure_tables(cls):
        """确保数据库表存在"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 创建每日签到记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                checkin_date DATE NOT NULL,
                checkin_time DATETIME NOT NULL,
                points_earned INTEGER NOT NULL DEFAULT 10,
                streak_days INTEGER NOT NULL DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, checkin_date)
            )
        ''')
        
        # 创建用户积分表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_points (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                total_points INTEGER NOT NULL DEFAULT 0,
                points_earned_today INTEGER NOT NULL DEFAULT 0,
                last_checkin_date DATE,
                current_streak INTEGER NOT NULL DEFAULT 0,
                longest_streak INTEGER NOT NULL DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建积分历史记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS point_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                points_change INTEGER NOT NULL,
                change_type TEXT NOT NULL,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    @classmethod
    def get_user_checkin_today(cls, user_id):
        """获取用户今日签到记录"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        today = date.today().isoformat()
        cursor.execute('''
            SELECT * FROM daily_checkins 
            WHERE user_id = ? AND checkin_date = ?
        ''', (user_id, today))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return dict(result)
        return None
    
    @classmethod
    def get_user_points(cls, user_id):
        """获取用户积分信息"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM user_points WHERE user_id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return dict(result)
        return None
    
    @classmethod
    def create_checkin(cls, user_id, points_earned, streak_days):
        """创建签到记录"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        today = date.today().isoformat()
        now = datetime.now().isoformat()
        
        # 插入签到记录
        cursor.execute('''
            INSERT INTO daily_checkins (user_id, checkin_date, checkin_time, points_earned, streak_days)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, today, now, points_earned, streak_days))
        
        checkin_id = cursor.lastrowid
        
        # 更新或创建用户积分记录
        cursor.execute('''
            INSERT OR REPLACE INTO user_points 
            (user_id, total_points, points_earned_today, last_checkin_date, current_streak, longest_streak, updated_at)
            VALUES (?, 
                    COALESCE((SELECT total_points FROM user_points WHERE user_id = ?), 0) + ?,
                    ?,
                    ?,
                    ?,
                    CASE WHEN ? > COALESCE((SELECT longest_streak FROM user_points WHERE user_id = ?), 0) 
                         THEN ? 
                         ELSE COALESCE((SELECT longest_streak FROM user_points WHERE user_id = ?), 0) 
                    END,
                    CURRENT_TIMESTAMP)
        ''', (user_id, user_id, points_earned, points_earned, today, streak_days, 
              streak_days, user_id, streak_days, user_id))
        
        # 记录积分历史
        cursor.execute('''
            INSERT INTO point_history (user_id, points_change, change_type, description)
            VALUES (?, ?, 'daily_checkin', '每日签到奖励')
        ''', (user_id, points_earned))
        
        conn.commit()
        conn.close()
        
        return checkin_id
    
    @classmethod
    def get_checkin_history(cls, user_id, limit=30):
        """获取用户签到历史"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM daily_checkins 
            WHERE user_id = ? 
            ORDER BY checkin_date DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    @classmethod
    def get_point_history(cls, user_id, limit=50):
        """获取用户积分历史"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM point_history 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    @classmethod
    def calculate_streak(cls, user_id):
        """计算用户连续签到天数"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT checkin_date FROM daily_checkins 
            WHERE user_id = ? 
            ORDER BY checkin_date DESC
        ''', (user_id,))
        
        dates = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if not dates:
            return 0
        
        # 计算连续天数
        streak = 1
        current_date = datetime.strptime(dates[0], '%Y-%m-%d').date()
        
        for i in range(1, len(dates)):
            prev_date = datetime.strptime(dates[i], '%Y-%m-%d').date()
            if (current_date - prev_date).days == 1:
                streak += 1
                current_date = prev_date
            else:
                break
        
        return streak
