from datetime import datetime
from .base import BaseModel

class StudyData(BaseModel):
    @classmethod
    def get_by_student_id(cls, student_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM study_data
            WHERE student_id = ?
            ORDER BY date DESC
        ''', (student_id,))
        study_data = [cls.dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return study_data
    
    @classmethod
    def create(cls, student_id, completion_rate, accuracy_rate, focus_rate, score, date=None):
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO study_data (student_id, completion_rate, accuracy_rate, focus_rate, score, date) VALUES (?, ?, ?, ?, ?, ?)',
            (student_id, completion_rate, accuracy_rate, focus_rate, score, date)
        )
        data_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return data_id 