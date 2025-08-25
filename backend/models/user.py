from .base import BaseModel
import sqlite3

class User(BaseModel):
    @classmethod
    def get_by_id(cls, user_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return cls.dict_from_row(user)
    
    @classmethod
    def get_by_username(cls, username):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        return cls.dict_from_row(user)
    
    @classmethod
    def get_by_name_or_id(cls, name_or_id, role):
        """根据姓名或学号/教职工号获取用户"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        if role == 'student':
            # 学生：支持姓名或学号登录
            cursor.execute('''
                SELECT * FROM users 
                WHERE (name = ? OR student_id = ?) AND role = ?
            ''', (name_or_id, name_or_id, role))
        else:
            # 教师：支持姓名或教职工号登录
            cursor.execute('''
                SELECT * FROM users 
                WHERE (name = ? OR teacher_id = ?) AND role = ?
            ''', (name_or_id, name_or_id, role))
        
        user = cursor.fetchone()
        conn.close()
        return cls.dict_from_row(user)
    
    @classmethod
    def check_id_exists(cls, id_number, role):
        """检查学号或教职工号是否已存在"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        if role == 'student':
            cursor.execute('SELECT id FROM users WHERE student_id = ?', (id_number,))
        else:
            cursor.execute('SELECT id FROM users WHERE teacher_id = ?', (id_number,))
        
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    
    @classmethod
    def get_next_class_number(cls):
        """获取下一个班级编号"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 获取当前最大班级编号
        cursor.execute('SELECT MAX(class_number) FROM users WHERE role = "student"')
        result = cursor.fetchone()
        max_class = result[0] if result[0] else 0
        
        conn.close()
        return max_class + 1
    
    @classmethod
    def assign_class(cls, role):
        """为学生分配班级（每30人一个班）"""
        if role != 'student':
            return None
            
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 获取当前班级的学生数量
        cursor.execute('''
            SELECT class_number, COUNT(*) as count 
            FROM users 
            WHERE role = 'student' AND class_number IS NOT NULL
            GROUP BY class_number
            ORDER BY class_number DESC
            LIMIT 1
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            # 第一个班级
            return 1
        else:
            current_class = result[0]
            current_count = result[1]
            
            if current_count >= 30:
                # 当前班级已满，创建新班级
                return current_class + 1
            else:
                # 当前班级未满，分配到当前班级
                return current_class
    
    @classmethod
    def create(cls, name, id_number, password, role):
        """创建用户（简化版）"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 检查学号/教职工号是否已存在
        if cls.check_id_exists(id_number, role):
            conn.close()
            raise ValueError(f"{'学号' if role == 'student' else '教职工号'}已存在")
        
        # 为学生分配班级
        class_number = cls.assign_class(role) if role == 'student' else None
        
        # 插入用户数据
        if role == 'student':
            cursor.execute('''
                INSERT INTO users (name, student_id, password, role, class_number) 
                VALUES (?, ?, ?, ?, ?)
            ''', (name, id_number, password, role, class_number))
        else:
            cursor.execute('''
                INSERT INTO users (name, teacher_id, password, role) 
                VALUES (?, ?, ?, ?)
            ''', (name, id_number, password, role))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id 