#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证系统更新测试脚本
"""

import requests
import json
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 测试配置
BASE_URL = "http://localhost:5000/api/v1"

def test_auth_apis():
    """测试认证相关API"""
    
    print("=== 认证系统更新测试 ===\n")
    
    # 1. 测试学生注册
    print("1. 测试学生注册...")
    student_data = {
        "name": "张三",
        "id_number": "1001001",
        "password": "123456",
        "role": "student"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=student_data)
        if response.status_code == 200:
            data = response.json()
            print("✓ 学生注册成功")
            print(f"   学生ID: {data['data']['user']['id']}")
            print(f"   姓名: {data['data']['user']['name']}")
            print(f"   学号: {data['data']['user']['student_id']}")
            print(f"   班级: {data['data']['user']['class_number']}")
            student_token = data['data']['access_token']
        else:
            print(f"✗ 学生注册失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")
        return
    
    print()
    
    # 2. 测试教师注册
    print("2. 测试教师注册...")
    teacher_data = {
        "name": "李老师",
        "id_number": "2001001",
        "password": "123456",
        "role": "teacher"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=teacher_data)
        if response.status_code == 200:
            data = response.json()
            print("✓ 教师注册成功")
            print(f"   教师ID: {data['data']['user']['id']}")
            print(f"   姓名: {data['data']['user']['name']}")
            print(f"   教职工号: {data['data']['user']['teacher_id']}")
            teacher_token = data['data']['access_token']
        else:
            print(f"✗ 教师注册失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")
    
    print()
    
    # 3. 测试学生登录（使用姓名）
    print("3. 测试学生登录（使用姓名）...")
    login_data = {
        "name_or_id": "张三",
        "password": "123456",
        "role": "student"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print("✓ 学生登录成功（姓名）")
            print(f"   用户信息: {data['data']['user']['name']} - {data['data']['user']['student_id']}")
        else:
            print(f"✗ 学生登录失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")
    
    print()
    
    # 4. 测试学生登录（使用学号）
    print("4. 测试学生登录（使用学号）...")
    login_data = {
        "name_or_id": "1001001",
        "password": "123456",
        "role": "student"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print("✓ 学生登录成功（学号）")
            print(f"   用户信息: {data['data']['user']['name']} - {data['data']['user']['student_id']}")
        else:
            print(f"✗ 学生登录失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")
    
    print()
    
    # 5. 测试教师登录（使用姓名）
    print("5. 测试教师登录（使用姓名）...")
    login_data = {
        "name_or_id": "李老师",
        "password": "123456",
        "role": "teacher"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print("✓ 教师登录成功（姓名）")
            print(f"   用户信息: {data['data']['user']['name']} - {data['data']['user']['teacher_id']}")
        else:
            print(f"✗ 教师登录失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")
    
    print()
    
    # 6. 测试教师登录（使用教职工号）
    print("6. 测试教师登录（使用教职工号）...")
    login_data = {
        "name_or_id": "2001001",
        "password": "123456",
        "role": "teacher"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print("✓ 教师登录成功（教职工号）")
            print(f"   用户信息: {data['data']['user']['name']} - {data['data']['user']['teacher_id']}")
        else:
            print(f"✗ 教师登录失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"✗ 请求失败: {str(e)}")
    
    print()
    
    # 7. 测试班级分配功能
    print("7. 测试班级分配功能...")
    
    # 注册更多学生来测试班级分配
    for i in range(2, 35):  # 注册33个学生，测试班级分配
        student_data = {
            "name": f"学生{i}",
            "id_number": f"1001{i:03d}",
            "password": "123456",
            "role": "student"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/auth/register", json=student_data)
            if response.status_code == 200:
                data = response.json()
                class_number = data['data']['user']['class_number']
                print(f"   {student_data['name']} ({student_data['id_number']}) -> 班级 {class_number}")
            else:
                print(f"   ✗ {student_data['name']} 注册失败")
        except Exception as e:
            print(f"   ✗ {student_data['name']} 请求失败: {str(e)}")
    
    print("\n✓ 班级分配测试完成")
    
    print("\n=== 测试完成 ===")

def print_usage():
    """打印使用说明"""
    print("认证系统更新测试说明：")
    print("1. 确保后端服务已启动")
    print("2. 确保已运行初始化脚本: python scripts/init_auth_update.py")
    print("3. 运行测试: python scripts/test_auth_update.py")
    print("\n主要更新：")
    print("- 学生注册：姓名 + 学号(1001开头) + 密码")
    print("- 教师注册：姓名 + 教职工号(2001开头) + 密码")
    print("- 学生登录：支持姓名或学号")
    print("- 教师登录：支持姓名或教职工号")
    print("- 自动班级分配：每30人一个班")

if __name__ == "__main__":
    print_usage()
    print("\n" + "="*50 + "\n")
    test_auth_apis() 