"""
学习数据服务模块

负责学习数据的处理、分析和统计
"""
from datetime import datetime
import json
import traceback

from core.helpers import get_db, db_fetch_one, db_fetch_all, db_execute
from core.errors import ApiError, ErrorCode
from utils.date_utils import now, format_date

class StudyService:
    @staticmethod
    def submit_study_data(student_id, data):
        """
        提交学习数据
        
        :param student_id: 学生ID
        :param data: 学习数据，包括完成率、准确率、专注度、分数等
        :return: 新数据ID
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证学生是否存在
            cursor.execute('SELECT id FROM users WHERE id = ? AND role = ?', (student_id, 'student'))
            if not cursor.fetchone():
                raise ApiError('学生不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 准备数据
            completion_rate = data.get('completion_rate', 0)
            accuracy_rate = data.get('accuracy_rate', 0)
            focus_rate = data.get('focus_rate', 0)
            score = data.get('score', 0)
            date = data.get('date') or format_date(now())
            knowledge_point = data.get('knowledge_point', '综合')
            
            # 插入数据
            cursor.execute('''
                INSERT INTO study_data 
                (user_id, completion_rate, accuracy_rate, focus_rate, score, date, knowledge_point) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, completion_rate, accuracy_rate, focus_rate, score, date, knowledge_point))
            
            data_id = cursor.lastrowid
            conn.commit()
            return data_id
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'提交学习数据失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_student_study_data(student_id, start_date=None, end_date=None, limit=30):
        """
        获取学生的学习数据
        
        :param student_id: 学生ID
        :param start_date: 开始日期（可选）
        :param end_date: 结束日期（可选）
        :param limit: 限制返回记录数
        :return: 学习数据列表
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证学生是否存在
            cursor.execute('SELECT id FROM users WHERE id = ? AND role = ?', (student_id, 'student'))
            if not cursor.fetchone():
                raise ApiError('学生不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 构建查询
            sql = 'SELECT * FROM study_data WHERE user_id = ?'
            params = [student_id]
            
            if start_date:
                sql += ' AND date >= ?'
                params.append(start_date)
            
            if end_date:
                sql += ' AND date <= ?'
                params.append(end_date)
            
            sql += ' ORDER BY date DESC LIMIT ?'
            params.append(limit)
            
            # 执行查询
            cursor.execute(sql, params)
            study_data = [dict(row) for row in cursor.fetchall()]
            
            return study_data
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取学习数据失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_knowledge_point_analysis(student_id):
        """
        获取知识点掌握情况分析
        
        :param student_id: 学生ID
        :return: 知识点分析结果
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证学生是否存在
            cursor.execute('SELECT id FROM users WHERE id = ? AND role = ?', (student_id, 'student'))
            if not cursor.fetchone():
                raise ApiError('学生不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 查询各知识点的平均分数、完成率和准确率
            cursor.execute('''
                SELECT 
                    knowledge_point,
                    AVG(score) as avg_score,
                    AVG(completion_rate) as avg_completion,
                    AVG(accuracy_rate) as avg_accuracy,
                    COUNT(*) as count
                FROM study_data
                WHERE user_id = ?
                GROUP BY knowledge_point
                ORDER BY avg_score DESC
            ''', (student_id,))
            
            analysis = [dict(row) for row in cursor.fetchall()]
            
            # 查询最近的学习趋势
            cursor.execute('''
                SELECT 
                    date,
                    AVG(score) as avg_score
                FROM study_data
                WHERE user_id = ?
                GROUP BY date
                ORDER BY date DESC
                LIMIT 10
            ''', (student_id,))
            
            trend = [dict(row) for row in cursor.fetchall()]
            trend.reverse()  # 按时间升序排列
            
            return {
                'knowledge_points': analysis,
                'trend': trend
            }
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取知识点分析失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_class_statistics(class_name):
        """
        获取班级学习统计数据
        
        :param class_name: 班级名称
        :return: 班级统计数据
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 查询班级是否存在
            cursor.execute('SELECT COUNT(*) as count FROM users WHERE class = ?', (class_name,))
            if cursor.fetchone()['count'] == 0:
                raise ApiError('班级不存在或没有学生', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 查询班级平均分数
            cursor.execute('''
                SELECT 
                    AVG(sd.score) as avg_score,
                    AVG(sd.completion_rate) as avg_completion,
                    AVG(sd.accuracy_rate) as avg_accuracy
                FROM study_data sd
                JOIN users u ON sd.user_id = u.id
                WHERE u.class = ?
            ''', (class_name,))
            
            overall = cursor.fetchone()
            
            # 查询班级每个学生的平均分数
            cursor.execute('''
                SELECT 
                    u.id as student_id,
                    u.name as student_name,
                    AVG(sd.score) as avg_score
                FROM study_data sd
                JOIN users u ON sd.user_id = u.id
                WHERE u.class = ?
                GROUP BY u.id
                ORDER BY avg_score DESC
            ''', (class_name,))
            
            students = [dict(row) for row in cursor.fetchall()]
            
            # 查询班级知识点掌握情况
            cursor.execute('''
                SELECT 
                    sd.knowledge_point,
                    AVG(sd.score) as avg_score,
                    COUNT(*) as count
                FROM study_data sd
                JOIN users u ON sd.user_id = u.id
                WHERE u.class = ?
                GROUP BY sd.knowledge_point
                ORDER BY avg_score
            ''', (class_name,))
            
            knowledge_points = [dict(row) for row in cursor.fetchall()]
            
            return {
                'overall': dict(overall) if overall else None,
                'students': students,
                'knowledge_points': knowledge_points
            }
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取班级统计失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def submit_practice_result(student_id, knowledge_point, is_correct):
        """
        提交练习题结果
        
        :param student_id: 学生ID
        :param knowledge_point: 知识点
        :param is_correct: 是否正确
        :return: 结果ID
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证学生是否存在
            cursor.execute('SELECT id FROM users WHERE id = ? AND role = ?', (student_id, 'student'))
            if not cursor.fetchone():
                raise ApiError('学生不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 如果没有提供知识点，使用默认值
            if not knowledge_point:
                knowledge_point = '综合'
            
            # 创建practices表（如果不存在）
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS practices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    knowledge_point TEXT NOT NULL,
                    is_correct INTEGER NOT NULL,
                    submitted_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES users (id)
                )
            ''')
            
            # 插入练习记录
            submitted_at = now()
            cursor.execute('''
                INSERT INTO practices 
                (student_id, knowledge_point, is_correct, submitted_at)
                VALUES (?, ?, ?, ?)
            ''', (student_id, knowledge_point, 1 if is_correct else 0, submitted_at))
            
            practice_id = cursor.lastrowid
            
            # 如果答错，添加到错题本
            if not is_correct:
                # 创建wrong_book表（如果不存在）
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS wrong_book (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER NOT NULL,
                        knowledge_point TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(student_id, knowledge_point)
                    )
                ''')
                
                try:
                    cursor.execute('''
                        INSERT INTO wrong_book 
                        (student_id, knowledge_point) 
                        VALUES (?, ?)
                    ''', (student_id, knowledge_point))
                except:
                    # 忽略唯一性约束错误（可能已经在错题本中）
                    pass
            
            conn.commit()
            return practice_id
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'提交练习结果失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_wrong_questions(student_id, page=1, page_size=20):
        """
        获取学生的错题本
        
        :param student_id: 学生ID
        :param page: 页码
        :param page_size: 每页数量
        :return: 错题列表及分页信息
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证学生是否存在
            cursor.execute('SELECT id FROM users WHERE id = ? AND role = ?', (student_id, 'student'))
            if not cursor.fetchone():
                raise ApiError('学生不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 计算总数
            cursor.execute('SELECT COUNT(*) as total FROM wrong_book WHERE student_id = ?', (student_id,))
            total = cursor.fetchone()['total']
            
            # 分页查询
            offset = (page - 1) * page_size
            cursor.execute('''
                SELECT wb.id, wb.knowledge_point, wb.created_at
                FROM wrong_book wb
                WHERE wb.student_id = ?
                ORDER BY wb.created_at DESC
                LIMIT ? OFFSET ?
            ''', (student_id, page_size, offset))
            
            items = []
            for row in cursor.fetchall():
                item = dict(row)
                if item.get('options'):
                    try:
                        item['options'] = json.loads(item['options'])
                    except:
                        pass
                items.append(item)
            
            return {
                'items': items,
                'total': total,
                'page': page,
                'page_size': page_size
            }
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取错题本失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close() 