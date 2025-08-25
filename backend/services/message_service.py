"""
消息中心服务模块

负责消息的发送、接收、管理和状态更新
"""
from datetime import datetime
import traceback

from core.helpers import get_db, db_fetch_one, db_fetch_all, db_execute
from core.errors import ApiError, ErrorCode
from models import Message

class MessageService:
    @staticmethod
    def get_messages_by_recipient(recipient_id, page=1, page_size=20, **filters):
        """
        获取用户接收的消息列表
        
        :param recipient_id: 接收者ID
        :param page: 页码
        :param page_size: 每页数量
        :param filters: 过滤条件
        :return: 消息列表及分页信息
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 构建查询
            sql = '''
                SELECT m.*, u.name as sender_name
                FROM messages m
                LEFT JOIN users u ON m.sender_id = u.id
                WHERE m.recipient_id = ?
            '''
            params = [recipient_id]
            
            # 应用过滤器
            if 'type' in filters and filters['type']:
                sql += ' AND m.type = ?'
                params.append(filters['type'])
            
            if 'read' in filters and filters['read'] is not None:
                sql += ' AND m.read = ?'
                params.append(1 if filters['read'] else 0)
            
            if 'sender_id' in filters and filters['sender_id']:
                sql += ' AND m.sender_id = ?'
                params.append(filters['sender_id'])
            
            # 排序
            sql += ' ORDER BY m.created_at DESC'
            
            # 计算总数
            count_sql = f"SELECT COUNT(*) as total FROM ({sql})"
            cursor.execute(count_sql, params)
            total = cursor.fetchone()['total']
            
            # 应用分页
            sql += ' LIMIT ? OFFSET ?'
            offset = (page - 1) * page_size
            params.extend([page_size, offset])
            
            # 执行查询
            cursor.execute(sql, params)
            messages = [dict(row) for row in cursor.fetchall()]
            
            return {
                'items': messages,
                'total': total,
                'page': page,
                'page_size': page_size,
                'pages': (total + page_size - 1) // page_size
            }
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取消息列表失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_messages_by_sender(sender_id, page=1, page_size=20, **filters):
        """
        获取用户发送的消息列表
        
        :param sender_id: 发送者ID
        :param page: 页码
        :param page_size: 每页数量
        :param filters: 过滤条件
        :return: 消息列表及分页信息
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 构建查询
            sql = '''
                SELECT m.*, u.name as recipient_name
                FROM messages m
                LEFT JOIN users u ON m.recipient_id = u.id
                WHERE m.sender_id = ?
            '''
            params = [sender_id]
            
            # 应用过滤器
            if 'type' in filters and filters['type']:
                sql += ' AND m.type = ?'
                params.append(filters['type'])
            
            if 'recipient_id' in filters and filters['recipient_id']:
                sql += ' AND m.recipient_id = ?'
                params.append(filters['recipient_id'])
            
            # 排序
            sql += ' ORDER BY m.created_at DESC'
            
            # 计算总数
            count_sql = f"SELECT COUNT(*) as total FROM ({sql})"
            cursor.execute(count_sql, params)
            total = cursor.fetchone()['total']
            
            # 应用分页
            sql += ' LIMIT ? OFFSET ?'
            offset = (page - 1) * page_size
            params.extend([page_size, offset])
            
            # 执行查询
            cursor.execute(sql, params)
            messages = [dict(row) for row in cursor.fetchall()]
            
            return {
                'items': messages,
                'total': total,
                'page': page,
                'page_size': page_size,
                'pages': (total + page_size - 1) // page_size
            }
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取发送消息列表失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_message_by_id(message_id, user_id):
        """
        获取消息详情
        
        :param message_id: 消息ID
        :param user_id: 用户ID（用于权限验证）
        :return: 消息详情
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 获取消息详情
            cursor.execute('''
                SELECT m.*, u.name as sender_name, r.name as recipient_name
                FROM messages m
                LEFT JOIN users u ON m.sender_id = u.id
                LEFT JOIN users r ON m.recipient_id = r.id
                WHERE m.id = ?
            ''', (message_id,))
            message = cursor.fetchone()
            
            if not message:
                raise ApiError('消息不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            message_dict = dict(message)
            
            # 验证权限（只有发送者或接收者可以查看消息）
            if message_dict['sender_id'] != user_id and message_dict['recipient_id'] != user_id:
                raise ApiError('无权查看此消息', code=ErrorCode.PERMISSION_DENIED)
            
            # 如果是接收者查看消息，标记为已读
            if message_dict['recipient_id'] == user_id and not message_dict['read']:
                Message.mark_as_read(message_id)
                message_dict['read'] = 1
            
            return message_dict
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取消息详情失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def create_message(type_, recipient_id, title, content, sender_id=None):
        """
        创建消息
        
        :param type_: 消息类型（announcement, private, system等）
        :param recipient_id: 接收者ID
        :param title: 消息标题
        :param content: 消息内容
        :param sender_id: 发送者ID（可选，系统消息可能没有发送者）
        :return: 新消息ID
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证接收者是否存在
            cursor.execute('SELECT id FROM users WHERE id = ?', (recipient_id,))
            if not cursor.fetchone():
                raise ApiError('接收者不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证发送者是否存在（如果有发送者）
            if sender_id:
                cursor.execute('SELECT id FROM users WHERE id = ?', (sender_id,))
                if not cursor.fetchone():
                    raise ApiError('发送者不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证消息内容
            if not title or not title.strip():
                raise ApiError('消息标题不能为空', code=ErrorCode.VALIDATION_ERROR)
            
            if not content or not content.strip():
                raise ApiError('消息内容不能为空', code=ErrorCode.VALIDATION_ERROR)
            
            # 创建消息
            message_id = Message.create(
                type_=type_,
                recipient_id=recipient_id,
                title=title.strip(),
                content=content.strip(),
                sender_id=sender_id
            )
            
            return message_id
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'创建消息失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def create_bulk_message(type_, recipient_ids, title, content, sender_id=None):
        """
        批量创建消息
        
        :param type_: 消息类型
        :param recipient_ids: 接收者ID列表
        :param title: 消息标题
        :param content: 消息内容
        :param sender_id: 发送者ID
        :return: 创建的消息数量
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证接收者列表
            if not recipient_ids:
                raise ApiError('接收者列表不能为空', code=ErrorCode.VALIDATION_ERROR)
            
            # 验证所有接收者是否存在
            placeholders = ','.join(['?' for _ in recipient_ids])
            cursor.execute(f'SELECT id FROM users WHERE id IN ({placeholders})', recipient_ids)
            existing_users = [row['id'] for row in cursor.fetchall()]
            
            if len(existing_users) != len(recipient_ids):
                missing_ids = set(recipient_ids) - set(existing_users)
                raise ApiError(f'以下用户不存在: {missing_ids}', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证消息内容
            if not title or not title.strip():
                raise ApiError('消息标题不能为空', code=ErrorCode.VALIDATION_ERROR)
            
            if not content or not content.strip():
                raise ApiError('消息内容不能为空', code=ErrorCode.VALIDATION_ERROR)
            
            # 批量创建消息
            created_count = 0
            for recipient_id in recipient_ids:
                Message.create(
                    type_=type_,
                    recipient_id=recipient_id,
                    title=title.strip(),
                    content=content.strip(),
                    sender_id=sender_id
                )
                created_count += 1
            
            return created_count
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'批量创建消息失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def mark_message_as_read(message_id, user_id):
        """
        标记消息为已读
        
        :param message_id: 消息ID
        :param user_id: 用户ID
        :return: 更新后的消息
        """
        try:
            # 验证消息是否存在且用户是接收者
            message = MessageService.get_message_by_id(message_id, user_id)
            if message['recipient_id'] != user_id:
                raise ApiError('只有消息接收者可以标记已读', code=ErrorCode.PERMISSION_DENIED)
            
            # 标记为已读
            updated_message = Message.mark_as_read(message_id)
            return updated_message
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'标记消息已读失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def mark_all_messages_as_read(user_id, **filters):
        """
        标记用户所有消息为已读
        
        :param user_id: 用户ID
        :param filters: 过滤条件
        :return: 更新的消息数量
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 构建更新查询
            sql = 'UPDATE messages SET read = 1 WHERE recipient_id = ?'
            params = [user_id]
            
            # 应用过滤器
            if 'type' in filters and filters['type']:
                sql += ' AND type = ?'
                params.append(filters['type'])
            
            if 'sender_id' in filters and filters['sender_id']:
                sql += ' AND sender_id = ?'
                params.append(filters['sender_id'])
            
            # 执行更新
            cursor.execute(sql, params)
            updated_count = cursor.rowcount
            
            conn.commit()
            return updated_count
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'批量标记消息已读失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def delete_message(message_id, user_id):
        """
        删除消息
        
        :param message_id: 消息ID
        :param user_id: 用户ID
        :return: 成功返回True
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证消息是否存在
            cursor.execute('SELECT * FROM messages WHERE id = ?', (message_id,))
            message = cursor.fetchone()
            
            if not message:
                raise ApiError('消息不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            message_dict = dict(message)
            
            # 验证权限（只有发送者或接收者可以删除消息）
            if message_dict['sender_id'] != user_id and message_dict['recipient_id'] != user_id:
                raise ApiError('无权删除此消息', code=ErrorCode.PERMISSION_DENIED)
            
            # 删除消息
            cursor.execute('DELETE FROM messages WHERE id = ?', (message_id,))
            conn.commit()
            
            return True
        except ApiError:
            conn.rollback()
            raise
        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            raise ApiError(f'删除消息失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_unread_count(user_id):
        """
        获取用户未读消息数量
        
        :param user_id: 用户ID
        :return: 未读消息数量
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT COUNT(*) as count FROM messages 
                WHERE recipient_id = ? AND read = 0
            ''', (user_id,))
            
            result = cursor.fetchone()
            return result['count'] if result else 0
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取未读消息数量失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_message_statistics(user_id):
        """
        获取用户消息统计信息
        
        :param user_id: 用户ID
        :return: 消息统计信息
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 总消息数
            cursor.execute('''
                SELECT COUNT(*) as total FROM messages 
                WHERE recipient_id = ?
            ''', (user_id,))
            total_received = cursor.fetchone()['total']
            
            # 未读消息数
            cursor.execute('''
                SELECT COUNT(*) as count FROM messages 
                WHERE recipient_id = ? AND read = 0
            ''', (user_id,))
            unread_count = cursor.fetchone()['count']
            
            # 按类型统计
            cursor.execute('''
                SELECT type, COUNT(*) as count FROM messages 
                WHERE recipient_id = ?
                GROUP BY type
            ''', (user_id,))
            type_statistics = [dict(row) for row in cursor.fetchall()]
            
            # 发送的消息数
            cursor.execute('''
                SELECT COUNT(*) as total FROM messages 
                WHERE sender_id = ?
            ''', (user_id,))
            total_sent = cursor.fetchone()['total']
            
            return {
                'total_received': total_received,
                'total_sent': total_sent,
                'unread_count': unread_count,
                'type_statistics': type_statistics
            }
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取消息统计失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close() 