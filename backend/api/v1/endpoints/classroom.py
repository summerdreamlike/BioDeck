"""
课程教室相关路由
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from core.auth import role_required, roles_required
from services.course_service import CourseService
import traceback

# 获取课程列表
@api.route('/classroom/courses', methods=['GET'])
@jwt_required()
def get_courses():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    # 提取过滤参数
    filters = {}
    if request.args.get('teacher_id'):
        filters['teacher_id'] = request.args.get('teacher_id', type=int)
    if request.args.get('title'):
        filters['title'] = request.args.get('title')
    if request.args.get('status'):
        filters['status'] = request.args.get('status')
    
    try:
        result = CourseService.get_courses(page, page_size, **filters)
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取课程列表失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('获取课程列表失败', code=ErrorCode.OPERATION_FAILED)

# 获取课程详情
@api.route('/classroom/courses/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course(course_id):
    try:
        course = CourseService.get_course_by_id(course_id)
        if not course:
            raise ApiError('课程不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
        return ok_response(course)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取课程详情失败: {str(e)}")
        raise ApiError('获取课程详情失败', code=ErrorCode.OPERATION_FAILED)

# 获取直播课程
@api.route('/classroom/live', methods=['GET'])
def get_live_courses():
    try:
        courses = CourseService.get_live_courses()
        return ok_response(courses)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取直播课程失败: {str(e)}")
        raise ApiError('获取直播课程失败', code=ErrorCode.OPERATION_FAILED)

# 创建课程
@api.route('/classroom/courses', methods=['POST'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def create_course():
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        required_fields = ['title', 'start_time', 'end_time']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        course_id = CourseService.create_course(
            teacher_id=identity['id'],
            title=data['title'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            poster_url=data.get('poster_url'),
            video_url=data.get('video_url')
        )
        
        course = CourseService.get_course_by_id(course_id)
        return ok_response(course, message='课程创建成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"创建课程失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('创建课程失败', code=ErrorCode.OPERATION_FAILED)

# 更新课程
@api.route('/classroom/courses/<int:course_id>', methods=['PUT'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def update_course(course_id):
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证权限（只有课程创建者或管理员可以更新）
        if identity['role'] != 'admin':
            course = CourseService.get_course_by_id(course_id)
            if not course or course['teacher_id'] != identity['id']:
                raise ApiError('无权更新此课程', code=ErrorCode.PERMISSION_DENIED)
        
        updated_course = CourseService.update_course(course_id, data)
        return ok_response(updated_course, message='课程更新成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"更新课程失败: {str(e)}")
        raise ApiError('更新课程失败', code=ErrorCode.OPERATION_FAILED)

# 删除课程
@api.route('/classroom/courses/<int:course_id>', methods=['DELETE'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def delete_course(course_id):
    identity = get_jwt_identity()
    
    try:
        # 验证权限（只有课程创建者或管理员可以删除）
        if identity['role'] != 'admin':
            course = CourseService.get_course_by_id(course_id)
            if not course or course['teacher_id'] != identity['id']:
                raise ApiError('无权删除此课程', code=ErrorCode.PERMISSION_DENIED)
        
        CourseService.delete_course(course_id)
        return ok_response(message='课程删除成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"删除课程失败: {str(e)}")
        raise ApiError('删除课程失败', code=ErrorCode.OPERATION_FAILED)

# 添加学生到课程
@api.route('/classroom/courses/<int:course_id>/students', methods=['POST'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def add_student_to_course(course_id):
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证权限（只有课程创建者或管理员可以添加学生）
        if identity['role'] != 'admin':
            course = CourseService.get_course_by_id(course_id)
            if not course or course['teacher_id'] != identity['id']:
                raise ApiError('无权操作此课程', code=ErrorCode.PERMISSION_DENIED)
        
        if 'student_id' not in data:
            raise ApiError('缺少必填字段: student_id', code=ErrorCode.VALIDATION_ERROR)
        
        CourseService.add_student_to_course(course_id, data['student_id'])
        return ok_response(message='学生已添加到课程')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"添加学生到课程失败: {str(e)}")
        raise ApiError('添加学生到课程失败', code=ErrorCode.OPERATION_FAILED)

# 从课程中移除学生
@api.route('/classroom/courses/<int:course_id>/students/<int:student_id>', methods=['DELETE'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def remove_student_from_course(course_id, student_id):
    identity = get_jwt_identity()
    
    try:
        # 验证权限（只有课程创建者或管理员可以移除学生）
        if identity['role'] != 'admin':
            course = CourseService.get_course_by_id(course_id)
            if not course or course['teacher_id'] != identity['id']:
                raise ApiError('无权操作此课程', code=ErrorCode.PERMISSION_DENIED)
        
        CourseService.remove_student_from_course(course_id, student_id)
        return ok_response(message='学生已从课程中移除')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"从课程移除学生失败: {str(e)}")
        raise ApiError('从课程移除学生失败', code=ErrorCode.OPERATION_FAILED)

# 获取课程的学生列表
@api.route('/classroom/courses/<int:course_id>/students', methods=['GET'])
@jwt_required()
def get_course_students(course_id):
    try:
        students = CourseService.get_course_students(course_id)
        return ok_response(students)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取课程学生列表失败: {str(e)}")
        raise ApiError('获取课程学生列表失败', code=ErrorCode.OPERATION_FAILED)

# 发送课程消息
@api.route('/classroom/courses/<int:course_id>/messages', methods=['POST'])
@jwt_required()
def send_course_message(course_id):
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        if 'message' not in data:
            raise ApiError('缺少必填字段: message', code=ErrorCode.VALIDATION_ERROR)
        
        # 验证用户是否在课程中（教师或学生）
        course = CourseService.get_course_by_id(course_id)
        if not course:
            raise ApiError('课程不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
        # 教师或管理员可以直接发送消息
        if identity['role'] not in ['teacher', 'admin']:
            # 学生必须在课程中才能发送消息
            students = CourseService.get_course_students(course_id)
            student_ids = [s['id'] for s in students]
            if identity['id'] not in student_ids:
                raise ApiError('您不是此课程的成员', code=ErrorCode.PERMISSION_DENIED)
        
        message = CourseService.send_course_message(course_id, identity['id'], data['message'])
        return ok_response(message, message='消息发送成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"发送课程消息失败: {str(e)}")
        raise ApiError('发送课程消息失败', code=ErrorCode.OPERATION_FAILED)

# 获取课程消息
@api.route('/classroom/courses/<int:course_id>/messages', methods=['GET'])
@jwt_required()
def get_course_messages(course_id):
    identity = get_jwt_identity()
    
    try:
        # 验证用户是否在课程中（教师或学生）
        course = CourseService.get_course_by_id(course_id)
        if not course:
            raise ApiError('课程不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
        # 教师或管理员可以直接查看消息
        if identity['role'] not in ['teacher', 'admin']:
            # 学生必须在课程中才能查看消息
            students = CourseService.get_course_students(course_id)
            student_ids = [s['id'] for s in students]
            if identity['id'] not in student_ids:
                raise ApiError('您不是此课程的成员', code=ErrorCode.PERMISSION_DENIED)
        
        messages = CourseService.get_course_messages(course_id)
        return ok_response(messages)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取课程消息失败: {str(e)}")
        raise ApiError('获取课程消息失败', code=ErrorCode.OPERATION_FAILED) 