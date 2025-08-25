#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证系统更新初始化脚本
"""

import sqlite3
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def init_auth_update():
    """初始化认证系统更新"""
    print("正在更新认证系统...")
    
    # 使用相对于项目根目录的数据库路径
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. 添加新字段到users表
        print("1. 更新users表结构...")
        
        # 检查并添加student_id字段
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'student_id' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN student_id TEXT')
            print("   ✓ 添加student_id字段")
        
        if 'teacher_id' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN teacher_id TEXT')
            print("   ✓ 添加teacher_id字段")
        
        if 'class_number' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN class_number INTEGER')
            print("   ✓ 添加class_number字段")
        
        # 2. 创建refresh_tokens表
        print("2. 创建refresh_tokens表...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS refresh_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        print("   ✓ 创建refresh_tokens表")
        
        # 为refresh_tokens表创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user_id ON refresh_tokens(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_refresh_tokens_expires_at ON refresh_tokens(expires_at)')
        print("   ✓ 创建refresh_tokens表索引")
        
        # 3. 创建索引以提高查询性能
        print("3. 创建用户表索引...")
        
        # 为学号创建唯一索引
        cursor.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS idx_student_id 
            ON users(student_id) 
            WHERE student_id IS NOT NULL
        ''')
        print("   ✓ 创建学号唯一索引")
        
        # 为教职工号创建唯一索引
        cursor.execute('''
            CREATE UNIQUE INDEX IF NOT EXISTS idx_teacher_id 
            ON users(teacher_id) 
            WHERE teacher_id IS NOT NULL
        ''')
        print("   ✓ 创建教职工号唯一索引")
        
        # 为姓名和角色创建复合索引
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_name_role 
            ON users(name, role)
        ''')
        print("   ✓ 创建姓名角色复合索引")
        
        # 为班级编号创建索引
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_class_number 
            ON users(class_number) 
            WHERE class_number IS NOT NULL
        ''')
        print("   ✓ 创建班级编号索引")
        
        # 4. 迁移现有数据（如果有的话）
        print("4. 检查现有数据...")
        
        # 检查是否有现有用户数据需要迁移
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        
        if user_count > 0:
            print(f"   发现 {user_count} 个现有用户，建议手动迁移数据")
            print("   注意：现有用户可能需要手动更新学号/教职工号字段")
        else:
            print("   ✓ 没有现有用户数据，无需迁移")
        
        conn.commit()
        print("\n✓ 认证系统更新完成！")
        
        print("\n新的注册格式：")
        print("学生注册：")
        print('  {"name": "张三", "id_number": "1001001", "password": "123456", "role": "student"}')
        print("教师注册：")
        print('  {"name": "李老师", "id_number": "2001001", "password": "123456", "role": "teacher"}')
        
        print("\n新的登录格式：")
        print("学生登录（支持姓名或学号）：")
        print('  {"name_or_id": "张三", "password": "123456", "role": "student"}')
        print('  {"name_or_id": "1001001", "password": "123456", "role": "student"}')
        print("教师登录（支持姓名或教职工号）：")
        print('  {"name_or_id": "李老师", "password": "123456", "role": "teacher"}')
        print('  {"name_or_id": "2001001", "password": "123456", "role": "teacher"}')
        
    except Exception as e:
        conn.rollback()
        print(f"✗ 更新失败: {str(e)}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    init_auth_update() 