"""
教学资源服务模块

负责教学资源的管理、上传、下载和分类标签管理
"""
import os
from datetime import datetime
import traceback

from core.helpers import get_db, db_fetch_one, db_fetch_all, db_execute
from core.errors import ApiError, ErrorCode
from models import Material, Category, Tag
from utils.file_utils import allowed_file, get_safe_filename, get_file_size, get_unique_filename, ensure_dir_exists

class MaterialService:
    @staticmethod
    def get_materials(page=1, page_size=12, **filters):
        """
        获取教学资源列表
        
        :param page: 页码
        :param page_size: 每页数量
        :param filters: 过滤条件
        :return: 资源列表及分页信息
        """
        try:
            result = Material.get_all(page, page_size, **filters)
            return result
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取教学资源列表失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def get_material_by_id(material_id):
        """
        获取教学资源详情
        
        :param material_id: 资源ID
        :return: 资源详情
        """
        try:
            material = Material.get_by_id(material_id)
            if not material:
                raise ApiError('教学资源不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            return material
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取教学资源详情失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def create_material(name, type_, url, uploader_id, size=None, thumbnail=None, category_id=None, description=None, tags=None):
        """
        创建教学资源
        
        :param name: 资源名称
        :param type_: 资源类型
        :param url: 资源URL
        :param uploader_id: 上传者ID
        :param size: 文件大小
        :param thumbnail: 缩略图URL
        :param category_id: 分类ID
        :param description: 描述
        :param tags: 标签ID列表
        :return: 新资源ID
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证上传者是否存在
            cursor.execute('SELECT id FROM users WHERE id = ?', (uploader_id,))
            if not cursor.fetchone():
                raise ApiError('上传者不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证分类是否存在
            if category_id:
                cursor.execute('SELECT id FROM categories WHERE id = ?', (category_id,))
                if not cursor.fetchone():
                    raise ApiError('分类不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证标签是否存在
            if tags:
                for tag_id in tags:
                    cursor.execute('SELECT id FROM tags WHERE id = ?', (tag_id,))
                    if not cursor.fetchone():
                        raise ApiError(f'标签ID {tag_id} 不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            material_id = Material.create(
                name=name,
                type_=type_,
                url=url,
                size=size or 0,
                uploader_id=uploader_id,
                thumbnail=thumbnail,
                category_id=category_id,
                description=description,
                tags=tags
            )
            
            return material_id
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'创建教学资源失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def update_material(material_id, data):
        """
        更新教学资源
        
        :param material_id: 资源ID
        :param data: 更新数据
        :return: 更新后的资源信息
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证资源是否存在
            cursor.execute('SELECT * FROM materials WHERE id = ?', (material_id,))
            material = cursor.fetchone()
            if not material:
                raise ApiError('教学资源不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            material_dict = dict(material)
            
            # 验证分类是否存在
            if 'category_id' in data and data['category_id']:
                cursor.execute('SELECT id FROM categories WHERE id = ?', (data['category_id'],))
                if not cursor.fetchone():
                    raise ApiError('分类不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证标签是否存在
            if 'tags' in data and data['tags']:
                for tag_id in data['tags']:
                    cursor.execute('SELECT id FROM tags WHERE id = ?', (tag_id,))
                    if not cursor.fetchone():
                        raise ApiError(f'标签ID {tag_id} 不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 更新资源
            Material.update(
                material_id=material_id,
                name=data.get('name', material_dict['name']),
                type_=data.get('type', material_dict['type']),
                url=data.get('url', material_dict['url']),
                size=data.get('size', material_dict['size']),
                uploader_id=material_dict['uploader_id'],  # 不允许修改上传者
                thumbnail=data.get('thumbnail', material_dict['thumbnail']),
                category_id=data.get('category_id', material_dict['category_id']),
                description=data.get('description', material_dict['description']),
                tags=data.get('tags')
            )
            
            return MaterialService.get_material_by_id(material_id)
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'更新教学资源失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def delete_material(material_id):
        """
        删除教学资源
        
        :param material_id: 资源ID
        :return: 成功返回True
        """
        try:
            # 验证资源是否存在
            material = MaterialService.get_material_by_id(material_id)
            if not material:
                raise ApiError('教学资源不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            Material.delete(material_id)
            return True
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'删除教学资源失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def increment_view_count(material_id):
        """
        增加资源浏览量
        
        :param material_id: 资源ID
        :return: 成功返回True
        """
        try:
            Material.increment_view_count(material_id)
            return True
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'更新浏览量失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)

    @staticmethod
    def upload_courseware(file, uploader_id, category_id=None, description=None, tags=None):
        """
        上传课件
        
        :param file: 文件对象
        :param uploader_id: 上传者ID
        :param category_id: 分类ID
        :param description: 描述
        :param tags: 标签ID列表
        :return: 新资源ID和资源信息
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证上传者是否存在
            cursor.execute('SELECT id FROM users WHERE id = ?', (uploader_id,))
            if not cursor.fetchone():
                raise ApiError('上传者不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证文件类型
            allowed_extensions = {'ppt', 'pptx', 'pdf', 'doc', 'docx', 'xls', 'xlsx'}
            if not allowed_file(file.filename, allowed_extensions):
                raise ApiError('不支持的文件类型，仅支持PPT、PDF、Word和Excel文件', code=ErrorCode.VALIDATION_ERROR)
            
            # 验证文件大小（限制为50MB）
            max_size = 50 * 1024 * 1024  # 50MB
            if file.content_length > max_size:
                raise ApiError('文件大小超过限制（最大50MB）', code=ErrorCode.VALIDATION_ERROR)
            
            # 确保上传目录存在
            upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads', 'courseware')
            ensure_dir_exists(upload_dir)
            
            # 生成安全的文件名
            filename = get_unique_filename(file.filename)
            file_path = os.path.join(upload_dir, filename)
            
            # 保存文件
            file.save(file_path)
            file_size = get_file_size(file_path)
            
            # 获取原始文件名（不含路径）
            original_filename = os.path.basename(file.filename)
            
            # 创建资源记录
            material_id = Material.create(
                name=original_filename,
                type_='courseware',  # 指定类型为课件
                url=f'/uploads/courseware/{filename}',
                size=file_size,
                uploader_id=uploader_id,
                thumbnail=None,  # 课件暂不生成缩略图
                category_id=category_id,
                description=description,
                tags=tags
            )
            
            # 获取创建的资源信息
            material = Material.get_by_id(material_id)
            
            return {
                'id': material_id,
                'material': material
            }
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'上传课件失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()

class CategoryService:
    @staticmethod
    def get_categories():
        """
        获取所有分类
        
        :return: 分类列表
        """
        try:
            return Category.get_all()
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取分类列表失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def create_category(name, parent_id=None):
        """
        创建分类
        
        :param name: 分类名称
        :param parent_id: 父分类ID
        :return: 新分类ID
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证分类名称不为空
            if not name or not name.strip():
                raise ApiError('分类名称不能为空', code=ErrorCode.VALIDATION_ERROR)
            
            # 验证父分类是否存在
            if parent_id:
                cursor.execute('SELECT id FROM categories WHERE id = ?', (parent_id,))
                if not cursor.fetchone():
                    raise ApiError('父分类不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 检查同名分类是否已存在
            cursor.execute('SELECT id FROM categories WHERE name = ? AND parent_id = ?', (name.strip(), parent_id))
            if cursor.fetchone():
                raise ApiError('该分类已存在', code=ErrorCode.VALIDATION_ERROR)
            
            category_id = Category.create(name.strip(), parent_id)
            return category_id
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'创建分类失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def update_category(category_id, name, parent_id=None):
        """
        更新分类
        
        :param category_id: 分类ID
        :param name: 分类名称
        :param parent_id: 父分类ID
        :return: 成功返回True
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证分类是否存在
            cursor.execute('SELECT id FROM categories WHERE id = ?', (category_id,))
            if not cursor.fetchone():
                raise ApiError('分类不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证分类名称不为空
            if not name or not name.strip():
                raise ApiError('分类名称不能为空', code=ErrorCode.VALIDATION_ERROR)
            
            # 验证父分类是否存在
            if parent_id:
                cursor.execute('SELECT id FROM categories WHERE id = ?', (parent_id,))
                if not cursor.fetchone():
                    raise ApiError('父分类不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
                
                # 防止循环引用
                if parent_id == category_id:
                    raise ApiError('不能将分类设为自己的父分类', code=ErrorCode.VALIDATION_ERROR)
            
            Category.update(category_id, name.strip(), parent_id)
            return True
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'更新分类失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def delete_category(category_id):
        """
        删除分类
        
        :param category_id: 分类ID
        :return: 成功返回True
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证分类是否存在
            cursor.execute('SELECT id FROM categories WHERE id = ?', (category_id,))
            if not cursor.fetchone():
                raise ApiError('分类不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 检查是否有子分类
            cursor.execute('SELECT id FROM categories WHERE parent_id = ?', (category_id,))
            if cursor.fetchone():
                raise ApiError('该分类下还有子分类，不能删除', code=ErrorCode.VALIDATION_ERROR)
            
            # 检查是否有关联的资源
            cursor.execute('SELECT id FROM materials WHERE category_id = ?', (category_id,))
            if cursor.fetchone():
                raise ApiError('该分类下还有教学资源，不能删除', code=ErrorCode.VALIDATION_ERROR)
            
            Category.delete(category_id)
            return True
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'删除分类失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()

class TagService:
    @staticmethod
    def get_tags():
        """
        获取所有标签
        
        :return: 标签列表
        """
        try:
            return Tag.get_all()
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取标签列表失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def create_tag(name):
        """
        创建标签
        
        :param name: 标签名称
        :return: 新标签ID
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证标签名称不为空
            if not name or not name.strip():
                raise ApiError('标签名称不能为空', code=ErrorCode.VALIDATION_ERROR)
            
            # 检查同名标签是否已存在
            cursor.execute('SELECT id FROM tags WHERE name = ?', (name.strip(),))
            if cursor.fetchone():
                raise ApiError('该标签已存在', code=ErrorCode.VALIDATION_ERROR)
            
            tag_id = Tag.create(name.strip())
            return tag_id
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'创建标签失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def update_tag(tag_id, name):
        """
        更新标签
        
        :param tag_id: 标签ID
        :param name: 标签名称
        :return: 成功返回True
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证标签是否存在
            cursor.execute('SELECT id FROM tags WHERE id = ?', (tag_id,))
            if not cursor.fetchone():
                raise ApiError('标签不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证标签名称不为空
            if not name or not name.strip():
                raise ApiError('标签名称不能为空', code=ErrorCode.VALIDATION_ERROR)
            
            # 检查同名标签是否已存在
            cursor.execute('SELECT id FROM tags WHERE name = ? AND id != ?', (name.strip(), tag_id))
            if cursor.fetchone():
                raise ApiError('该标签已存在', code=ErrorCode.VALIDATION_ERROR)
            
            Tag.update(tag_id, name.strip())
            return True
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'更新标签失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def delete_tag(tag_id):
        """
        删除标签
        
        :param tag_id: 标签ID
        :return: 成功返回True
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证标签是否存在
            cursor.execute('SELECT id FROM tags WHERE id = ?', (tag_id,))
            if not cursor.fetchone():
                raise ApiError('标签不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 删除标签及其关联关系
            cursor.execute('DELETE FROM material_tags WHERE tag_id = ?', (tag_id,))
            Tag.delete(tag_id)
            return True
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'删除标签失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close() 