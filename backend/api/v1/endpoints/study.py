"""
学习数据相关路由
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from core.auth import role_required, roles_required
from services.study_service import StudyService

# 提交学习数据
@api.route('/study/data', methods=['POST'])
@jwt_required()
@role_required('student')
def submit_study_data():
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 提交学习数据
        data_id = StudyService.submit_study_data(identity['id'], data)
        return ok_response({'id': data_id, 'message': '学习数据提交成功'})
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"提交学习数据失败: {str(e)}")
        raise ApiError('提交学习数据失败', code=ErrorCode.OPERATION_FAILED)

# 获取学生学习数据
@api.route('/study/data/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_study_data(student_id):
    identity = get_jwt_identity()
    
    # 只有学生本人或教师/管理员可以查看学习数据
    if identity['role'] == 'student' and identity['id'] != student_id:
        raise ApiError('无权限查看其他学生的学习数据', code=ErrorCode.FORBIDDEN)
    
    try:
        # 获取查询参数
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = int(request.args.get('limit', 30))
        
        # 获取学习数据
        data = StudyService.get_student_study_data(student_id, start_date, end_date, limit)
        return ok_response({'study_data': data})
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取学习数据失败: {str(e)}")
        raise ApiError('获取学习数据失败', code=ErrorCode.OPERATION_FAILED)

# 获取学生的知识点分析
@api.route('/study/analysis/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_knowledge_analysis(student_id):
    identity = get_jwt_identity()
    
    # 只有学生本人或教师/管理员可以查看学习数据分析
    if identity['role'] == 'student' and identity['id'] != student_id:
        raise ApiError('无权限查看其他学生的学习数据分析', code=ErrorCode.FORBIDDEN)
    
    try:
        # 获取知识点分析
        analysis = StudyService.get_knowledge_point_analysis(student_id)
        return ok_response(analysis)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取知识点分析失败: {str(e)}")
        raise ApiError('获取知识点分析失败', code=ErrorCode.OPERATION_FAILED)

# 获取班级学习统计
@api.route('/study/class/<string:class_name>', methods=['GET'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def get_class_statistics(class_name):
    try:
        # 获取班级统计数据
        statistics = StudyService.get_class_statistics(class_name)
        return ok_response(statistics)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取班级统计失败: {str(e)}")
        raise ApiError('获取班级统计失败', code=ErrorCode.OPERATION_FAILED)

# 提交练习结果
@api.route('/study/<int:student_id>/practice', methods=['POST'])
@jwt_required()
def submit_practice_result(student_id):
    identity = get_jwt_identity()
    
    # 只有学生本人或教师/管理员可以提交练习结果
    if identity['role'] == 'student' and identity['id'] != student_id:
        raise ApiError('无权限为其他学生提交练习结果', code=ErrorCode.FORBIDDEN)
    
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        required_fields = ['knowledge_point', 'is_correct']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        # 提交练习结果
        knowledge_point = data['knowledge_point']
        is_correct = data['is_correct']
        
        practice_id = StudyService.submit_practice_result(student_id, knowledge_point, is_correct)
        return ok_response({'id': practice_id, 'message': '练习结果提交成功'})
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"提交练习结果失败: {str(e)}")
        raise ApiError('提交练习结果失败', code=ErrorCode.OPERATION_FAILED)

# 获取错题本
@api.route('/study/<int:student_id>/wrongs', methods=['GET'])
@jwt_required()
def get_wrong_questions(student_id):
    identity = get_jwt_identity()
    
    # 只有学生本人或教师/管理员可以查看错题本
    if identity['role'] == 'student' and identity['id'] != student_id:
        raise ApiError('无权限查看其他学生的错题本', code=ErrorCode.FORBIDDEN)
    
    try:
        # 获取分页参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        
        # 获取错题本
        wrong_questions = StudyService.get_wrong_questions(student_id, page, page_size)
        return ok_response(wrong_questions)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取错题本失败: {str(e)}")
        raise ApiError('获取错题本失败', code=ErrorCode.OPERATION_FAILED) 