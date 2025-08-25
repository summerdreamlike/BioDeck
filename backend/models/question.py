import json
from .base import BaseModel

class Question(BaseModel):
    @classmethod
    def get_all(cls, page=1, page_size=10, **filters):
        conn = cls.get_db()
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
        questions = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
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
    
    @classmethod
    def get_by_id(cls, question_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM questions WHERE id = ?', (question_id,))
        question = cursor.fetchone()
        question_dict = cls.dict_from_row(question)
        
        if question_dict and question_dict['options']:
            question_dict['options'] = json.loads(question_dict['options'])
        
        conn.close()
        return question_dict
    
    @classmethod
    def create(cls, title, type_, difficulty, knowledge_point, answer, options=None, analysis=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        options_json = json.dumps(options) if options else None
        
        cursor.execute(
            'INSERT INTO questions (title, type, difficulty, knowledge_point, options, answer, analysis) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (title, type_, difficulty, knowledge_point, options_json, answer, analysis)
        )
        question_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return question_id

    @classmethod
    def update(cls, question_id, title, type_, difficulty, knowledge_point, answer, options=None, analysis=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        options_json = json.dumps(options) if options else None
        cursor.execute('''
            UPDATE questions
            SET title = ?, type = ?, difficulty = ?, knowledge_point = ?, options = ?, answer = ?, analysis = ?
            WHERE id = ?
        ''', (title, type_, difficulty, knowledge_point, options_json, answer, analysis, question_id))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def delete(cls, question_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def recommend_for_student(cls, student_id, limit_per_point=3):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM students WHERE id = ?', (student_id,))
        if not cursor.fetchone():
            conn.close()
            return None
        cursor.execute('''
            SELECT knowledge_point, AVG(accuracy_rate) as avg_accuracy
            FROM study_data
            WHERE student_id = ?
            GROUP BY knowledge_point
            ORDER BY avg_accuracy ASC
            LIMIT 3
        ''', (student_id,))
        weak_points = [row['knowledge_point'] for row in cursor.fetchall()]
        if len(weak_points) < 3:
            default_points = ['细胞结构与功能', '遗传与变异', '生态系统与稳态']
            weak_points.extend(default_points[len(weak_points):])
        questions = []
        for point in weak_points:
            cursor.execute('''
                SELECT * FROM questions
                WHERE knowledge_point LIKE ?
                ORDER BY RANDOM()
                LIMIT ?
            ''', (f'%{point}%', limit_per_point))
            point_questions = [cls.dict_from_row(row) for row in cursor.fetchall()]
            for q in point_questions:
                if q.get('options'):
                    q['options'] = json.loads(q['options'])
            questions.extend(point_questions)
        conn.close()
        return questions 