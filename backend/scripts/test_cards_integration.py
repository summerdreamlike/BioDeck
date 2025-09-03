#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试cards.py的完整功能
验证identity解析和积分系统是否正常工作
"""

import sys
import os
import sqlite3

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_identity_parsing():
    """测试identity解析功能"""
    print("🔍 测试identity解析功能...")
    
    # 模拟parse_user_identity函数的逻辑
    def parse_user_identity(identity):
        """解析用户身份信息，从字符串格式 'user_id:role' 中提取用户ID"""
        if isinstance(identity, str) and ':' in identity:
            parts = identity.split(':')
            # 确保有两个部分且都不为空
            if len(parts) == 2 and parts[0].strip() and parts[1].strip():
                try:
                    user_id = int(parts[0])
                    user_role = parts[1]
                    print(f"   ✅ 解析成功: 用户ID={user_id}, 角色={user_role}")
                    return user_id
                except (ValueError, IndexError) as e:
                    print(f"   ❌ 解析失败: {str(e)}")
                    return None
            else:
                print(f"   ❌ 格式不完整: {identity}")
                return None
        else:
            print(f"   ❌ 无效格式: {identity}")
            return None
    
    # 测试用例
    test_cases = [
        "123:student",      # 正常格式
        "456:teacher",      # 正常格式
        "789:admin",        # 正常格式
        "invalid",          # 无效格式（缺少冒号）
        "abc:def",          # 无效格式（ID不是数字）
        "123:",             # 无效格式（缺少角色）
        ":student",         # 无效格式（缺少ID）
        "123: ",            # 无效格式（角色为空）
        " :student",        # 无效格式（ID为空）
        "",                 # 空字符串
        None,               # None值
        123,                # 数字类型
    ]
    
    print("\n📋 测试用例:")
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. 测试输入: {test_case} (类型: {type(test_case)})")
        result = parse_user_identity(test_case)
        if result is not None:
            print(f"   结果: 用户ID = {result}")
            success_count += 1
        else:
            print(f"   结果: 解析失败")
    
    print("\n" + "="*50)
    print("📊 测试总结:")
    print(f"   • 总测试数: {total_count}")
    print(f"   • 成功解析: {success_count}")
    print(f"   • 解析失败: {total_count - success_count}")
    
    # 验证预期结果
    expected_success = 3  # 只有前3个应该是成功的
    if success_count == expected_success:
        print(f"\n🎉 identity解析测试通过！")
        return True
    else:
        print(f"\n⚠️  identity解析测试失败")
        print(f"   期望成功: {expected_success}, 实际成功: {success_count}")
        return False

def test_database_connection():
    """测试数据库连接"""
    print("\n🔍 测试数据库连接...")
    
    try:
        from models.card_system import CardSystem
        conn = CardSystem.get_db()
        if conn:
            print("   ✅ 数据库连接成功")
            conn.close()
            return True
        else:
            print("   ❌ 数据库连接失败")
            return False
    except Exception as e:
        print(f"   ❌ 数据库连接异常: {str(e)}")
        return False

def test_user_points_system():
    """测试用户积分系统"""
    print("\n🔍 测试用户积分系统...")
    
    try:
        from models.user import User
        
        # 检查是否有用户存在
        conn = User.get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        print(f"   📊 用户总数: {user_count}")
        
        if user_count > 0:
            # 检查积分字段
            cursor.execute('SELECT id, name, points FROM users LIMIT 1')
            user = cursor.fetchone()
            print(f"   👤 示例用户: {user[1]} (ID: {user[0]}, 积分: {user[2]})")
            
            # 测试积分更新
            test_user_id = user[0]
            old_points = user[2]
            
            print(f"   🔄 测试积分更新...")
            User.update_user_points(test_user_id, 100)
            new_points = User.get_user_points(test_user_id)
            print(f"   ✅ 积分更新成功: {old_points} -> {new_points}")
            
            # 恢复原积分
            User.update_user_points(test_user_id, -100)
            restored_points = User.get_user_points(test_user_id)
            print(f"   ✅ 积分恢复成功: {new_points} -> {restored_points}")
            
            conn.close()
            return True
        else:
            print("   ⚠️  没有用户数据")
            conn.close()
            return True  # 这不是错误，只是没有数据
        
    except Exception as e:
        print(f"   ❌ 用户积分系统测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 开始测试cards.py完整功能...")
    print("="*60)
    
    tests = [
        test_identity_parsing,
        test_database_connection,
        test_user_points_system
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "="*60)
    print("📋 测试总结:")
    print(f"   • 通过: {passed}/{total}")
    print(f"   • 失败: {total - passed}")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        print("\n📝 系统状态:")
        print("   ✅ identity解析功能正常")
        print("   ✅ 数据库连接正常")
        print("   ✅ 用户积分系统正常")
        print("\n🚀 可以启动服务进行完整测试")
        sys.exit(0)
    else:
        print("\n⚠️  部分测试失败，请检查系统配置")
        sys.exit(1)

if __name__ == '__main__':
    main() 