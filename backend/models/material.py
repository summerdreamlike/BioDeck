from .base import BaseModel

class Material(BaseModel):
    @classmethod
    def get_all(cls, page=1, page_size=12, **filters):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 构建SQL查询
        sql = '''
            SELECT DISTINCT m.*, u.name as uploader_name, c.name as category_name
            FROM materials m
            LEFT JOIN users u ON m.uploader_id = u.id
            LEFT JOIN categories c ON m.category_id = c.id
            LEFT JOIN material_tags mt ON m.id = mt.material_id
        '''
        
        where_clauses = []
        params = []
        
        if 'query' in filters and filters['query']:
            where_clauses.append('(m.name LIKE ? OR m.description LIKE ?)')
            query = f"%{filters['query']}%"
            params.extend([query, query])
        
        if 'type' in filters and filters['type']:
            where_clauses.append('m.type = ?')
            params.append(filters['type'])
        
        if 'category_id' in filters and filters['category_id']:
            where_clauses.append('m.category_id = ?')
            params.append(filters['category_id'])
        
        if 'tag_id' in filters and filters['tag_id']:
            where_clauses.append('mt.tag_id = ?')
            params.append(filters['tag_id'])
        
        if where_clauses:
            sql += ' WHERE ' + ' AND '.join(where_clauses)
        
        # 排序
        sort_by = filters.get('sort_by', 'uploadTime')
        if sort_by == 'uploadTime':
            sql += ' ORDER BY m.upload_time DESC'
        elif sort_by == 'viewCount':
            sql += ' ORDER BY m.view_count DESC'
        elif sort_by == 'name':
            sql += ' ORDER BY m.name ASC'
        
        # 计算总数
        count_sql = f"SELECT COUNT(DISTINCT m.id) as count FROM ({sql})"
        cursor.execute(count_sql, params)
        total = cursor.fetchone()['count']
        
        # 应用分页
        sql += ' LIMIT ? OFFSET ?'
        offset = (page - 1) * page_size
        params.extend([page_size, offset])
        
        cursor.execute(sql, params)
        materials = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        # 获取每个资源的标签
        for material in materials:
            cursor.execute('''
                SELECT t.* FROM tags t
                JOIN material_tags mt ON t.id = mt.tag_id
                WHERE mt.material_id = ?
            ''', (material['id'],))
            material['tags'] = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'items': materials,
            'total': total,
            'page': page,
            'page_size': page_size
        }
    
    @classmethod
    def get_by_id(cls, material_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.*, u.name as uploader_name, c.name as category_name
            FROM materials m
            LEFT JOIN users u ON m.uploader_id = u.id
            LEFT JOIN categories c ON m.category_id = c.id
            WHERE m.id = ?
        ''', (material_id,))
        material = cursor.fetchone()
        
        if not material:
            conn.close()
            return None
        
        material_dict = cls.dict_from_row(material)
        
        # 获取标签
        cursor.execute('''
            SELECT t.* FROM tags t
            JOIN material_tags mt ON t.id = mt.tag_id
            WHERE mt.material_id = ?
        ''', (material_id,))
        material_dict['tags'] = [cls.dict_from_row(row) for row in cursor.fetchall()]
        
        conn.close()
        return material_dict
    
    @classmethod
    def create(cls, name, type_, url, size, uploader_id, thumbnail=None, category_id=None, description=None, tags=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO materials (name, type, url, thumbnail, size, uploader_id, category_id, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (name, type_, url, thumbnail, size, uploader_id, category_id, description)
        )
        material_id = cursor.lastrowid
        
        # 处理标签
        if tags:
            for tag_id in tags:
                cursor.execute(
                    'INSERT INTO material_tags (material_id, tag_id) VALUES (?, ?)',
                    (material_id, tag_id)
                )
        
        conn.commit()
        conn.close()
        return material_id
    
    @classmethod
    def update(cls, material_id, name, type_, url, size, uploader_id, thumbnail=None, category_id=None, description=None, tags=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE materials
            SET name = ?, type = ?, url = ?, thumbnail = ?, size = ?, uploader_id = ?, category_id = ?, description = ?
            WHERE id = ?
        ''', (name, type_, url, thumbnail, size, uploader_id, category_id, description, material_id))
        if tags is not None:
            cursor.execute('DELETE FROM material_tags WHERE material_id = ?', (material_id,))
            for tag_id in tags:
                cursor.execute('INSERT INTO material_tags (material_id, tag_id) VALUES (?, ?)', (material_id, tag_id))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def delete(cls, material_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM material_tags WHERE material_id = ?', (material_id,))
        cursor.execute('DELETE FROM materials WHERE id = ?', (material_id,))
        conn.commit()
        conn.close()
        return True
    
    @classmethod
    def increment_view_count(cls, material_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE materials SET view_count = view_count + 1 WHERE id = ?',
            (material_id,)
        )
        
        conn.commit()
        conn.close() 