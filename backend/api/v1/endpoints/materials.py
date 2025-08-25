"""
教学资源相关路由
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from core.auth import role_required, roles_required
from services.material_service import MaterialService, CategoryService, TagService
import traceback

# ================== 教学资源相关路由 ==================

# 获取教学资源列表
@api.route('/materials', methods=['GET'])
def get_materials():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 12, type=int)
    
    # 提取过滤参数
    filters = {}
    if request.args.get('query'):
        filters['query'] = request.args.get('query')
    if request.args.get('type'):
        filters['type'] = request.args.get('type')
    if request.args.get('category_id'):
        filters['category_id'] = request.args.get('category_id', type=int)
    if request.args.get('tag_id'):
        filters['tag_id'] = request.args.get('tag_id', type=int)
    if request.args.get('sort_by'):
        filters['sort_by'] = request.args.get('sort_by')
    
    try:
        result = MaterialService.get_materials(page, page_size, **filters)
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取教学资源列表失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('获取教学资源列表失败', code=ErrorCode.OPERATION_FAILED)

# 获取教学资源详情
@api.route('/materials/<int:material_id>', methods=['GET'])
def get_material(material_id):
    try:
        material = MaterialService.get_material_by_id(material_id)
        # 增加浏览量
        MaterialService.increment_view_count(material_id)
        return ok_response(material)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取教学资源详情失败: {str(e)}")
        raise ApiError('获取教学资源详情失败', code=ErrorCode.OPERATION_FAILED)

# 创建教学资源
@api.route('/materials', methods=['POST'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def create_material():
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        required_fields = ['name', 'type', 'url']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        material_id = MaterialService.create_material(
            name=data['name'],
            type_=data['type'],
            url=data['url'],
            uploader_id=identity['id'],
            size=data.get('size'),
            thumbnail=data.get('thumbnail'),
            category_id=data.get('category_id'),
            description=data.get('description'),
            tags=data.get('tags', [])
        )
        
        material = MaterialService.get_material_by_id(material_id)
        return ok_response(material, message='教学资源创建成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"创建教学资源失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('创建教学资源失败', code=ErrorCode.OPERATION_FAILED)

# 更新教学资源
@api.route('/materials/<int:material_id>', methods=['PUT'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def update_material(material_id):
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证权限（只有上传者或管理员可以更新）
        if identity['role'] != 'admin':
            material = MaterialService.get_material_by_id(material_id)
            if not material or material['uploader_id'] != identity['id']:
                raise ApiError('无权更新此教学资源', code=ErrorCode.PERMISSION_DENIED)
        
        updated_material = MaterialService.update_material(material_id, data)
        return ok_response(updated_material, message='教学资源更新成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"更新教学资源失败: {str(e)}")
        raise ApiError('更新教学资源失败', code=ErrorCode.OPERATION_FAILED)

# 删除教学资源
@api.route('/materials/<int:material_id>', methods=['DELETE'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def delete_material(material_id):
    identity = get_jwt_identity()
    
    try:
        # 验证权限（只有上传者或管理员可以删除）
        if identity['role'] != 'admin':
            material = MaterialService.get_material_by_id(material_id)
            if not material or material['uploader_id'] != identity['id']:
                raise ApiError('无权删除此教学资源', code=ErrorCode.PERMISSION_DENIED)
        
        MaterialService.delete_material(material_id)
        return ok_response(message='教学资源删除成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"删除教学资源失败: {str(e)}")
        raise ApiError('删除教学资源失败', code=ErrorCode.OPERATION_FAILED)

# ================== 分类相关路由 ==================

# 获取分类列表
@api.route('/materials/categories', methods=['GET'])
def get_categories():
    try:
        categories = CategoryService.get_categories()
        return ok_response(categories)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取分类列表失败: {str(e)}")
        raise ApiError('获取分类列表失败', code=ErrorCode.OPERATION_FAILED)

# 创建分类
@api.route('/materials/categories', methods=['POST'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def create_category():
    data = request.get_json() or {}
    
    try:
        if 'name' not in data:
            raise ApiError('缺少必填字段: name', code=ErrorCode.VALIDATION_ERROR)
        
        category_id = CategoryService.create_category(
            name=data['name'],
            parent_id=data.get('parent_id')
        )
        
        return ok_response({'id': category_id}, message='分类创建成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"创建分类失败: {str(e)}")
        raise ApiError('创建分类失败', code=ErrorCode.OPERATION_FAILED)

# 更新分类
@api.route('/materials/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def update_category(category_id):
    data = request.get_json() or {}
    
    try:
        if 'name' not in data:
            raise ApiError('缺少必填字段: name', code=ErrorCode.VALIDATION_ERROR)
        
        CategoryService.update_category(
            category_id=category_id,
            name=data['name'],
            parent_id=data.get('parent_id')
        )
        
        return ok_response(message='分类更新成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"更新分类失败: {str(e)}")
        raise ApiError('更新分类失败', code=ErrorCode.OPERATION_FAILED)

# 删除分类
@api.route('/materials/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def delete_category(category_id):
    try:
        CategoryService.delete_category(category_id)
        return ok_response(message='分类删除成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"删除分类失败: {str(e)}")
        raise ApiError('删除分类失败', code=ErrorCode.OPERATION_FAILED)

# ================== 标签相关路由 ==================

# 获取标签列表
@api.route('/materials/tags', methods=['GET'])
def get_tags():
    try:
        tags = TagService.get_tags()
        return ok_response(tags)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取标签列表失败: {str(e)}")
        raise ApiError('获取标签列表失败', code=ErrorCode.OPERATION_FAILED)

# 创建标签
@api.route('/materials/tags', methods=['POST'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def create_tag():
    data = request.get_json() or {}
    
    try:
        if 'name' not in data:
            raise ApiError('缺少必填字段: name', code=ErrorCode.VALIDATION_ERROR)
        
        tag_id = TagService.create_tag(data['name'])
        
        return ok_response({'id': tag_id}, message='标签创建成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"创建标签失败: {str(e)}")
        raise ApiError('创建标签失败', code=ErrorCode.OPERATION_FAILED)

# 更新标签
@api.route('/materials/tags/<int:tag_id>', methods=['PUT'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def update_tag(tag_id):
    data = request.get_json() or {}
    
    try:
        if 'name' not in data:
            raise ApiError('缺少必填字段: name', code=ErrorCode.VALIDATION_ERROR)
        
        TagService.update_tag(tag_id, data['name'])
        
        return ok_response(message='标签更新成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"更新标签失败: {str(e)}")
        raise ApiError('更新标签失败', code=ErrorCode.OPERATION_FAILED)

# 删除标签
@api.route('/materials/tags/<int:tag_id>', methods=['DELETE'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def delete_tag(tag_id):
    try:
        TagService.delete_tag(tag_id)
        return ok_response(message='标签删除成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"删除标签失败: {str(e)}")
        raise ApiError('删除标签失败', code=ErrorCode.OPERATION_FAILED) 