"""
认证相关的中间件
"""
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from .errors import ApiError, ErrorCode

# 登录验证装饰器
def login_required(fn):
    """验证用户是否登录的装饰器"""
    @wraps(fn)
    def decorated(*args, **kwargs):
        # 验证令牌
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return decorated

# 角色验证装饰器
def role_required(role):
    """验证用户角色的装饰器"""
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            # 验证令牌
            verify_jwt_in_request()
            
            # 检查角色
            identity_str = get_jwt_identity()
            user_role = identity_str.split(':')[1]  # 解析用户角色
            if user_role != role:
                raise ApiError("权限不足", code=ErrorCode.FORBIDDEN, http_status=403)
            
            return fn(*args, **kwargs)
        return decorated
    return wrapper

# 多角色验证装饰器
def roles_required(roles):
    """验证用户多个角色的装饰器"""
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            # 验证令牌
            verify_jwt_in_request()
            
            # 检查角色
            identity_str = get_jwt_identity()
            user_role = identity_str.split(':')[1]  # 解析用户角色
            if user_role not in roles:
                raise ApiError("权限不足", code=ErrorCode.FORBIDDEN, http_status=403)
            
            return fn(*args, **kwargs)
        return decorated
    return wrapper 