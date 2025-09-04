"""
每日签到相关路由
"""
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from core.auth import role_required, roles_required
from services.daily_checkin_service import DailyCheckinService
import traceback

# ================== 每日签到相关路由 ==================

# 获取用户签到状态
@api.route('/daily-checkin/status', methods=['GET'])
@jwt_required()
def get_checkin_status():
    """获取用户今日签到状态"""
    identity = get_jwt_identity()
    
    try:
        # 确保数据库表存在
        DailyCheckinService.ensure_tables()
        
        result = DailyCheckinService.get_user_checkin_status(identity)
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        current_app.logger.error(f"获取签到状态失败: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        raise ApiError('获取签到状态失败', code=ErrorCode.OPERATION_FAILED)

# 执行签到
@api.route('/daily-checkin/checkin', methods=['POST'])
@jwt_required()
def perform_checkin():
    """执行每日签到"""
    identity = get_jwt_identity()
    
    try:
        # 确保数据库表存在
        DailyCheckinService.ensure_tables()
        
        result = DailyCheckinService.perform_checkin(identity)
        return ok_response(result, message='签到成功！')
    except ApiError:
        raise
    except Exception as e:
        current_app.logger.error(f"签到失败: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        raise ApiError('签到失败', code=ErrorCode.OPERATION_FAILED)

# 获取签到历史
@api.route('/daily-checkin/history', methods=['GET'])
@jwt_required()
def get_checkin_history():
    """获取用户签到历史"""
    identity = get_jwt_identity()
    limit = request.args.get('limit', 30, type=int)
    
    try:
        result = DailyCheckinService.get_checkin_history(identity, limit)
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        current_app.logger.error(f"获取签到历史失败: {str(e)}")
        raise ApiError('获取签到历史失败', code=ErrorCode.OPERATION_FAILED)

# 获取积分历史
@api.route('/daily-checkin/point-history', methods=['GET'])
@jwt_required()
def get_point_history():
    """获取用户积分历史"""
    identity = get_jwt_identity()
    limit = request.args.get('limit', 50, type=int)
    
    try:
        result = DailyCheckinService.get_point_history(identity, limit)
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        current_app.logger.error(f"获取积分历史失败: {str(e)}")
        raise ApiError('获取积分历史失败', code=ErrorCode.OPERATION_FAILED)

# 获取积分排行榜
@api.route('/daily-checkin/leaderboard', methods=['GET'])
@jwt_required()
def get_leaderboard():
    """获取积分排行榜"""
    limit = request.args.get('limit', 20, type=int)
    
    try:
        result = DailyCheckinService.get_leaderboard(limit)
        return ok_response(result)
    except Exception as e:
        current_app.logger.error(f"获取排行榜失败: {str(e)}")
        raise ApiError('获取排行榜失败', code=ErrorCode.OPERATION_FAILED)

# ================== 管理员功能 ==================

# 重置用户积分（管理员功能）
@api.route('/daily-checkin/reset-points/<int:user_id>', methods=['POST'])
@jwt_required()
@roles_required(['admin'])
def reset_user_points(user_id):
    """重置用户积分（管理员功能）"""
    data = request.get_json() or {}
    new_points = data.get('points', 0)
    
    try:
        # 这里可以实现重置积分的逻辑
        # 暂时返回成功消息
        return ok_response({
            'user_id': user_id,
            'new_points': new_points
        }, message='积分重置成功')
    except Exception as e:
        current_app.logger.error(f"重置积分失败: {str(e)}")
        raise ApiError('重置积分失败', code=ErrorCode.OPERATION_FAILED)

# 获取签到统计（管理员功能）
@api.route('/daily-checkin/statistics', methods=['GET'])
@jwt_required()
@roles_required(['admin'])
def get_checkin_statistics():
    """获取签到统计信息（管理员功能）"""
    try:
        # 这里可以实现统计逻辑
        # 暂时返回基础统计信息
        return ok_response({
            'total_users': 0,
            'today_checkins': 0,
            'total_points_distributed': 0
        })
    except Exception as e:
        current_app.logger.error(f"获取统计信息失败: {str(e)}")
        raise ApiError('获取统计信息失败', code=ErrorCode.OPERATION_FAILED)
