from .base import BaseModel

class Message(BaseModel):
    @classmethod
    def get_by_recipient_id(cls, recipient_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.*, u.name as sender_name
            FROM messages m
            LEFT JOIN users u ON m.sender_id = u.id
            WHERE m.recipient_id = ?
            ORDER BY m.created_at DESC
        ''', (recipient_id,))
        messages = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        return messages
    
    @classmethod
    def mark_as_read(cls, message_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE messages SET read = 1 WHERE id = ?',
            (message_id,)
        )
        
        conn.commit()
        
        cursor.execute('''
            SELECT m.*, u.name as sender_name
            FROM messages m
            LEFT JOIN users u ON m.sender_id = u.id
            WHERE m.id = ?
        ''', (message_id,))
        message = cursor.fetchone()
        
        conn.close()
        return cls.dict_from_row(message)
    
    @classmethod
    def create(cls, type_, recipient_id, title, content, sender_id=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO messages (type, sender_id, recipient_id, title, content) VALUES (?, ?, ?, ?, ?)',
            (type_, sender_id, recipient_id, title, content)
        )
        message_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        return message_id 