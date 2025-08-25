"""
消息中心相关路由
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from core.auth import role_required, roles_required
from services.message_service import MessageService
import traceback

# ================== 消息管理相关路由 ==================

# 获取用户接收的消息列表
@api.route('/messages/received', methods=['GET'])
@jwt_required()
def get_received_messages():
    identity = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    # 提取过滤参数
    filters = {}
    if request.args.get('type'):
        filters['type'] = request.args.get('type')
    if request.args.get('read') is not None:
        filters['read'] = request.args.get('read', type=bool)
    if request.args.get('sender_id'):
        filters['sender_id'] = request.args.get('sender_id', type=int)
    
    try:
        result = MessageService.get_messages_by_recipient(
            recipient_id=identity['id'],
            page=page,
            page_size=page_size,
            **filters
        )
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取接收消息列表失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('获取接收消息列表失败', code=ErrorCode.OPERATION_FAILED)

# 获取用户发送的消息列表
@api.route('/messages/sent', methods=['GET'])
@jwt_required()
def get_sent_messages():
    identity = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    # 提取过滤参数
    filters = {}
    if request.args.get('type'):
        filters['type'] = request.args.get('type')
    if request.args.get('recipient_id'):
        filters['recipient_id'] = request.args.get('recipient_id', type=int)
    
    try:
        result = MessageService.get_messages_by_sender(
            sender_id=identity['id'],
            page=page,
            page_size=page_size,
            **filters
        )
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取发送消息列表失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('获取发送消息列表失败', code=ErrorCode.OPERATION_FAILED)

# 获取消息详情
@api.route('/messages/<int:message_id>', methods=['GET'])
@jwt_required()
def get_message(message_id):
    identity = get_jwt_identity()
    
    try:
        message = MessageService.get_message_by_id(message_id, identity['id'])
        return ok_response(message)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取消息详情失败: {str(e)}")
        raise ApiError('获取消息详情失败', code=ErrorCode.OPERATION_FAILED)

# 发送私信
@api.route('/messages', methods=['POST'])
@jwt_required()
def send_message():
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        required_fields = ['recipient_id', 'title', 'content']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        # 不能给自己发消息
        if data['recipient_id'] == identity['id']:
            raise ApiError('不能给自己发送消息', code=ErrorCode.VALIDATION_ERROR)
        
        message_id = MessageService.create_message(
            type_=data.get('type', 'private'),
            recipient_id=data['recipient_id'],
            title=data['title'],
            content=data['content'],
            sender_id=identity['id']
        )
        
        return ok_response({'id': message_id}, message='消息发送成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"发送消息失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('发送消息失败', code=ErrorCode.OPERATION_FAILED)

# 发送公告（管理员和教师）
@api.route('/messages/announcement', methods=['POST'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def send_announcement():
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        required_fields = ['recipient_ids', 'title', 'content']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        # 验证接收者列表
        if not isinstance(data['recipient_ids'], list) or not data['recipient_ids']:
            raise ApiError('接收者列表不能为空', code=ErrorCode.VALIDATION_ERROR)
        
        created_count = MessageService.create_bulk_message(
            type_='announcement',
            recipient_ids=data['recipient_ids'],
            title=data['title'],
            content=data['content'],
            sender_id=identity['id']
        )
        
        return ok_response({
            'created_count': created_count
        }, message=f'公告发送成功，共发送给 {created_count} 个用户')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"发送公告失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('发送公告失败', code=ErrorCode.OPERATION_FAILED)

# 标记消息为已读
@api.route('/messages/<int:message_id>/read', methods=['PUT'])
@jwt_required()
def mark_message_read(message_id):
    identity = get_jwt_identity()
    
    try:
        updated_message = MessageService.mark_message_as_read(message_id, identity['id'])
        return ok_response(updated_message, message='消息已标记为已读')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"标记消息已读失败: {str(e)}")
        raise ApiError('标记消息已读失败', code=ErrorCode.OPERATION_FAILED)

# 批量标记消息为已读
@api.route('/messages/read-all', methods=['PUT'])
@jwt_required()
def mark_all_messages_read():
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 提取过滤参数
        filters = {}
        if 'type' in data:
            filters['type'] = data['type']
        if 'sender_id' in data:
            filters['sender_id'] = data['sender_id']
        
        updated_count = MessageService.mark_all_messages_as_read(
            user_id=identity['id'],
            **filters
        )
        
        return ok_response({
            'updated_count': updated_count
        }, message=f'已标记 {updated_count} 条消息为已读')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"批量标记消息已读失败: {str(e)}")
        raise ApiError('批量标记消息已读失败', code=ErrorCode.OPERATION_FAILED)

# 删除消息
@api.route('/messages/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    identity = get_jwt_identity()
    
    try:
        MessageService.delete_message(message_id, identity['id'])
        return ok_response(message='消息删除成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"删除消息失败: {str(e)}")
        raise ApiError('删除消息失败', code=ErrorCode.OPERATION_FAILED)

# ================== 消息统计相关路由 ==================

# 获取未读消息数量
@api.route('/messages/unread-count', methods=['GET'])
@jwt_required()
def get_unread_count():
    identity = get_jwt_identity()
    
    try:
        count = MessageService.get_unread_count(identity['id'])
        return ok_response({'unread_count': count})
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取未读消息数量失败: {str(e)}")
        raise ApiError('获取未读消息数量失败', code=ErrorCode.OPERATION_FAILED)

# 获取消息统计信息
@api.route('/messages/statistics', methods=['GET'])
@jwt_required()
def get_message_statistics():
    identity = get_jwt_identity()
    
    try:
        statistics = MessageService.get_message_statistics(identity['id'])
        return ok_response(statistics)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取消息统计失败: {str(e)}")
        raise ApiError('获取消息统计失败', code=ErrorCode.OPERATION_FAILED)

# ================== 系统消息相关路由 ==================

# 发送系统消息（仅管理员）
@api.route('/messages/system', methods=['POST'])
@jwt_required()
@role_required('admin')
def send_system_message():
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        required_fields = ['recipient_ids', 'title', 'content']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ApiError(f"缺少必填字段: {', '.join(missing_fields)}", code=ErrorCode.VALIDATION_ERROR)
        
        # 验证接收者列表
        if not isinstance(data['recipient_ids'], list) or not data['recipient_ids']:
            raise ApiError('接收者列表不能为空', code=ErrorCode.VALIDATION_ERROR)
        
        created_count = MessageService.create_bulk_message(
            type_='system',
            recipient_ids=data['recipient_ids'],
            title=data['title'],
            content=data['content'],
            sender_id=None  # 系统消息没有发送者
        )
        
        return ok_response({
            'created_count': created_count
        }, message=f'系统消息发送成功，共发送给 {created_count} 个用户')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"发送系统消息失败: {str(e)}")
        api.logger.error(traceback.format_exc())
        raise ApiError('发送系统消息失败', code=ErrorCode.OPERATION_FAILED)

# 获取所有用户列表（用于选择消息接收者）
@api.route('/messages/users', methods=['GET'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def get_users_for_messaging():
    try:
        from services.student_service import StudentService
        
        # 获取所有学生
        students = StudentService.get_all_students()
        
        # 获取所有教师
        from core.helpers import get_db
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, name FROM users WHERE role = ?', ('teacher',))
        teachers = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return ok_response({
            'students': students,
            'teachers': teachers
        })
    except Exception as e:
        api.logger.error(f"获取用户列表失败: {str(e)}")
        raise ApiError('获取用户列表失败', code=ErrorCode.OPERATION_FAILED) 