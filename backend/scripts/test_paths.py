#!/usr/bin/env python3
"""
测试路径构建脚本
"""
import os

def test_paths():
    """测试路径构建"""
    print("=== 测试路径构建 ===")
    
    # 获取当前脚本的绝对路径
    script_path = os.path.abspath(__file__)
    print(f"当前脚本路径: {script_path}")
    
    # 获取脚本所在目录
    script_dir = os.path.dirname(script_path)
    print(f"脚本目录: {script_dir}")
    
    # 获取backend目录
    backend_dir = os.path.dirname(script_dir)
    print(f"后端目录: {backend_dir}")
    
    # 获取项目根目录
    root_dir = os.path.dirname(backend_dir)
    print(f"项目根目录: {root_dir}")
    
    # 测试前端资源路径
    frontend_assets = os.path.join(root_dir, 'frontend', 'src', 'assets')
    print(f"前端资源目录: {frontend_assets}")
    
    # 检查目录是否存在
    print(f"项目根目录存在: {os.path.exists(root_dir)}")
    print(f"前端资源目录存在: {os.path.exists(frontend_assets)}")
    
    # 测试具体的卡牌目录
    test_paths = [
        os.path.join(frontend_assets, 'img', 'Decks', 'A卡'),
        os.path.join(frontend_assets, 'img', 'Decks', 'B卡'),
        os.path.join(frontend_assets, 'img', 'Decks', 'R卡'),
        os.path.join(frontend_assets, 'img', 'Decks', 'SR卡'),
        os.path.join(frontend_assets, 'img', 'Decks', 'UR卡'),
    ]
    
    print("\n测试各卡牌目录:")
    for path in test_paths:
        exists = os.path.exists(path)
        print(f"  {path}: {'✅ 存在' if exists else '❌ 不存在'}")
        
        if exists:
            # 列出目录内容
            try:
                files = os.listdir(path)
                print(f"    包含 {len(files)} 个文件")
                if files:
                    print(f"    示例文件: {files[0]}")
            except Exception as e:
                print(f"    读取目录失败: {e}")
    
    print("\n=== 路径测试完成 ===")

if __name__ == "__main__":
    test_paths() 