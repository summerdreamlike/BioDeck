from datetime import datetime
import json
from .base import BaseModel

class Practice(BaseModel):
    @classmethod
    def submit(cls, student_id, knowledge_point, is_correct, submitted_at=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        if not submitted_at:
            submitted_at = datetime.now().isoformat()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS practices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                knowledge_point TEXT NOT NULL,
                is_correct INTEGER NOT NULL,
                submitted_at TIMESTAMP NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students (id)
            )
        ''')
        cursor.execute('''
            INSERT INTO practices (student_id, knowledge_point, is_correct, submitted_at)
            VALUES (?, ?, ?, ?)
        ''', (student_id, knowledge_point, 1 if is_correct else 0, submitted_at))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    @classmethod
    def get_student_stats(cls, student_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT knowledge_point,
                   COUNT(*) as total,
                   SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct
            FROM practices
            WHERE student_id = ?
            GROUP BY knowledge_point
        ''', (student_id,))
        rows = cursor.fetchall()
        conn.close()
        stats = []
        for r in rows:
            kp = r['knowledge_point'] or '综合'
            total = r['total'] or 0
            correct = r['correct'] or 0
            acc = round(correct / total * 100, 2) if total > 0 else 0
            stats.append({'knowledge_point': kp, 'total': total, 'correct': correct, 'accuracy': acc})
        return stats

class WrongBook(BaseModel):
    @classmethod
    def add(cls, student_id, knowledge_point):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS wrong_book (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                knowledge_point TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(student_id, knowledge_point)
            )
        ''')
        try:
            cursor.execute('INSERT INTO wrong_book (student_id, knowledge_point) VALUES (?, ?)',
                           (student_id, knowledge_point))
            conn.commit()
        except Exception:
            pass
        conn.close()
        return True

    @classmethod
    def list_by_student(cls, student_id, page=1, page_size=20):
        conn = cls.get_db()
        cursor = conn.cursor()
        offset = (page - 1) * page_size
        cursor.execute('SELECT COUNT(*) FROM wrong_book WHERE student_id = ?', (student_id,))
        total = cursor.fetchone()[0]
        cursor.execute('''
            SELECT wb.id, wb.knowledge_point, wb.created_at
            FROM wrong_book wb
            WHERE wb.student_id = ?
            ORDER BY wb.created_at DESC
            LIMIT ? OFFSET ?
        ''', (student_id, page_size, offset))
        items = []
        for row in cursor.fetchall():
            d = cls.dict_from_row(row)
            if d.get('options'):
                try:
                    d['options'] = json.loads(d['options'])
                except Exception:
                    pass
            items.append(d)
        conn.close()
        return {'items': items, 'total': total, 'page': page, 'page_size': page_size} 