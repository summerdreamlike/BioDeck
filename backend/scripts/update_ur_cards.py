#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新UR卡数据脚本
"""

import sqlite3
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def update_ur_cards():
    """更新UR卡数据"""
    print("正在更新UR卡数据...")
    
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
        
        # 删除旧的UR卡
        print("1. 删除旧的UR卡...")
        cursor.execute("DELETE FROM card_definitions WHERE rarity = 'UR'")
        deleted_count = cursor.rowcount
        print(f"   ✓ 删除了 {deleted_count} 张旧UR卡")
        
        # 插入新的UR卡
        print("2. 插入新的UR卡...")
        new_ur_cards = [
            ('UR001', '物质循环', '生物圈中物质在生物与非生物环境之间的循环过程，维持生态系统的物质平衡', 'UR', 'assets/img/Decks/UR卡/物质循环.png', 2500, 0.05),
            ('UR002', '生物多样性', '地球上所有生物种类、基因和生态系统的丰富程度，是生命进化的宝贵财富', 'UR', 'assets/img/Decks/UR卡/生物多样性.png', 2500, 0.05),
            ('UR003', '能量流动', '生态系统中能量从生产者到消费者的单向流动过程，驱动整个生命系统的运转', 'UR', 'assets/img/Decks/UR卡/能量流动.png', 2500, 0.05),
            ('UR004', '自然选择', '达尔文进化论的核心机制，适者生存，不适者被淘汰的自然过程', 'UR', 'assets/img/Decks/UR卡/自然选择.png', 2500, 0.05),
            ('UR005', '减数分裂', '生殖细胞形成过程中的特殊细胞分裂方式，产生单倍体配子', 'UR', 'assets/img/Decks/UR卡/减数分裂.png', 2500, 0.05),
        ]
        
        cursor.executemany('''
            INSERT INTO card_definitions (card_id, name, description, rarity, image_url, points_cost, drop_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', new_ur_cards)
        
        print(f"   ✓ 插入了 {len(new_ur_cards)} 张新UR卡")
        
        # 显示更新后的UR卡信息
        cursor.execute('SELECT card_id, name, image_url FROM card_definitions WHERE rarity = "UR" ORDER BY card_id')
        ur_cards = cursor.fetchall()
        
        print("\n3. 更新后的UR卡列表:")
        for card_id, name, image_url in ur_cards:
            print(f"   - {card_id}: {name} ({image_url})")
        
        # 更新稀有度概率配置
        print("\n4. 更新稀有度概率配置...")
        cursor.execute('UPDATE rarity_drop_config SET rate = 0.05 WHERE rarity = "UR"')
        print("   ✓ UR级概率保持5%")
        
        conn.commit()
        print("\n✅ UR卡数据更新完成！")
        
        # 显示统计信息
        cursor.execute('SELECT COUNT(*) FROM card_definitions WHERE rarity = "UR"')
        ur_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM card_definitions')
        total_count = cursor.fetchone()[0]
        
        print(f"\n📊 更新统计:")
        print(f"   - UR级卡牌: {ur_count}张")
        print(f"   - 总卡牌数: {total_count}张")
        
    except Exception as e:
        print(f"❌ 更新失败: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    update_ur_cards() 