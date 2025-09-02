#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
头像功能测试脚本
"""

import requests
import json
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 测试配置
BASE_URL = "http://localhost:5000/api/v1"

def test_avatar_apis():
    """测试头像相关API"""
    
    print("=== 头像功能测试 ===\n")
    
    # 1. 登录获取token
    print("1. 登录获取token...")
    login_data = {
        "name_or_id": "小芳",
        "password": "123456",
        "role": "student"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print("✓ 登录成功")
            access_token = data['data']['access_token']
            user_id = data['data']['user']['id']
            print(f"   用户ID: {user_id}")
            print(f"   当前头像: {data['data']['user'].get('avatar_url', '无')}")
        else:
            print(f"✗ 登录失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")
        return
    
    print()
    
    # 2. 测试获取头像
    print("2. 测试获取头像...")
    headers = {'Authorization': f'Bearer {access_token}'}
    
    try:
        response = requests.get(f"{BASE_URL}/users/avatar/{user_id}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✓ 获取头像成功")
            print(f"   头像URL: {data['data']['avatar_url']}")
        else:
            print(f"✗ 获取头像失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")
    
    print()
    
    # 3. 测试上传头像（模拟）
    print("3. 测试上传头像...")
    print("   注意：这里只是测试API接口，实际需要真实的图片文件")
    print("   可以使用以下命令测试真实上传：")
    print(f"   curl -X POST {BASE_URL}/users/avatar \\")
    print(f"     -H 'Authorization: Bearer {access_token}' \\")
    print(f"     -F 'avatar=@/path/to/your/image.jpg'")
    
    # 4. 测试获取头像信息
    print("\n4. 测试获取头像信息...")
    try:
        response = requests.get(f"{BASE_URL}/users/avatar/{user_id}/info", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✓ 获取头像信息成功")
            avatar_info = data['data']['avatar_info']
            if avatar_info:
                print(f"   文件名: {avatar_info['filename']}")
                print(f"   原始文件名: {avatar_info['original_filename']}")
                print(f"   文件大小: {avatar_info['file_size']} bytes")
                print(f"   MIME类型: {avatar_info['mime_type']}")
                print(f"   创建时间: {avatar_info['created_at']}")
            else:
                print("   用户没有头像")
        else:
            print(f"✗ 获取头像信息失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")
    
    print()
    
    # 5. 测试删除头像
    print("5. 测试删除头像...")
    try:
        response = requests.delete(f"{BASE_URL}/users/avatar", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✓ 删除头像成功")
            print(f"   消息: {data['data']['message']}")
        else:
            print(f"✗ 删除头像失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")
    
    print()
    
    # 6. 验证删除结果
    print("6. 验证删除结果...")
    try:
        response = requests.get(f"{BASE_URL}/users/avatar/{user_id}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✓ 验证成功")
            if data['data']['avatar_url'] is None:
                print("   头像已成功删除")
            else:
                print(f"   头像仍然存在: {data['data']['avatar_url']}")
        else:
            print(f"✗ 验证失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")
    
    print("\n=== 测试完成 ===")
    print("\n使用说明：")
    print("1. 确保后端服务正在运行")
    print("2. 运行初始化脚本: python scripts/init_avatar.py")
    print("3. 使用真实图片文件测试上传功能")
    print("4. 检查 uploads/avatars/ 目录中的文件")

def create_test_image():
    """创建一个测试图片文件"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # 创建一个简单的测试图片
        img = Image.new('RGB', (200, 200), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # 添加文字
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, 90), "Test Avatar", fill='black', font=font)
        
        # 保存图片
        test_image_path = os.path.join(os.path.dirname(__file__), 'test_avatar.jpg')
        img.save(test_image_path, 'JPEG')
        print(f"✓ 创建测试图片: {test_image_path}")
        return test_image_path
    except ImportError:
        print("✗ 需要安装 Pillow 库来创建测试图片")
        print("   运行: pip install Pillow")
        return None
    except Exception as e:
        print(f"✗ 创建测试图片失败: {str(e)}")
        return None

if __name__ == "__main__":
    print("头像功能测试脚本")
    print("=" * 50)
    
    # 创建测试图片
    test_image = create_test_image()
    
    # 运行API测试
    test_avatar_apis()
    
    if test_image:
        print(f"\n测试图片已创建: {test_image}")
        print("可以使用此图片测试上传功能")
