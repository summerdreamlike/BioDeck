"""
文件处理工具函数
"""
import os
import uuid
import mimetypes
from werkzeug.utils import secure_filename

def allowed_file(filename, allowed_extensions=None):
    """
    检查文件扩展名是否在允许的扩展名列表中
    
    :param filename: 文件名
    :param allowed_extensions: 允许的扩展名列表，如果为None，允许所有扩展名
    :return: 是否允许
    """
    if allowed_extensions is None:
        return True
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_extension(filename):
    """
    获取文件扩展名
    
    :param filename: 文件名
    :return: 扩展名（小写）
    """
    if '.' in filename:
        return filename.rsplit('.', 1)[1].lower()
    return ''

def get_mime_type(filename):
    """
    根据文件名获取MIME类型
    
    :param filename: 文件名
    :return: MIME类型
    """
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

def get_safe_filename(filename):
    """
    获取安全的文件名，防止恶意文件名
    
    :param filename: 原始文件名
    :return: 安全的文件名
    """
    return secure_filename(filename)

def get_unique_filename(filename):
    """
    获取唯一的文件名，在原文件名前添加UUID
    
    :param filename: 原始文件名
    :return: 唯一的文件名
    """
    ext = get_file_extension(filename)
    basename = os.path.splitext(get_safe_filename(filename))[0]
    return f"{uuid.uuid4().hex}_{basename}.{ext}"

def get_file_size(file_path):
    """
    获取文件大小（字节）
    
    :param file_path: 文件路径
    :return: 文件大小（字节）
    """
    return os.path.getsize(file_path)

def format_file_size(size_bytes):
    """
    格式化文件大小，自动选择合适的单位
    
    :param size_bytes: 文件大小（字节）
    :return: 格式化后的大小字符串
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def ensure_dir_exists(directory):
    """
    确保目录存在，如果不存在则创建
    
    :param directory: 目录路径
    """
    os.makedirs(directory, exist_ok=True) 