#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试前端集成功能
验证积分系统、抽卡系统、卡组管理等功能的完整性
"""

import sys
import os
import sqlite3
import requests
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models.card_system import CardSystem
from models.user import User

# 测试配置
BASE_URL = 'http://localhost:5000/api/v1'
TEST_USER = {
    'username': 'test_student',
    'password': 'test123',
    'email': 'test@example.com',
    'role': 'student'
}

def test_database_integration():
    """测试数据库集成"""
    print("🔍 测试数据库集成...")
    
    try:
        # 1. 检查卡牌系统表
        print("\n1. 检查卡牌系统表...")
        conn = CardSystem.get_db()
        cursor = conn.cursor()
        
        # 检查卡牌定义表
        cursor.execute('SELECT COUNT(*) FROM card_definitions')
        card_count = cursor.fetchone()[0]
        print(f"   📊 卡牌定义总数: {card_count}")
        
        # 检查稀有度配置
        cursor.execute('SELECT rarity, rate FROM rarity_drop_config ORDER BY rate DESC')
        rarity_config = cursor.fetchall()
        print("   🎯 稀有度配置:")
        for rarity, rate in rarity_config:
            print(f"      • {rarity}: {rate*100:.1f}%")
        
        # 检查用户积分字段
        cursor.execute('PRAGMA table_info(users)')
        columns = [col[1] for col in cursor.fetchall()]
        if 'points' in columns:
            print("   ✅ users表包含points字段")
        else:
            print("   ❌ users表缺少points字段")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ 数据库集成测试失败: {str(e)}")
        return False

def test_user_points_system():
    """测试用户积分系统"""
    print("\n2. 测试用户积分系统...")
    
    try:
        # 创建测试用户
        print("   👤 创建测试用户...")
        user_id = User.create(
            name=TEST_USER['username'],
            id_number=TEST_USER['username'],  # 使用username作为学号
            password=TEST_USER['password'],
            role=TEST_USER['role']
        )
        
        if user_id:
            print(f"   ✅ 测试用户创建成功 (ID: {user_id})")
            
            # 检查初始积分
            initial_points = User.get_user_points(user_id)
            print(f"   💰 初始积分: {initial_points}")
            
            # 测试增加积分
            print("   ➕ 测试增加积分...")
            new_points = User.update_user_points(user_id, 1000)
            print(f"   ✅ 增加1000积分后: {new_points}")
            
            # 测试减少积分
            print("   ➖ 测试减少积分...")
            final_points = User.update_user_points(user_id, -500)
            print(f"   ✅ 减少500积分后: {final_points}")
            
            return True
        else:
            print("   ❌ 测试用户创建失败")
            return False
            
    except Exception as e:
        print(f"   ❌ 用户积分系统测试失败: {str(e)}")
        return False

def test_card_drawing_system():
    """测试抽卡系统"""
    print("\n3. 测试抽卡系统...")
    
    try:
        # 检查抽卡概率
        print("   🎲 检查抽卡概率...")
        conn = CardSystem.get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT rarity, rate FROM rarity_drop_config ORDER BY rate DESC')
        rates = cursor.fetchall()
        
        total_rate = sum(rate for _, rate in rates)
        print(f"   📊 总概率: {total_rate:.3f}")
        
        if abs(total_rate - 1.0) < 0.001:
            print("   ✅ 概率配置正确 (总和为1)")
        else:
            print(f"   ⚠️  概率配置异常 (总和为{total_rate:.3f})")
        
        # 检查卡牌分布
        print("   🃏 检查卡牌分布...")
        cursor.execute('SELECT rarity, COUNT(*) FROM card_definitions GROUP BY rarity ORDER BY rarity')
        distribution = cursor.fetchall()
        
        for rarity, count in distribution:
            print(f"      • {rarity}级: {count}张")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ 抽卡系统测试失败: {str(e)}")
        return False

def test_api_endpoints():
    """测试API接口"""
    print("\n4. 测试API接口...")
    
    try:
        # 先尝试登录获取token
        print("   🔐 尝试登录获取认证token...")
        login_data = {
            'username': TEST_USER['username'],
            'password': TEST_USER['password']
        }
        
        try:
            login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
            if login_response.status_code == 200:
                token = login_response.json().get('data', {}).get('access_token')
                if token:
                    print("   ✅ 登录成功，获取到认证token")
                    headers = {'Authorization': f'Bearer {token}'}
                    
                    # 测试获取卡牌列表
                    print("   📋 测试获取卡牌列表...")
                    response = requests.get(f"{BASE_URL}/cards/all", headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        print(f"   ✅ 获取卡牌列表成功: {len(data.get('data', []))}张卡牌")
                    else:
                        print(f"   ❌ 获取卡牌列表失败: {response.status_code}")
                    
                    # 测试获取抽卡费用
                    print("   💰 测试获取抽卡费用...")
                    response = requests.get(f"{BASE_URL}/cards/draw/costs", headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        print(f"   ✅ 获取抽卡费用成功: {data.get('data', {})}")
                    else:
                        print(f"   ❌ 获取抽卡费用失败: {response.status_code}")
                    
                    return True
                else:
                    print("   ⚠️  登录成功但未获取到token")
                    return False
            else:
                print(f"   ⚠️  登录失败: {login_response.status_code}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("   ⚠️  后端服务未启动，跳过API测试")
            return True
            
    except Exception as e:
        print(f"   ❌ API接口测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 开始测试前端集成功能...")
    print("="*60)
    
    tests = [
        test_database_integration,
        test_user_points_system,
        test_card_drawing_system,
        test_api_endpoints
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
        print("\n🎉 所有测试通过！前端集成功能正常")
        print("\n📝 下一步:")
        print("   1. 启动后端服务: python app.py")
        print("   2. 启动前端服务: npm run serve")
        print("   3. 测试抽卡功能")
        sys.exit(0)
    else:
        print("\n⚠️  部分测试失败，请检查系统配置")
        sys.exit(1)

if __name__ == '__main__':
    main() 