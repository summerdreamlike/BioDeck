"""
认证相关路由
"""
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from services.auth_service import AuthService
import traceback

# 令牌刷新端点
@api.route('/auth/refresh', methods=['POST'])
def refresh_token():
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        if not data.get('refresh_token'):
            raise ApiError('缺少必填字段: refresh_token', code=ErrorCode.VALIDATION_ERROR)
        
        refresh_token = data.get('refresh_token')
        result = AuthService.refresh_token(refresh_token)
        
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"令牌刷新失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('令牌刷新失败', code=ErrorCode.OPERATION_FAILED)

# 登出端点
@api.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    identity = get_jwt_identity()
    user_id = identity['id']
    
    result = AuthService.logout(user_id)
    return ok_response(result)

# 修改密码端点
@api.route('/auth/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """
    修改用户密码
    
    请求体:
    {
        "old_password": "旧密码",
        "new_password": "新密码"
    }
    """
    identity = get_jwt_identity()
    user_id = identity['id']
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        required_fields = ['old_password', 'new_password']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        # 调用服务层修改密码
        result = AuthService.change_password(user_id, old_password, new_password)
        
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"修改密码失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError("修改密码失败", code=ErrorCode.OPERATION_FAILED)

# 统一注册接口
@api.route('/auth/register', methods=['POST'])
def register_user():
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        required_fields = ['name', 'id_number', 'password', 'role']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        # 验证角色
        role = data.get('role')
        if role not in ['student', 'teacher']:
            raise ApiError("无效的用户角色，只能是 student 或 teacher", code=ErrorCode.VALIDATION_ERROR)
        
        # 验证学号/教职工号格式
        id_number = data.get('id_number')
        if role == 'student' and not id_number.startswith('1001'):
            raise ApiError("学号必须以1001开头", code=ErrorCode.VALIDATION_ERROR)
        elif role == 'teacher' and not id_number.startswith('2001'):
            raise ApiError("教职工号必须以2001开头", code=ErrorCode.VALIDATION_ERROR)
        
        # 调用服务层注册
        result = AuthService.register(data)
        
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"注册失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError(f"注册失败: {str(e)}", code=ErrorCode.OPERATION_FAILED)

# 保留旧的注册端点以保持向后兼容，但内部调用新的统一接口
@api.route('/auth/student/register', methods=['POST'])
def register_student():
    data = request.get_json() or {}
    data['role'] = 'student'
    return register_user()

@api.route('/auth/teacher/register', methods=['POST'])
def register_teacher():
    data = request.get_json() or {}
    data['role'] = 'teacher'
    return register_user()

# 登录接口
@api.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        required_fields = ['name_or_id', 'password', 'role']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        name_or_id = data.get('name_or_id')
        password = data.get('password')
        role = data.get('role')
        
        # 验证角色
        if role not in ['student', 'teacher', 'admin']:
            raise ApiError("无效的用户角色", code=ErrorCode.VALIDATION_ERROR)
        
        # 调用服务层登录
        result = AuthService.login(name_or_id, password, role)
        
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"登录失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError("登录失败", code=ErrorCode.OPERATION_FAILED) 