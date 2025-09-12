from models.level_record import LevelRecord
from core.errors import ApiError, ErrorCode


class LevelService:
    """闯关记录服务层"""

    @staticmethod
    def ensure_tables():
        LevelRecord.ensure_tables()

    @staticmethod
    def get_student_level_progress(identity):
        """根据身份(支持 'user_id:role' 或 int) 获取学生全部关卡记录"""
        try:
            if isinstance(identity, str) and ':' in identity:
                user_id = int(identity.split(':')[0])
            else:
                user_id = int(identity)
            return {
                'records': LevelRecord.get_student_level_records(user_id)
            }
        except Exception as e:
            raise ApiError(f'获取闯关记录失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)

    @staticmethod
    def get_level_record(identity, level_name: str):
        """获取单个关卡记录"""
        try:
            if not level_name:
                raise ApiError('关卡名不能为空', code=ErrorCode.VALIDATION_ERROR)
            if isinstance(identity, str) and ':' in identity:
                user_id = int(identity.split(':')[0])
            else:
                user_id = int(identity)
            record = LevelRecord.get_level_record(user_id, level_name)
            return record or {}
        except ApiError:
            raise
        except Exception as e:
            raise ApiError(f'获取关卡记录失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)

    @staticmethod
    def record_level_attempt(identity, level_name: str, is_success: bool):
        """记录一次闯关尝试（成功或失败）并返回最新记录"""
        try:
            if not level_name:
                raise ApiError('关卡名不能为空', code=ErrorCode.VALIDATION_ERROR)
            if isinstance(identity, str) and ':' in identity:
                user_id = int(identity.split(':')[0])
            else:
                user_id = int(identity)
            LevelRecord.ensure_tables()
            latest = LevelRecord.upsert_level_attempt(user_id, level_name, bool(is_success))
            return latest or {}
        except ApiError:
            raise
        except Exception as e:
            raise ApiError(f'记录闯关尝试失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)

    @staticmethod
    def get_failure_counts(identity):
        """获取所有关卡的失败次数映射"""
        try:
            if isinstance(identity, str) and ':' in identity:
                user_id = int(identity.split(':')[0])
            else:
                user_id = int(identity)
            return LevelRecord.get_failure_counts_by_student(user_id)
        except Exception as e:
            raise ApiError(f'获取失败次数失败: {str(e)}', code=ErrorCode.OPERATION_FAILED) 