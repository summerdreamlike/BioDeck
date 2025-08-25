"""
试卷服务模块

负责试卷的创建、管理和评分
"""
import json
import traceback
from datetime import datetime

from core.helpers import get_db, db_fetch_one, db_fetch_all, db_execute
from core.errors import ApiError, ErrorCode

class PaperService:
    @staticmethod
    def get_papers(page=1, page_size=10, **filters):
        """
        获取试卷列表
        
        :param page: 页码
        :param page_size: 每页数量
        :param filters: 过滤条件
        :return: 试卷列表及分页信息
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 构建查询
            sql = '''
                SELECT p.*, u.name as creator_name, COUNT(pq.id) as question_count 
                FROM papers p
                LEFT JOIN users u ON p.creator_id = u.id
                LEFT JOIN paper_questions pq ON p.id = pq.paper_id
                WHERE 1=1
            '''
            params = []
            
            # 应用过滤器
            if 'creator_id' in filters:
                sql += ' AND p.creator_id = ?'
                params.append(filters['creator_id'])
            
            if 'name' in filters:
                sql += ' AND p.name LIKE ?'
                params.append(f"%{filters['name']}%")
            
            # 分组
            sql += ' GROUP BY p.id'
            
            # 排序
            sql += ' ORDER BY p.created_at DESC'
            
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
            papers = [dict(row) for row in cursor.fetchall()]
            
            return {
                'items': papers,
                'total': total,
                'page': page,
                'page_size': page_size
            }
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取试卷列表失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_paper_by_id(paper_id, include_questions=True):
        """
        根据ID获取试卷
        
        :param paper_id: 试卷ID
        :param include_questions: 是否包含题目详情
        :return: 试卷详情
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 获取试卷基本信息
            cursor.execute('''
                SELECT p.*, u.name as creator_name
                FROM papers p
                LEFT JOIN users u ON p.creator_id = u.id
                WHERE p.id = ?
            ''', (paper_id,))
            
            paper = cursor.fetchone()
            if not paper:
                raise ApiError('试卷不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            paper_dict = dict(paper)
            
            # 如果需要包含题目详情
            if include_questions:
                # 获取试卷题目
                cursor.execute('''
                    SELECT q.*, pq.score, pq.order_num
                    FROM questions q
                    JOIN paper_questions pq ON q.id = pq.question_id
                    WHERE pq.paper_id = ?
                    ORDER BY pq.order_num ASC
                ''', (paper_id,))
                
                questions = []
                for row in cursor.fetchall():
                    question = dict(row)
                    if question['options']:
                        question['options'] = json.loads(question['options'])
                    questions.append(question)
                
                paper_dict['questions'] = questions
                
                # 重新计算总分
                if questions:
                    paper_dict['total_score'] = sum(q['score'] for q in questions)
            
            return paper_dict
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取试卷详情失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def create_paper(creator_id, name, description=None):
        """
        创建试卷
        
        :param creator_id: 创建者ID
        :param name: 试卷名称
        :param description: 试卷描述
        :return: 新试卷ID
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证创建者是否存在
            cursor.execute('SELECT id FROM users WHERE id = ?', (creator_id,))
            if not cursor.fetchone():
                raise ApiError('创建者不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 创建试卷
            cursor.execute('''
                INSERT INTO papers (name, description, creator_id, total_score, created_at) 
                VALUES (?, ?, ?, ?, ?)
            ''', (name, description, creator_id, 0, datetime.now()))
            
            paper_id = cursor.lastrowid
            conn.commit()
            return paper_id
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'创建试卷失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def update_paper(paper_id, data):
        """
        更新试卷
        
        :param paper_id: 试卷ID
        :param data: 更新数据
        :return: 是否成功
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证试卷是否存在
            cursor.execute('SELECT id FROM papers WHERE id = ?', (paper_id,))
            if not cursor.fetchone():
                raise ApiError('试卷不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 构建更新语句
            update_fields = []
            params = []
            
            if 'name' in data:
                update_fields.append('name = ?')
                params.append(data['name'])
            
            if 'description' in data:
                update_fields.append('description = ?')
                params.append(data['description'])
            
            if not update_fields:
                return True  # 没有需要更新的字段
            
            # 执行更新
            sql = f"UPDATE papers SET {', '.join(update_fields)} WHERE id = ?"
            params.append(paper_id)
            
            cursor.execute(sql, params)
            conn.commit()
            return True
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'更新试卷失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def delete_paper(paper_id):
        """
        删除试卷
        
        :param paper_id: 试卷ID
        :return: 是否成功
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证试卷是否存在
            cursor.execute('SELECT id FROM papers WHERE id = ?', (paper_id,))
            if not cursor.fetchone():
                raise ApiError('试卷不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 删除试卷题目关联
            cursor.execute('DELETE FROM paper_questions WHERE paper_id = ?', (paper_id,))
            
            # 删除试卷
            cursor.execute('DELETE FROM papers WHERE id = ?', (paper_id,))
            
            conn.commit()
            return True
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'删除试卷失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def add_questions_to_paper(paper_id, questions):
        """
        向试卷添加题目
        
        :param paper_id: 试卷ID
        :param questions: 题目列表，每个题目包含id和score
        :return: 是否成功
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证试卷是否存在
            cursor.execute('SELECT id FROM papers WHERE id = ?', (paper_id,))
            if not cursor.fetchone():
                raise ApiError('试卷不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 获取当前试卷中最大的题目序号
            cursor.execute('SELECT MAX(order_num) as max_order FROM paper_questions WHERE paper_id = ?', (paper_id,))
            row = cursor.fetchone()
            next_order = (row['max_order'] or 0) + 1
            
            # 批量添加题目
            for question in questions:
                question_id = question['id']
                score = question['score']
                
                # 验证题目是否存在
                cursor.execute('SELECT id FROM questions WHERE id = ?', (question_id,))
                if not cursor.fetchone():
                    raise ApiError(f'题目ID {question_id} 不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
                
                # 验证题目是否已在试卷中
                cursor.execute('SELECT id FROM paper_questions WHERE paper_id = ? AND question_id = ?', (paper_id, question_id))
                if cursor.fetchone():
                    # 题目已存在，更新分数和顺序
                    cursor.execute('''
                        UPDATE paper_questions 
                        SET score = ?, order_num = ? 
                        WHERE paper_id = ? AND question_id = ?
                    ''', (score, next_order, paper_id, question_id))
                else:
                    # 添加新题目
                    cursor.execute('''
                        INSERT INTO paper_questions (paper_id, question_id, score, order_num) 
                        VALUES (?, ?, ?, ?)
                    ''', (paper_id, question_id, score, next_order))
                
                next_order += 1
            
            # 更新试卷总分
            cursor.execute('SELECT SUM(score) as total_score FROM paper_questions WHERE paper_id = ?', (paper_id,))
            total_score = cursor.fetchone()['total_score'] or 0
            cursor.execute('UPDATE papers SET total_score = ? WHERE id = ?', (total_score, paper_id))
            
            conn.commit()
            return True
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'添加题目失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def remove_question_from_paper(paper_id, question_id):
        """
        从试卷中移除题目
        
        :param paper_id: 试卷ID
        :param question_id: 题目ID
        :return: 是否成功
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证试卷是否存在
            cursor.execute('SELECT id FROM papers WHERE id = ?', (paper_id,))
            if not cursor.fetchone():
                raise ApiError('试卷不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证题目是否在试卷中
            cursor.execute('SELECT id FROM paper_questions WHERE paper_id = ? AND question_id = ?', (paper_id, question_id))
            if not cursor.fetchone():
                raise ApiError('题目不在试卷中', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 删除题目
            cursor.execute('DELETE FROM paper_questions WHERE paper_id = ? AND question_id = ?', (paper_id, question_id))
            
            # 更新试卷总分
            cursor.execute('SELECT SUM(score) as total_score FROM paper_questions WHERE paper_id = ?', (paper_id,))
            total_score = cursor.fetchone()['total_score'] or 0
            cursor.execute('UPDATE papers SET total_score = ? WHERE id = ?', (total_score, paper_id))
            
            # 重新排序题目
            cursor.execute('''
                SELECT id, question_id FROM paper_questions 
                WHERE paper_id = ? 
                ORDER BY order_num ASC
            ''', (paper_id,))
            questions = cursor.fetchall()
            
            for i, q in enumerate(questions):
                cursor.execute('UPDATE paper_questions SET order_num = ? WHERE id = ?', (i + 1, q['id']))
            
            conn.commit()
            return True
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'移除题目失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def reorder_questions(paper_id, question_orders):
        """
        重新排序试卷题目
        
        :param paper_id: 试卷ID
        :param question_orders: 题目顺序映射，格式为[{question_id: x, order: y}, ...]
        :return: 是否成功
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证试卷是否存在
            cursor.execute('SELECT id FROM papers WHERE id = ?', (paper_id,))
            if not cursor.fetchone():
                raise ApiError('试卷不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 获取试卷中的所有题目ID
            cursor.execute('SELECT question_id FROM paper_questions WHERE paper_id = ?', (paper_id,))
            existing_questions = {row['question_id'] for row in cursor.fetchall()}
            
            # 验证所有要排序的题目是否都在试卷中
            for item in question_orders:
                if item['question_id'] not in existing_questions:
                    raise ApiError(f'题目ID {item["question_id"]} 不在试卷中', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 更新题目顺序
            for item in question_orders:
                cursor.execute('''
                    UPDATE paper_questions 
                    SET order_num = ? 
                    WHERE paper_id = ? AND question_id = ?
                ''', (item['order'], paper_id, item['question_id']))
            
            conn.commit()
            return True
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'重排题目失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_random_paper(knowledge_points=None, difficulty_min=None, difficulty_max=None, question_count=10):
        """
        生成随机试卷
        
        :param knowledge_points: 知识点列表
        :param difficulty_min: 最小难度
        :param difficulty_max: 最大难度
        :param question_count: 题目数量
        :return: 随机试卷数据
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 构建查询条件
            sql = "SELECT * FROM questions WHERE 1=1"
            params = []
            
            if knowledge_points:
                placeholders = " OR ".join(["knowledge_point LIKE ?" for _ in knowledge_points])
                sql += f" AND ({placeholders})"
                params.extend([f"%{kp}%" for kp in knowledge_points])
            
            if difficulty_min is not None:
                sql += " AND difficulty >= ?"
                params.append(difficulty_min)
            
            if difficulty_max is not None:
                sql += " AND difficulty <= ?"
                params.append(difficulty_max)
            
            # 随机排序并限制数量
            sql += " ORDER BY RANDOM() LIMIT ?"
            params.append(question_count)
            
            cursor.execute(sql, params)
            questions = []
            total_score = 0
            
            for i, row in enumerate(cursor.fetchall()):
                question = dict(row)
                if question['options']:
                    question['options'] = json.loads(question['options'])
                
                # 根据难度分配分值
                score = question['difficulty'] * 2
                question['score'] = score
                question['order_num'] = i + 1
                
                total_score += score
                questions.append(question)
            
            # 构建随机试卷数据
            paper = {
                'name': '随机试卷',
                'description': '系统自动生成的随机试卷',
                'total_score': total_score,
                'questions': questions,
                'question_count': len(questions)
            }
            
            return paper
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'生成随机试卷失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close() 