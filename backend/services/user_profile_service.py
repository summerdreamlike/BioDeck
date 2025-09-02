from models.user_profile import UserProfile
from models.study import StudyData
from models.daily_checkin import DailyCheckin
from models.material import Material
from models.user import User
import sqlite3
from datetime import datetime, timedelta

def init_user_profile_table():
    """初始化用户画像表"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            learning_level TEXT,
            study_style TEXT,
            preferred_time TEXT,
            preferred_material_type TEXT,
            attendance_rate REAL DEFAULT 0,
            avg_completion_rate REAL DEFAULT 0,
            avg_accuracy_rate REAL DEFAULT 0,
            avg_focus_rate REAL DEFAULT 0,
            avg_score REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

class UserProfileService:
    
    @staticmethod
    def analyze_user_profile(user_id):
        """分析用户画像"""
        profile_data = {}
        
        # 1. 分析学习能力画像
        learning_metrics = UserProfileService._analyze_learning_ability(user_id)
        profile_data.update(learning_metrics)
        
        # 2. 分析学习行为画像
        behavior_metrics = UserProfileService._analyze_learning_behavior(user_id)
        profile_data.update(behavior_metrics)
        
        # 3. 分析学习偏好画像
        preference_metrics = UserProfileService._analyze_learning_preferences(user_id)
        profile_data.update(preference_metrics)
        
        # 4. 生成综合画像标签
        profile_data['learning_level'] = UserProfileService._determine_learning_level(
            profile_data.get('avg_score', 0),
            profile_data.get('avg_completion_rate', 0)
        )
        
        profile_data['study_style'] = UserProfileService._determine_study_style(
            profile_data.get('avg_focus_rate', 0),
            profile_data.get('attendance_rate', 0)
        )
        
        return profile_data
    
    @staticmethod
    def _analyze_learning_ability(user_id):
        """分析学习能力指标"""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # 获取学习数据
        cursor.execute('''
            SELECT completion_rate, accuracy_rate, focus_rate, score
            FROM study_data 
            WHERE student_id = ?
            ORDER BY date DESC
            LIMIT 30
        ''', (user_id,))
        
        study_records = cursor.fetchall()
        conn.close()
        
        if not study_records:
            return {
                'avg_completion_rate': 0,
                'avg_accuracy_rate': 0,
                'avg_focus_rate': 0,
                'avg_score': 0
            }
        
        # 计算平均值
        total_completion = sum(record[0] for record in study_records)
        total_accuracy = sum(record[1] for record in study_records)
        total_focus = sum(record[2] for record in study_records)
        total_score = sum(record[3] for record in study_records)
        count = len(study_records)
        
        return {
            'avg_completion_rate': round(total_completion / count, 2),
            'avg_accuracy_rate': round(total_accuracy / count, 2),
            'avg_focus_rate': round(total_focus / count, 2),
            'avg_score': round(total_score / count, 2)
        }
    
    @staticmethod
    def _analyze_learning_behavior(user_id):
        """分析学习行为指标"""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # 计算出勤率
        cursor.execute('''
            SELECT COUNT(*) as total_sessions,
                   SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present_sessions
            FROM attendance 
            WHERE student_id = ?
        ''', (user_id,))
        
        attendance_result = cursor.fetchone()
        total_sessions = attendance_result[0] if attendance_result[0] else 0
        present_sessions = attendance_result[1] if attendance_result[1] else 0
        
        attendance_rate = round((present_sessions / total_sessions * 100), 2) if total_sessions > 0 else 0
        
        conn.close()
        
        return {
            'attendance_rate': attendance_rate
        }
    
    @staticmethod
    def _analyze_learning_preferences(user_id):
        """分析学习偏好"""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # 分析课件类型偏好（简化版，基于材料类型统计）
        cursor.execute('''
            SELECT m.type, COUNT(*) as view_count
            FROM materials m
            WHERE m.uploader_id = ? OR m.id IN (
                SELECT DISTINCT material_id FROM study_data WHERE student_id = ?
            )
            GROUP BY m.type
            ORDER BY view_count DESC
            LIMIT 1
        ''', (user_id, user_id))
        
        material_preference = cursor.fetchone()
        preferred_material_type = material_preference[0] if material_preference else 'unknown'
        
        # 分析学习时间偏好（简化版，基于最近的学习记录时间）
        cursor.execute('''
            SELECT strftime('%H', date) as hour
            FROM study_data 
            WHERE student_id = ?
            ORDER BY date DESC
            LIMIT 10
        ''', (user_id,))
        
        study_hours = [int(record[0]) for record in cursor.fetchall()]
        
        if study_hours:
            avg_hour = sum(study_hours) / len(study_hours)
            if avg_hour < 12:
                preferred_time = 'morning'
            elif avg_hour < 18:
                preferred_time = 'afternoon'
            else:
                preferred_time = 'evening'
        else:
            preferred_time = 'unknown'
        
        conn.close()
        
        return {
            'preferred_material_type': preferred_material_type,
            'preferred_time': preferred_time
        }
    
    @staticmethod
    def _determine_learning_level(avg_score, avg_completion_rate):
        """确定学习水平"""
        if avg_score >= 85 and avg_completion_rate >= 90:
            return '优秀'
        elif avg_score >= 70 and avg_completion_rate >= 75:
            return '良好'
        elif avg_score >= 60 and avg_completion_rate >= 60:
            return '一般'
        else:
            return '需要提升'
    
    @staticmethod
    def _determine_study_style(avg_focus_rate, attendance_rate):
        """确定学习风格"""
        if avg_focus_rate >= 80 and attendance_rate >= 90:
            return '专注型'
        elif avg_focus_rate >= 70 and attendance_rate >= 80:
            return '稳定型'
        elif avg_focus_rate >= 60 and attendance_rate >= 70:
            return '波动型'
        else:
            return '需要关注'
    
    @staticmethod
    def generate_user_profile(user_id):
        """生成用户画像"""
        # 分析用户数据
        profile_data = UserProfileService.analyze_user_profile(user_id)
        
        # 保存到数据库
        UserProfile.create_or_update(user_id, profile_data)
        
        return profile_data
    
    @staticmethod
    def get_user_profile(user_id):
        """获取用户画像"""
        profile = UserProfile.get_by_user_id(user_id)
        if not profile:
            # 如果不存在，生成新的画像
            return UserProfileService.generate_user_profile(user_id)
        return profile
    
    @staticmethod
    def get_all_profiles():
        """获取所有用户画像"""
        return UserProfile.get_all_profiles()
    
    @staticmethod
    def update_user_profile(user_id):
        """更新用户画像"""
        return UserProfileService.generate_user_profile(user_id) 