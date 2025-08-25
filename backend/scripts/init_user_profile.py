#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户画像功能初始化脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.user_profile_service import init_user_profile_table

def main():
    """初始化用户画像功能"""
    print("正在初始化用户画像功能...")
    
    try:
        # 初始化用户画像表
        init_user_profile_table()
        print("✓ 用户画像表初始化成功")
        
        print("用户画像功能初始化完成！")
        print("\n可用的API接口：")
        print("- GET /api/v1/profile/<user_id> - 获取用户画像")
        print("- POST /api/v1/profile/<user_id>/generate - 生成用户画像")
        print("- PUT /api/v1/profile/<user_id>/update - 更新用户画像")
        print("- GET /api/v1/profiles - 获取所有用户画像")
        print("- GET /api/v1/profile/<user_id>/analysis - 分析用户画像")
        
    except Exception as e:
        print(f"✗ 初始化失败: {str(e)}")

if __name__ == "__main__":
    main() 