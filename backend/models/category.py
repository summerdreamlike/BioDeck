from .base import BaseModel

class Category(BaseModel):
    @classmethod
    def get_all(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM categories ORDER BY id DESC')
        items = [cls.dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @classmethod
    def create(cls, name, parent_id=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO categories (name, parent_id) VALUES (?, ?)', (name, parent_id))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    @classmethod
    def update(cls, category_id, name, parent_id=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE categories SET name = ?, parent_id = ? WHERE id = ?', (name, parent_id, category_id))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def delete(cls, category_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
        conn.commit()
        conn.close()
        return True

class Tag(BaseModel):
    @classmethod
    def get_all(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tags ORDER BY id DESC')
        items = [cls.dict_from_row(row) for row in cursor.fetchall()]
        conn.close()
        return items

    @classmethod
    def create(cls, name):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tags (name) VALUES (?)', (name,))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    @classmethod
    def update(cls, tag_id, name):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE tags SET name = ? WHERE id = ?', (name, tag_id))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def delete(cls, tag_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tags WHERE id = ?', (tag_id,))
        conn.commit()
        conn.close()
        return True 