from flask import Blueprint, request, jsonify
from services.user_profile_service import UserProfileService
from core.auth import login_required
from core.responses import success_response, error_response

user_profile_bp = Blueprint('user_profile', __name__)

@user_profile_bp.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def get_user_profile(user_id):
    """获取用户画像"""
    try:
        profile = UserProfileService.get_user_profile(user_id)
        return success_response(profile, "获取用户画像成功")
    except Exception as e:
        return error_response(str(e), "获取用户画像失败")

@user_profile_bp.route('/profile/<int:user_id>/generate', methods=['POST'])
@login_required
def generate_user_profile(user_id):
    """生成用户画像"""
    try:
        profile = UserProfileService.generate_user_profile(user_id)
        return success_response(profile, "生成用户画像成功")
    except Exception as e:
        return error_response(str(e), "生成用户画像失败")

@user_profile_bp.route('/profile/<int:user_id>/update', methods=['PUT'])
@login_required
def update_user_profile(user_id):
    """更新用户画像"""
    try:
        profile = UserProfileService.update_user_profile(user_id)
        return success_response(profile, "更新用户画像成功")
    except Exception as e:
        return error_response(str(e), "更新用户画像失败")

@user_profile_bp.route('/profiles', methods=['GET'])
@login_required
def get_all_profiles():
    """获取所有用户画像"""
    try:
        profiles = UserProfileService.get_all_profiles()
        return success_response(profiles, "获取所有用户画像成功")
    except Exception as e:
        return error_response(str(e), "获取所有用户画像失败")

@user_profile_bp.route('/profile/<int:user_id>/analysis', methods=['GET'])
@login_required
def analyze_user_profile(user_id):
    """分析用户画像（不保存到数据库）"""
    try:
        analysis = UserProfileService.analyze_user_profile(user_id)
        return success_response(analysis, "分析用户画像成功")
    except Exception as e:
        return error_response(str(e), "分析用户画像失败") 