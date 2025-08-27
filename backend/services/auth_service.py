"""
认证服务模块

负责用户认证、注册、令牌管理等功能
"""
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token

from core.helpers import db_fetch_one, db_execute, db_insert
from core.errors import ApiError, ErrorCode
from utils.date_utils import now

class AuthService:
    @staticmethod
    def login(name_or_id, password, role):
        """
        用户登录（支持姓名或学号/教职工号登录）
        
        :param name_or_id: 姓名或学号/教职工号
        :param password: 密码
        :param role: 角色
        :return: 用户信息和令牌
        """
        # 验证角色
        if role not in ['student', 'teacher', 'admin']:
            raise ApiError("无效的用户角色", code=ErrorCode.VALIDATION_ERROR)
        
        # 根据姓名或学号/教职工号查询用户
        if role == 'student':
            # 学生：支持姓名或学号登录
            user = db_fetch_one('''
                SELECT * FROM users 
                WHERE (name = ? OR student_id = ?) AND role = ?
            ''', (name_or_id, name_or_id, role))
        else:
            # 教师：支持姓名或教职工号登录
            user = db_fetch_one('''
                SELECT * FROM users 
                WHERE (name = ? OR teacher_id = ?) AND role = ?
            ''', (name_or_id, name_or_id, role))
        
        if not user:
            raise ApiError("用户不存在或密码错误", code=ErrorCode.INVALID_CREDENTIALS)
        
        # 验证密码
        password_ok = False
        try:
            password_ok = check_password_hash(user['password'], password)
        except Exception:
            # 兼容旧系统明文密码
            password_ok = (user['password'] == password)
        
        if not password_ok:
            raise ApiError("用户不存在或密码错误", code=ErrorCode.INVALID_CREDENTIALS)
        
        # 创建令牌
        access_token, refresh_token = AuthService.create_tokens(user['id'], user['role'])
        
        # 获取完整的用户信息
        user_info = AuthService.get_user_info(user['id'], user['role'])
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user_info
        }
    
    @staticmethod
    def register(data):
        """
        用户注册（简化版）
        
        :param data: 注册数据 {name, id_number, password, role}
        :return: 注册成功消息
        """
        name = data.get('name')
        id_number = data.get('id_number')
        password = data.get('password')
        role = data.get('role')
        
        # 验证必填字段
        if not all([name, id_number, password, role]):
            raise ApiError("缺少必填字段", code=ErrorCode.VALIDATION_ERROR)
        
        # 验证角色
        if role not in ['student', 'teacher']:
            raise ApiError("无效的用户角色", code=ErrorCode.VALIDATION_ERROR)
        
        # 验证学号/教职工号格式
        if role == 'student' and not id_number.startswith('1001'):
            raise ApiError("学号必须以1001开头", code=ErrorCode.VALIDATION_ERROR)
        elif role == 'teacher' and not id_number.startswith('2001'):
            raise ApiError("教职工号必须以2001开头", code=ErrorCode.VALIDATION_ERROR)
        
        # 检查学号/教职工号是否已存在
        if role == 'student':
            existing_user = db_fetch_one('SELECT * FROM users WHERE student_id = ?', (id_number,))
        else:
            existing_user = db_fetch_one('SELECT * FROM users WHERE teacher_id = ?', (id_number,))
        
        if existing_user:
            raise ApiError(f"{'学号' if role == 'student' else '教职工号'}已存在", code=ErrorCode.DUPLICATE_ENTRY)
        
        # 创建用户
        hashed_password = generate_password_hash(password)
        
        # 为学生分配班级
        if role == 'student':
            class_number = AuthService._assign_student_class()
            user_id = db_insert('''
                INSERT INTO users (username, name, student_id, password, role, class_number) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, name, id_number, hashed_password, role, class_number))
        else:
            user_id = db_insert('''
                INSERT INTO users (username, name, teacher_id, password, role) 
                VALUES (?, ?, ?, ?, ?)
            ''', (name, name, id_number, hashed_password, role))
        
        # 注册成功后不创建令牌，只返回成功消息
        return {
            'message': '注册成功',
            'user_id': user_id,
            'role': role
        }
    
    @staticmethod
    def _assign_student_class():
        """为学生分配班级（每30人一个班）"""
        # 获取当前班级的学生数量
        result = db_fetch_one('''
            SELECT class_number, COUNT(*) as count 
            FROM users 
            WHERE role = 'student' AND class_number IS NOT NULL
            GROUP BY class_number
            ORDER BY class_number DESC
            LIMIT 1
        ''')
        
        if not result:
            # 第一个班级
            return 1
        else:
            current_class = result['class_number']
            current_count = result['count']
            
            if current_count >= 30:
                # 当前班级已满，创建新班级
                return current_class + 1
            else:
                # 当前班级未满，分配到当前班级
                return current_class
    
    @staticmethod
    def refresh_token(refresh_token_str):
        """
        刷新令牌
        
        :param refresh_token_str: 刷新令牌
        :return: 新的访问令牌和用户信息
        """
        # 验证刷新令牌是否存在于数据库
        token_record = db_fetch_one(
            'SELECT * FROM refresh_tokens WHERE token = ? AND expires_at > ?',
            (refresh_token_str, now())
        )
        
        if not token_record:
            raise ApiError('无效或过期的刷新令牌', code=ErrorCode.TOKEN_EXPIRED)
        
        # 验证JWT刷新令牌
        decoded = decode_token(refresh_token_str)
        identity = decoded['sub']
        
        # 获取用户信息
        user_id = identity['id']
        role = identity['role']
        user_info = AuthService.get_user_info(user_id, role)
        
        if not user_info:
            raise ApiError('用户不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
        
        # 创建新的访问令牌
        access_token = create_access_token(identity={'id': user_id, 'role': role})
        
        return {
            'access_token': access_token,
            'user': user_info
        }
    
    @staticmethod
    def logout(user_id):
        """
        用户登出
        
        :param user_id: 用户ID
        """
        # 从数据库中删除用户的所有刷新令牌
        db_execute('DELETE FROM refresh_tokens WHERE user_id = ?', (user_id,), commit=True)
        
        return {'message': '登出成功'}
    
    @staticmethod
    def create_tokens(user_id, role):
        """
        创建访问令牌和刷新令牌
        
        :param user_id: 用户ID
        :param role: 用户角色
        :return: 访问令牌和刷新令牌
        """
        identity = {'id': user_id, 'role': role}
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        
        # 将刷新令牌存储到数据库
        expires_at = now() + timedelta(days=30)
        db_execute(
            'INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES (?, ?, ?)',
            (user_id, refresh_token, expires_at),
            commit=True
        )
        
        return access_token, refresh_token
    
    @staticmethod
    def get_user_info(user_id, role):
        """
        获取用户信息
        
        :param user_id: 用户ID
        :param role: 用户角色
        :return: 用户信息
        """
        user = db_fetch_one('SELECT * FROM users WHERE id = ? AND role = ?', (user_id, role))
        if not user:
            return None
        
        # 将 SQLite Row 对象转换为字典
        if hasattr(user, 'keys'):
            user_dict = dict(user)
        else:
            user_dict = user
        
        user_info = {
            'id': user_dict['id'],
            'name': user_dict['name'],
            'role': user_dict['role']
        }
        
        if user_dict['role'] == 'student':
            user_info['student_id'] = user_dict['student_id']
            user_info['class_number'] = user_dict.get('class_number')
        else:
            user_info['teacher_id'] = user_dict['teacher_id']
            # 教师也应该有班级信息
            user_info['class_number'] = user_dict.get('class_number')
        
        return user_info 