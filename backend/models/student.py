from .base import BaseModel

class Student(BaseModel):
    @classmethod
    def get_all(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students')
        students = [cls.dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return students
    
    @classmethod
    def get_by_id(cls, student_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        conn.close()
        return cls.dict_from_row(student)
    
    @classmethod
    def get_rankings(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT s.id, s.name, s.student_id, s.class, s.gender, s.age,
                   AVG(sd.completion_rate) as completion_rate,
                   AVG(sd.accuracy_rate) as accuracy_rate,
                   AVG(sd.score) as score
            FROM students s
            JOIN study_data sd ON s.id = sd.student_id
            GROUP BY s.id
            ORDER BY score DESC
        ''')
        rankings = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        # 计算排名
        for i, student in enumerate(rankings):
            student['rank'] = i + 1
        
        conn.close()
        return rankings
    
    @classmethod
    def create(cls, name, student_id, class_name, gender=None, age=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO students (name, student_id, class, gender, age) VALUES (?, ?, ?, ?, ?)',
            (name, student_id, class_name, gender, age)
        )
        student_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return student_id

    @classmethod
    def update(cls, student_id, name, student_number, class_name, gender=None, age=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE students
            SET name = ?, student_id = ?, class = ?, gender = ?, age = ?
            WHERE id = ?
        ''', (name, student_number, class_name, gender, age, student_id))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def delete(cls, student_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def get_detail(cls, student_id, limit=30):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student = cursor.fetchone()
        if not student:
            conn.close()
            return None
        student_dict = cls.dict_from_row(student)
        cursor.execute('''
            SELECT * FROM study_data
            WHERE student_id = ?
            ORDER BY date DESC
            LIMIT ?
        ''', (student_id, limit))
        study_data = [cls.dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        student_dict['study_data'] = study_data
        return student_dict 