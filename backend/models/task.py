from .base import BaseModel

class Task(BaseModel):
    @classmethod
    def get_all(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.*, u.name as creator_name, p.name as paper_name
            FROM tasks t
            JOIN users u ON t.creator_id = u.id
            LEFT JOIN papers p ON t.paper_id = p.id
            ORDER BY t.created_at DESC
        ''')
        tasks = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        # 获取每个任务的班级
        for task in tasks:
            cursor.execute('''
                SELECT class_name FROM task_classes
                WHERE task_id = ?
            ''', (task['id'],))
            task['classes'] = [row['class_name'] for row in cursor.fetchall()]
        
        conn.close()
        return tasks
    
    @classmethod
    def get_by_id(cls, task_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.*, u.name as creator_name, p.name as paper_name
            FROM tasks t
            JOIN users u ON t.creator_id = u.id
            LEFT JOIN papers p ON t.paper_id = p.id
            WHERE t.id = ?
        ''', (task_id,))
        task = cursor.fetchone()
        
        if not task:
            conn.close()
            return None
        
        task_dict = cls.dict_from_row(task)
        
        # 获取任务的班级
        cursor.execute('''
            SELECT class_name FROM task_classes
            WHERE task_id = ?
        ''', (task_id,))
        task_dict['classes'] = [row['class_name'] for row in cursor.fetchall()]
        
        # 获取任务的提交情况
        cursor.execute('''
            SELECT ts.*, s.name as student_name, s.student_id as student_number
            FROM task_submissions ts
            JOIN students s ON ts.student_id = s.id
            WHERE ts.task_id = ?
        ''', (task_id,))
        task_dict['submissions'] = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        return task_dict
    
    @classmethod
    def get_statistics(cls, task_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 获取任务信息
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        
        if not task:
            conn.close()
            return None
        
        # 获取任务分配的班级
        cursor.execute('SELECT class_name FROM task_classes WHERE task_id = ?', (task_id,))
        classes = [row['class_name'] for row in cursor.fetchall()]
        
        # 获取这些班级的学生总数
        placeholders = ','.join(['?' for _ in classes])
        cursor.execute(f'SELECT COUNT(*) as total FROM students WHERE class IN ({placeholders})', classes)
        total_students = cursor.fetchone()['total']
        
        # 获取已提交的学生数
        cursor.execute('SELECT COUNT(*) as submitted FROM task_submissions WHERE task_id = ?', (task_id,))
        submitted_count = cursor.fetchone()['submitted']
        
        # 计算完成率
        completion_rate = (submitted_count / total_students) * 100 if total_students > 0 else 0
        
        # 获取分数分布
        cursor.execute('''
            SELECT 
                COUNT(CASE WHEN score < 60 THEN 1 END) as below_60,
                COUNT(CASE WHEN score >= 60 AND score < 70 THEN 1 END) as between_60_70,
                COUNT(CASE WHEN score >= 70 AND score < 80 THEN 1 END) as between_70_80,
                COUNT(CASE WHEN score >= 80 AND score < 90 THEN 1 END) as between_80_90,
                COUNT(CASE WHEN score >= 90 THEN 1 END) as above_90
            FROM task_submissions
            WHERE task_id = ? AND score IS NOT NULL
        ''', (task_id,))
        score_distribution = cls.dict_from_row(cursor.fetchone())
        
        # 获取提交时间分布
        cursor.execute('''
            SELECT 
                COUNT(CASE WHEN julianday(submitted_at) - julianday(?) <= 1 THEN 1 END) as first_day,
                COUNT(CASE WHEN julianday(submitted_at) - julianday(?) > 1 AND julianday(submitted_at) - julianday(?) <= 3 THEN 1 END) as first_three_days,
                COUNT(CASE WHEN julianday(submitted_at) - julianday(?) > 3 AND julianday(?) - julianday(submitted_at) > 0 THEN 1 END) as before_due,
                COUNT(CASE WHEN julianday(submitted_at) - julianday(?) > 0 THEN 1 END) as after_due
            FROM task_submissions
            WHERE task_id = ? AND submitted_at IS NOT NULL
        ''', (task['created_at'], task['created_at'], task['created_at'], task['created_at'], task['due_date'], task['due_date'], task_id))
        time_distribution = cls.dict_from_row(cursor.fetchone())
        
        conn.close()
        
        return {
            'total_students': total_students,
            'submitted_count': submitted_count,
            'completion_rate': completion_rate,
            'score_distribution': score_distribution,
            'time_distribution': time_distribution
        }
    
    @classmethod
    def list_overview(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.id, t.title, t.description, t.paper_id, t.due_date,
                   t.allow_late_submission, t.created_at, u.name as creator_name
            FROM tasks t
            JOIN users u ON t.creator_id = u.id
            ORDER BY t.due_date DESC
        ''')
        rows = cursor.fetchall()
        result = []
        for row in rows:
            task_id = row[0]
            cursor.execute('SELECT class_name FROM task_classes WHERE task_id = ?', (task_id,))
            classes = [r[0] for r in cursor.fetchall()]
            cursor.execute('''
                SELECT COUNT(ts.id), 
                       (SELECT COUNT(*) FROM students s JOIN task_classes tc ON s.class = tc.class_name WHERE tc.task_id = ?)
                FROM task_submissions ts
                WHERE ts.task_id = ?
            ''', (task_id, task_id))
            submission_row = cursor.fetchone()
            submitted = submission_row[0] if submission_row else 0
            total_students = submission_row[1] if submission_row else 0
            cursor.execute('SELECT AVG(score) FROM task_submissions WHERE task_id = ? AND score IS NOT NULL', (task_id,))
            avg_row = cursor.fetchone()
            avg_score = round(avg_row[0], 2) if avg_row and avg_row[0] else None
            result.append({
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'paper_id': row[3],
                'due_date': row[4],
                'allow_late_submission': bool(row[5]),
                'created_at': row[6],
                'creator': row[7],
                'classes': classes,
                'submitted': submitted,
                'total_students': total_students,
                'completion_rate': round((submitted / total_students * 100), 2) if total_students > 0 else 0,
                'avg_score': avg_score
            })
        conn.close()
        return result

    @classmethod
    def create(cls, title, description, creator_id, due_date, classes, paper_id=None, allow_late_submission=False):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO tasks (title, description, creator_id, paper_id, due_date, allow_late_submission) VALUES (?, ?, ?, ?, ?, ?)',
            (title, description, creator_id, paper_id, due_date, allow_late_submission)
        )
        task_id = cursor.lastrowid
        
        # 添加班级
        for class_name in classes:
            cursor.execute(
                'INSERT INTO task_classes (task_id, class_name) VALUES (?, ?)',
                (task_id, class_name)
            )
        
        conn.commit()
        conn.close()
        return task_id

    @classmethod
    def update(cls, task_id, title, description, paper_id, due_date, allow_late_submission, classes=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tasks
            SET title = ?, description = ?, paper_id = ?, due_date = ?, allow_late_submission = ?
            WHERE id = ?
        ''', (title, description, paper_id, due_date, allow_late_submission, task_id))
        if classes is not None:
            cursor.execute('DELETE FROM task_classes WHERE task_id = ?', (task_id,))
            for class_name in classes:
                cursor.execute('INSERT INTO task_classes (task_id, class_name) VALUES (?, ?)', (task_id, class_name))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def delete(cls, task_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM task_classes WHERE task_id = ?', (task_id,))
        cursor.execute('DELETE FROM task_submissions WHERE task_id = ?', (task_id,))
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
        return True 