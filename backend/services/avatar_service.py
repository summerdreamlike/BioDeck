"""
头像服务模块

负责头像的上传、存储、删除等功能
"""
import os
import uuid
import traceback
from PIL import Image
from werkzeug.utils import secure_filename

from core.helpers import get_db, db_fetch_one, db_execute
from core.errors import ApiError, ErrorCode
from utils.file_utils import allowed_file, get_mime_type, get_unique_filename

class AvatarService:
    # 允许的头像文件类型
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    # 最大文件大小 (5MB)
    MAX_FILE_SIZE = 5 * 1024 * 1024
    # 头像存储目录
    AVATAR_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'avatars')
    
    @staticmethod
    def _ensure_schema(conn, cursor):
        """
        确保所需的数据表与字段已存在：
        - users.avatar_url 列
        - avatar_files 表
        """
        try:
            # 确保 users 表存在 avatar_url 列
            cursor.execute('PRAGMA table_info(users)')
            columns = [row[1] for row in cursor.fetchall()]
            if 'avatar_url' not in columns:
                cursor.execute('ALTER TABLE users ADD COLUMN avatar_url TEXT')
                conn.commit()
        except Exception:
            conn.rollback()
            raise

        try:
            # 确保 avatar_files 表存在
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS avatar_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    filename TEXT NOT NULL,
                    original_filename TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    mime_type TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    @staticmethod
    def upload_avatar(user_id, file):
        """
        上传用户头像
        
        :param user_id: 用户ID
        :param file: 上传的文件对象
        :return: 头像URL
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 确保所需表结构存在
            AvatarService._ensure_schema(conn, cursor)
            # 验证用户是否存在
            cursor.execute('SELECT id FROM users WHERE id = ?', (user_id,))
            if not cursor.fetchone():
                raise ApiError('用户不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证文件
            if not file or file.filename == '':
                raise ApiError('未选择文件', code=ErrorCode.VALIDATION_ERROR)
            
            # 检查文件类型
            if not allowed_file(file.filename, AvatarService.ALLOWED_EXTENSIONS):
                raise ApiError(f'不支持的文件类型，支持的类型: {", ".join(AvatarService.ALLOWED_EXTENSIONS)}', 
                             code=ErrorCode.VALIDATION_ERROR)
            
            # 检查文件大小
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > AvatarService.MAX_FILE_SIZE:
                raise ApiError(f'文件大小超过限制，最大允许 {AvatarService.MAX_FILE_SIZE // (1024*1024)}MB', 
                             code=ErrorCode.VALIDATION_ERROR)
            
            # 确保存储目录存在
            os.makedirs(AvatarService.AVATAR_DIR, exist_ok=True)
            
            # 生成唯一文件名
            original_filename = secure_filename(file.filename)
            file_extension = original_filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
            file_path = os.path.join(AvatarService.AVATAR_DIR, unique_filename)
            
            # 保存文件
            file.save(file_path)
            
            # 处理图片（可选：压缩、调整大小等）
            AvatarService._process_image(file_path)
            
            # 删除旧头像
            AvatarService._delete_old_avatar(user_id, cursor)
            
            # 更新数据库（与路由保持一致：蓝图前缀 /api/v1）
            avatar_url = f"/api/v1/uploads/avatars/{unique_filename}"
            cursor.execute('UPDATE users SET avatar_url = ? WHERE id = ?', (avatar_url, user_id))
            
            # 记录文件信息
            cursor.execute('''
                INSERT INTO avatar_files (user_id, filename, original_filename, file_size, mime_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, unique_filename, original_filename, file_size, get_mime_type(original_filename)))
            
            conn.commit()
            return avatar_url
            
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'上传头像失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_avatar_url(user_id):
        """
        获取用户头像URL
        
        :param user_id: 用户ID
        :return: 头像URL或None
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 确保所需表结构存在
            AvatarService._ensure_schema(conn, cursor)
            cursor.execute('SELECT avatar_url FROM users WHERE id = ?', (user_id,))
            result = cursor.fetchone()
            return result['avatar_url'] if result else None
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取头像失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def delete_avatar(user_id):
        """
        删除用户头像
        
        :param user_id: 用户ID
        :return: 是否删除成功
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 确保所需表结构存在
            AvatarService._ensure_schema(conn, cursor)
            # 验证用户是否存在
            cursor.execute('SELECT avatar_url FROM users WHERE id = ?', (user_id,))
            result = cursor.fetchone()
            if not result:
                raise ApiError('用户不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            avatar_url = result['avatar_url']
            if not avatar_url:
                return True  # 没有头像，直接返回成功
            
            # 删除文件
            filename = avatar_url.split('/')[-1]
            file_path = os.path.join(AvatarService.AVATAR_DIR, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # 更新数据库
            cursor.execute('UPDATE users SET avatar_url = NULL WHERE id = ?', (user_id,))
            cursor.execute('DELETE FROM avatar_files WHERE user_id = ?', (user_id,))
            
            conn.commit()
            return True
            
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'删除头像失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def _process_image(file_path):
        """
        处理图片（压缩、调整大小等）
        
        :param file_path: 图片文件路径
        """
        try:
            with Image.open(file_path) as img:
                # 转换为RGB模式（如果是RGBA）
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                
                # 调整大小（最大200x200）
                max_size = (200, 200)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # 保存处理后的图片
                img.save(file_path, quality=85, optimize=True)
        except Exception as e:
            # 图片处理失败不影响上传
            print(f"图片处理失败: {str(e)}")
    
    @staticmethod
    def _delete_old_avatar(user_id, cursor):
        """
        删除用户旧头像
        
        :param user_id: 用户ID
        :param cursor: 数据库游标
        """
        try:
            # 获取旧头像信息
            cursor.execute('SELECT avatar_url FROM users WHERE id = ?', (user_id,))
            result = cursor.fetchone()
            if result and result['avatar_url']:
                old_filename = result['avatar_url'].split('/')[-1]
                old_file_path = os.path.join(AvatarService.AVATAR_DIR, old_filename)
                
                # 删除旧文件
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
                
                # 删除旧文件记录
                cursor.execute('DELETE FROM avatar_files WHERE user_id = ?', (user_id,))
        except Exception as e:
            # 删除旧头像失败不影响新头像上传
            print(f"删除旧头像失败: {str(e)}")
    
    @staticmethod
    def get_avatar_info(user_id):
        """
        获取头像详细信息
        
        :param user_id: 用户ID
        :return: 头像信息字典
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 确保所需表结构存在
            AvatarService._ensure_schema(conn, cursor)
            cursor.execute('''
                SELECT u.avatar_url, af.filename, af.original_filename, af.file_size, af.mime_type, af.created_at
                FROM users u
                LEFT JOIN avatar_files af ON u.id = af.user_id
                WHERE u.id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            if not result:
                return None
            
            return {
                'avatar_url': result['avatar_url'],
                'filename': result['filename'],
                'original_filename': result['original_filename'],
                'file_size': result['file_size'],
                'mime_type': result['mime_type'],
                'created_at': result['created_at']
            }
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取头像信息失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
