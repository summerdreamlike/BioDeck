from models.card_system import CardSystem
from models.daily_checkin import DailyCheckin
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
            user_points = DailyCheckin.get_user_points(user_id)
            if not user_points or user_points['total_points'] < CardService.SINGLE_DRAW_COST:
                raise ApiError(f'积分不足，需要 {CardService.SINGLE_DRAW_COST} 积分', code=ErrorCode.VALIDATION_ERROR)
            
            # 扣除积分
            CardService._deduct_points(user_id, CardService.SINGLE_DRAW_COST)
            
            # 抽卡
            result = CardSystem.draw_card(user_id, CardService.SINGLE_DRAW_COST)
            
            # 获取更新后的积分
            updated_points = DailyCheckin.get_user_points(user_id)
            
            return {
                **result,
                'points_spent': CardService.SINGLE_DRAW_COST,
                'remaining_points': updated_points['total_points'] if updated_points else 0
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
            user_points = DailyCheckin.get_user_points(user_id)
            if not user_points or user_points['total_points'] < CardService.TEN_DRAW_COST:
                raise ApiError(f'积分不足，需要 {CardService.TEN_DRAW_COST} 积分', code=ErrorCode.VALIDATION_ERROR)
            
            # 扣除积分
            CardService._deduct_points(user_id, CardService.TEN_DRAW_COST)
            
            # 十连抽
            results = []
            for i in range(10):
                result = CardSystem.draw_card(user_id, CardService.TEN_DRAW_COST // 10)
                results.append(result)
            
            # 获取更新后的积分
            updated_points = DailyCheckin.get_user_points(user_id)
            
            return {
                'draws': results,
                'points_spent': CardService.TEN_DRAW_COST,
                'remaining_points': updated_points['total_points'] if updated_points else 0,
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
    
    @staticmethod
    def _deduct_points(user_id, points):
        """扣除用户积分"""
        from datetime import datetime
        
        conn = DailyCheckin.get_db()
        cursor = conn.cursor()
        
        try:
            # 更新用户积分
            cursor.execute('''
                UPDATE user_points 
                SET total_points = total_points - ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (points, user_id))
            
            # 记录积分历史
            cursor.execute('''
                INSERT INTO point_history (user_id, points_change, change_type, description)
                VALUES (?, ?, 'card_draw', '卡牌抽奖消耗')
            ''', (user_id, -points))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
