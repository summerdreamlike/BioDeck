from datetime import datetime, date, timedelta
from models.daily_checkin import DailyCheckin
from core.errors import ApiError, ErrorCode

class DailyCheckinService:
    """每日签到服务"""
    
    # 基础积分配置
    BASE_POINTS = 10  # 基础签到积分
    STREAK_BONUS = 2  # 连续签到每天额外积分
    MAX_STREAK_BONUS = 20  # 最大连续签到奖励
    
    # 特殊日期奖励
    WEEKEND_BONUS = 5  # 周末额外奖励
    MONTH_START_BONUS = 20  # 月初额外奖励
    
    @staticmethod
    def ensure_tables():
        """确保数据库表存在"""
        DailyCheckin.ensure_tables()
    
    @staticmethod
    def get_user_checkin_status(identity):
        """获取用户今日签到状态"""
        try:
            # 解析JWT identity，格式为 "user_id:role"
            if isinstance(identity, str) and ':' in identity:
                user_id = int(identity.split(':')[0])
            else:
                user_id = identity
            
            # 检查今日是否已签到
            today_checkin = DailyCheckin.get_user_checkin_today(user_id)
            user_points = DailyCheckin.get_user_points(user_id)
            
            # 计算连续签到天数
            current_streak = DailyCheckin.calculate_streak(user_id)
            
            # 计算今日可获得的积分
            today_points = DailyCheckinService._calculate_today_points(current_streak)
            
            result = {
                'checked_today': today_checkin is not None,  # 修改字段名以匹配前端
                'consecutive_days': current_streak,  # 修改字段名以匹配前端
                'today_checkin': today_checkin,
                'user_points': user_points or {
                    'total_points': 0,
                    'current_streak': 0,
                    'longest_streak': 0,
                    'points_earned_today': 0
                },
                'current_streak': current_streak,
                'today_points': today_points,
                'next_checkin_time': DailyCheckinService._get_next_checkin_time()
            }
            
            return result
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise ApiError(f'获取签到状态失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def perform_checkin(identity):
        """执行签到 - 简化版本"""
        try:
            # 解析JWT identity，格式为 "user_id:role"
            if isinstance(identity, str) and ':' in identity:
                user_id = int(identity.split(':')[0])
            else:
                user_id = identity
                
            # 检查今日是否已签到
            today_checkin = DailyCheckin.get_user_checkin_today(user_id)
            if today_checkin:
                raise ApiError('今日已签到，请明天再来', code=ErrorCode.VALIDATION_ERROR)
            
            # 简化的连续签到计算
            current_streak = 1  # 暂时设为1，后续可以优化
            
            # 固定1000积分
            points_earned = 1000
            
            # 创建签到记录
            checkin_id = DailyCheckin.create_checkin(user_id, points_earned, current_streak)
            
            # 获取更新后的用户积分信息
            user_points = DailyCheckin.get_user_points(user_id)
            
            # 返回成功结果
            result = {
                'checkin_id': checkin_id,
                'points_earned': points_earned,
                'consecutive_days': current_streak,
                'total_points': user_points.get('total_points', 0) if user_points else 0,
                'message': f'签到成功！获得{points_earned}积分'
            }
            
            return result
            
        except ApiError as e:
            raise
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise ApiError(f'签到失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def get_checkin_history(identity, limit=30):
        """获取签到历史"""
        try:
            # 解析JWT identity，格式为 "user_id:role"
            if isinstance(identity, str) and ':' in identity:
                user_id = int(identity.split(':')[0])
            else:
                user_id = identity
                
            history = DailyCheckin.get_checkin_history(user_id, limit)
            return {
                'history': history,
                'total_days': len(history)
            }
        except Exception as e:
            raise ApiError(f'获取签到历史失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def get_point_history(identity, limit=50):
        """获取积分历史"""
        try:
            # 解析JWT identity，格式为 "user_id:role"
            if isinstance(identity, str) and ':' in identity:
                user_id = int(identity.split(':')[0])
            else:
                user_id = identity
                
            history = DailyCheckin.get_point_history(user_id, limit)
            return {
                'history': history,
                'total_records': len(history)
            }
        except Exception as e:
            raise ApiError(f'获取积分历史失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def get_leaderboard(limit=20):
        """获取积分排行榜"""
        try:
            # 这里可以实现排行榜逻辑
            # 暂时返回空列表，后续可以扩展
            return {
                'leaderboard': [],
                'total_users': 0
            }
        except Exception as e:
            raise ApiError(f'获取排行榜失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def _calculate_today_points(streak_days):
        """计算今日可获得的积分"""
        points = DailyCheckinService.BASE_POINTS
        
        # 连续签到奖励
        streak_bonus = min(streak_days * DailyCheckinService.STREAK_BONUS, DailyCheckinService.MAX_STREAK_BONUS)
        points += streak_bonus
        
        # 周末奖励
        if date.today().weekday() >= 5:  # 周六或周日
            points += DailyCheckinService.WEEKEND_BONUS
        
        # 月初奖励
        if date.today().day == 1:
            points += DailyCheckinService.MONTH_START_BONUS
        
        return points
    
    @staticmethod
    def _get_checkin_message(points_earned, streak_days):
        """生成签到成功消息"""
        messages = [
            f"签到成功！获得 {points_earned} 积分",
            f"连续签到 {streak_days} 天，继续加油！"
        ]
        
        if streak_days >= 7:
            messages.append("🎉 连续签到一周，太棒了！")
        elif streak_days >= 30:
            messages.append("🏆 连续签到一个月，你是真正的坚持者！")
        
        if date.today().weekday() >= 5:
            messages.append("🌅 周末签到，额外奖励！")
        
        if date.today().day == 1:
            messages.append("🎊 月初签到，特别奖励！")
        
        return " ".join(messages)
    
    @staticmethod
    def _get_next_checkin_time():
        """获取下次签到时间"""
        from datetime import datetime, timedelta
        
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
