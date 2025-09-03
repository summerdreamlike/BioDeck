"""
卡牌抽奖相关路由
"""
from flask import request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from core.auth import role_required, roles_required
from services.card_service import CardService
import traceback

def parse_user_identity(identity):
    """解析用户身份信息，从字符串格式 'user_id:role' 中提取用户ID"""
    if isinstance(identity, str) and ':' in identity:
        parts = identity.split(':')
        # 确保有两个部分且都不为空
        if len(parts) == 2 and parts[0].strip() and parts[1].strip():
            try:
                user_id = int(parts[0])
                user_role = parts[1]
                current_app.logger.info(f"解析用户ID: {user_id}, 角色: {user_role}")
                return user_id
            except (ValueError, IndexError) as e:
                current_app.logger.error(f"解析用户身份信息失败: {str(e)}")
                raise ApiError('无效的用户身份信息格式', code=ErrorCode.INVALID_PARAMETER)
        else:
            current_app.logger.error(f"用户身份信息格式不完整: {identity}")
            raise ApiError('用户身份信息格式不完整', code=ErrorCode.INVALID_PARAMETER)
    else:
        current_app.logger.error(f"无效的用户身份信息格式: {identity}")
        raise ApiError('无效的用户身份信息格式', code=ErrorCode.INVALID_PARAMETER)

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
        
        user_id = parse_user_identity(identity)
        result = CardService.get_user_collection(user_id)
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        current_app.logger.error(f"获取卡牌收集失败: {str(e)}")
        current_app.logger.error(traceback.format_exc())
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
        current_app.logger.error(f"获取卡牌列表失败: {str(e)}")
        raise ApiError('获取卡牌列表失败', code=ErrorCode.OPERATION_FAILED)

# ================== 抽奖相关路由 ==================

# 单抽
@api.route('/cards/draw/single', methods=['POST'])
@jwt_required()
def single_draw():
    """单抽"""
    identity = get_jwt_identity()
    
    try:
        user_id = parse_user_identity(identity)
        result = CardService.single_draw(user_id)
        return ok_response(result, message='抽卡成功！')
    except ApiError:
        raise
    except Exception as e:
        current_app.logger.error(f"单抽失败: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        raise ApiError('单抽失败', code=ErrorCode.OPERATION_FAILED)

# 十连抽
@api.route('/cards/draw/ten', methods=['POST'])
@jwt_required()
def ten_draw():
    """十连抽"""
    identity = get_jwt_identity()
    
    try:
        user_id = parse_user_identity(identity)
        result = CardService.ten_draw(user_id)
        return ok_response(result, message='十连抽成功！')
    except ApiError:
        raise
    except Exception as e:
        current_app.logger.error(f"十连抽失败: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        raise ApiError('十连抽失败', code=ErrorCode.OPERATION_FAILED)

# 获取抽奖历史
@api.route('/cards/draw/history', methods=['GET'])
@jwt_required()
def get_draw_history():
    """获取抽奖历史"""
    identity = get_jwt_identity()
    limit = request.args.get('limit', 50, type=int)
    
    try:
        user_id = parse_user_identity(identity)
        result = CardService.get_draw_history(user_id, limit)
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        current_app.logger.error(f"获取抽奖历史失败: {str(e)}")
        raise ApiError('获取抽奖历史失败', code=ErrorCode.OPERATION_FAILED)

# 获取用户积分
@api.route('/cards/user/points', methods=['GET'])
@jwt_required()
def get_user_points():
    """获取用户积分"""
    identity = get_jwt_identity()
    
    try:
        user_id = parse_user_identity(identity)
        
        from models.user import User
        points = User.get_user_points(user_id)
        return ok_response({'points': points})
    except Exception as e:
        current_app.logger.error(f"获取用户积分失败: {str(e)}")
        raise ApiError('获取用户积分失败', code=ErrorCode.OPERATION_FAILED)

# 增加用户积分
@api.route('/cards/user/points', methods=['POST'])
@jwt_required()
def add_user_points():
    """增加用户积分"""
    try:
        identity = get_jwt_identity()
        current_app.logger.info(f"用户身份信息: {identity}, 类型: {type(identity)}")
        
        user_id = parse_user_identity(identity)
        
        data = request.get_json() or {}
        current_app.logger.info(f"请求数据: {data}, 类型: {type(data)}")
        
        points_to_add = data.get('points', 0)
        current_app.logger.info(f"积分数量: {points_to_add}, 类型: {type(points_to_add)}")
        
        if points_to_add <= 0:
            raise ApiError('积分数量必须大于0', code=ErrorCode.INVALID_PARAMETER)
        
        from models.user import User
        current_app.logger.info(f"调用User.update_user_points({user_id}, {points_to_add})")
        new_points = User.update_user_points(user_id, points_to_add)
        current_app.logger.info(f"积分更新成功，新积分: {new_points}")
        
        return ok_response({'points': new_points, 'added': points_to_add})
        
    except Exception as e:
        current_app.logger.error(f"增加用户积分失败: {str(e)}")
        current_app.logger.error(f"错误类型: {type(e)}")
        import traceback
        current_app.logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise ApiError('增加用户积分失败', code=ErrorCode.OPERATION_FAILED)

# 获取抽奖费用
@api.route('/cards/draw/costs', methods=['GET'])
@jwt_required()
def get_draw_costs():
    """获取抽奖费用"""
    try:
        result = CardService.get_draw_costs()
        return ok_response(result)
    except Exception as e:
        current_app.logger.error(f"获取抽奖费用失败: {str(e)}")
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
        current_app.logger.error(f"添加卡牌失败: {str(e)}")
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
        current_app.logger.error(f"修改掉落率失败: {str(e)}")
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
        current_app.logger.error(f"获取稀有度概率失败: {str(e)}")
        raise ApiError('获取稀有度概率失败', code=ErrorCode.OPERATION_FAILED)
