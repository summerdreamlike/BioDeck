from datetime import datetime
from .base import BaseModel

class Course(BaseModel):
    @classmethod
    def get_live_courses(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 获取当前时间
        now = datetime.now().isoformat()
        
        # 查询直播中的课程
        cursor.execute('''
            SELECT c.*, u.name as teacher_name
            FROM courses c
            JOIN users u ON c.teacher_id = u.id
            WHERE c.start_time <= ? AND c.end_time >= ?
        ''', (now, now))
        live_courses = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        # 查询即将开始的课程
        cursor.execute('''
            SELECT c.*, u.name as teacher_name
            FROM courses c
            JOIN users u ON c.teacher_id = u.id
            WHERE c.start_time > ?
            ORDER BY c.start_time
            LIMIT 5
        ''', (now,))
        upcoming_courses = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        # 查询已结束的课程
        cursor.execute('''
            SELECT c.*, u.name as teacher_name
            FROM courses c
            JOIN users u ON c.teacher_id = u.id
            WHERE c.end_time < ?
            ORDER BY c.end_time DESC
            LIMIT 5
        ''', (now,))
        ended_courses = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        # 为每个课程添加学生列表
        all_courses = live_courses + upcoming_courses + ended_courses
        for course in all_courses:
            cursor.execute('''
                SELECT s.* FROM students s
                JOIN course_students cs ON s.id = cs.student_id
                WHERE cs.course_id = ?
            ''', (course['id'],))
            course['students'] = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'live': live_courses,
            'upcoming': upcoming_courses,
            'ended': ended_courses
        }
    
    @classmethod
    def get_by_id(cls, course_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 获取课程基本信息
        cursor.execute('''
            SELECT c.*, u.name as teacher_name
            FROM courses c
            JOIN users u ON c.teacher_id = u.id
            WHERE c.id = ?
        ''', (course_id,))
        course = cursor.fetchone()
        
        if not course:
            conn.close()
            return None
        
        course_dict = cls.dict_from_row(course)
        
        # 获取课程学生
        cursor.execute('''
            SELECT s.* FROM students s
            JOIN course_students cs ON s.id = cs.student_id
            WHERE cs.course_id = ?
        ''', (course_id,))
        course_dict['students'] = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        return course_dict
    
    @classmethod
    def create(cls, title, teacher_id, start_time, end_time, poster_url=None, video_url=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 确定课程状态
        now = datetime.now()
        start_time_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_time_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        
        if now < start_time_dt:
            status = 'upcoming'
        elif now > end_time_dt:
            status = 'ended'
        else:
            status = 'live'
        
        cursor.execute(
            'INSERT INTO courses (title, teacher_id, start_time, end_time, status, poster_url, video_url) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (title, teacher_id, start_time, end_time, status, poster_url, video_url)
        )
        course_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return course_id

    @classmethod
    def update(cls, course_id, title, teacher_id, start_time, end_time, poster_url=None, video_url=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE courses
            SET title = ?, teacher_id = ?, start_time = ?, end_time = ?, poster_url = ?, video_url = ?
            WHERE id = ?
        ''', (title, teacher_id, start_time, end_time, poster_url, video_url, course_id))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def delete(cls, course_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM course_students WHERE course_id = ?', (course_id,))
        cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def list_all_with_counts(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.id, c.title, u.name as teacher, c.start_time, c.end_time, c.status,
                   COUNT(cs.student_id) as total_students
            FROM courses c
            LEFT JOIN users u ON c.teacher_id = u.id
            LEFT JOIN course_students cs ON c.id = cs.course_id
            GROUP BY c.id
            ORDER BY c.start_time DESC
        ''')
        rows = cursor.fetchall()
        result = []
        for row in rows:
            start_dt = row[3]
            end_dt = row[4]
            try:
                start_datetime = datetime.strptime(start_dt, '%Y-%m-%d %H:%M:%S')
            except Exception:
                start_datetime = datetime.fromisoformat(str(start_dt).replace('Z', '+00:00'))
            result.append({
                'id': row[0],
                'title': row[1],
                'teacher': row[2],
                'date': start_datetime.strftime('%Y-%m-%d'),
                'start_time': row[3],
                'end_time': row[4],
                'status': row[5],
                'total_students': row[6]
            })
        conn.close()
        return result

class CourseMessage(BaseModel):
    @classmethod
    def get_by_course_id(cls, course_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT cm.*, u.name as sender_name
            FROM course_messages cm
            JOIN users u ON cm.sender_id = u.id
            WHERE cm.course_id = ?
            ORDER BY cm.sent_at DESC
            LIMIT 100
        ''', (course_id,))
        messages = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        return messages
    
    @classmethod
    def create(cls, course_id, sender_id, message):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO course_messages (course_id, sender_id, message) VALUES (?, ?, ?)',
            (course_id, sender_id, message)
        )
        message_id = cursor.lastrowid
        
        # 获取刚插入的消息
        cursor.execute('''
            SELECT cm.*, u.name as sender_name
            FROM course_messages cm
            JOIN users u ON cm.sender_id = u.id
            WHERE cm.id = ?
        ''', (message_id,))
        new_message = cursor.fetchone()
        
        conn.commit()
        conn.close()
        return cls.dict_from_row(new_message) 