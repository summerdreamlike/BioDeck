"""
课程服务模块

负责课程管理、在线课堂和消息交互功能
"""
from datetime import datetime
import json
import traceback

from core.helpers import get_db, db_fetch_one, db_fetch_all, db_execute
from core.errors import ApiError, ErrorCode
from models import Course, CourseMessage

class CourseService:
    @staticmethod
    def get_courses(page=1, page_size=10, **filters):
        """
        获取课程列表
        
        :param page: 页码
        :param page_size: 每页数量
        :param filters: 过滤条件
        :return: 课程列表及分页信息
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 构建查询
            sql = '''
                SELECT c.*, u.name as teacher_name, COUNT(cs.student_id) as student_count 
                FROM courses c
                LEFT JOIN users u ON c.teacher_id = u.id
                LEFT JOIN course_students cs ON c.id = cs.course_id
                WHERE 1=1
            '''
            params = []
            
            # 应用过滤器
            if 'teacher_id' in filters:
                sql += ' AND c.teacher_id = ?'
                params.append(filters['teacher_id'])
            
            if 'title' in filters:
                sql += ' AND c.title LIKE ?'
                params.append(f"%{filters['title']}%")
                
            if 'status' in filters:
                sql += ' AND c.status = ?'
                params.append(filters['status'])
            
            # 分组
            sql += ' GROUP BY c.id'
            
            # 排序
            sql += ' ORDER BY c.start_time DESC'
            
            # 计算总数
            count_sql = f'SELECT COUNT(*) as total FROM ({sql})'
            cursor.execute(count_sql, params)
            total = cursor.fetchone()['total']
            
            # 应用分页
            sql += ' LIMIT ? OFFSET ?'
            offset = (page - 1) * page_size
            params.extend([page_size, offset])
            
            # 执行查询
            cursor.execute(sql, params)
            courses = [dict(row) for row in cursor.fetchall()]
            
            return {
                'items': courses,
                'total': total,
                'page': page,
                'page_size': page_size,
                'pages': (total + page_size - 1) // page_size
            }
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取课程列表失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_course_by_id(course_id):
        """
        获取课程详情
        
        :param course_id: 课程ID
        :return: 课程详情
        """
        return Course.get_by_id(course_id)
    
    @staticmethod
    def get_live_courses():
        """
        获取当前直播中、即将开始和已结束的课程
        
        :return: 课程列表
        """
        return Course.get_live_courses()
    
    @staticmethod
    def create_course(teacher_id, title, start_time, end_time, poster_url=None, video_url=None):
        """
        创建课程
        
        :param teacher_id: 教师ID
        :param title: 课程标题
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param poster_url: 海报URL
        :param video_url: 视频URL
        :return: 课程ID
        """
        # 验证开始和结束时间
        try:
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            if end_dt <= start_dt:
                raise ApiError('结束时间必须晚于开始时间', code=ErrorCode.VALIDATION_ERROR)
        except ValueError:
            raise ApiError('无效的时间格式', code=ErrorCode.VALIDATION_ERROR)
        
        course_id = Course.create(
            title=title,
            teacher_id=teacher_id,
            start_time=start_time,
            end_time=end_time,
            poster_url=poster_url,
            video_url=video_url
        )
        return course_id
    
    @staticmethod
    def update_course(course_id, data):
        """
        更新课程信息
        
        :param course_id: 课程ID
        :param data: 更新数据
        :return: 更新后的课程信息
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证课程是否存在
            cursor.execute('SELECT id FROM courses WHERE id = ?', (course_id,))
            if not cursor.fetchone():
                raise ApiError('课程不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 准备更新数据
            updates = []
            params = []
            
            # 可更新字段
            allowed_fields = ['title', 'teacher_id', 'start_time', 'end_time', 'status', 'poster_url', 'video_url']
            
            for field in allowed_fields:
                if field in data:
                    updates.append(f'{field} = ?')
                    params.append(data[field])
            
            if not updates:
                return CourseService.get_course_by_id(course_id)
            
            # 执行更新
            sql = f'''
                UPDATE courses
                SET {', '.join(updates)}
                WHERE id = ?
            '''
            params.append(course_id)
            cursor.execute(sql, params)
            conn.commit()
            
            # 返回更新后的数据
            return CourseService.get_course_by_id(course_id)
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'更新课程失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def delete_course(course_id):
        """
        删除课程
        
        :param course_id: 课程ID
        :return: 成功返回True
        """
        if Course.delete(course_id):
            return True
        raise ApiError('删除课程失败', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def add_student_to_course(course_id, student_id):
        """
        将学生添加到课程
        
        :param course_id: 课程ID
        :param student_id: 学生ID
        :return: 成功返回True
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证课程和学生是否存在
            cursor.execute('SELECT id FROM courses WHERE id = ?', (course_id,))
            if not cursor.fetchone():
                raise ApiError('课程不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            cursor.execute('SELECT id FROM users WHERE id = ? AND role = ?', (student_id, 'student'))
            if not cursor.fetchone():
                raise ApiError('学生不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 检查学生是否已在课程中
            cursor.execute('SELECT 1 FROM course_students WHERE course_id = ? AND student_id = ?', (course_id, student_id))
            if cursor.fetchone():
                return True  # 学生已在课程中，视为成功
            
            # 添加学生到课程
            cursor.execute('''
                INSERT INTO course_students (course_id, student_id, joined_at)
                VALUES (?, ?, ?)
            ''', (course_id, student_id, datetime.now()))
            
            conn.commit()
            return True
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'添加学生到课程失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def remove_student_from_course(course_id, student_id):
        """
        从课程中移除学生
        
        :param course_id: 课程ID
        :param student_id: 学生ID
        :return: 成功返回True
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证关系是否存在
            cursor.execute('SELECT 1 FROM course_students WHERE course_id = ? AND student_id = ?', (course_id, student_id))
            if not cursor.fetchone():
                raise ApiError('学生不在此课程中', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 移除学生
            cursor.execute('DELETE FROM course_students WHERE course_id = ? AND student_id = ?', (course_id, student_id))
            
            conn.commit()
            return True
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'从课程移除学生失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_course_students(course_id):
        """
        获取课程的所有学生
        
        :param course_id: 课程ID
        :return: 学生列表
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证课程是否存在
            cursor.execute('SELECT id FROM courses WHERE id = ?', (course_id,))
            if not cursor.fetchone():
                raise ApiError('课程不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 获取学生列表
            cursor.execute('''
                SELECT u.id, u.username, u.name, u.student_id, cs.joined_at
                FROM users u
                JOIN course_students cs ON u.id = cs.student_id
                WHERE cs.course_id = ?
                ORDER BY u.name
            ''', (course_id,))
            
            students = [dict(row) for row in cursor.fetchall()]
            return students
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取课程学生列表失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def send_course_message(course_id, sender_id, message):
        """
        发送课程消息
        
        :param course_id: 课程ID
        :param sender_id: 发送者ID
        :param message: 消息内容
        :return: 新消息对象
        """
        # 验证消息长度
        if not message or len(message) > 1000:
            raise ApiError('消息长度无效', code=ErrorCode.VALIDATION_ERROR)
        
        # 创建消息
        return CourseMessage.create(course_id, sender_id, message)
    
    @staticmethod
    def get_course_messages(course_id):
        """
        获取课程消息
        
        :param course_id: 课程ID
        :return: 消息列表
        """
        return CourseMessage.get_by_course_id(course_id) 