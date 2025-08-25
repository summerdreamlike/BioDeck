"""
任务服务模块

负责任务的发布、管理、提交和统计分析
"""
from datetime import datetime
import traceback

from core.helpers import get_db, db_fetch_one, db_fetch_all, db_execute
from core.errors import ApiError, ErrorCode
from models import Task, Paper

class TaskService:
    @staticmethod
    def get_tasks(page=1, page_size=10, **filters):
        """
        获取任务列表
        
        :param page: 页码
        :param page_size: 每页数量
        :param filters: 过滤条件
        :return: 任务列表及分页信息
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 构建查询
            sql = '''
                SELECT t.*, u.name as creator_name, p.name as paper_name
                FROM tasks t
                JOIN users u ON t.creator_id = u.id
                LEFT JOIN papers p ON t.paper_id = p.id
                WHERE 1=1
            '''
            params = []
            
            # 应用过滤器
            if 'creator_id' in filters and filters['creator_id']:
                sql += ' AND t.creator_id = ?'
                params.append(filters['creator_id'])
            
            if 'title' in filters and filters['title']:
                sql += ' AND t.title LIKE ?'
                params.append(f"%{filters['title']}%")
            
            if 'class_name' in filters and filters['class_name']:
                sql += ' AND t.id IN (SELECT task_id FROM task_classes WHERE class_name = ?)'
                params.append(filters['class_name'])
                
            if 'status' in filters:
                now = datetime.now().isoformat()
                if filters['status'] == 'upcoming':
                    sql += ' AND t.due_date > ?'
                    params.append(now)
                elif filters['status'] == 'expired':
                    sql += ' AND (t.due_date < ? AND t.allow_late_submission = 0)'
                    params.append(now)
                elif filters['status'] == 'late':
                    sql += ' AND (t.due_date < ? AND t.allow_late_submission = 1)'
                    params.append(now)
            
            # 获取与特定学生相关的任务
            if 'student_id' in filters and filters['student_id']:
                sql += ' AND EXISTS (SELECT 1 FROM students s JOIN task_classes tc ON s.class = tc.class_name WHERE s.id = ? AND tc.task_id = t.id)'
                params.append(filters['student_id'])
            
            # 排序
            order_by = filters.get('order_by', 'due_date')
            order_dir = 'DESC' if filters.get('order_dir', 'desc').upper() == 'DESC' else 'ASC'
            
            if order_by == 'due_date':
                sql += f' ORDER BY t.due_date {order_dir}'
            elif order_by == 'created_at':
                sql += f' ORDER BY t.created_at {order_dir}'
            elif order_by == 'title':
                sql += f' ORDER BY t.title {order_dir}'
            else:
                sql += ' ORDER BY t.due_date DESC'
            
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
            tasks = [dict(row) for row in cursor.fetchall()]
            
            # 获取每个任务的班级和提交统计
            for task in tasks:
                # 获取班级
                cursor.execute('SELECT class_name FROM task_classes WHERE task_id = ?', (task['id'],))
                task['classes'] = [row['class_name'] for row in cursor.fetchall()]
                
                # 获取提交统计
                cursor.execute('''
                    SELECT COUNT(ts.id) as submitted_count,
                           (SELECT COUNT(*) FROM students s JOIN task_classes tc ON s.class = tc.class_name WHERE tc.task_id = ?) as total_students
                    FROM task_submissions ts
                    WHERE ts.task_id = ?
                ''', (task['id'], task['id']))
                
                stats = cursor.fetchone()
                if stats:
                    task['submitted_count'] = stats['submitted_count']
                    task['total_students'] = stats['total_students']
                    task['completion_rate'] = round((stats['submitted_count'] / stats['total_students'] * 100), 2) if stats['total_students'] > 0 else 0
                else:
                    task['submitted_count'] = 0
                    task['total_students'] = 0
                    task['completion_rate'] = 0
                
                # 获取平均分
                cursor.execute('SELECT AVG(score) as avg_score FROM task_submissions WHERE task_id = ? AND score IS NOT NULL', (task['id'],))
                avg_score_row = cursor.fetchone()
                task['avg_score'] = round(avg_score_row['avg_score'], 2) if avg_score_row and avg_score_row['avg_score'] else None
            
            return {
                'items': tasks,
                'total': total,
                'page': page,
                'page_size': page_size,
                'pages': (total + page_size - 1) // page_size
            }
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取任务列表失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_task_by_id(task_id):
        """
        获取任务详情
        
        :param task_id: 任务ID
        :return: 任务详情
        """
        task = Task.get_by_id(task_id)
        if not task:
            raise ApiError('任务不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
        return task
    
    @staticmethod
    def create_task(title, description, creator_id, due_date, classes, paper_id=None, allow_late_submission=False):
        """
        创建任务
        
        :param title: 任务标题
        :param description: 任务描述
        :param creator_id: 创建者ID
        :param due_date: 截止日期
        :param classes: 班级列表
        :param paper_id: 试卷ID（可选）
        :param allow_late_submission: 是否允许迟交
        :return: 新任务ID
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证创建者是否存在
            cursor.execute('SELECT id FROM users WHERE id = ? AND role IN (?, ?)', (creator_id, 'admin', 'teacher'))
            if not cursor.fetchone():
                raise ApiError('创建者不存在或无权创建任务', code=ErrorCode.PERMISSION_DENIED)
            
            # 验证班级是否为空
            if not classes:
                raise ApiError('班级列表不能为空', code=ErrorCode.VALIDATION_ERROR)
            
            # 验证班级是否存在
            unique_classes = set(classes)
            placeholders = ','.join(['?' for _ in unique_classes])
            cursor.execute(f'SELECT class, COUNT(*) FROM students WHERE class IN ({placeholders}) GROUP BY class', list(unique_classes))
            existing_classes = {row['class']: row['COUNT(*)'] for row in cursor.fetchall()}
            
            missing_classes = unique_classes - set(existing_classes.keys())
            if missing_classes:
                raise ApiError(f'以下班级不存在: {", ".join(missing_classes)}', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证试卷是否存在（如果提供）
            if paper_id:
                cursor.execute('SELECT id FROM papers WHERE id = ?', (paper_id,))
                if not cursor.fetchone():
                    raise ApiError('试卷不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 创建任务
            task_id = Task.create(
                title=title,
                description=description,
                creator_id=creator_id,
                due_date=due_date,
                classes=list(unique_classes),
                paper_id=paper_id,
                allow_late_submission=allow_late_submission
            )
            
            return task_id
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'创建任务失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def update_task(task_id, data):
        """
        更新任务
        
        :param task_id: 任务ID
        :param data: 更新数据
        :return: 更新后的任务详情
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证任务是否存在
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            task = cursor.fetchone()
            if not task:
                raise ApiError('任务不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            task_dict = dict(task)
            
            # 验证试卷是否存在（如果提供）
            if 'paper_id' in data and data['paper_id']:
                cursor.execute('SELECT id FROM papers WHERE id = ?', (data['paper_id'],))
                if not cursor.fetchone():
                    raise ApiError('试卷不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证班级是否存在（如果提供）
            if 'classes' in data and data['classes']:
                if not data['classes']:
                    raise ApiError('班级列表不能为空', code=ErrorCode.VALIDATION_ERROR)
                
                unique_classes = set(data['classes'])
                placeholders = ','.join(['?' for _ in unique_classes])
                cursor.execute(f'SELECT class, COUNT(*) FROM students WHERE class IN ({placeholders}) GROUP BY class', list(unique_classes))
                existing_classes = {row['class']: row['COUNT(*)'] for row in cursor.fetchall()}
                
                missing_classes = unique_classes - set(existing_classes.keys())
                if missing_classes:
                    raise ApiError(f'以下班级不存在: {", ".join(missing_classes)}', code=ErrorCode.RESOURCE_NOT_FOUND)
                
                data['classes'] = list(unique_classes)
            
            # 更新任务
            Task.update(
                task_id=task_id,
                title=data.get('title', task_dict['title']),
                description=data.get('description', task_dict['description']),
                paper_id=data.get('paper_id', task_dict['paper_id']),
                due_date=data.get('due_date', task_dict['due_date']),
                allow_late_submission=data.get('allow_late_submission', task_dict['allow_late_submission']),
                classes=data.get('classes')
            )
            
            return TaskService.get_task_by_id(task_id)
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'更新任务失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def delete_task(task_id):
        """
        删除任务
        
        :param task_id: 任务ID
        :return: 成功返回True
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证任务是否存在
            cursor.execute('SELECT id FROM tasks WHERE id = ?', (task_id,))
            if not cursor.fetchone():
                raise ApiError('任务不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 删除任务
            Task.delete(task_id)
            return True
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'删除任务失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_task_statistics(task_id):
        """
        获取任务统计信息
        
        :param task_id: 任务ID
        :return: 任务统计信息
        """
        stats = Task.get_statistics(task_id)
        if not stats:
            raise ApiError('任务不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
        return stats
    
    @staticmethod
    def get_student_tasks(student_id, status=None):
        """
        获取学生的任务列表
        
        :param student_id: 学生ID
        :param status: 任务状态（可选）
        :return: 学生的任务列表
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 获取学生信息
            cursor.execute('SELECT id, class FROM students WHERE id = ?', (student_id,))
            student = cursor.fetchone()
            if not student:
                raise ApiError('学生不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            student_class = student['class']
            now = datetime.now().isoformat()
            
            # 构建查询
            sql = '''
                SELECT t.*, u.name as creator_name, p.name as paper_name,
                       (SELECT COUNT(*) FROM task_submissions ts WHERE ts.task_id = t.id AND ts.student_id = ?) as submitted
                FROM tasks t
                JOIN task_classes tc ON t.id = tc.task_id
                JOIN users u ON t.creator_id = u.id
                LEFT JOIN papers p ON t.paper_id = p.id
                WHERE tc.class_name = ?
            '''
            params = [student_id, student_class]
            
            # 根据状态过滤
            if status == 'upcoming':
                sql += ' AND t.due_date > ?'
                params.append(now)
            elif status == 'expired':
                sql += ' AND (t.due_date < ? AND t.allow_late_submission = 0)'
                params.append(now)
            elif status == 'late':
                sql += ' AND (t.due_date < ? AND t.allow_late_submission = 1)'
                params.append(now)
            elif status == 'submitted':
                sql += ' AND EXISTS (SELECT 1 FROM task_submissions ts WHERE ts.task_id = t.id AND ts.student_id = ?)'
                params.append(student_id)
            elif status == 'not_submitted':
                sql += ' AND NOT EXISTS (SELECT 1 FROM task_submissions ts WHERE ts.task_id = t.id AND ts.student_id = ?)'
                params.append(student_id)
            
            sql += ' ORDER BY t.due_date ASC'
            
            cursor.execute(sql, params)
            tasks = [dict(row) for row in cursor.fetchall()]
            
            # 处理状态
            for task in tasks:
                task['submitted'] = bool(task['submitted'])
                if task['due_date'] > now:
                    task['status'] = 'upcoming'
                elif task['due_date'] < now and not task['allow_late_submission']:
                    task['status'] = 'expired'
                else:
                    task['status'] = 'active'
            
            return tasks
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取学生任务列表失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def submit_task(task_id, student_id, answers=None, file_urls=None):
        """
        提交任务
        
        :param task_id: 任务ID
        :param student_id: 学生ID
        :param answers: 答案（可选）
        :param file_urls: 文件URL（可选）
        :return: 提交ID
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证任务是否存在
            cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            task = cursor.fetchone()
            if not task:
                raise ApiError('任务不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            task_dict = dict(task)
            
            # 验证学生是否存在
            cursor.execute('SELECT id, class FROM students WHERE id = ?', (student_id,))
            student = cursor.fetchone()
            if not student:
                raise ApiError('学生不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证学生是否在任务的班级中
            student_class = student['class']
            cursor.execute('SELECT 1 FROM task_classes WHERE task_id = ? AND class_name = ?', (task_id, student_class))
            if not cursor.fetchone():
                raise ApiError('此任务不适用于您的班级', code=ErrorCode.PERMISSION_DENIED)
            
            # 验证截止时间
            now = datetime.now().isoformat()
            if task_dict['due_date'] < now and not task_dict['allow_late_submission']:
                raise ApiError('任务已过截止时间，不允许迟交', code=ErrorCode.VALIDATION_ERROR)
            
            # 检查是否已提交
            cursor.execute('SELECT id FROM task_submissions WHERE task_id = ? AND student_id = ?', (task_id, student_id))
            existing_submission = cursor.fetchone()
            
            if existing_submission:
                # 更新现有提交
                if answers is not None:
                    cursor.execute(
                        'UPDATE task_submissions SET answers = ?, updated_at = ? WHERE id = ?',
                        (answers, now, existing_submission['id'])
                    )
                
                if file_urls is not None:
                    cursor.execute(
                        'UPDATE task_submissions SET file_urls = ?, updated_at = ? WHERE id = ?',
                        (file_urls, now, existing_submission['id'])
                    )
                
                submission_id = existing_submission['id']
            else:
                # 创建新提交
                cursor.execute(
                    'INSERT INTO task_submissions (task_id, student_id, answers, file_urls, submitted_at) VALUES (?, ?, ?, ?, ?)',
                    (task_id, student_id, answers, file_urls, now)
                )
                submission_id = cursor.lastrowid
            
            conn.commit()
            return submission_id
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'提交任务失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def grade_submission(submission_id, score, feedback=None):
        """
        评分提交
        
        :param submission_id: 提交ID
        :param score: 分数
        :param feedback: 反馈（可选）
        :return: 更新后的提交
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证提交是否存在
            cursor.execute('SELECT * FROM task_submissions WHERE id = ?', (submission_id,))
            submission = cursor.fetchone()
            if not submission:
                raise ApiError('提交记录不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证分数
            if score is None or not isinstance(score, (int, float)) or score < 0 or score > 100:
                raise ApiError('分数必须是0-100之间的数值', code=ErrorCode.VALIDATION_ERROR)
            
            # 更新分数和反馈
            cursor.execute(
                'UPDATE task_submissions SET score = ?, feedback = ?, graded_at = ? WHERE id = ?',
                (score, feedback, datetime.now().isoformat(), submission_id)
            )
            
            conn.commit()
            
            # 获取更新后的提交
            cursor.execute('''
                SELECT ts.*, s.name as student_name, s.student_id as student_number
                FROM task_submissions ts
                JOIN students s ON ts.student_id = s.id
                WHERE ts.id = ?
            ''', (submission_id,))
            
            updated_submission = cursor.fetchone()
            return dict(updated_submission) if updated_submission else None
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'评分失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_submission(submission_id):
        """
        获取提交详情
        
        :param submission_id: 提交ID
        :return: 提交详情
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT ts.*, s.name as student_name, s.student_id as student_number
                FROM task_submissions ts
                JOIN students s ON ts.student_id = s.id
                WHERE ts.id = ?
            ''', (submission_id,))
            
            submission = cursor.fetchone()
            if not submission:
                raise ApiError('提交记录不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            return dict(submission)
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取提交详情失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_student_submission(task_id, student_id):
        """
        获取学生的提交记录
        
        :param task_id: 任务ID
        :param student_id: 学生ID
        :return: 提交记录
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT ts.*
                FROM task_submissions ts
                WHERE ts.task_id = ? AND ts.student_id = ?
            ''', (task_id, student_id))
            
            submission = cursor.fetchone()
            if not submission:
                return None
            
            return dict(submission)
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取提交记录失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
            
    @staticmethod
    def get_available_classes():
        """
        获取所有可用班级
        
        :return: 班级列表
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT DISTINCT class, COUNT(*) as student_count
                FROM students
                GROUP BY class
                ORDER BY class
            ''')
            
            classes = [dict(row) for row in cursor.fetchall()]
            return classes
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取班级列表失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close() 