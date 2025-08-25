"""
考勤管理相关路由
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from core.auth import role_required, roles_required
from services.attendance_service import AttendanceService
import traceback
from datetime import datetime

# ================== 考勤记录管理相关路由 ==================

# 获取考勤记录列表
@api.route('/attendance', methods=['GET'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def get_attendances():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    # 提取过滤参数
    filters = {}
    if request.args.get('course_id'):
        filters['course_id'] = request.args.get('course_id', type=int)
    if request.args.get('student_id'):
        filters['student_id'] = request.args.get('student_id', type=int)
    if request.args.get('status'):
        filters['status'] = request.args.get('status')
    if request.args.get('date_from'):
        filters['date_from'] = request.args.get('date_from')
    if request.args.get('date_to'):
        filters['date_to'] = request.args.get('date_to')
    
    try:
        result = AttendanceService.get_attendances(page, page_size, **filters)
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取考勤记录列表失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('获取考勤记录列表失败', code=ErrorCode.OPERATION_FAILED)

# 获取考勤记录详情
@api.route('/attendance/<int:attendance_id>', methods=['GET'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def get_attendance(attendance_id):
    try:
        attendance = AttendanceService.get_attendance_by_id(attendance_id)
        return ok_response(attendance)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取考勤记录详情失败: {str(e)}")
        raise ApiError('获取考勤记录详情失败', code=ErrorCode.OPERATION_FAILED)

# 创建考勤记录（教师手动录入）
@api.route('/attendance', methods=['POST'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def create_attendance():
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        required_fields = ['course_id', 'student_id', 'status']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        # 验证状态值
        valid_statuses = ['present', 'late', 'absent']
        if data['status'] not in valid_statuses:
            raise ApiError(f"无效的考勤状态，有效值: {', '.join(valid_statuses)}", code=ErrorCode.VALIDATION_ERROR)
        
        attendance_id = AttendanceService.create_attendance(
            course_id=data['course_id'],
            student_id=data['student_id'],
            status=data['status'],
            check_in_time=data.get('check_in_time')
        )
        
        attendance = AttendanceService.get_attendance_by_id(attendance_id)
        return ok_response(attendance, message='考勤记录创建成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"创建考勤记录失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('创建考勤记录失败', code=ErrorCode.OPERATION_FAILED)

# 更新考勤记录
@api.route('/attendance/<int:attendance_id>', methods=['PUT'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def update_attendance(attendance_id):
    data = request.get_json() or {}
    
    try:
        # 验证状态值（如果提供）
        if 'status' in data:
            valid_statuses = ['present', 'late', 'absent']
            if data['status'] not in valid_statuses:
                raise ApiError(f"无效的考勤状态，有效值: {', '.join(valid_statuses)}", code=ErrorCode.VALIDATION_ERROR)
        
        updated_attendance = AttendanceService.update_attendance(attendance_id, data)
        return ok_response(updated_attendance, message='考勤记录更新成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"更新考勤记录失败: {str(e)}")
        raise ApiError('更新考勤记录失败', code=ErrorCode.OPERATION_FAILED)

# 删除考勤记录
@api.route('/attendance/<int:attendance_id>', methods=['DELETE'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def delete_attendance(attendance_id):
    try:
        AttendanceService.delete_attendance(attendance_id)
        return ok_response(message='考勤记录删除成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"删除考勤记录失败: {str(e)}")
        raise ApiError('删除考勤记录失败', code=ErrorCode.OPERATION_FAILED)

# ================== 学生签到相关路由 ==================

# 学生签到
@api.route('/attendance/check-in', methods=['POST'])
@jwt_required()
@role_required('student')
def student_check_in():
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        if 'course_id' not in data:
            raise ApiError('缺少必填字段: course_id', code=ErrorCode.VALIDATION_ERROR)
        
        result = AttendanceService.student_check_in(
            student_id=identity['id'],
            course_id=data['course_id'],
            check_in_code=data.get('check_in_code')
        )
        
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"学生签到失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('签到失败', code=ErrorCode.OPERATION_FAILED)

# 获取学生自己的考勤记录
@api.route('/attendance/my-records', methods=['GET'])
@jwt_required()
@role_required('student')
def get_my_attendance_records():
    identity = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    # 提取过滤参数
    filters = {'student_id': identity['id']}
    if request.args.get('course_id'):
        filters['course_id'] = request.args.get('course_id', type=int)
    if request.args.get('status'):
        filters['status'] = request.args.get('status')
    if request.args.get('date_from'):
        filters['date_from'] = request.args.get('date_from')
    if request.args.get('date_to'):
        filters['date_to'] = request.args.get('date_to')
    
    try:
        result = AttendanceService.get_attendances(page, page_size, **filters)
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取学生考勤记录失败: {str(e)}")
        raise ApiError('获取考勤记录失败', code=ErrorCode.OPERATION_FAILED)

# ================== 签到码管理相关路由 ==================

# 生成签到码（教师）
@api.route('/attendance/check-in-code', methods=['POST'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def generate_check_in_code():
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        if 'course_id' not in data:
            raise ApiError('缺少必填字段: course_id', code=ErrorCode.VALIDATION_ERROR)
        
        expiry_minutes = data.get('expiry_minutes', 60)
        if not isinstance(expiry_minutes, int) or expiry_minutes <= 0 or expiry_minutes > 480:
            raise ApiError('过期时间必须是1-480分钟之间的整数', code=ErrorCode.VALIDATION_ERROR)
        
        result = AttendanceService.generate_check_in_code(
            course_id=data['course_id'],
            expiry_minutes=expiry_minutes
        )
        
        return ok_response(result, message='签到码生成成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"生成签到码失败: {str(e)}")
        raise ApiError('生成签到码失败', code=ErrorCode.OPERATION_FAILED)

# ================== 考勤统计相关路由 ==================

# 获取考勤统计信息
@api.route('/attendance/statistics', methods=['GET'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def get_attendance_statistics():
    # 提取过滤参数
    course_id = request.args.get('course_id', type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    try:
        statistics = AttendanceService.get_attendance_statistics(
            course_id=course_id,
            date_from=date_from,
            date_to=date_to
        )
        return ok_response(statistics)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取考勤统计失败: {str(e)}")
        raise ApiError('获取考勤统计失败', code=ErrorCode.OPERATION_FAILED)

# 获取学生个人考勤统计
@api.route('/attendance/my-statistics', methods=['GET'])
@jwt_required()
@role_required('student')
def get_my_attendance_statistics():
    identity = get_jwt_identity()
    
    # 提取过滤参数
    course_id = request.args.get('course_id', type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    try:
        # 使用学生ID作为过滤条件获取统计
        from core.helpers import get_db
        conn = get_db()
        cursor = conn.cursor()
        
        # 构建查询条件
        where_clauses = ['a.student_id = ?']
        params = [identity['id']]
        
        if course_id:
            where_clauses.append('a.course_id = ?')
            params.append(course_id)
        
        if date_from:
            where_clauses.append('DATE(a.check_in_time) >= ?')
            params.append(date_from)
        
        if date_to:
            where_clauses.append('DATE(a.check_in_time) <= ?')
            params.append(date_to)
        
        where_clause = ' AND '.join(where_clauses)
        
        # 获取个人统计
        cursor.execute(f'''
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'present' THEN 1 END) as present_count,
                COUNT(CASE WHEN status = 'late' THEN 1 END) as late_count,
                COUNT(CASE WHEN status = 'absent' THEN 1 END) as absent_count
            FROM attendance a
            WHERE {where_clause}
        ''', params)
        
        stats = dict(cursor.fetchone())
        
        # 计算百分比
        total = stats['total']
        if total > 0:
            stats['present_rate'] = round(stats['present_count'] / total * 100, 2)
            stats['late_rate'] = round(stats['late_count'] / total * 100, 2)
            stats['absent_rate'] = round(stats['absent_count'] / total * 100, 2)
        else:
            stats.update({'present_rate': 0, 'late_rate': 0, 'absent_rate': 0})
        
        # 按课程统计
        cursor.execute(f'''
            SELECT 
                c.id as course_id,
                c.title as course_title,
                COUNT(*) as total,
                COUNT(CASE WHEN a.status = 'present' THEN 1 END) as present_count,
                COUNT(CASE WHEN a.status = 'late' THEN 1 END) as late_count,
                COUNT(CASE WHEN a.status = 'absent' THEN 1 END) as absent_count
            FROM attendance a
            JOIN courses c ON a.course_id = c.id
            WHERE {where_clause}
            GROUP BY c.id, c.title
            ORDER BY total DESC
        ''', params)
        
        course_stats = [dict(row) for row in cursor.fetchall()]
        for stat in course_stats:
            total = stat['total']
            if total > 0:
                stat['present_rate'] = round(stat['present_count'] / total * 100, 2)
        
        conn.close()
        
        return ok_response({
            'overall_stats': stats,
            'course_stats': course_stats
        })
    except Exception as e:
        api.logger.error(f"获取个人考勤统计失败: {str(e)}")
        raise ApiError('获取个人考勤统计失败', code=ErrorCode.OPERATION_FAILED)

# ================== 数据导出相关路由 ==================

# 导出考勤数据
@api.route('/attendance/export', methods=['GET'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def export_attendance_data():
    # 提取过滤参数
    course_id = request.args.get('course_id', type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    try:
        data = AttendanceService.export_attendance_data(
            course_id=course_id,
            date_from=date_from,
            date_to=date_to
        )
        
        return ok_response({
            'data': data,
            'total_records': len(data),
            'export_time': datetime.now().isoformat()
        }, message='考勤数据导出成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"导出考勤数据失败: {str(e)}")
        raise ApiError('导出考勤数据失败', code=ErrorCode.OPERATION_FAILED) 