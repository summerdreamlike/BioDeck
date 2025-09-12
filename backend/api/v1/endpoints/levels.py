"""
闯关记录相关路由
"""
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.responses import success_response, error_response
from core.errors import ApiError
from services.level_service import LevelService

# 从主API导入蓝图
from ..api import api

@api.route('/levels/records', methods=['GET'])
@jwt_required()
def get_my_level_records():
    try:
        identity = get_jwt_identity()
        data = LevelService.get_student_level_progress(identity)
        return success_response(data=data)
    except ApiError as e:
        return error_response(str(e), e.code)
    except Exception as e:
        return error_response(str(e))

@api.route('/levels/records/<string:level_name>', methods=['GET'])
@jwt_required()
def get_my_level_record(level_name):
    try:
        identity = get_jwt_identity()
        record = LevelService.get_level_record(identity, level_name)
        return success_response(data=record)
    except ApiError as e:
        return error_response(str(e), e.code)
    except Exception as e:
        return error_response(str(e))

@api.route('/levels/records', methods=['POST'])
@jwt_required()
def post_level_attempt():
    try:
        identity = get_jwt_identity()
        payload = request.get_json() or {}
        level_name = payload.get('level_name')
        is_success = bool(payload.get('is_success'))
        latest = LevelService.record_level_attempt(identity, level_name, is_success)
        return success_response(data=latest, message='记录已更新')
    except ApiError as e:
        return error_response(str(e), e.code)
    except Exception as e:
        return error_response(str(e)) 