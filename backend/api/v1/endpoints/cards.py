"""
卡牌抽奖相关路由
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from core.auth import role_required, roles_required
from services.card_service import CardService
import traceback

# ================== 卡牌收集相关路由 ==================

# 获取用户卡牌收集
@api.route('/cards/collection', methods=['GET'])
@jwt_required()
def get_user_collection():
    """获取用户卡牌收集"""
    identity = get_jwt_identity()
    
    try:
        # 确保数据库表存在
        CardService.ensure_tables()
        
        result = CardService.get_user_collection(identity['id'])
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取卡牌收集失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('获取卡牌收集失败', code=ErrorCode.OPERATION_FAILED)

# 获取所有卡牌定义
@api.route('/cards/all', methods=['GET'])
@jwt_required()
def get_all_cards():
    """获取所有卡牌定义"""
    try:
        result = CardService.get_all_cards()
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取卡牌列表失败: {str(e)}")
        raise ApiError('获取卡牌列表失败', code=ErrorCode.OPERATION_FAILED)

# ================== 抽奖相关路由 ==================

# 单抽
@api.route('/cards/draw/single', methods=['POST'])
@jwt_required()
def single_draw():
    """单抽"""
    identity = get_jwt_identity()
    
    try:
        result = CardService.single_draw(identity['id'])
        return ok_response(result, message='抽卡成功！')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"单抽失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('单抽失败', code=ErrorCode.OPERATION_FAILED)

# 十连抽
@api.route('/cards/draw/ten', methods=['POST'])
@jwt_required()
def ten_draw():
    """十连抽"""
    identity = get_jwt_identity()
    
    try:
        result = CardService.ten_draw(identity['id'])
        return ok_response(result, message='十连抽成功！')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"十连抽失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('十连抽失败', code=ErrorCode.OPERATION_FAILED)

# 获取抽奖历史
@api.route('/cards/draw/history', methods=['GET'])
@jwt_required()
def get_draw_history():
    """获取抽奖历史"""
    identity = get_jwt_identity()
    limit = request.args.get('limit', 50, type=int)
    
    try:
        result = CardService.get_draw_history(identity['id'], limit)
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取抽奖历史失败: {str(e)}")
        raise ApiError('获取抽奖历史失败', code=ErrorCode.OPERATION_FAILED)

# 获取抽奖费用
@api.route('/cards/draw/costs', methods=['GET'])
@jwt_required()
def get_draw_costs():
    """获取抽奖费用"""
    try:
        result = CardService.get_draw_costs()
        return ok_response(result)
    except Exception as e:
        api.logger.error(f"获取抽奖费用失败: {str(e)}")
        raise ApiError('获取抽奖费用失败', code=ErrorCode.OPERATION_FAILED)

# ================== 管理员功能 ==================

# 添加新卡牌（管理员功能）
@api.route('/cards/admin/add', methods=['POST'])
@jwt_required()
@roles_required(['admin'])
def add_new_card():
    """添加新卡牌（管理员功能）"""
    data = request.get_json() or {}
    
    try:
        # 这里可以实现添加新卡牌的逻辑
        # 暂时返回成功消息
        return ok_response({
            'message': '卡牌添加成功',
            'card_data': data
        })
    except Exception as e:
        api.logger.error(f"添加卡牌失败: {str(e)}")
        raise ApiError('添加卡牌失败', code=ErrorCode.OPERATION_FAILED)

# 修改卡牌掉落率（管理员功能）
@api.route('/cards/admin/drop-rate', methods=['PUT'])
@jwt_required()
@roles_required(['admin'])
def modify_drop_rate():
    """修改卡牌掉落率（管理员功能）"""
    data = request.get_json() or {}
    
    try:
        result = CardService.update_rarity_drop_config(data)
        return ok_response(result, message='稀有度概率已更新')
    except Exception as e:
        api.logger.error(f"修改掉落率失败: {str(e)}")
        raise ApiError('修改掉落率失败', code=ErrorCode.OPERATION_FAILED)

# 查询稀有度掉落概率（管理员功能）
@api.route('/cards/admin/drop-rate', methods=['GET'])
@jwt_required()
@roles_required(['admin'])
def get_drop_rate():
    """查询稀有度掉落概率（管理员功能）"""
    try:
        result = CardService.get_rarity_drop_config()
        return ok_response(result)
    except Exception as e:
        api.logger.error(f"获取稀有度概率失败: {str(e)}")
        raise ApiError('获取稀有度概率失败', code=ErrorCode.OPERATION_FAILED)
