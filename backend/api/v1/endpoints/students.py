"""
学生相关路由
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from core.auth import role_required, roles_required
from services.student_service import StudentService
from core.helpers import get_db

# 获取学生信息
@api.route('/students', methods=['GET'])
def get_students():
    students = StudentService.get_all_students()
    return jsonify(students)

# 获取学生排名
@api.route('/students/rankings', methods=['GET'])
def get_student_rankings():
    rankings = StudentService.get_student_rankings()
    return jsonify(rankings)

# 获取学生详情
@api.route('/students/<int:id>', methods=['GET'])
def get_student_detail(id):
    try:
        result = StudentService.get_student_detail(id)
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取学生详情失败: {str(e)}")
        raise ApiError('获取学生详情失败', code=ErrorCode.OPERATION_FAILED)

# 创建学生
@api.route('/students', methods=['POST'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def create_student():
    data = request.get_json() or {}
    
    try:
        # 验证必要字段
        required_fields = ['name', 'student_id']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        new_id = StudentService.create_student(data)
        return ok_response({'id': new_id})
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f"创建学生失败: {str(e)}", code=ErrorCode.OPERATION_FAILED)

# 更新学生
@api.route('/students/<int:student_id>', methods=['PUT'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def update_student(student_id):
    data = request.get_json() or {}
    
    try:
        # 验证必要字段
        required_fields = ['name', 'student_id']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        success = StudentService.update_student(student_id, data)
        return ok_response({'success': success})
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f"更新学生失败: {str(e)}", code=ErrorCode.OPERATION_FAILED)

# 删除学生
@api.route('/students/<int:student_id>', methods=['DELETE'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def delete_student(student_id):
    try:
        success = StudentService.delete_student(student_id)
        return ok_response({'success': success})
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f"删除学生失败: {str(e)}", code=ErrorCode.OPERATION_FAILED)

# 学生个人资料
@api.route('/student/profile', methods=['GET'])
@jwt_required()
@role_required('student')
def student_profile():
    identity = get_jwt_identity()
    
    try:
        result = StudentService.get_student_profile(identity['id'])
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f"获取学生资料失败: {str(e)}", code=ErrorCode.OPERATION_FAILED)

# 教师个人资料
@api.route('/teacher/profile', methods=['GET'])
@jwt_required()
@role_required('teacher')
def teacher_profile():
    identity = get_jwt_identity()
    
    # 这里应该调用教师服务，暂时放在学生路由中，未来可以移至teacher模块
    conn = get_db()
    cursor = conn.cursor()
    
    # 获取教师创建的课程
    cursor.execute('SELECT * FROM courses WHERE teacher_id = ?', (identity['id'],))
    courses = cursor.fetchall()
    conn.close()
    
    courses_data = [dict(course) for course in courses]
    
    return ok_response({
        'profile': {
            'id': identity['id'],
            'name': identity['name'] if 'name' in identity else None,
            'username': identity['username'] if 'username' in identity else None,
        },
        'courses': courses_data
    })

# 学生查看自己的学习数据
@api.route('/student/study-data', methods=['GET'])
@jwt_required()
@role_required('student')
def get_my_study_data():
    identity = get_jwt_identity()
    
    try:
        result = StudentService.get_student_study_data(identity['id'])
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f"获取学习数据失败: {str(e)}", code=ErrorCode.OPERATION_FAILED)

# 教师获取所有学生
@api.route('/teacher/students', methods=['GET'])
@jwt_required()
@role_required('teacher')
def get_teacher_students():
    students = StudentService.get_all_students()
    return ok_response({'students': students}) 