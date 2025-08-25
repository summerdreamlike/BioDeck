from .base import BaseModel

class Attendance(BaseModel):
    @classmethod
    def get_by_course_id(cls, course_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, s.name as student_name, s.student_id as student_number, s.class as student_class
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            WHERE a.course_id = ?
            ORDER BY a.check_in_time DESC
        ''', (course_id,))
        attendance = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        return attendance

    @classmethod
    def list_all(cls, course_id=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        query = '''
            SELECT a.id, a.course_id, a.student_id, a.status, a.check_in_time, a.created_at,
                   s.name as student_name, s.student_id as student_id_num, s.class as student_class
            FROM attendance a
            JOIN students s ON a.student_id = s.id
        '''
        params = []
        if course_id:
            query += ' WHERE a.course_id = ?'
            params.append(course_id)
        cursor.execute(query, params)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'course_id': row[1],
                'student_id': row[2],
                'status': row[3],
                'check_in_time': row[4],
                'created_at': row[5],
                'student_name': row[6],
                'student_id_num': row[7],
                'student_class': row[8]
            })
        conn.close()
        return result

    @classmethod
    def export_data(cls, course_id=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        query = '''
            SELECT s.name, s.student_id, s.class, a.status, a.check_in_time, c.title as course_title
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            JOIN courses c ON a.course_id = c.id
        '''
        params = []
        if course_id:
            query += ' WHERE a.course_id = ?'
            params.append(course_id)
        cursor.execute(query, params)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                'name': row[0],
                'student_id': row[1],
                'class': row[2],
                'status': row[3],
                'check_in_time': row[4],
                'course_title': row[5]
            })
        conn.close()
        return result

    @classmethod
    def create_entry(cls, course_id, student_id, status, check_in_time=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO attendance (course_id, student_id, status, check_in_time)
            VALUES (?, ?, ?, ?)
        ''', (course_id, student_id, status, check_in_time))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id 