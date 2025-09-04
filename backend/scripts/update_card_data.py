#!/usr/bin/env python3
"""
更新卡牌数据脚本
包含所有新增的卡片
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.card_system import CardSystem
from models.base import DATABASE
import sqlite3

def update_card_data():
    """更新卡牌数据"""
    print("=== 更新卡牌数据 ===")
    
    # 确保数据库表存在
    CardSystem.ensure_tables()
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        # 清空现有卡牌数据
        cursor.execute('DELETE FROM card_definitions')
        print("已清空现有卡牌数据")
        
        # 新的卡牌数据 - 按B、A、R、SR、UR顺序排列
        new_cards = [
            # B级卡牌 (B) - 6张
            ('B001', '协助扩散', '物质在载体蛋白协助下的扩散', 'B', '/assets/img/Decks/B卡/协助扩散.png', 100, 0.35),
            ('B002', '核糖体', '蛋白质合成的场所', 'B', '/assets/img/Decks/B卡/核糖体.png', 100, 0.35),
            ('B003', '种群密度', '单位面积内个体的数量', 'B', '/assets/img/Decks/B卡/种群密度.png', 100, 0.35),
            ('B004', '细胞学说奠基', '细胞学说的建立基础', 'B', '/assets/img/Decks/B卡/细胞学说奠基.png', 100, 0.35),
            ('B005', '水', '生命之源', 'B', '/assets/img/Decks/B卡/水.png', 100, 0.35),
            ('B006', '光能', '光合作用的能量来源', 'B', '/assets/img/Decks/B卡/光能.png', 100, 0.35),
            
            # A级卡牌 (A) - 12张
            ('A001', '主动运输', '细胞主动运输物质的过程', 'A', '/assets/img/Decks/A卡/主动运输.png', 300, 0.25),
            ('A002', '单基因遗传病', '由单个基因突变引起的遗传疾病', 'A', '/assets/img/Decks/A卡/单基因遗传病.png', 300, 0.25),
            ('A003', '叶绿体', '植物细胞进行光合作用的场所', 'A', '/assets/img/Decks/A卡/叶绿体.png', 300, 0.25),
            ('A004', '点突变', 'DNA序列中单个碱基的改变', 'A', '/assets/img/Decks/A卡/点突变.png', 300, 0.25),
            ('A005', '生物催化剂', '加速生物化学反应的物质', 'A', '/assets/img/Decks/A卡/生物催化剂.png', 300, 0.25),
            ('A006', '磷脂双分子层', '细胞膜的基本结构', 'A', '/assets/img/Decks/A卡/磷脂双分子层.png', 300, 0.25),
            ('A007', '程序性死亡', '细胞程序性死亡过程', 'A', '/assets/img/Decks/A卡/程序性死亡.png', 300, 0.25),
            ('A008', '细胞膜', '细胞与外界的分界', 'A', '/assets/img/Decks/A卡/细胞膜.png', 300, 0.25),
            ('A009', '蛋白质', '生命活动的主要承担者', 'A', '/assets/img/Decks/A卡/蛋白质.png', 300, 0.25),
            ('A010', '赤霉素', '植物生长调节激素', 'A', '/assets/img/Decks/A卡/赤霉素.png', 300, 0.25),
            ('A011', '酸碱平衡', '维持体内酸碱平衡的机制', 'A', '/assets/img/Decks/A卡/酸碱平衡.png', 300, 0.25),
            ('A012', '氧气', '生命活动必需的气体', 'A', '/assets/img/Decks/A卡/氧气.png', 300, 0.25),
            
            # R级卡牌 (R) - 15张
            ('R001', '分离定律', '孟德尔遗传学第一定律', 'R', '/assets/img/Decks/R卡/分离定律.png', 600, 0.20),
            ('R002', '反射弧', '神经反射的基本结构', 'R', '/assets/img/Decks/R卡/反射弧.png', 600, 0.20),
            ('R003', '多基因遗传病', '由多个基因共同作用的遗传疾病', 'R', '/assets/img/Decks/R卡/多基因遗传病.png', 600, 0.20),
            ('R004', '无氧呼吸', '不需要氧气的呼吸方式', 'R', '/assets/img/Decks/R卡/无氧呼吸.png', 600, 0.20),
            ('R005', '染色体异常遗传病', '由染色体异常引起的遗传疾病', 'R', '/assets/img/Decks/R卡/染色体异常遗传病.png', 600, 0.20),
            ('R006', '染色体结构变异', '染色体结构的改变', 'R', '/assets/img/Decks/R卡/染色体结构变异.png', 600, 0.20),
            ('R007', '激素调节', '激素对生命活动的调节', 'R', '/assets/img/Decks/R卡/激素调节.png', 600, 0.20),
            ('R008', '生长素', '植物生长调节激素', 'R', '/assets/img/Decks/R卡/生长素.png', 600, 0.20),
            ('R009', '线粒体', '细胞的能量工厂', 'R', '/assets/img/Decks/R卡/线粒体.png', 600, 0.20),
            ('R010', '细胞全能性', '细胞发育成完整个体的能力', 'R', '/assets/img/Decks/R卡/细胞全能性.png', 600, 0.20),
            ('R011', '能量货币', '细胞内的能量载体', 'R', '/assets/img/Decks/R卡/能量货币.png', 600, 0.20),
            ('R012', '食物链', '生物之间的食物关系', 'R', '/assets/img/Decks/R卡/食物链.png', 600, 0.20),
            ('R013', '类囊体膜', '叶绿体内进行光反应的膜结构', 'R', '/assets/img/Decks/R卡/类囊体膜.png', 600, 0.20),
            ('R014', '基质', '叶绿体内进行暗反应的场所', 'R', '/assets/img/Decks/R卡/基质.png', 600, 0.20),
            ('R015', 'NADPH', '光合作用中的还原剂', 'R', '/assets/img/Decks/R卡/NADPH.png', 600, 0.20),
            
            # SR级卡牌 (SR) - 12张
            ('SR001', '伴X遗传', '位于X染色体上的基因遗传', 'SR', '/assets/img/Decks/SR卡/伴X遗传.png', 1200, 0.15),
            ('SR002', '光反应', '光合作用的光依赖反应', 'SR', '/assets/img/Decks/SR卡/光反应.png', 1200, 0.15),
            ('SR003', '半保留复制', 'DNA复制的特点', 'SR', '/assets/img/Decks/SR卡/半保留复制.png', 1200, 0.15),
            ('SR004', '暗反应', '光合作用的碳固定反应', 'SR', '/assets/img/Decks/SR卡/暗反应.png', 1200, 0.15),
            ('SR005', '有丝分裂', '细胞分裂的主要方式', 'SR', '/assets/img/Decks/SR卡/有丝分裂.png', 1200, 0.15),
            ('SR006', '有氧呼吸', '需要氧气的呼吸方式', 'SR', '/assets/img/Decks/SR卡/有氧呼吸.png', 1200, 0.15),
            ('SR007', '染色体数目变异', '染色体数量的改变', 'SR', '/assets/img/Decks/SR卡/染色体数目变异.png', 1200, 0.15),
            ('SR008', '现代生物进化理论', '现代生物进化的理论体系', 'SR', '/assets/img/Decks/SR卡/现代生物进化理论.png', 1200, 0.15),
            ('SR009', '翻译', '蛋白质合成的过程', 'SR', '/assets/img/Decks/SR卡/翻译.png', 1200, 0.15),
            ('SR010', '自由组合定律', '孟德尔遗传学第二定律', 'SR', '/assets/img/Decks/SR卡/自由组合定律.png', 1200, 0.15),
            ('SR011', '转录', 'DNA到RNA的合成过程', 'SR', '/assets/img/Decks/SR卡/转录.png', 1200, 0.15),
            ('SR012', '食物网', '复杂的食物关系网络', 'SR', '/assets/img/Decks/SR卡/食物网.png', 1200, 0.15),
            
            # UR级卡牌 (UR) - 6张
            ('UR001', '减数分裂', '生殖细胞形成时的特殊分裂', 'UR', '/assets/img/Decks/UR卡/减数分裂.png', 2500, 0.05),
            ('UR002', '物质循环', '生物圈中物质循环过程', 'UR', '/assets/img/Decks/UR卡/物质循环.png', 2500, 0.05),
            ('UR003', '生物多样性', '地球生物多样性', 'UR', '/assets/img/Decks/UR卡/生物多样性.png', 2500, 0.05),
            ('UR004', '能量流动', '生态系统能量流动', 'UR', '/assets/img/Decks/UR卡/能量流动.png', 2500, 0.05),
            ('UR005', '自然选择', '生物进化的主要机制', 'UR', '/assets/img/Decks/UR卡/自然选择.png', 2500, 0.05),
            ('UR006', '葡萄糖', '细胞的主要能源物质', 'UR', '/assets/img/Decks/UR卡/葡萄糖.png', 2500, 0.05),
        ]
        
        # 插入新卡牌
        cursor.executemany('''
            INSERT INTO card_definitions 
            (card_id, name, description, rarity, image_url, points_cost, drop_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', new_cards)
        
        # 更新稀有度概率配置
        cursor.execute('DELETE FROM rarity_drop_config')
        
        # 根据卡牌数量重新计算概率
        rarity_rates = [
            ('B', 0.35),   # B级: 6张, 35%
            ('A', 0.25),   # A级: 12张, 25%
            ('R', 0.20),   # R级: 15张, 20%
            ('SR', 0.15),  # SR级: 12张, 15%
            ('UR', 0.05),  # UR级: 6张, 5%
        ]
        
        cursor.executemany('INSERT INTO rarity_drop_config (rarity, rate) VALUES (?, ?)', rarity_rates)
        print("已更新稀有度概率配置")
        
        conn.commit()
        print(f"成功插入 {len(new_cards)} 张新卡牌")
        
        # 显示各稀有度的卡牌数量
        cursor.execute('''
            SELECT rarity, COUNT(*) as count 
            FROM card_definitions 
            GROUP BY rarity 
            ORDER BY rarity
        ''')
        
        rarity_counts = cursor.fetchall()
        print("\n各稀有度卡牌数量:")
        for rarity, count in rarity_counts:
            print(f"  {rarity}级: {count}张")
        
        # 显示所有卡牌
        cursor.execute('SELECT card_id, name, rarity FROM card_definitions ORDER BY rarity, card_id')
        all_cards = cursor.fetchall()
        
        print("\n所有卡牌列表:")
        current_rarity = None
        for card_id, name, rarity in all_cards:
            if rarity != current_rarity:
                print(f"\n{rarity}级卡牌:")
                current_rarity = rarity
            print(f"  {card_id}: {name}")
        
        print("\n=== 卡牌数据更新完成 ===")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ 更新失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    update_card_data() 