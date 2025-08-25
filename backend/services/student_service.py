"""
学生服务模块

负责学生信息管理、学习数据分析等功能
"""
from werkzeug.security import generate_password_hash
import traceback

from core.helpers import get_db, db_fetch_one, db_fetch_all
from core.errors import ApiError, ErrorCode
from models import Student, StudyData

class StudentService:
    @staticmethod
    def get_all_students():
        """
        获取所有学生
        
        :return: 学生列表
        """
        conn = get_db()
        cursor = conn.cursor()
        
        # 获取所有学生
        cursor.execute('SELECT * FROM users WHERE role = ?', ('student',))
        students = cursor.fetchall()
        result = [dict(student) for student in students]
        
        return result
    
    @staticmethod
    def get_student_rankings():
        """
        获取学生排名
        
        :return: 学生排名列表
        """
        conn = get_db()
        cursor = conn.cursor()
        
        # 获取学生排名
        cursor.execute('''
            SELECT u.id, u.username, u.student_id, 
                   AVG(s.completion_rate) as avg_completion,
                   AVG(s.accuracy_rate) as avg_accuracy,
                   AVG(s.focus_rate) as avg_focus,
                   AVG(s.score) as avg_score
            FROM users u
            LEFT JOIN study_data s ON u.id = s.user_id
            WHERE u.role = 'student'
            GROUP BY u.id
            ORDER BY avg_score DESC
        ''')
        
        rankings = cursor.fetchall()
        result = [dict(rank) for rank in rankings]
        
        return result
    
    @staticmethod
    def get_student_detail(student_id):
        """
        获取学生详情
        
        :param student_id: 学生ID
        :return: 学生详情
        """
        try:
            # 确保是从users表中查询学生
            student = db_fetch_one(
                'SELECT * FROM users WHERE id = ? AND role = ?', 
                (student_id, 'student')
            )
            
            if not student:
                raise ApiError('学生不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 获取学习数据
            study_data_records = db_fetch_all(
                'SELECT * FROM study_data WHERE user_id = ? ORDER BY date DESC LIMIT 30',
                (student_id,)
            )
            
            # 构建结果
            result = dict(student)
            result['study_data'] = [dict(data) for data in study_data_records]
            
            return result
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError('获取学生详情失败', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def create_student(data):
        """
        创建学生
        
        :param data: 学生数据
        :return: 新学生ID
        """
        # 生成随机密码或使用默认密码
        password = data.get('password', 'password123')
        hashed_password = generate_password_hash(password)
        
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, password, role, name, student_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                data.get('username', data['student_id']),  # 如果没提供用户名，使用学号
                hashed_password,
                'student',
                data['name'],
                data['student_id']
            ))
            
            new_id = cursor.lastrowid
            conn.commit()
            return new_id
        except Exception as e:
            conn.rollback()
            raise ApiError(str(e), code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def update_student(student_id, data):
        """
        更新学生信息
        
        :param student_id: 学生ID
        :param data: 学生数据
        :return: 是否成功
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 更新学生信息
            cursor.execute('''
                UPDATE users
                SET name = ?, student_id = ?
                WHERE id = ? AND role = ?
            ''', (
                data['name'],
                data['student_id'],
                student_id,
                'student'
            ))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise ApiError(str(e), code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def delete_student(student_id):
        """
        删除学生
        
        :param student_id: 学生ID
        :return: 是否成功
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 删除学生
            cursor.execute('DELETE FROM users WHERE id = ? AND role = ?', (student_id, 'student'))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise ApiError(str(e), code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_student_profile(student_id):
        """
        获取学生个人资料
        
        :param student_id: 学生ID
        :return: 学生个人资料
        """
        conn = get_db()
        cursor = conn.cursor()
        
        # 获取学生信息
        cursor.execute('SELECT * FROM users WHERE id = ? AND role = ?', (student_id, 'student'))
        student = cursor.fetchone()
        conn.close()
        
        if not student:
            raise ApiError('学生信息不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
        
        student_data = dict(student)
        
        return {'profile': student_data}
    
    @staticmethod
    def get_student_study_data(student_id):
        """
        获取学生学习数据
        
        :param student_id: 学生ID
        :return: 学生学习数据
        """
        conn = get_db()
        cursor = conn.cursor()
        
        # 获取学生ID
        cursor.execute('SELECT id FROM users WHERE id = ? AND role = ?', (student_id, 'student'))
        student = cursor.fetchone()
        
        if not student:
            conn.close()
            raise ApiError('学生信息不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
        
        # 获取学习数据
        cursor.execute('''
            SELECT * FROM study_data
            WHERE user_id = ?
            ORDER BY date DESC
        ''', (student['id'],))
        
        study_data = cursor.fetchall()
        result = [dict(data) for data in study_data]
        
        conn.close()
        return {'study_data': result} 