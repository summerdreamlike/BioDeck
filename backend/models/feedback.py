from .base import BaseModel

class Feedback(BaseModel):
    @classmethod
    def get_all(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.*, s.name as student_name, s.class as student_class
            FROM feedbacks f
            JOIN students s ON f.student_id = s.id
            ORDER BY f.created_at DESC
        ''')
        feedbacks = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        return feedbacks
    
    @classmethod
    def get_statistics(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 满意度分布
        cursor.execute('''
            SELECT 
                COUNT(CASE WHEN satisfaction = 1 THEN 1 END) as very_dissatisfied,
                COUNT(CASE WHEN satisfaction = 2 THEN 1 END) as dissatisfied,
                COUNT(CASE WHEN satisfaction = 3 THEN 1 END) as neutral,
                COUNT(CASE WHEN satisfaction = 4 THEN 1 END) as satisfied,
                COUNT(CASE WHEN satisfaction = 5 THEN 1 END) as very_satisfied
            FROM feedbacks
        ''')
        satisfaction_distribution = cls.dict_from_row(cursor.fetchone())
        
        # 计算平均满意度
        cursor.execute('SELECT AVG(satisfaction) as avg_satisfaction FROM feedbacks')
        avg_satisfaction = cursor.fetchone()['avg_satisfaction'] or 0
        
        # 按班级统计满意度
        cursor.execute('''
            SELECT s.class, AVG(f.satisfaction) as avg_satisfaction
            FROM feedbacks f
            JOIN students s ON f.student_id = s.id
            GROUP BY s.class
            ORDER BY avg_satisfaction DESC
        ''')
        satisfaction_by_class = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'satisfaction_distribution': satisfaction_distribution,
            'avg_satisfaction': avg_satisfaction,
            'satisfaction_by_class': satisfaction_by_class
        }
    
    @classmethod
    def create(cls, student_id, content, satisfaction):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO feedbacks (student_id, content, satisfaction) VALUES (?, ?, ?)',
            (student_id, content, satisfaction)
        )
        feedback_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return feedback_id

    @classmethod
    def update(cls, feedback_id, content=None, satisfaction=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        sets = []
        params = []
        if content is not None:
            sets.append('content = ?')
            params.append(content)
        if satisfaction is not None:
            sets.append('satisfaction = ?')
            params.append(satisfaction)
        if not sets:
            conn.close()
            return True
        params.append(feedback_id)
        cursor.execute(f"UPDATE feedbacks SET {', '.join(sets)} WHERE id = ?", params)
        conn.commit()
        conn.close()
        return True

    @classmethod
    def delete(cls, feedback_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM feedbacks WHERE id = ?', (feedback_id,))
        conn.commit()
        conn.close()
        return True 