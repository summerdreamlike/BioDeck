"""
响应格式化模块
"""
from flask import jsonify, request as flask_request
from .errors import ErrorCode

def ok_response(data=None, message=None, code=ErrorCode.SUCCESS, meta=None, http_status=200):
    """统一成功响应格式"""
    response_body = {
        'code': code,
        'message': message or ErrorCode.get_message(code),
        'data': data,
    }
    if meta is not None:
        response_body['meta'] = meta
    return jsonify(response_body), http_status

# 为兼容性提供别名
success_response = ok_response

def error_response(message=None, code=ErrorCode.SERVER_ERROR, payload=None, http_status=None):
    """统一错误响应格式"""
    if http_status is None:
        # 根据错误码自动判断HTTP状态码
        if ErrorCode.is_client_error(code):
            http_status = 400
        elif ErrorCode.is_server_error(code):
            http_status = 500
        else:
            http_status = 400
    
    response_body = {
        'code': code,
        'message': message or ErrorCode.get_message(code),
        'data': payload or {}
    }
    return jsonify(response_body), http_status

def wants_envelope(req=None):
    try:
        req = req or flask_request
        val = (req.args.get('envelope') or '').strip().lower()
        return val in ('1', 'true', 'yes')
    except Exception:
        return False 