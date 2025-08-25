"""
题目相关路由
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from core.auth import role_required, roles_required
from services.question_service import QuestionService

# 获取题目列表
@api.route('/questions', methods=['GET'])
def get_questions():
    # 获取过滤参数
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    query = request.args.get('query')
    types = request.args.getlist('type')
    difficulty_min = request.args.get('difficulty_min')
    difficulty_max = request.args.get('difficulty_max')
    
    # 构建过滤条件
    filters = {}
    if query:
        filters['query'] = query
    if types:
        filters['types'] = types
    if difficulty_min:
        filters['difficulty_min'] = int(difficulty_min)
    if difficulty_max:
        filters['difficulty_max'] = int(difficulty_max)
    
    # 调用服务层获取题目
    result = QuestionService.get_questions(page, page_size, **filters)
    return ok_response(result)

# 获取题目详情
@api.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    try:
        question = QuestionService.get_question_by_id(question_id)
        return ok_response(question)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取题目详情失败: {str(e)}")
        raise ApiError('获取题目详情失败', code=ErrorCode.OPERATION_FAILED)

# 创建题目
@api.route('/questions', methods=['POST'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def create_question():
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        required_fields = ['title', 'type', 'difficulty', 'knowledge_point', 'answer']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        # 调用服务层创建题目
        question_id = QuestionService.create_question(data)
        return ok_response({'id': question_id})
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"创建题目失败: {str(e)}")
        raise ApiError('创建题目失败', code=ErrorCode.OPERATION_FAILED)

# 更新题目
@api.route('/questions/<int:question_id>', methods=['PUT'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def update_question(question_id):
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        required_fields = ['title', 'type', 'difficulty', 'knowledge_point', 'answer']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        # 调用服务层更新题目
        success = QuestionService.update_question(question_id, data)
        return ok_response({'success': success})
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"更新题目失败: {str(e)}")
        raise ApiError('更新题目失败', code=ErrorCode.OPERATION_FAILED)

# 删除题目
@api.route('/questions/<int:question_id>', methods=['DELETE'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def delete_question(question_id):
    try:
        # 调用服务层删除题目
        success = QuestionService.delete_question(question_id)
        return ok_response({'success': success})
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"删除题目失败: {str(e)}")
        raise ApiError('删除题目失败', code=ErrorCode.OPERATION_FAILED)

# 为学生推荐题目
@api.route('/questions/recommended/<int:student_id>', methods=['GET'])
def recommend_questions(student_id):
    try:
        # 调用服务层推荐题目
        questions = QuestionService.recommend_for_student(student_id)
        return ok_response(questions)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"推荐题目失败: {str(e)}")
        raise ApiError('推荐题目失败', code=ErrorCode.OPERATION_FAILED) 