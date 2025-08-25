from datetime import datetime
from .base import BaseModel

class UserProfile(BaseModel):
    @classmethod
    def get_by_user_id(cls, user_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
        profile = cursor.fetchone()
        conn.close()
        return cls.dict_from_row(profile) if profile else None
    
    @classmethod
    def create_or_update(cls, user_id, profile_data):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 检查是否已存在
        cursor.execute('SELECT id FROM user_profiles WHERE user_id = ?', (user_id,))
        existing = cursor.fetchone()
        
        if existing:
            # 更新现有画像
            cursor.execute('''
                UPDATE user_profiles SET
                learning_level = ?, study_style = ?, preferred_time = ?, 
                preferred_material_type = ?, attendance_rate = ?, 
                avg_completion_rate = ?, avg_accuracy_rate = ?, 
                avg_focus_rate = ?, avg_score = ?, last_updated = ?
                WHERE user_id = ?
            ''', (
                profile_data.get('learning_level'),
                profile_data.get('study_style'),
                profile_data.get('preferred_time'),
                profile_data.get('preferred_material_type'),
                profile_data.get('attendance_rate'),
                profile_data.get('avg_completion_rate'),
                profile_data.get('avg_accuracy_rate'),
                profile_data.get('avg_focus_rate'),
                profile_data.get('avg_score'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                user_id
            ))
        else:
            # 创建新画像
            cursor.execute('''
                INSERT INTO user_profiles (
                    user_id, learning_level, study_style, preferred_time,
                    preferred_material_type, attendance_rate, avg_completion_rate,
                    avg_accuracy_rate, avg_focus_rate, avg_score, created_at, last_updated
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                profile_data.get('learning_level'),
                profile_data.get('study_style'),
                profile_data.get('preferred_time'),
                profile_data.get('preferred_material_type'),
                profile_data.get('attendance_rate'),
                profile_data.get('avg_completion_rate'),
                profile_data.get('avg_accuracy_rate'),
                profile_data.get('avg_focus_rate'),
                profile_data.get('avg_score'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
        
        conn.commit()
        conn.close()
        return True
    
    @classmethod
    def get_all_profiles(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT up.*, u.name as user_name, u.username
            FROM user_profiles up
            JOIN users u ON up.user_id = u.id
            ORDER BY up.last_updated DESC
        ''')
        profiles = [cls.dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return profiles 