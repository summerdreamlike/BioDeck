"""
反馈服务模块

负责反馈的收集、管理和统计分析
"""
import traceback
from datetime import datetime

from core.helpers import get_db, db_fetch_one, db_fetch_all, db_execute
from core.errors import ApiError, ErrorCode
from models import Feedback

class FeedbackService:
    @staticmethod
    def get_feedbacks(page=1, page_size=20):
        """
        获取反馈列表
        
        :param page: 页码
        :param page_size: 每页数量
        :return: 反馈列表及分页信息
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 获取总数
            cursor.execute('SELECT COUNT(*) as total FROM feedbacks')
            total = cursor.fetchone()['total']
            
            # 获取分页数据
            offset = (page - 1) * page_size
            cursor.execute('''
                SELECT f.*, s.name as student_name, s.student_id as student_number, s.class as student_class
                FROM feedbacks f
                JOIN students s ON f.student_id = s.id
                ORDER BY f.created_at DESC
                LIMIT ? OFFSET ?
            ''', (page_size, offset))
            
            feedbacks = [dict(row) for row in cursor.fetchall()]
            
            return {
                'items': feedbacks,
                'total': total,
                'page': page,
                'page_size': page_size,
                'pages': (total + page_size - 1) // page_size
            }
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取反馈列表失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_feedback_by_id(feedback_id):
        """
        获取反馈详情
        
        :param feedback_id: 反馈ID
        :return: 反馈详情
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT f.*, s.name as student_name, s.student_id as student_number, s.class as student_class
                FROM feedbacks f
                JOIN students s ON f.student_id = s.id
                WHERE f.id = ?
            ''', (feedback_id,))
            
            feedback = cursor.fetchone()
            if not feedback:
                raise ApiError('反馈不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            return dict(feedback)
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取反馈详情失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def create_feedback(student_id, content, satisfaction):
        """
        创建反馈
        
        :param student_id: 学生ID
        :param content: 反馈内容
        :param satisfaction: 满意度（1-5）
        :return: 新反馈ID
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证学生是否存在
            cursor.execute('SELECT id FROM students WHERE id = ?', (student_id,))
            if not cursor.fetchone():
                raise ApiError('学生不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证满意度值
            if not isinstance(satisfaction, int) or satisfaction < 1 or satisfaction > 5:
                raise ApiError('满意度必须是1-5之间的整数', code=ErrorCode.VALIDATION_ERROR)
            
            # 验证内容
            if not content or not content.strip():
                raise ApiError('反馈内容不能为空', code=ErrorCode.VALIDATION_ERROR)
            
            # 检查是否已有同一学生的最近反馈（可选限制，防止频繁提交）
            cursor.execute('''
                SELECT id FROM feedbacks
                WHERE student_id = ? AND created_at > datetime('now', '-1 day')
            ''', (student_id,))
            
            if cursor.fetchone():
                raise ApiError('您最近已经提交过反馈，请24小时后再试', code=ErrorCode.VALIDATION_ERROR)
            
            # 创建反馈
            feedback_id = Feedback.create(
                student_id=student_id,
                content=content.strip(),
                satisfaction=satisfaction
            )
            
            return feedback_id
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'创建反馈失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def update_feedback(feedback_id, content=None, satisfaction=None):
        """
        更新反馈
        
        :param feedback_id: 反馈ID
        :param content: 反馈内容（可选）
        :param satisfaction: 满意度（可选）
        :return: 更新后的反馈
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证反馈是否存在
            cursor.execute('SELECT * FROM feedbacks WHERE id = ?', (feedback_id,))
            feedback = cursor.fetchone()
            if not feedback:
                raise ApiError('反馈不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 验证满意度值（如果提供）
            if satisfaction is not None:
                if not isinstance(satisfaction, int) or satisfaction < 1 or satisfaction > 5:
                    raise ApiError('满意度必须是1-5之间的整数', code=ErrorCode.VALIDATION_ERROR)
            
            # 验证内容（如果提供）
            if content is not None and not content.strip():
                raise ApiError('反馈内容不能为空', code=ErrorCode.VALIDATION_ERROR)
            
            # 更新反馈
            Feedback.update(
                feedback_id=feedback_id,
                content=content.strip() if content is not None else None,
                satisfaction=satisfaction
            )
            
            return FeedbackService.get_feedback_by_id(feedback_id)
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'更新反馈失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def delete_feedback(feedback_id):
        """
        删除反馈
        
        :param feedback_id: 反馈ID
        :return: 成功返回True
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 验证反馈是否存在
            cursor.execute('SELECT id FROM feedbacks WHERE id = ?', (feedback_id,))
            if not cursor.fetchone():
                raise ApiError('反馈不存在', code=ErrorCode.RESOURCE_NOT_FOUND)
            
            # 删除反馈
            Feedback.delete(feedback_id)
            return True
        except ApiError:
            raise
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'删除反馈失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def get_statistics():
        """
        获取反馈统计信息
        
        :return: 统计信息
        """
        try:
            stats = Feedback.get_statistics()
            return stats
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取统计信息失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
    
    @staticmethod
    def get_student_feedback(student_id):
        """
        获取学生自己的反馈
        
        :param student_id: 学生ID
        :return: 学生的反馈列表
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM feedbacks
                WHERE student_id = ?
                ORDER BY created_at DESC
            ''', (student_id,))
            
            feedbacks = [dict(row) for row in cursor.fetchall()]
            return feedbacks
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'获取学生反馈失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()
    
    @staticmethod
    def analyze_keywords(limit=10):
        """
        分析反馈内容中的关键词
        
        :param limit: 返回的关键词数量
        :return: 关键词列表及出现频率
        """
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # 获取所有反馈内容
            cursor.execute('SELECT content FROM feedbacks WHERE content IS NOT NULL')
            feedbacks = [row['content'] for row in cursor.fetchall()]
            
            # 简单的关键词分析（实际项目中可能需要更复杂的自然语言处理）
            # 这里我们只是做一个简单的词频统计
            # 首先拼接所有反馈内容
            all_content = ' '.join(feedbacks)
            
            # 去除标点符号（简化版本）
            for char in ',.?!;:()[]{}""\'':
                all_content = all_content.replace(char, ' ')
            
            # 分词并统计频率
            words = all_content.lower().split()
            word_count = {}
            
            # 停用词列表（常见但无意义的词）
            stop_words = {'的', '是', '在', '我', '了', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '那', '这个', '那个'}
            
            for word in words:
                if len(word) > 1 and word not in stop_words:
                    word_count[word] = word_count.get(word, 0) + 1
            
            # 按频率排序并限制数量
            keywords = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:limit]
            
            # 格式化结果
            result = [{'word': word, 'count': count} for word, count in keywords]
            
            return result
        except Exception as e:
            traceback.print_exc()
            raise ApiError(f'分析关键词失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close() 