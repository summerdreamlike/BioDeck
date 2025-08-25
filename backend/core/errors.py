"""
错误处理模块
"""

# 统一错误码系统
class ErrorCode:
    # 成功
    SUCCESS = 0
    
    # 客户端错误 (4xx)
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    
    # 服务器错误 (5xx)
    SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    SERVICE_UNAVAILABLE = 503
    
    # 自定义业务错误码 (1000+)
    VALIDATION_ERROR = 1001
    DUPLICATE_ENTRY = 1002
    INVALID_CREDENTIALS = 1003
    TOKEN_EXPIRED = 1004
    RESOURCE_EXISTS = 1005
    RESOURCE_NOT_FOUND = 1006
    OPERATION_FAILED = 1007
    
    # 错误消息映射
    MESSAGES = {
        SUCCESS: "操作成功",
        BAD_REQUEST: "请求参数错误",
        UNAUTHORIZED: "未授权的访问",
        FORBIDDEN: "权限不足",
        NOT_FOUND: "资源不存在",
        METHOD_NOT_ALLOWED: "不支持的请求方法",
        CONFLICT: "资源冲突",
        UNPROCESSABLE_ENTITY: "请求参数验证失败",
        SERVER_ERROR: "服务器内部错误",
        NOT_IMPLEMENTED: "功能未实现",
        SERVICE_UNAVAILABLE: "服务不可用",
        VALIDATION_ERROR: "数据验证失败",
        DUPLICATE_ENTRY: "记录已存在",
        INVALID_CREDENTIALS: "用户名或密码错误",
        TOKEN_EXPIRED: "令牌已过期",
        RESOURCE_EXISTS: "资源已存在",
        RESOURCE_NOT_FOUND: "资源未找到",
        OPERATION_FAILED: "操作失败"
    }
    
    @staticmethod
    def get_message(code):
        """获取错误码对应的消息"""
        return ErrorCode.MESSAGES.get(code, "未知错误")
    
    @staticmethod
    def is_client_error(code):
        """判断是否为客户端错误"""
        return 400 <= code < 500 or 1000 <= code < 2000
    
    @staticmethod
    def is_server_error(code):
        """判断是否为服务器错误"""
        return 500 <= code < 600 or code >= 2000

# API错误异常
class ApiError(Exception):
    def __init__(self, message=None, code=ErrorCode.BAD_REQUEST, payload=None):
        self.code = code
        self.message = message or ErrorCode.get_message(code)
        self.payload = payload or {}
        super().__init__(self.message) 