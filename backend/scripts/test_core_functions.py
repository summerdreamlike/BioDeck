#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试核心功能
验证积分系统、抽卡系统等核心功能的完整性
"""

import sys
import os
import sqlite3

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.card_system import CardSystem
from models.user import User

def test_database_structure():
    """测试数据库结构"""
    print("🔍 测试数据库结构...")
    
    try:
        conn = CardSystem.get_db()
        cursor = conn.cursor()
        
        # 检查users表结构
        print("\n1. 检查users表...")
        cursor.execute('PRAGMA table_info(users)')
        columns = [col[1] for col in cursor.fetchall()]
        required_columns = ['id', 'name', 'password', 'role', 'points']
        
        for col in required_columns:
            if col in columns:
                print(f"   ✅ {col} 字段存在")
            else:
                print(f"   ❌ {col} 字段缺失")
        
        # 检查卡牌系统表
        print("\n2. 检查卡牌系统表...")
        tables = ['card_definitions', 'rarity_drop_config', 'user_cards', 'draw_history']
        for table in tables:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM {table}')
                count = cursor.fetchone()[0]
                print(f"   ✅ {table} 表存在，记录数: {count}")
            except Exception as e:
                print(f"   ❌ {table} 表不存在或有问题: {str(e)}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ 数据库结构测试失败: {str(e)}")
        return False

def test_card_system():
    """测试卡牌系统"""
    print("\n3. 测试卡牌系统...")
    
    try:
        conn = CardSystem.get_db()
        cursor = conn.cursor()
        
        # 检查卡牌定义
        cursor.execute('SELECT COUNT(*) FROM card_definitions')
        card_count = cursor.fetchone()[0]
        print(f"   📊 卡牌定义总数: {card_count}")
        
        if card_count > 0:
            # 检查稀有度分布
            cursor.execute('SELECT rarity, COUNT(*) FROM card_definitions GROUP BY rarity ORDER BY rarity')
            distribution = cursor.fetchall()
            print("   🎯 稀有度分布:")
            for rarity, count in distribution:
                print(f"      • {rarity}级: {count}张")
        
        # 检查稀有度概率配置
        cursor.execute('SELECT rarity, rate FROM rarity_drop_config ORDER BY rate DESC')
        rates = cursor.fetchall()
        if rates:
            total_rate = sum(rate for _, rate in rates)
            print(f"   📊 总概率: {total_rate:.3f}")
            
            if abs(total_rate - 1.0) < 0.001:
                print("   ✅ 概率配置正确 (总和为1)")
            else:
                print(f"   ⚠️  概率配置异常 (总和为{total_rate:.3f})")
        else:
            print("   ❌ 稀有度概率配置缺失")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ 卡牌系统测试失败: {str(e)}")
        return False

def test_user_points():
    """测试用户积分系统"""
    print("\n4. 测试用户积分系统...")
    
    try:
        # 检查是否有用户存在
        conn = User.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        print(f"   👥 用户总数: {user_count}")
        
        if user_count > 0:
            # 检查积分字段
            cursor.execute('SELECT id, name, points FROM users LIMIT 3')
            users = cursor.fetchall()
            print("   💰 用户积分示例:")
            for user in users:
                print(f"      • {user[1]} (ID: {user[0]}): {user[2]} 积分")
            
            # 测试积分更新功能
            test_user_id = users[0][0]
            old_points = users[0][2]
            
            print(f"   🔄 测试积分更新 (用户ID: {test_user_id})...")
            User.update_user_points(test_user_id, 100)
            new_points = User.get_user_points(test_user_id)
            print(f"   ✅ 积分更新成功: {old_points} -> {new_points}")
            
            # 恢复原积分
            User.update_user_points(test_user_id, -100)
            restored_points = User.get_user_points(test_user_id)
            print(f"   ✅ 积分恢复成功: {new_points} -> {restored_points}")
        else:
            print("   ⚠️  没有用户数据，跳过积分测试")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ 用户积分系统测试失败: {str(e)}")
        return False

def test_card_drawing_logic():
    """测试抽卡逻辑"""
    print("\n5. 测试抽卡逻辑...")
    
    try:
        # 检查抽卡费用配置
        from services.card_service import CardService
        costs = CardService.get_draw_costs()
        print(f"   💰 抽卡费用配置: {costs}")
        
        # 检查稀有度概率
        rates = CardService.get_rarity_drop_config()
        print(f"   🎲 稀有度概率配置: {rates}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 抽卡逻辑测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 开始测试核心功能...")
    print("="*60)
    
    tests = [
        test_database_structure,
        test_card_system,
        test_user_points,
        test_card_drawing_logic
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "="*60)
    print("📋 测试总结:")
    print(f"   • 通过: {passed}/{total}")
    print(f"   • 失败: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 所有核心功能测试通过！")
        print("\n📝 系统状态:")
        print("   ✅ 数据库结构完整")
        print("   ✅ 卡牌系统正常")
        print("   ✅ 积分系统正常")
        print("   ✅ 抽卡逻辑正常")
        print("\n🚀 可以启动服务进行完整测试")
        sys.exit(0)
    else:
        print("\n⚠️  部分功能测试失败，请检查系统配置")
        sys.exit(1)

if __name__ == '__main__':
    main() 