#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
头像功能初始化脚本
"""

import sqlite3
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def init_avatar_feature():
    """初始化头像功能"""
    print("正在初始化头像功能...")
    
    # 使用相对于项目根目录的数据库路径
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. 检查并添加avatar_url字段到users表
        print("1. 更新users表结构...")
        
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'avatar_url' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN avatar_url TEXT')
            print("   ✓ 添加avatar_url字段")
        else:
            print("   ✓ avatar_url字段已存在")
        
        # 2. 创建头像存储目录
        print("2. 创建头像存储目录...")
        avatar_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'uploads', 'avatars')
        os.makedirs(avatar_dir, exist_ok=True)
        print(f"   ✓ 创建目录: {avatar_dir}")
        
        # 3. 创建头像文件信息表（可选，用于管理头像文件）
        print("3. 创建头像文件信息表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS avatar_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                mime_type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        print("   ✓ 创建avatar_files表")
        
        # 4. 为avatar_files表创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_avatar_files_user_id ON avatar_files(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_avatar_files_created_at ON avatar_files(created_at)')
        print("   ✓ 创建avatar_files表索引")
        
        conn.commit()
        print("✓ 头像功能初始化完成！")
        
        print("\n可用的API接口：")
        print("- POST /api/v1/users/avatar - 上传头像")
        print("- GET /api/v1/users/avatar/{user_id} - 获取用户头像")
        print("- DELETE /api/v1/users/avatar - 删除头像")
        print("- PUT /api/v1/users/avatar - 更新头像")
        
    except Exception as e:
        conn.rollback()
        print(f"✗ 初始化失败: {str(e)}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    init_avatar_feature()
