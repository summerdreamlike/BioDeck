#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的卡片API功能
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/v1"

def test_cards_api():
    """测试卡片相关API"""
    print("🧪 测试修复后的卡片API功能")
    print("=" * 50)
    
    # 1. 测试获取所有卡片定义
    print("\n1️⃣ 测试获取所有卡片定义")
    try:
        response = requests.get(f"{BASE_URL}/cards/all-cards")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            cards = data.get('data', {}).get('cards', [])
            print(f"✅ 成功获取 {len(cards)} 张卡片定义")
            
            # 按稀有度统计
            rarity_count = {}
            for card in cards:
                rarity = card.get('rarity', 'Unknown')
                rarity_count[rarity] = rarity_count.get(rarity, 0) + 1
            
            print("📊 稀有度分布:")
            for rarity, count in sorted(rarity_count.items()):
                print(f"   {rarity}: {count} 张")
        else:
            print(f"❌ 获取卡片定义失败: {response.status_code}")
            print(f"   响应: {response.text}")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
    
    # 2. 测试获取用户收集统计（需要认证）
    print("\n2️⃣ 测试获取用户收集统计")
    print("   注意：此API需要JWT认证，请先登录获取token")
    
    # 3. 测试数据库表结构
    print("\n3️⃣ 检查数据库表结构")
    try:
        import sys
        import os
        # 添加父目录到Python路径
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from models.card_system import CardSystem
        CardSystem.ensure_tables()
        print("✅ 数据库表结构正常")
        
        # 获取卡片总数
        all_cards = CardSystem.get_all_cards()
        print(f"📚 数据库中共有 {len(all_cards)} 张卡片定义")
        
        # 获取稀有度配置
        rarity_config = CardSystem.get_rarity_drop_config()
        print("🎲 稀有度概率配置:")
        for rarity, rate in rarity_config.items():
            print(f"   {rarity}: {rate * 100:.1f}%")
            
    except Exception as e:
        print(f"❌ 数据库检查失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cards_api() 