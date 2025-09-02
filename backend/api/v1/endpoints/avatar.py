"""
头像相关路由
"""
from flask import request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from core.auth import role_required
from services.avatar_service import AvatarService

# 上传头像
@api.route('/users/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    """上传用户头像"""
    identity = get_jwt_identity()
    
    try:
        # 检查是否有文件上传
        if 'avatar' not in request.files:
            raise ApiError('未选择头像文件', code=ErrorCode.VALIDATION_ERROR)
        
        file = request.files['avatar']
        
        # 上传头像
        avatar_url = AvatarService.upload_avatar(identity['id'], file)
        
        return ok_response({
            'avatar_url': avatar_url,
            'message': '头像上传成功'
        })
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"上传头像失败: {str(e)}")
        raise ApiError('上传头像失败', code=ErrorCode.OPERATION_FAILED)

# 获取用户头像
@api.route('/users/avatar/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_avatar(user_id):
    """获取用户头像"""
    identity = get_jwt_identity()
    
    try:
        # 获取头像URL
        avatar_url = AvatarService.get_avatar_url(user_id)
        
        if not avatar_url:
            return ok_response({
                'avatar_url': None,
                'message': '用户没有头像'
            })
        
        return ok_response({
            'avatar_url': avatar_url,
            'message': '获取头像成功'
        })
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取头像失败: {str(e)}")
        raise ApiError('获取头像失败', code=ErrorCode.OPERATION_FAILED)

# 获取头像详细信息
@api.route('/users/avatar/<int:user_id>/info', methods=['GET'])
@jwt_required()
def get_avatar_info(user_id):
    """获取头像详细信息"""
    identity = get_jwt_identity()
    
    try:
        # 获取头像信息
        avatar_info = AvatarService.get_avatar_info(user_id)
        
        if not avatar_info:
            return ok_response({
                'avatar_info': None,
                'message': '用户没有头像'
            })
        
        return ok_response({
            'avatar_info': avatar_info,
            'message': '获取头像信息成功'
        })
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取头像信息失败: {str(e)}")
        raise ApiError('获取头像信息失败', code=ErrorCode.OPERATION_FAILED)

# 删除头像
@api.route('/users/avatar', methods=['DELETE'])
@jwt_required()
def delete_avatar():
    """删除用户头像"""
    identity = get_jwt_identity()
    
    try:
        # 删除头像
        AvatarService.delete_avatar(identity['id'])
        
        return ok_response({
            'message': '头像删除成功'
        })
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"删除头像失败: {str(e)}")
        raise ApiError('删除头像失败', code=ErrorCode.OPERATION_FAILED)

# 更新头像（实际上是重新上传）
@api.route('/users/avatar', methods=['PUT'])
@jwt_required()
def update_avatar():
    """更新用户头像"""
    identity = get_jwt_identity()
    
    try:
        # 检查是否有文件上传
        if 'avatar' not in request.files:
            raise ApiError('未选择头像文件', code=ErrorCode.VALIDATION_ERROR)
        
        file = request.files['avatar']
        
        # 上传新头像（会自动删除旧头像）
        avatar_url = AvatarService.upload_avatar(identity['id'], file)
        
        return ok_response({
            'avatar_url': avatar_url,
            'message': '头像更新成功'
        })
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"更新头像失败: {str(e)}")
        raise ApiError('更新头像失败', code=ErrorCode.OPERATION_FAILED)

# 静态文件服务 - 提供头像文件访问
@api.route('/uploads/avatars/<filename>', methods=['GET'])
def serve_avatar(filename):
    """提供头像文件访问"""
    try:
        avatar_dir = AvatarService.AVATAR_DIR
        return send_from_directory(avatar_dir, filename)
    except Exception as e:
        api.logger.error(f"访问头像文件失败: {str(e)}")
        raise ApiError('头像文件不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
