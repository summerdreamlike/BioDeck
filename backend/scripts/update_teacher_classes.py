#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为现有教师用户添加班级信息的脚本
"""

import sqlite3
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def update_teacher_classes():
    """为现有教师用户添加班级信息"""
    
    # 数据库路径
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')
    
    if not os.path.exists(db_path):
        print(f"错误：数据库文件不存在: {db_path}")
        return False
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("正在连接数据库...")
        
        # 检查users表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            print("错误：users表不存在")
            return False
        
        # 检查users表结构
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"users表列: {columns}")
        
        # 如果class_number列不存在，添加它
        if 'class_number' not in columns:
            print("正在添加class_number列...")
            cursor.execute("ALTER TABLE users ADD COLUMN class_number INTEGER")
            print("✓ 已添加class_number列")
        
        # 获取所有教师用户
        cursor.execute("SELECT id, name, teacher_id FROM users WHERE role = 'teacher'")
        teachers = cursor.fetchall()
        
        if not teachers:
            print("没有找到教师用户")
            return True
        
        print(f"找到 {len(teachers)} 个教师用户:")
        
        # 为每个教师分配班级（这里简单按顺序分配1-5班）
        for i, (user_id, name, teacher_id) in enumerate(teachers):
            class_number = (i % 5) + 1  # 1-5班循环分配
            
            # 检查是否已有班级信息
            cursor.execute("SELECT class_number FROM users WHERE id = ?", (user_id,))
            current_class = cursor.fetchone()
            
            if current_class and current_class[0] is not None:
                print(f"  {name} (ID: {teacher_id}) - 已有班级: {current_class[0]}")
            else:
                # 更新班级信息
                cursor.execute(
                    "UPDATE users SET class_number = ? WHERE id = ?", 
                    (class_number, user_id)
                )
                print(f"  {name} (ID: {teacher_id}) - 分配班级: {class_number}")
        
        # 提交更改
        conn.commit()
        print("✓ 所有教师班级信息已更新")
        
        # 验证更新结果
        cursor.execute("SELECT name, teacher_id, class_number FROM users WHERE role = 'teacher'")
        updated_teachers = cursor.fetchall()
        
        print("\n更新后的教师信息:")
        for name, teacher_id, class_number in updated_teachers:
            print(f"  {name} (ID: {teacher_id}) - 班级: {class_number}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"错误：{e}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    print("=== 教师班级信息更新脚本 ===")
    
    success = update_teacher_classes()
    
    if success:
        print("\n✓ 脚本执行成功！")
    else:
        print("\n✗ 脚本执行失败！")
        sys.exit(1)
