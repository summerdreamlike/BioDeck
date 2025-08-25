"""
题目服务模块

负责题目管理、推荐等功能
"""
import json
from core.helpers import get_db, db_fetch_one
from core.errors import ApiError, ErrorCode
from models import Question

class QuestionService:
    @staticmethod
    def get_questions(page=1, page_size=10, **filters):
        """
        获取题目列表
        
        :param page: 页码
        :param page_size: 每页数量
        :param filters: 过滤条件
        :return: 题目列表
        """
        conn = get_db()
        cursor = conn.cursor()
        
        # 构建SQL查询
        sql = 'SELECT * FROM questions WHERE 1=1'
        params = []
        
        # 应用过滤器
        if 'query' in filters and filters['query']:
            sql += ' AND (title LIKE ? OR knowledge_point LIKE ?)'
            query = f"%{filters['query']}%"
            params.extend([query, query])
        
        if 'types' in filters and filters['types']:
            placeholders = ','.join(['?' for _ in filters['types']])
            sql += f' AND type IN ({placeholders})'
            params.extend(filters['types'])
        
        if 'difficulty_min' in filters and 'difficulty_max' in filters:
            sql += ' AND difficulty BETWEEN ? AND ?'
            params.extend([filters['difficulty_min'], filters['difficulty_max']])
        
        # 计算总数
        cursor.execute(f'SELECT COUNT(*) as count FROM ({sql})', params)
        total = cursor.fetchone()['count']
        
        # 应用分页
        sql += ' LIMIT ? OFFSET ?'
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        cursor.execute(sql, params)
        questions = [dict(row) for row in cursor.fetchall()]
        
        # 处理选项数据
        for question in questions:
            if question['options']:
                question['options'] = json.loads(question['options'])
        
        conn.close()
        return {
            'items': questions,
            'total': total,
            'page': page,
            'page_size': page_size
        }
    
    @staticmethod
    def get_question_by_id(question_id):
        """
        根据ID获取题目
        
        :param question_id: 题目ID
        :return: 题目详情
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM questions WHERE id = ?', (question_id,))
        question = cursor.fetchone()
        
        if not question:
            conn.close()
            raise ApiError('题目不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
        
        question_dict = dict(question)
        
        if question_dict and question_dict['options']:
            question_dict['options'] = json.loads(question_dict['options'])
        
        conn.close()
        return question_dict
    
    @staticmethod
    def create_question(data):
        """
        创建题目
        
        :param data: 题目数据
        :return: 新题目ID
        """
        conn = get_db()
        cursor = conn.cursor()
        
        options_json = json.dumps(data.get('options')) if data.get('options') else None
        
        try:
            cursor.execute(
                'INSERT INTO questions (title, type, difficulty, knowledge_point, options, answer, analysis) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (data['title'], data['type'], data['difficulty'], data['knowledge_point'], options_json, data['answer'], data.get('analysis'))
            )
            question_id = cursor.lastrowid
            conn.commit()
            return question_id
        except Exception as e:
            conn.rollback()
            raise ApiError(str(e), code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def update_question(question_id, data):
        """
        更新题目
        
        :param question_id: 题目ID
        :param data: 题目数据
        :return: 是否成功
        """
        conn = get_db()
        cursor = conn.cursor()
        options_json = json.dumps(data.get('options')) if data.get('options') else None
        
        try:
            cursor.execute('''
                UPDATE questions
                SET title = ?, type = ?, difficulty = ?, knowledge_point = ?, options = ?, answer = ?, analysis = ?
                WHERE id = ?
            ''', (data['title'], data['type'], data['difficulty'], data['knowledge_point'], options_json, data['answer'], data.get('analysis'), question_id))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise ApiError(str(e), code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def delete_question(question_id):
        """
        删除题目
        
        :param question_id: 题目ID
        :return: 是否成功
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise ApiError(str(e), code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def recommend_for_student(student_id, limit_per_point=3):
        """
        为学生推荐题目
        
        :param student_id: 学生ID
        :param limit_per_point: 每个知识点推荐的题目数量
        :return: 推荐题目列表
        """
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE id = ? AND role = ?', (student_id, 'student'))
        if not cursor.fetchone():
            conn.close()
            raise ApiError('学生不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
        
        # 查询学生的薄弱知识点
        cursor.execute('''
            SELECT knowledge_point, AVG(accuracy_rate) as avg_accuracy
            FROM study_data
            WHERE user_id = ?
            GROUP BY knowledge_point
            ORDER BY avg_accuracy ASC
            LIMIT 3
        ''', (student_id,))
        weak_points = [row['knowledge_point'] for row in cursor.fetchall()]
        
        # 如果没有足够的学习数据，使用默认知识点
        if len(weak_points) < 3:
            default_points = ['细胞结构与功能', '遗传与变异', '生态系统与稳态']
            weak_points.extend(default_points[len(weak_points):])
        
        # 为每个知识点查询题目
        questions = []
        for point in weak_points:
            cursor.execute('''
                SELECT * FROM questions
                WHERE knowledge_point LIKE ?
                ORDER BY RANDOM()
                LIMIT ?
            ''', (f'%{point}%', limit_per_point))
            point_questions = [dict(row) for row in cursor.fetchall()]
            for q in point_questions:
                if q.get('options'):
                    q['options'] = json.loads(q['options'])
            questions.extend(point_questions)
        
        conn.close()
        return questions 