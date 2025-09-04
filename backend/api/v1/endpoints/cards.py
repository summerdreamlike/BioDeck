"""
卡牌抽奖相关路由
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.card_system import CardSystem
from core.responses import success_response, error_response
from core.errors import ApiError

# 从主API导入
from ..api import api

@api.route('/cards/user-cards', methods=['GET'])
@jwt_required()
def get_user_cards():
    """获取用户拥有的卡片"""
    try:
        identity = get_jwt_identity()
        # 解析用户ID
        if ':' in identity:
            user_id = int(identity.split(':')[0])
        else:
            user_id = int(identity)
        
        cards = CardSystem.get_user_cards(user_id)
        return success_response(data={'cards': cards})
    except Exception as e:
        return error_response(str(e), 500)

@api.route('/cards/all-cards', methods=['GET'])
@jwt_required()
def get_all_cards():
    """获取所有卡片定义"""
    try:
        cards = CardSystem.get_all_cards()
        return success_response(data={'cards': cards})
    except Exception as e:
        return error_response(str(e), 500)

@api.route('/cards/collection-stats', methods=['GET'])
@jwt_required()
def get_user_collection_stats():
    """获取用户收集统计"""
    try:
        identity = get_jwt_identity()
        # 解析用户ID
        if ':' in identity:
            user_id = int(identity.split(':')[0])
        else:
            user_id = int(identity)
        
        stats = CardSystem.get_user_collection_stats(user_id)
        return success_response(data=stats)
    except Exception as e:
        return error_response(str(e), 500)

@api.route('/cards/user/points', methods=['GET'])
@jwt_required()
def get_user_points():
    """获取用户积分"""
    try:
        identity = get_jwt_identity()
        # 解析用户ID
        if ':' in identity:
            user_id = int(identity.split(':')[0])
        else:
            user_id = int(identity)
        
        from models.user import User
        points = User.get_user_points(user_id)
        return success_response(data={'points': points})
    except Exception as e:
        return error_response(str(e), 500)

@api.route('/cards/user/points', methods=['POST'])
@jwt_required()
def add_user_points():
    """增加用户积分"""
    try:
        identity = get_jwt_identity()
        # 解析用户ID
        if ':' in identity:
            user_id = int(identity.split(':')[0])
        else:
            user_id = int(identity)
        
        data = request.get_json() or {}
        points_to_add = data.get('points', 0)
        
        if points_to_add <= 0:
            return error_response('积分数量必须大于0', 400)
        
        from models.user import User
        new_points = User.update_user_points(user_id, points_to_add)
        return success_response(data={'points': new_points, 'added': points_to_add})
    except Exception as e:
        return error_response(str(e), 500)
