"""
试卷相关路由
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..api import api
from core.errors import ApiError, ErrorCode
from core.responses import ok_response
from core.auth import role_required, roles_required
from services.paper_service import PaperService

# 获取试卷列表
@api.route('/papers', methods=['GET'])
@jwt_required()
def get_papers():
    """获取试卷列表"""
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        
        # 构建过滤条件
        filters = {}
        if request.args.get('creator_id'):
            filters['creator_id'] = int(request.args.get('creator_id'))
        
        if request.args.get('name'):
            filters['name'] = request.args.get('name')
        
        # 获取试卷列表
        result = PaperService.get_papers(page, page_size, **filters)
        return ok_response(result)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取试卷列表失败: {str(e)}")
        raise ApiError('获取试卷列表失败', code=ErrorCode.OPERATION_FAILED)

# 获取试卷详情
@api.route('/papers/<int:paper_id>', methods=['GET'])
@jwt_required()
def get_paper(paper_id):
    """获取试卷详情"""
    try:
        # 获取是否包含题目详情参数
        include_questions = request.args.get('include_questions', 'true').lower() in ['true', '1', 'yes']
        
        # 获取试卷详情
        paper = PaperService.get_paper_by_id(paper_id, include_questions)
        return ok_response(paper)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"获取试卷详情失败: {str(e)}")
        raise ApiError('获取试卷详情失败', code=ErrorCode.OPERATION_FAILED)

# 创建试卷
@api.route('/papers', methods=['POST'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def create_paper():
    """创建试卷"""
    identity = get_jwt_identity()
    data = request.get_json() or {}
    
    try:
        # 验证必填字段
        if 'name' not in data:
            raise ApiError('缺少试卷名称', code=ErrorCode.VALIDATION_ERROR)
        
        # 创建试卷
        paper_id = PaperService.create_paper(
            creator_id=identity['id'],
            name=data['name'],
            description=data.get('description')
        )
        
        # 如果提供了题目，添加题目
        if 'questions' in data and isinstance(data['questions'], list) and data['questions']:
            PaperService.add_questions_to_paper(paper_id, data['questions'])
        
        # 返回新创建的试卷
        paper = PaperService.get_paper_by_id(paper_id)
        return ok_response(paper, message='试卷创建成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"创建试卷失败: {str(e)}")
        raise ApiError('创建试卷失败', code=ErrorCode.OPERATION_FAILED)

# 更新试卷
@api.route('/papers/<int:paper_id>', methods=['PUT'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def update_paper(paper_id):
    """更新试卷"""
    data = request.get_json() or {}
    
    try:
        # 验证权限（只允许创建者或管理员更新）
        identity = get_jwt_identity()
        if identity['role'] != 'admin':
            paper = PaperService.get_paper_by_id(paper_id, include_questions=False)
            if paper['creator_id'] != identity['id']:
                raise ApiError('无权限更新此试卷', code=ErrorCode.FORBIDDEN)
        
        # 更新试卷
        PaperService.update_paper(paper_id, data)
        
        # 返回更新后的试卷
        paper = PaperService.get_paper_by_id(paper_id)
        return ok_response(paper, message='试卷更新成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"更新试卷失败: {str(e)}")
        raise ApiError('更新试卷失败', code=ErrorCode.OPERATION_FAILED)

# 删除试卷
@api.route('/papers/<int:paper_id>', methods=['DELETE'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def delete_paper(paper_id):
    """删除试卷"""
    try:
        # 验证权限（只允许创建者或管理员删除）
        identity = get_jwt_identity()
        if identity['role'] != 'admin':
            paper = PaperService.get_paper_by_id(paper_id, include_questions=False)
            if paper['creator_id'] != identity['id']:
                raise ApiError('无权限删除此试卷', code=ErrorCode.FORBIDDEN)
        
        # 删除试卷
        PaperService.delete_paper(paper_id)
        return ok_response({'success': True}, message='试卷删除成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"删除试卷失败: {str(e)}")
        raise ApiError('删除试卷失败', code=ErrorCode.OPERATION_FAILED)

# 向试卷添加题目
@api.route('/papers/<int:paper_id>/questions', methods=['POST'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def add_questions_to_paper(paper_id):
    """向试卷添加题目"""
    data = request.get_json() or {}
    
    try:
        # 验证权限（只允许创建者或管理员添加题目）
        identity = get_jwt_identity()
        if identity['role'] != 'admin':
            paper = PaperService.get_paper_by_id(paper_id, include_questions=False)
            if paper['creator_id'] != identity['id']:
                raise ApiError('无权限修改此试卷', code=ErrorCode.FORBIDDEN)
        
        # 验证题目数据
        if 'questions' not in data or not isinstance(data['questions'], list):
            raise ApiError('缺少有效的题目数据', code=ErrorCode.VALIDATION_ERROR)
        
        # 验证每个题目都有id和score
        for question in data['questions']:
            if 'id' not in question or 'score' not in question:
                raise ApiError('题目数据必须包含id和score', code=ErrorCode.VALIDATION_ERROR)
        
        # 添加题目
        PaperService.add_questions_to_paper(paper_id, data['questions'])
        
        # 返回更新后的试卷
        paper = PaperService.get_paper_by_id(paper_id)
        return ok_response(paper, message='题目添加成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"添加题目失败: {str(e)}")
        raise ApiError('添加题目失败', code=ErrorCode.OPERATION_FAILED)

# 从试卷中移除题目
@api.route('/papers/<int:paper_id>/questions/<int:question_id>', methods=['DELETE'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def remove_question_from_paper(paper_id, question_id):
    """从试卷中移除题目"""
    try:
        # 验证权限（只允许创建者或管理员移除题目）
        identity = get_jwt_identity()
        if identity['role'] != 'admin':
            paper = PaperService.get_paper_by_id(paper_id, include_questions=False)
            if paper['creator_id'] != identity['id']:
                raise ApiError('无权限修改此试卷', code=ErrorCode.FORBIDDEN)
        
        # 移除题目
        PaperService.remove_question_from_paper(paper_id, question_id)
        
        # 返回更新后的试卷
        paper = PaperService.get_paper_by_id(paper_id)
        return ok_response(paper, message='题目移除成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"移除题目失败: {str(e)}")
        raise ApiError('移除题目失败', code=ErrorCode.OPERATION_FAILED)

# 重新排序题目
@api.route('/papers/<int:paper_id>/reorder', methods=['PUT'])
@jwt_required()
@roles_required(['admin', 'teacher'])
def reorder_questions(paper_id):
    """重新排序试卷题目"""
    data = request.get_json() or {}
    
    try:
        # 验证权限（只允许创建者或管理员重排题目）
        identity = get_jwt_identity()
        if identity['role'] != 'admin':
            paper = PaperService.get_paper_by_id(paper_id, include_questions=False)
            if paper['creator_id'] != identity['id']:
                raise ApiError('无权限修改此试卷', code=ErrorCode.FORBIDDEN)
        
        # 验证题目排序数据
        if 'question_orders' not in data or not isinstance(data['question_orders'], list):
            raise ApiError('缺少有效的题目排序数据', code=ErrorCode.VALIDATION_ERROR)
        
        # 验证每个排序项都有question_id和order
        for item in data['question_orders']:
            if 'question_id' not in item or 'order' not in item:
                raise ApiError('排序数据必须包含question_id和order', code=ErrorCode.VALIDATION_ERROR)
        
        # 重排题目
        PaperService.reorder_questions(paper_id, data['question_orders'])
        
        # 返回更新后的试卷
        paper = PaperService.get_paper_by_id(paper_id)
        return ok_response(paper, message='题目重排成功')
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"重排题目失败: {str(e)}")
        raise ApiError('重排题目失败', code=ErrorCode.OPERATION_FAILED)

# 生成随机试卷
@api.route('/papers/random', methods=['GET'])
@jwt_required()
def get_random_paper():
    """生成随机试卷"""
    try:
        # 获取查询参数
        knowledge_points = request.args.getlist('knowledge_point')
        difficulty_min = request.args.get('difficulty_min')
        difficulty_max = request.args.get('difficulty_max')
        question_count = int(request.args.get('question_count', 10))
        
        # 转换参数类型
        if difficulty_min:
            difficulty_min = int(difficulty_min)
        if difficulty_max:
            difficulty_max = int(difficulty_max)
        
        # 生成随机试卷
        paper = PaperService.get_random_paper(
            knowledge_points=knowledge_points,
            difficulty_min=difficulty_min,
            difficulty_max=difficulty_max,
            question_count=question_count
        )
        
        return ok_response(paper)
    except ApiError:
        raise
    except Exception as e:
        api.logger.error(f"生成随机试卷失败: {str(e)}")
        raise ApiError('生成随机试卷失败', code=ErrorCode.OPERATION_FAILED) 