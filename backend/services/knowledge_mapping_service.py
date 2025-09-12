from typing import Dict, List
from models.card_system import CardSystem
from core.errors import ApiError, ErrorCode


class KnowledgeMappingService:
    """知识点映射服务层：维护 关卡<->知识点 与 知识点<->卡牌 的映射"""

    @staticmethod
    def ensure_tables():
        CardSystem.ensure_tables()

    # ========== 关卡 <-> 知识点 ==========
    @staticmethod
    def list_knowledge_by_level(level_name: str) -> List[Dict]:
        if not level_name:
            raise ApiError('level_name 不能为空', code=ErrorCode.VALIDATION_ERROR)
        KnowledgeMappingService.ensure_tables()
        conn = CardSystem.get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                'SELECT knowledge_point, level_name, created_at FROM knowledge_level_mapping WHERE level_name = ? ORDER BY knowledge_point',
                (level_name,)
            )
            rows = [dict(row) for row in cur.fetchall()]
            return rows
        finally:
            conn.close()

    @staticmethod
    def upsert_level_mapping(level_name: str, knowledge_point: str) -> Dict:
        if not level_name or not knowledge_point:
            raise ApiError('level_name 与 knowledge_point 不能为空', code=ErrorCode.VALIDATION_ERROR)
        KnowledgeMappingService.ensure_tables()
        conn = CardSystem.get_db()
        cur = conn.cursor()
        try:
            # 去重：若存在则忽略插入
            cur.execute(
                'SELECT id FROM knowledge_level_mapping WHERE level_name = ? AND knowledge_point = ? LIMIT 1',
                (level_name, knowledge_point)
            )
            row = cur.fetchone()
            if not row:
                cur.execute(
                    'INSERT INTO knowledge_level_mapping (knowledge_point, level_name) VALUES (?, ?)',
                    (knowledge_point, level_name)
                )
                conn.commit()
            return {'level_name': level_name, 'knowledge_point': knowledge_point}
        except Exception as e:
            conn.rollback()
            raise ApiError(f'保存关卡映射失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()

    @staticmethod
    def delete_level_mapping(level_name: str, knowledge_point: str) -> Dict:
        if not level_name or not knowledge_point:
            raise ApiError('level_name 与 knowledge_point 不能为空', code=ErrorCode.VALIDATION_ERROR)
        KnowledgeMappingService.ensure_tables()
        conn = CardSystem.get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                'DELETE FROM knowledge_level_mapping WHERE level_name = ? AND knowledge_point = ?',
                (level_name, knowledge_point)
            )
            conn.commit()
            return {'deleted': True}
        except Exception as e:
            conn.rollback()
            raise ApiError(f'删除关卡映射失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()

    # ========== 知识点 <-> 卡牌 ==========
    @staticmethod
    def list_cards_by_knowledge(knowledge_point: str) -> List[Dict]:
        if not knowledge_point:
            raise ApiError('knowledge_point 不能为空', code=ErrorCode.VALIDATION_ERROR)
        KnowledgeMappingService.ensure_tables()
        conn = CardSystem.get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                'SELECT knowledge_point, card_id, relevance, created_at FROM knowledge_card_mapping WHERE knowledge_point = ? ORDER BY card_id',
                (knowledge_point,)
            )
            rows = [dict(row) for row in cur.fetchall()]
            return rows
        finally:
            conn.close()

    @staticmethod
    def upsert_card_mapping(knowledge_point: str, card_id: str, relevance: float = 1.0) -> Dict:
        if not knowledge_point or not card_id:
            raise ApiError('knowledge_point 与 card_id 不能为空', code=ErrorCode.VALIDATION_ERROR)
        try:
            relevance = float(relevance)
            if relevance <= 0:
                raise ValueError('relevance 必须为正数')
        except Exception:
            raise ApiError('relevance 参数无效', code=ErrorCode.VALIDATION_ERROR)
        KnowledgeMappingService.ensure_tables()
        conn = CardSystem.get_db()
        cur = conn.cursor()
        try:
            # 若存在则更新相关性，否则插入
            cur.execute(
                'SELECT id FROM knowledge_card_mapping WHERE knowledge_point = ? AND card_id = ? LIMIT 1',
                (knowledge_point, card_id)
            )
            row = cur.fetchone()
            if row:
                cur.execute(
                    'UPDATE knowledge_card_mapping SET relevance = ? WHERE id = ?',
                    (relevance, row['id'])
                )
            else:
                cur.execute(
                    'INSERT INTO knowledge_card_mapping (knowledge_point, card_id, relevance) VALUES (?, ?, ?)',
                    (knowledge_point, card_id, relevance)
                )
            conn.commit()
            return {'knowledge_point': knowledge_point, 'card_id': card_id, 'relevance': relevance}
        except Exception as e:
            conn.rollback()
            raise ApiError(f'保存卡牌映射失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close()

    @staticmethod
    def delete_card_mapping(knowledge_point: str, card_id: str) -> Dict:
        if not knowledge_point or not card_id:
            raise ApiError('knowledge_point 与 card_id 不能为空', code=ErrorCode.VALIDATION_ERROR)
        KnowledgeMappingService.ensure_tables()
        conn = CardSystem.get_db()
        cur = conn.cursor()
        try:
            cur.execute(
                'DELETE FROM knowledge_card_mapping WHERE knowledge_point = ? AND card_id = ?',
                (knowledge_point, card_id)
            )
            conn.commit()
            return {'deleted': True}
        except Exception as e:
            conn.rollback()
            raise ApiError(f'删除卡牌映射失败: {str(e)}', code=ErrorCode.OPERATION_FAILED)
        finally:
            conn.close() 