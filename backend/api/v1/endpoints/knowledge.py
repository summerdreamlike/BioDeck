"""
知识点映射管理路由
"""
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.responses import success_response, error_response
from core.errors import ApiError
from services.knowledge_mapping_service import KnowledgeMappingService

from ..api import api

# ========== 关卡 <-> 知识点 ==========
@api.route('/knowledge/levels/<string:level_name>', methods=['GET'])
@jwt_required()
def list_knowledge_for_level(level_name):
    try:
        data = KnowledgeMappingService.list_knowledge_by_level(level_name)
        return success_response(data=data)
    except ApiError as e:
        return error_response(str(e), e.code)
    except Exception as e:
        return error_response(str(e))

@api.route('/knowledge/levels', methods=['POST'])
@jwt_required()
def add_level_mapping():
    try:
        payload = request.get_json() or {}
        level_name = payload.get('level_name')
        knowledge_point = payload.get('knowledge_point')
        data = KnowledgeMappingService.upsert_level_mapping(level_name, knowledge_point)
        return success_response(data=data, message='关卡-知识点映射已保存')
    except ApiError as e:
        return error_response(str(e), e.code)
    except Exception as e:
        return error_response(str(e))

@api.route('/knowledge/levels', methods=['DELETE'])
@jwt_required()
def delete_level_mapping():
    try:
        payload = request.get_json() or {}
        level_name = payload.get('level_name')
        knowledge_point = payload.get('knowledge_point')
        data = KnowledgeMappingService.delete_level_mapping(level_name, knowledge_point)
        return success_response(data=data, message='关卡-知识点映射已删除')
    except ApiError as e:
        return error_response(str(e), e.code)
    except Exception as e:
        return error_response(str(e))

# ========== 知识点 <-> 卡牌 ==========
@api.route('/knowledge/cards/<string:knowledge_point>', methods=['GET'])
@jwt_required()
def list_cards_for_knowledge(knowledge_point):
    try:
        data = KnowledgeMappingService.list_cards_by_knowledge(knowledge_point)
        return success_response(data=data)
    except ApiError as e:
        return error_response(str(e), e.code)
    except Exception as e:
        return error_response(str(e))

@api.route('/knowledge/cards', methods=['POST'])
@jwt_required()
def add_card_mapping():
    try:
        payload = request.get_json() or {}
        knowledge_point = payload.get('knowledge_point')
        card_id = payload.get('card_id')
        relevance = payload.get('relevance', 1.0)
        data = KnowledgeMappingService.upsert_card_mapping(knowledge_point, card_id, relevance)
        return success_response(data=data, message='知识点-卡牌映射已保存')
    except ApiError as e:
        return error_response(str(e), e.code)
    except Exception as e:
        return error_response(str(e))

@api.route('/knowledge/cards', methods=['DELETE'])
@jwt_required()
def delete_card_mapping():
    try:
        payload = request.get_json() or {}
        knowledge_point = payload.get('knowledge_point')
        card_id = payload.get('card_id')
        data = KnowledgeMappingService.delete_card_mapping(knowledge_point, card_id)
        return success_response(data=data, message='知识点-卡牌映射已删除')
    except ApiError as e:
        return error_response(str(e), e.code)
    except Exception as e:
        return error_response(str(e)) 