from models.card_system import CardSystem
from models.daily_checkin import DailyCheckin
from models.user import User
from core.errors import ApiError, ErrorCode

class CardService:
    """卡牌抽奖服务"""
    
    # 抽奖消耗积分
    SINGLE_DRAW_COST = 100  # 单抽消耗积分
    TEN_DRAW_COST = 900     # 十连抽消耗积分（优惠）
    
    @staticmethod
    def ensure_tables():
        """确保数据库表存在"""
        CardSystem.ensure_tables()
    
    @staticmethod
    def get_user_collection(user_id):
        """获取用户卡牌收集"""
        try:
            cards = CardSystem.get_user_cards(user_id)
            stats = CardSystem.get_user_collection_stats(user_id)
            
            return {
                'cards': cards,
                'stats': stats
            }
        except Exception as e:
            raise ApiError(f'获取卡牌收集失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def get_all_cards():
        """获取所有卡牌定义"""
        try:
            cards = CardSystem.get_all_cards()
            return {
                'cards': cards,
                'total': len(cards)
            }
        except Exception as e:
            raise ApiError(f'获取卡牌列表失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def single_draw(user_id):
        """单抽"""
        try:
            # 检查用户积分
            user_points = User.get_user_points(user_id)
            if user_points < CardService.SINGLE_DRAW_COST:
                raise ApiError(f'积分不足，需要 {CardService.SINGLE_DRAW_COST} 积分', code=ErrorCode.VALIDATION_ERROR)
            
            # 扣除积分
            User.update_user_points(user_id, -CardService.SINGLE_DRAW_COST)
            
            # 抽卡
            result = CardSystem.draw_card(user_id, CardService.SINGLE_DRAW_COST)
            
            # 获取更新后的积分
            updated_points = User.get_user_points(user_id)
            
            return {
                **result,
                'points_spent': CardService.SINGLE_DRAW_COST,
                'remaining_points': updated_points
            }
        except ApiError:
            raise
        except Exception as e:
            raise ApiError(f'抽卡失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def ten_draw(user_id):
        """十连抽"""
        try:
            # 检查用户积分
            user_points = User.get_user_points(user_id)
            if user_points < CardService.TEN_DRAW_COST:
                raise ApiError(f'积分不足，需要 {CardService.TEN_DRAW_COST} 积分', code=ErrorCode.VALIDATION_ERROR)
            
            # 扣除积分
            User.update_user_points(user_id, -CardService.TEN_DRAW_COST)
            
            # 十连抽
            results = []
            for i in range(10):
                result = CardSystem.draw_card(user_id, CardService.TEN_DRAW_COST // 10)
                results.append(result)
            
            # 获取更新后的积分
            updated_points = User.get_user_points(user_id)
            
            return {
                'draws': results,
                'points_spent': CardService.TEN_DRAW_COST,
                'remaining_points': updated_points,
                'new_cards_count': sum(1 for r in results if not r['is_duplicate']),
                'duplicate_cards_count': sum(1 for r in results if r['is_duplicate'])
            }
        except ApiError:
            raise
        except Exception as e:
            raise ApiError(f'十连抽失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def get_draw_history(user_id, limit=50):
        """获取抽奖历史"""
        try:
            history = CardSystem.get_draw_history(user_id, limit)
            return {
                'history': history,
                'total_draws': len(history)
            }
        except Exception as e:
            raise ApiError(f'获取抽奖历史失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def get_draw_costs():
        """获取抽奖费用"""
        return {
            'single_draw': CardService.SINGLE_DRAW_COST,
            'ten_draw': CardService.TEN_DRAW_COST,
            'ten_draw_discount': CardService.SINGLE_DRAW_COST * 10 - CardService.TEN_DRAW_COST
        }
    
    # =============== 稀有度概率配置 ===============
    @staticmethod
    def get_rarity_drop_config():
        """获取稀有度概率配置"""
        try:
            config = CardSystem.get_rarity_drop_config()
            # 返回并补足缺省项
            defaults = {
                'B': 0.35,
                'A': 0.25,
                'R': 0.20,
                'SR': 0.15,
                'UR': 0.05,
            }
            merged = {**defaults, **config}
            total = sum(merged.values())
            return {
                'config': merged,
                'total_rate': total
            }
        except Exception as e:
            raise ApiError(f'获取稀有度概率失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)

    @staticmethod
    def update_rarity_drop_config(payload):
        """更新稀有度概率配置"""
        try:
            if not isinstance(payload, dict):
                raise ApiError('参数格式错误', code=ErrorCode.VALIDATION_ERROR)
            # 允许部分更新
            CardSystem.update_rarity_drop_config(payload)
            config = CardSystem.get_rarity_drop_config()
            return {'config': config, 'total_rate': sum(config.values())}
        except ApiError:
            raise
        except ValueError as e:
            raise ApiError(str(e), code=ErrorCode.VALIDATION_ERROR)
        except Exception as e:
            raise ApiError(f'更新稀有度概率失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    

