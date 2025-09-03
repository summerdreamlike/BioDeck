 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试抽卡API功能
"""

import sys
import os
import requests
import json

def test_draw_api():
    """测试抽卡API"""
    print("🔍 测试抽卡API功能...")
    
    base_url = "http://localhost:5000/api/v1"
    
    # 1. 获取用户积分
    print("\n1. 获取用户积分...")
    try:
        token = input("请输入JWT token (Bearer xxx): ").strip()
        if not token:
            print("   ❌ 未提供token")
            return False
        
        if not token.startswith('Bearer '):
            token = f"Bearer {token}"
        
        headers = {'Authorization': token}
        
        response = requests.get(f"{base_url}/cards/user/points", headers=headers)
        if response.status_code == 200:
            result = response.json()
            current_points = result['data']['points']
            print(f"   ✅ 当前积分: {current_points}")
        else:
            print(f"   ❌ 获取积分失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ 获取积分异常: {str(e)}")
        return False
    
    # 2. 测试单抽
    print("\n2. 测试单抽...")
    try:
        if current_points < 100:
            print("   ⚠️  积分不足，无法测试单抽")
        else:
            response = requests.post(f"{base_url}/cards/draw/single", headers=headers)
            print(f"   📊 响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ 单抽成功: {result['message']}")
                print(f"   🎴 抽到卡牌: {result['data'].get('card', {}).get('name', '未知')}")
                print(f"   💰 消耗积分: {result['data'].get('points_spent', 0)}")
                print(f"   💎 剩余积分: {result['data'].get('remaining_points', 0)}")
                
                # 检查响应格式
                if 'data' in result and 'remaining_points' in result['data']:
                    print("   ✅ 响应格式正确")
                else:
                    print("   ⚠️  响应格式异常")
            else:
                print(f"   ❌ 单抽失败: {response.text}")
                
    except Exception as e:
        print(f"   ❌ 单抽异常: {str(e)}")
    
    # 3. 测试十连抽
    print("\n3. 测试十连抽...")
    try:
        if current_points < 900:
            print("   ⚠️  积分不足，无法测试十连抽")
        else:
            response = requests.post(f"{base_url}/cards/draw/ten", headers=headers)
            print(f"   📊 响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ 十连抽成功: {result['message']}")
                
                # 检查响应格式
                if 'data' in result:
                    data = result['data']
                    if 'draws' in data and 'remaining_points' in data:
                        print(f"   🎴 抽到卡牌数量: {len(data['draws'])}")
                        print(f"   💰 消耗积分: {data.get('points_spent', 0)}")
                        print(f"   💎 剩余积分: {data.get('remaining_points', 0)}")
                        print("   ✅ 响应格式正确")
                        
                        # 显示前几张卡牌
                        for i, draw in enumerate(data['draws'][:3]):
                            card = draw.get('card', draw)
                            print(f"      {i+1}. {card.get('name', '未知')} ({card.get('rarity', '未知')})")
                        if len(data['draws']) > 3:
                            print(f"      ... 还有 {len(data['draws']) - 3} 张卡牌")
                    else:
                        print("   ⚠️  响应格式异常，缺少必要字段")
                else:
                    print("   ⚠️  响应格式异常，缺少data字段")
            else:
                print(f"   ❌ 十连抽失败: {response.text}")
                
    except Exception as e:
        print(f"   ❌ 十连抽异常: {str(e)}")
    
    return True

def main():
    """主函数"""
    print("🚀 开始测试抽卡API...")
    print("="*60)
    
    if test_draw_api():
        print("\n🎉 抽卡API测试完成！")
        print("\n📝 如果前端仍然有问题，请检查:")
        print("   1. 响应数据格式是否与前端期望一致")
        print("   2. 前端数据处理逻辑是否正确")
        print("   3. 浏览器控制台的错误信息")
    else:
        print("\n⚠️  抽卡API测试失败")
        print("\n🔧 请检查:")
        print("   1. 后端服务是否运行")
        print("   2. JWT token是否有效")
        print("   3. 数据库连接是否正常")

if __name__ == '__main__':
    main()