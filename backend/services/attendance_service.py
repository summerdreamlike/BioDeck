"""
考勤服务模块

负责考勤管理、签到、统计分析和数据导出
"""
from datetime import datetime, timedelta
import traceback
import random
import string

from core.helpers import get_db, db_fetch_one, db_fetch_all, db_execute
from core.errors import ApiError, ErrorCode
from models import Attendance

class AttendanceService:
    @staticmethod
    def get_attendances(page=1, page_size=20, **filters):
        """
        获取考勤记录列表
        
        :param page: 页码
        :param page_size: 每页数量
        :param filters: 过滤条件
        :return: 考勤记录列表及分页信息
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 构建查询
            sql = '''
                SELECT a.*, u.name as student_name, u.student_id as student_number, 
                       c.title as course_title, c.start_time as course_start_time
                FROM attendance a
                JOIN users u ON a.student_id = u.id
                LEFT JOIN courses c ON a.course_id = c.id
                WHERE 1=1
            '''
            params = []
            
            # 应用过滤器
            if 'course_id' in filters and filters['course_id']:
                sql += ' AND a.course_id = ?'
                params.append(filters['course_id'])
            
            if 'student_id' in filters and filters['student_id']:
                sql += ' AND a.student_id = ?'
                params.append(filters['student_id'])
            
            if 'status' in filters and filters['status']:
                sql += ' AND a.status = ?'
                params.append(filters['status'])
            
            if 'date_from' in filters and filters['date_from']:
                sql += ' AND DATE(a.check_in_time) >= ?'
                params.append(filters['date_from'])
            
            if 'date_to' in filters and filters['date_to']:
                sql += ' AND DATE(a.check_in_time) <= ?'
                params.append(filters['date_to'])
            
            # 排序
            sql += ' ORDER BY a.check_in_time DESC'
            
            # 计算总数
            count_sql = f"SELECT COUNT(*) as total FROM ({sql})"
            cursor.execute(count_sql, params)
            total = cursor.fetchone()['total']
            
            # 应用分页
            sql += ' LIMIT ? OFFSET ?'
            offset = (page - 1) * page_size
            params.extend([page_size, offset])
            
            # 执行查询
            cursor.execute(sql, params)
            attendances = [dict(row) for row in cursor.fetchall()]
            
            return {
                'items': attendances,
                'total': total,
                'page': page,
                'page_size': page_size,
                'pages': (total + page_size - 1) // page_size
            }
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取考勤记录失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_attendance_by_id(attendance_id):
        """
        获取考勤记录详情
        
        :param attendance_id: 考勤记录ID
        :return: 考勤记录详情
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT a.*, u.name as student_name, u.student_id as student_number,
                       c.title as course_title
                FROM attendance a
                JOIN users u ON a.student_id = u.id
                LEFT JOIN courses c ON a.course_id = c.id
                WHERE a.id = ?
            ''', (attendance_id,))
            
            attendance = cursor.fetchone()
            if not attendance:
                raise ApiError('考勤记录不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            return dict(attendance)
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取考勤记录详情失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def create_attendance(course_id, student_id, status='present', check_in_time=None):
        """
        创建考勤记录
        
        :param course_id: 课程ID
        :param student_id: 学生ID
        :param status: 考勤状态（present, absent, late）
        :param check_in_time: 签到时间
        :return: 新考勤记录ID
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证课程是否存在
            cursor.execute('SELECT id FROM courses WHERE id = ?', (course_id,))
            if not cursor.fetchone():
                raise ApiError('课程不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证学生是否存在
            cursor.execute('SELECT id FROM users WHERE id = ? AND role = ?', (student_id, 'student'))
            if not cursor.fetchone():
                raise ApiError('学生不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 检查是否已有考勤记录
            cursor.execute('SELECT id FROM attendance WHERE course_id = ? AND student_id = ?', (course_id, student_id))
            if cursor.fetchone():
                raise ApiError('该学生在此课程已有考勤记录', code=ErrorCode.VALIDATION_ERROR)
            
            # 如果没有指定签到时间，使用当前时间
            if not check_in_time:
                check_in_time = datetime.now()
            
            # 创建考勤记录
            cursor.execute('''
                INSERT INTO attendance (course_id, student_id, status, check_in_time, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (course_id, student_id, status, check_in_time, datetime.now()))
            
            attendance_id = cursor.lastrowid
            conn.commit()
            return attendance_id
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'创建考勤记录失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def update_attendance(attendance_id, data):
        """
        更新考勤记录
        
        :param attendance_id: 考勤记录ID
        :param data: 更新数据
        :return: 更新后的考勤记录
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证考勤记录是否存在
            cursor.execute('SELECT * FROM attendance WHERE id = ?', (attendance_id,))
            attendance = cursor.fetchone()
            if not attendance:
                raise ApiError('考勤记录不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            attendance_dict = dict(attendance)
            
            # 准备更新数据
            updates = []
            params = []
            
            # 可更新字段
            allowed_fields = ['status', 'check_in_time', 'remarks']
            
            for field in allowed_fields:
                if field in data:
                    updates.append(f'{field} = ?')
                    params.append(data[field])
            
            if not updates:
                return AttendanceService.get_attendance_by_id(attendance_id)
            
            # 执行更新
            sql = f'''
                UPDATE attendance
                SET {', '.join(updates)}
                WHERE id = ?
            '''
            params.append(attendance_id)
            cursor.execute(sql, params)
            conn.commit()
            
            # 返回更新后的数据
            return AttendanceService.get_attendance_by_id(attendance_id)
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'更新考勤记录失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def delete_attendance(attendance_id):
        """
        删除考勤记录
        
        :param attendance_id: 考勤记录ID
        :return: 成功返回True
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证考勤记录是否存在
            cursor.execute('SELECT id FROM attendance WHERE id = ?', (attendance_id,))
            if not cursor.fetchone():
                raise ApiError('考勤记录不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 删除考勤记录
            cursor.execute('DELETE FROM attendance WHERE id = ?', (attendance_id,))
            conn.commit()
            return True
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'删除考勤记录失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def student_check_in(student_id, course_id, check_in_code=None):
        """
        学生签到
        
        :param student_id: 学生ID
        :param course_id: 课程ID
        :param check_in_code: 签到码（可选）
        :return: 签到结果
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证课程是否存在
            cursor.execute('SELECT * FROM courses WHERE id = ?', (course_id,))
            course = cursor.fetchone()
            if not course:
                raise ApiError('课程不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            course_dict = dict(course)
            
            # 验证学生是否在课程中
            cursor.execute('SELECT 1 FROM course_students WHERE course_id = ? AND student_id = ?', (course_id, student_id))
            if not cursor.fetchone():
                raise ApiError('您不在此课程中', code=ErrorCode.PERMISSION_DENIED)
            
            # 检查是否已签到
            cursor.execute('SELECT id FROM attendance WHERE course_id = ? AND student_id = ?', (course_id, student_id))
            if cursor.fetchone():
                raise ApiError('您已经签到过了', code=ErrorCode.VALIDATION_ERROR)
            
            # 验证签到码（如果提供）
            if check_in_code:
                # 这里可以添加签到码验证逻辑
                # 例如从课程表或临时存储中获取当前有效的签到码
                pass
            
            # 判断签到状态
            now = datetime.now()
            course_start_time = datetime.fromisoformat(course_dict['start_time'].replace('Z', '+00:00'))
            
            # 允许提前30分钟签到，迟到15分钟内算迟到，超过15分钟算缺勤
            early_time = course_start_time - timedelta(minutes=30)
            late_time = course_start_time + timedelta(minutes=15)
            
            if now < early_time:
                raise ApiError('签到时间还未开始', code=ErrorCode.VALIDATION_ERROR)
            elif now <= course_start_time:
                status = 'present'
            elif now <= late_time:
                status = 'late'
            else:
                status = 'absent'
            
            # 创建签到记录
            attendance_id = AttendanceService.create_attendance(
                course_id=course_id,
                student_id=student_id,
                status=status,
                check_in_time=now
            )
            
            return {
                'attendance_id': attendance_id,
                'status': status,
                'check_in_time': now.isoformat(),
                'message': f'签到成功，状态：{AttendanceService._get_status_text(status)}'
            }
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'签到失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_attendance_statistics(course_id=None, date_from=None, date_to=None):
        """
        获取考勤统计信息
        
        :param course_id: 课程ID（可选）
        :param date_from: 开始日期（可选）
        :param date_to: 结束日期（可选）
        :return: 考勤统计信息
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 基础查询条件
            where_clauses = []
            params = []
            
            if course_id:
                where_clauses.append('a.course_id = ?')
                params.append(course_id)
            
            if date_from:
                where_clauses.append('DATE(a.check_in_time) >= ?')
                params.append(date_from)
            
            if date_to:
                where_clauses.append('DATE(a.check_in_time) <= ?')
                params.append(date_to)
            
            where_clause = ' AND '.join(where_clauses) if where_clauses else '1=1'
            
            # 总体统计
            cursor.execute(f'''
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN status = 'present' THEN 1 END) as present_count,
                    COUNT(CASE WHEN status = 'late' THEN 1 END) as late_count,
                    COUNT(CASE WHEN status = 'absent' THEN 1 END) as absent_count
                FROM attendance a
                WHERE {where_clause}
            ''', params)
            
            overall_stats = dict(cursor.fetchone())
            
            # 计算百分比
            total = overall_stats['total']
            if total > 0:
                overall_stats['present_rate'] = round(overall_stats['present_count'] / total * 100, 2)
                overall_stats['late_rate'] = round(overall_stats['late_count'] / total * 100, 2)
                overall_stats['absent_rate'] = round(overall_stats['absent_count'] / total * 100, 2)
            else:
                overall_stats.update({'present_rate': 0, 'late_rate': 0, 'absent_rate': 0})
            
            # 按日期统计
            cursor.execute(f'''
                SELECT 
                    DATE(a.check_in_time) as date,
                    COUNT(*) as total,
                    COUNT(CASE WHEN status = 'present' THEN 1 END) as present_count,
                    COUNT(CASE WHEN status = 'late' THEN 1 END) as late_count,
                    COUNT(CASE WHEN status = 'absent' THEN 1 END) as absent_count
                FROM attendance a
                WHERE {where_clause}
                GROUP BY DATE(a.check_in_time)
                ORDER BY date DESC
                LIMIT 30
            ''', params)
            
            daily_stats = [dict(row) for row in cursor.fetchall()]
            
            # 按课程统计（如果没有指定course_id）
            course_stats = []
            if not course_id:
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
            
            # 学生考勤排名
            cursor.execute(f'''
                SELECT 
                    u.id as student_id,
                    u.name as student_name,
                    u.student_id as student_number,
                    COUNT(*) as total_attendance,
                    COUNT(CASE WHEN a.status = 'present' THEN 1 END) as present_count,
                    COUNT(CASE WHEN a.status = 'late' THEN 1 END) as late_count,
                    COUNT(CASE WHEN a.status = 'absent' THEN 1 END) as absent_count
                FROM attendance a
                JOIN users u ON a.student_id = u.id
                WHERE {where_clause}
                GROUP BY u.id, u.name, u.student_id
                ORDER BY present_count DESC, late_count ASC, absent_count ASC
                LIMIT 20
            ''', params)
            
            student_rankings = [dict(row) for row in cursor.fetchall()]
            for ranking in student_rankings:
                total = ranking['total_attendance']
                if total > 0:
                    ranking['attendance_rate'] = round(ranking['present_count'] / total * 100, 2)
                else:
                    ranking['attendance_rate'] = 0
            
            return {
                'overall_stats': overall_stats,
                'daily_stats': daily_stats,
                'course_stats': course_stats,
                'student_rankings': student_rankings
            }
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取考勤统计失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def export_attendance_data(course_id=None, date_from=None, date_to=None):
        """
        导出考勤数据
        
        :param course_id: 课程ID（可选）
        :param date_from: 开始日期（可选）
        :param date_to: 结束日期（可选）
        :return: 导出数据
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 构建查询
            sql = '''
                SELECT 
                    u.name as student_name,
                    u.student_id as student_number,
                    c.title as course_title,
                    a.status,
                    a.check_in_time,
                    a.remarks,
                    a.created_at
                FROM attendance a
                JOIN users u ON a.student_id = u.id
                LEFT JOIN courses c ON a.course_id = c.id
                WHERE 1=1
            '''
            params = []
            
            if course_id:
                sql += ' AND a.course_id = ?'
                params.append(course_id)
            
            if date_from:
                sql += ' AND DATE(a.check_in_time) >= ?'
                params.append(date_from)
            
            if date_to:
                sql += ' AND DATE(a.check_in_time) <= ?'
                params.append(date_to)
            
            sql += ' ORDER BY a.check_in_time DESC'
            
            cursor.execute(sql, params)
            records = [dict(row) for row in cursor.fetchall()]
            
            # 处理状态文本
            for record in records:
                record['status_text'] = AttendanceService._get_status_text(record['status'])
            
            return records
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'导出考勤数据失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def generate_check_in_code(course_id, expiry_minutes=60):
        """
        生成签到码
        
        :param course_id: 课程ID
        :param expiry_minutes: 过期时间（分钟）
        :return: 签到码信息
        """
        # 生成6位随机数字码
        code = ''.join(random.choices(string.digits, k=6))
        expiry_time = datetime.now() + timedelta(minutes=expiry_minutes)
        
        # 这里可以将签到码存储到缓存或临时表中
        # 为简化实现，这里只返回码和过期时间
        
        return {
            'code': code,
            'course_id': course_id,
            'expiry_time': expiry_time.isoformat(),
            'expiry_minutes': expiry_minutes
        }
    
    @staticmethod
    def _get_status_text(status):
        """
        获取状态文本
        
        :param status: 状态码
        :return: 状态文本
        """
        status_map = {
            'present': '出勤',
            'late': '迟到',
            'absent': '缺勤'
        }
        return status_map.get(status, status) 