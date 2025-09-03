#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复卡牌图片URL路径脚本
"""

import sqlite3
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def fix_image_urls():
    """修复数据库中的图片URL路径"""
    print("正在修复卡牌图片URL路径...")
    
    # 使用相对于项目根目录的数据库路径
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='card_definitions'")
        if not cursor.fetchone():
            print("❌ 卡牌定义表不存在，请先运行初始化脚本")
            return
        
        # 更新所有图片URL，去掉开头的/
        print("1. 更新图片URL路径...")
        cursor.execute('''
            UPDATE card_definitions 
            SET image_url = REPLACE(image_url, '/assets/', 'assets/')
            WHERE image_url LIKE '/assets/%'
        ''')
        
        updated_count = cursor.rowcount
        print(f"   ✓ 更新了 {updated_count} 张卡牌的图片路径")
        
        # 显示更新后的图片路径示例
        cursor.execute('SELECT card_id, name, image_url FROM card_definitions LIMIT 5')
        examples = cursor.fetchall()
        
        print("\n2. 更新后的图片路径示例:")
        for card_id, name, image_url in examples:
            print(f"   - {card_id} ({name}): {image_url}")
        
        conn.commit()
        print("\n✅ 图片URL路径修复完成！")
        
    except Exception as e:
        print(f"❌ 修复失败: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    fix_image_urls() 