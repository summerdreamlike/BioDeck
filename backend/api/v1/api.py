"""
API路由注册
"""
from flask import Blueprint

# 创建一个蓝图，注册所有API路由
api = Blueprint('api', __name__, url_prefix='/api/v1')

# 导入所有端点以注册路由
from .endpoints import (
    auth,
    students,
    study,
    materials,
    messages,
    user_profile,
    avatar,
    daily_checkin,
    cards
    # 以下模块尚未创建，暂时注释掉
    # categories,
    # tags
)

def register_routes(app):
    """注册所有API路由到Flask应用"""
    app.register_blueprint(api)
    return app 