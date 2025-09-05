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

# 服务层
from services.card_service import CardService

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
def get_all_cards_legacy():
    """获取所有卡片定义（兼容旧路由）"""
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

# ===================== 前端要求的新路由 =====================

@api.route('/cards/collection', methods=['GET'])
@jwt_required()
def api_get_collection():
    """组合返回用户卡牌与统计信息，满足前端 cardApi.getUserCollection"""
    try:
        identity = get_jwt_identity()
        user_id = int(identity.split(':')[0]) if ':' in identity else int(identity)
        data = CardService.get_user_collection(user_id)
        return success_response(data=data)
    except ApiError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)

@api.route('/cards/all', methods=['GET'])
@jwt_required()
def api_get_all():
    try:
        data = CardService.get_all_cards()
        return success_response(data=data)
    except ApiError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)

@api.route('/cards/draw/single', methods=['POST'])
@jwt_required()
def api_draw_single():
    try:
        identity = get_jwt_identity()
        user_id = int(identity.split(':')[0]) if ':' in identity else int(identity)
        data = CardService.single_draw(user_id)
        # 统一前端期望的字段：单抽直接返回 card 字段
        return success_response(data={'card': data.get('card') if 'card' in data else data, **data})
    except ApiError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)

@api.route('/cards/draw/ten', methods=['POST'])
@jwt_required()
def api_draw_ten():
    try:
        identity = get_jwt_identity()
        user_id = int(identity.split(':')[0]) if ':' in identity else int(identity)
        data = CardService.ten_draw(user_id)
        return success_response(data=data)
    except ApiError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)

@api.route('/cards/draw/history', methods=['GET'])
@jwt_required()
def api_draw_history():
    try:
        identity = get_jwt_identity()
        user_id = int(identity.split(':')[0]) if ':' in identity else int(identity)
        limit = int(request.args.get('limit', 50))
        data = CardService.get_draw_history(user_id, limit)
        return success_response(data=data)
    except ApiError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response(str(e), 500)

@api.route('/cards/draw/costs', methods=['GET'])
@jwt_required()
def api_draw_costs():
    try:
        data = CardService.get_draw_costs()
        return success_response(data=data)
    except Exception as e:
        return error_response(str(e), 500)
