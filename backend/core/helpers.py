"""
辅助函数模块
"""
import os
import sqlite3
from datetime import datetime, timedelta
from flask import g, current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from .errors import ApiError, ErrorCode

# 数据库路径
DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')

# 数据库连接工具函数
def get_db():
    """获取数据库连接，如果当前请求中已有连接则复用"""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# 数据库操作工具函数
def db_execute(query, args=(), commit=False):
    """执行SQL查询并返回结果"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(query, args)
        if commit:
            conn.commit()
        return cursor
    except Exception as e:
        if commit:
            conn.rollback()
        raise e

def db_fetch_one(query, args=()):
    """执行查询并返回单条结果"""
    cursor = db_execute(query, args)
    return cursor.fetchone()

def db_fetch_all(query, args=()):
    """执行查询并返回所有结果"""
    cursor = db_execute(query, args)
    return cursor.fetchall()

def db_insert(query, args=()):
    """执行插入操作并返回新记录ID"""
    cursor = db_execute(query, args, commit=True)
    return cursor.lastrowid

def db_update(query, args=()):
    """执行更新操作并返回影响的行数"""
    cursor = db_execute(query, args, commit=True)
    return cursor.rowcount

def db_delete(query, args=()):
    """执行删除操作并返回影响的行数"""
    return db_update(query, args)

# 字段验证函数
def validate_required(data, required_fields):
    """验证必填字段"""
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
    return True

def validate_field(value, field_name, min_length=None, max_length=None, pattern=None):
    """验证字段值"""
    if value is None:
        raise ApiError(f"字段 {field_name} 不能为空", code=ErrorCode.VALIDATION_ERROR)
    
    if min_length is not None and len(str(value)) < min_length:
        raise ApiError(f"字段 {field_name} 长度不能小于 {min_length}", code=ErrorCode.VALIDATION_ERROR)
    
    if max_length is not None and len(str(value)) > max_length:
        raise ApiError(f"字段 {field_name} 长度不能大于 {max_length}", code=ErrorCode.VALIDATION_ERROR)
    
    if pattern is not None and not pattern.match(str(value)):
        raise ApiError(f"字段 {field_name} 格式不正确", code=ErrorCode.VALIDATION_ERROR)
    
    return True

def validate_datetime(value, field_name, format="%Y-%m-%d %H:%M:%S"):
    """验证日期时间字段"""
    try:
        datetime.strptime(value, format)
        return True
    except (ValueError, TypeError):
        raise ApiError(f"字段 {field_name} 必须是有效的日期时间格式 ({format})", code=ErrorCode.VALIDATION_ERROR)

# 用户认证相关函数
def create_tokens(user_id, role):
    """创建访问令牌和刷新令牌"""
    identity = {'id': user_id, 'role': role}
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    
    # 将刷新令牌存储到数据库
    expires_at = datetime.now() + timedelta(days=30)
    db_execute(
        'INSERT INTO refresh_tokens (user_id, token, expires_at) VALUES (?, ?, ?)',
        (user_id, refresh_token, expires_at),
        commit=True
    )
    
    return access_token, refresh_token

def get_user_info(user_id, role):
    """获取用户信息"""
    user = db_fetch_one('SELECT * FROM users WHERE id = ? AND role = ?', (user_id, role))
    if not user:
        return None
    
    user_info = {
        'id': user['id'],
        'username': user['username'],
        'role': user['role']
    }
    
    if user['name']:
        user_info['name'] = user['name']
    
    if user['role'] == 'student' and user['student_id']:
        user_info['student_id'] = user['student_id']
    
    return user_info 