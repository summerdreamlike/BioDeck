#!/usr/bin/env python3
"""
验证卡牌图片路径脚本
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.card_system import CardSystem

def verify_card_images():
    """验证卡牌图片路径"""
    print("=== 验证卡牌图片路径 ===")
    
    try:
        # 获取所有卡牌
        all_cards = CardSystem.get_all_cards()
        print(f"数据库中共有 {len(all_cards)} 张卡牌")
        
        # 检查图片路径
        missing_images = []
        valid_images = []
        
        # 显示路径信息
        script_dir = os.path.dirname(os.path.abspath(__file__))  # backend/scripts
        backend_dir = os.path.dirname(script_dir)  # backend
        root_dir = os.path.dirname(backend_dir)  # 项目根目录
        print(f"脚本目录: {script_dir}")
        print(f"后端目录: {backend_dir}")
        print(f"项目根目录: {root_dir}")
        print(f"前端资源目录: {os.path.join(root_dir, 'frontend', 'src', 'assets')}")
        print()
        
        for card in all_cards:
            image_url = card['image_url']
            card_name = card['name']
            rarity = card['rarity']
            
            # 构建完整的图片路径
            if image_url.startswith('/assets/'):
                # 转换为相对路径，去掉开头的 /
                relative_path = image_url[1:]  # 去掉开头的 /
                
                # 从backend/scripts目录回到项目根目录，然后到frontend/src
                full_path = os.path.join(root_dir, 'frontend', 'src', relative_path)
                
                # 标准化路径分隔符
                full_path = os.path.normpath(full_path)
                
                if os.path.exists(full_path):
                    valid_images.append((card_name, rarity, image_url))
                else:
                    missing_images.append((card_name, rarity, image_url, full_path))
            else:
                missing_images.append((card_name, rarity, image_url, "路径格式不正确"))
        
        # 显示结果
        print(f"\n✅ 有效图片: {len(valid_images)} 张")
        print(f"❌ 缺失图片: {len(missing_images)} 张")
        
        if missing_images:
            print("\n缺失的图片:")
            for name, rarity, url, path in missing_images:
                print(f"  {rarity}级 - {name}: {path}")
        
        # 按稀有度统计
        rarity_stats = {}
        for card in all_cards:
            rarity = card['rarity']
            if rarity not in rarity_stats:
                rarity_stats[rarity] = {'total': 0, 'valid': 0, 'missing': 0}
            rarity_stats[rarity]['total'] += 1
        
        for name, rarity, url, path in valid_images:
            rarity_stats[rarity]['valid'] += 1
        
        for name, rarity, url, path in missing_images:
            rarity_stats[rarity]['missing'] += 1
        
        print("\n各稀有度图片状态:")
        for rarity in sorted(rarity_stats.keys()):
            stats = rarity_stats[rarity]
            print(f"  {rarity}级: 总计{stats['total']}张, 有效{stats['valid']}张, 缺失{stats['missing']}张")
        
        if len(missing_images) == 0:
            print("\n🎉 所有卡牌图片路径都有效！")
        else:
            print(f"\n⚠️  有 {len(missing_images)} 张卡牌的图片路径需要修复")
        
        print("\n=== 验证完成 ===")
        
    except Exception as e:
        print(f"❌ 验证失败: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify_card_images() 