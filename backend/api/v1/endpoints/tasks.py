"""
任务管理相关路由
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from core.auth import role_required, roles_required
from core.helpers import get_db
from services.task_service import TaskService
import traceback

# ================== 任务管理相关路由 ==================

# 获取任务列表
@api.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    # 提取过滤参数
    filters = {}
    if request.args.get('creator_id'):
        filters['creator_id'] = request.args.get('creator_id', type=int)
    if request.args.get('title'):
        filters['title'] = request.args.get('title')
    if request.args.get('class_name'):
        filters['class_name'] = request.args.get('class_name')
    if request.args.get('status'):
        filters['status'] = request.args.get('status')
    if request.args.get('order_by'):
        filters['order_by'] = request.args.get('order_by')
    if request.args.get('order_dir'):
        filters['order_dir'] = request.args.get('order_dir')
        
    # 获取当前用户身份
    identity = get_jwt_identity()
    
    # 如果是学生，只能查看与自己相关的任务
    if identity['role'] == 'student':
        filters['student_id'] = identity['id']
    
    try:
        result = TaskService.get_tasks(page, page_size, **filters)
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取任务列表失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('获取任务列表失败', code=ErrorCode.OPERATION_FAILED)

# 获取任务详情
@api.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    try:
        task = TaskService.get_task_by_id(task_id)
        
        # 如果是学生，检查任务是否与自己相关
        identity = get_jwt_identity()
        if identity['role'] == 'student':
            # 检查学生的班级是否在任务的班级列表中
            student_class = None
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('SELECT class FROM students WHERE id = ?', (identity['id'],))
            student_row = cursor.fetchone()
            conn.close()
            
            if student_row:
                student_class = student_row['class']
                
            if not student_class or student_class not in task['classes']:
                raise ApiError('无权查看此任务', code=ErrorCode.PERMISSION_DENIED)
        
        return ok_response(task)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取任务详情失败: {str(e)}")
        raise ApiError('获取任务详情失败', code=ErrorCode.OPERATION_FAILED)

# 创建任务
@api.route('/tasks', methods=['POST'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def create_task():
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        required_fields = ['title', 'description', 'due_date', 'classes']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        # 创建任务
        task_id = TaskService.create_task(
            title=data['title'],
            description=data['description'],
            creator_id=identity['id'],
            due_date=data['due_date'],
            classes=data['classes'],
            paper_id=data.get('paper_id'),
            allow_late_submission=data.get('allow_late_submission', False)
        )
        
        task = TaskService.get_task_by_id(task_id)
        return ok_response(task, message='任务创建成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"创建任务失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('创建任务失败', code=ErrorCode.OPERATION_FAILED)

# 更新任务
@api.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def update_task(task_id):
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证权限（只有创建者或管理员可以更新）
        if identity['role'] != 'admin':
            task = TaskService.get_task_by_id(task_id)
            if task['creator_id'] != identity['id']:
                raise ApiError('无权更新此任务', code=ErrorCode.PERMISSION_DENIED)
        
        updated_task = TaskService.update_task(task_id, data)
        return ok_response(updated_task, message='任务更新成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"更新任务失败: {str(e)}")
        raise ApiError('更新任务失败', code=ErrorCode.OPERATION_FAILED)

# 删除任务
@api.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def delete_task(task_id):
    identity = get_jwt_identity()
    
    try:
        # 验证权限（只有创建者或管理员可以删除）
        if identity['role'] != 'admin':
            task = TaskService.get_task_by_id(task_id)
            if task['creator_id'] != identity['id']:
                raise ApiError('无权删除此任务', code=ErrorCode.PERMISSION_DENIED)
        
        TaskService.delete_task(task_id)
        return ok_response(message='任务删除成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"删除任务失败: {str(e)}")
        raise ApiError('删除任务失败', code=ErrorCode.OPERATION_FAILED)

# ================== 任务提交相关路由 ==================

# 学生提交任务
@api.route('/tasks/<int:task_id>/submit', methods=['POST'])
@jwt_required()
@role_required('student')
def submit_task(task_id):
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 提交任务
        submission_id = TaskService.submit_task(
            task_id=task_id,
            student_id=identity['id'],
            answers=data.get('answers'),
            file_urls=data.get('file_urls')
        )
        
        return ok_response({'id': submission_id}, message='任务提交成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"提交任务失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('提交任务失败', code=ErrorCode.OPERATION_FAILED)

# 获取学生任务列表
@api.route('/tasks/student', methods=['GET'])
@jwt_required()
@role_required('student')
def get_student_tasks():
    identity = get_jwt_identity()
    status = request.args.get('status')
    
    try:
        tasks = TaskService.get_student_tasks(
            student_id=identity['id'],
            status=status
        )
        
        return ok_response(tasks)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取学生任务列表失败: {str(e)}")
        raise ApiError('获取学生任务列表失败', code=ErrorCode.OPERATION_FAILED)

# 获取学生提交详情
@api.route('/tasks/<int:task_id>/submission', methods=['GET'])
@jwt_required()
def get_student_submission(task_id):
    identity = get_jwt_identity()
    
    try:
        # 如果是学生，只能查看自己的提交
        student_id = identity['id'] if identity['role'] == 'student' else request.args.get('student_id', type=int)
        
        if not student_id:
            raise ApiError('缺少学生ID参数', code=ErrorCode.VALIDATION_ERROR)
        
        # 如果是老师，验证任务权限
        if identity['role'] in ['admin', 'teacher'] and identity['role'] != 'admin':
            task = TaskService.get_task_by_id(task_id)
            if task['creator_id'] != identity['id']:
                raise ApiError('无权查看此任务的提交', code=ErrorCode.PERMISSION_DENIED)
        
        submission = TaskService.get_student_submission(task_id, student_id)
        
        if not submission:
            return ok_response(None, message='尚未提交')
        
        return ok_response(submission)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取提交记录失败: {str(e)}")
        raise ApiError('获取提交记录失败', code=ErrorCode.OPERATION_FAILED)

# ================== 任务评分相关路由 ==================

# 教师评分
@api.route('/tasks/submissions/<int:submission_id>/grade', methods=['POST'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def grade_submission(submission_id):
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        if 'score' not in data:
            raise ApiError('缺少必填字段: score', code=ErrorCode.VALIDATION_ERROR)
        
        # 获取提交的任务ID和创建者
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT ts.id, ts.task_id, t.creator_id
            FROM task_submissions ts
            JOIN tasks t ON ts.task_id = t.id
            WHERE ts.id = ?
        ''', (submission_id,))
        submission_info = cursor.fetchone()
        conn.close()
        
        if not submission_info:
            raise ApiError('提交记录不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
        
        # 验证权限（只有任务创建者或管理员可以评分）
        if identity['role'] != 'admin' and submission_info['creator_id'] != identity['id']:
            raise ApiError('无权评分此提交', code=ErrorCode.PERMISSION_DENIED)
        
        # 评分
        updated_submission = TaskService.grade_submission(
            submission_id=submission_id,
            score=data['score'],
            feedback=data.get('feedback')
        )
        
        return ok_response(updated_submission, message='评分成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"评分失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('评分失败', code=ErrorCode.OPERATION_FAILED)

# 获取提交详情
@api.route('/tasks/submissions/<int:submission_id>', methods=['GET'])
@jwt_required()
def get_submission(submission_id):
    identity = get_jwt_identity()
    
    try:
        # 获取提交信息
        submission = TaskService.get_submission(submission_id)
        
        # 验证权限（只有学生本人、任务创建者或管理员可以查看）
        if identity['role'] == 'student':
            if submission['student_id'] != identity['id']:
                raise ApiError('无权查看此提交', code=ErrorCode.PERMISSION_DENIED)
        elif identity['role'] == 'teacher':
            # 获取任务信息，检查创建者
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('SELECT creator_id FROM tasks WHERE id = ?', (submission['task_id'],))
            task = cursor.fetchone()
            conn.close()
            
            if not task or task['creator_id'] != identity['id']:
                raise ApiError('无权查看此提交', code=ErrorCode.PERMISSION_DENIED)
        
        return ok_response(submission)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取提交详情失败: {str(e)}")
        raise ApiError('获取提交详情失败', code=ErrorCode.OPERATION_FAILED)

# ================== 任务统计相关路由 ==================

# 获取任务统计信息
@api.route('/tasks/<int:task_id>/statistics', methods=['GET'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def get_task_statistics(task_id):
    identity = get_jwt_identity()
    
    try:
        # 验证权限（只有任务创建者或管理员可以查看统计信息）
        if identity['role'] != 'admin':
            task = TaskService.get_task_by_id(task_id)
            if task['creator_id'] != identity['id']:
                raise ApiError('无权查看此任务的统计信息', code=ErrorCode.PERMISSION_DENIED)
        
        statistics = TaskService.get_task_statistics(task_id)
        return ok_response(statistics)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取任务统计信息失败: {str(e)}")
        raise ApiError('获取任务统计信息失败', code=ErrorCode.OPERATION_FAILED)

# ================== 辅助功能路由 ==================

# 获取可用班级列表
@api.route('/tasks/classes', methods=['GET'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def get_available_classes():
    try:
        classes = TaskService.get_available_classes()
        return ok_response(classes)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取班级列表失败: {str(e)}")
        raise ApiError('获取班级列表失败', code=ErrorCode.OPERATION_FAILED) 