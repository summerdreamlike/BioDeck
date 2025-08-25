import json
from .base import BaseModel

class Paper(BaseModel):
    @classmethod
    def create(cls, name, creator_id, total_score, questions):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 创建试卷
        cursor.execute(
            'INSERT INTO papers (name, creator_id, total_score) VALUES (?, ?, ?)',
            (name, creator_id, total_score)
        )
        paper_id = cursor.lastrowid
        
        # 添加题目
        for question in questions:
            question_id = question['id']
            score = question['score']
            cursor.execute(
                'INSERT INTO paper_questions (paper_id, question_id, score) VALUES (?, ?, ?)',
                (paper_id, question_id, score)
            )
        
        conn.commit()
        conn.close()
        
        return {
            'id': paper_id,
            'name': name,
            'creator_id': creator_id,
            'total_score': total_score,
            'question_count': len(questions)
        }
    
    @classmethod
    def get_by_id(cls, paper_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 获取试卷基本信息
        cursor.execute('SELECT * FROM papers WHERE id = ?', (paper_id,))
        paper = cursor.fetchone()
        
        if not paper:
            conn.close()
            return None
        
        paper_dict = cls.dict_from_row(paper)
        
        # 获取试卷题目
        cursor.execute('''
            SELECT q.*, pq.score
            FROM questions q
            JOIN paper_questions pq ON q.id = pq.question_id
            WHERE pq.paper_id = ?
            ORDER BY pq.id
        ''', (paper_id,))
        questions = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        # 处理选项数据
        for question in questions:
            if question['options']:
                question['options'] = json.loads(question['options'])
        
        paper_dict['questions'] = questions
        
        conn.close()
        return paper_dict 