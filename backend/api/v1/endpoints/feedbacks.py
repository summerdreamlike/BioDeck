"""
反馈管理相关路由
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from core.auth import role_required, roles_required
from core.helpers import get_db
from services.feedback_service import FeedbackService
import traceback

# ================== 反馈管理相关路由 ==================

# 获取反馈列表（管理员和教师）
@api.route('/feedbacks', methods=['GET'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def get_feedbacks():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    try:
        result = FeedbackService.get_feedbacks(page, page_size)
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取反馈列表失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('获取反馈列表失败', code=ErrorCode.OPERATION_FAILED)

# 获取反馈详情（管理员和教师）
@api.route('/feedbacks/<int:feedback_id>', methods=['GET'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def get_feedback(feedback_id):
    try:
        feedback = FeedbackService.get_feedback_by_id(feedback_id)
        return ok_response(feedback)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取反馈详情失败: {str(e)}")
        raise ApiError('获取反馈详情失败', code=ErrorCode.OPERATION_FAILED)

# 删除反馈（管理员）
@api.route('/feedbacks/<int:feedback_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_feedback(feedback_id):
    try:
        FeedbackService.delete_feedback(feedback_id)
        return ok_response(message='反馈删除成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"删除反馈失败: {str(e)}")
        raise ApiError('删除反馈失败', code=ErrorCode.OPERATION_FAILED)

# ================== 反馈统计相关路由 ==================

# 获取反馈统计信息
@api.route('/feedbacks/statistics', methods=['GET'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def get_feedback_statistics():
    try:
        statistics = FeedbackService.get_statistics()
        return ok_response(statistics)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取反馈统计信息失败: {str(e)}")
        raise ApiError('获取反馈统计信息失败', code=ErrorCode.OPERATION_FAILED)

# 获取反馈关键词分析
@api.route('/feedbacks/keywords', methods=['GET'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def analyze_feedback_keywords():
    limit = request.args.get('limit', 10, type=int)
    
    try:
        keywords = FeedbackService.analyze_keywords(limit)
        return ok_response(keywords)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"分析反馈关键词失败: {str(e)}")
        raise ApiError('分析反馈关键词失败', code=ErrorCode.OPERATION_FAILED)

# ================== 学生反馈相关路由 ==================

# 学生提交反馈
@api.route('/feedbacks/submit', methods=['POST'])
@jwt_required()
@role_required('student')
def submit_feedback():
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        required_fields = ['content', 'satisfaction']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        feedback_id = FeedbackService.create_feedback(
            student_id=identity['id'],
            content=data['content'],
            satisfaction=data['satisfaction']
        )
        
        return ok_response({'id': feedback_id}, message='反馈提交成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"提交反馈失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('提交反馈失败', code=ErrorCode.OPERATION_FAILED)

# 学生查看自己的反馈
@api.route('/feedbacks/my', methods=['GET'])
@jwt_required()
@role_required('student')
def get_my_feedbacks():
    identity = get_jwt_identity()
    
    try:
        feedbacks = FeedbackService.get_student_feedback(identity['id'])
        return ok_response(feedbacks)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取学生反馈失败: {str(e)}")
        raise ApiError('获取学生反馈失败', code=ErrorCode.OPERATION_FAILED)

# 学生更新自己的反馈
@api.route('/feedbacks/<int:feedback_id>', methods=['PUT'])
@jwt_required()
@role_required('student')
def update_feedback(feedback_id):
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证是否为自己的反馈
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT student_id FROM feedbacks WHERE id = ?', (feedback_id,))
        feedback = cursor.fetchone()
        conn.close()
        
        if not feedback or feedback['student_id'] != identity['id']:
            raise ApiError('无权更新此反馈', code=ErrorCode.PERMISSION_DENIED)
        
        # 提取更新数据
        content = data.get('content')
        satisfaction = data.get('satisfaction')
        
        updated_feedback = FeedbackService.update_feedback(
            feedback_id=feedback_id,
            content=content,
            satisfaction=satisfaction
        )
        
        return ok_response(updated_feedback, message='反馈更新成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"更新反馈失败: {str(e)}")
        raise ApiError('更新反馈失败', code=ErrorCode.OPERATION_FAILED) 