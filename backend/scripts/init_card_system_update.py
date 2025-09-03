#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
卡牌系统更新初始化脚本
"""

import sqlite3
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def init_card_system_update():
    """初始化卡牌系统更新"""
    print("正在更新卡牌系统...")
    
    # 使用相对于项目根目录的数据库路径
    db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. 添加积分字段到users表
        print("1. 更新users表结构...")
        
        # 检查并添加points字段
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'points' not in columns:
            cursor.execute('ALTER TABLE users ADD COLUMN points INTEGER DEFAULT 100')
            print("   ✓ 添加points字段")
        else:
            print("   ✓ points字段已存在")
        
        # 2. 更新现有用户的积分
        print("2. 更新现有用户积分...")
        cursor.execute('UPDATE users SET points = 100 WHERE points IS NULL OR points < 100')
        updated_count = cursor.rowcount
        print(f"   ✓ 更新了 {updated_count} 个用户的积分")
        
        # 3. 清空并重新初始化卡牌定义
        print("3. 重新初始化卡牌定义...")
        cursor.execute('DELETE FROM card_definitions')
        cursor.execute('DELETE FROM rarity_drop_config')
        print("   ✓ 清空旧卡牌数据")
        
        # 4. 重新创建卡牌定义表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS card_definitions_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_id TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                description TEXT,
                rarity TEXT NOT NULL,
                image_url TEXT,
                points_cost INTEGER NOT NULL DEFAULT 100,
                drop_rate REAL NOT NULL DEFAULT 0.1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 5. 插入新的卡牌定义
        new_cards = [
            # B级卡牌 (B) - 基础生物学概念
            ('B001', '种群密度', '种群在单位面积或单位体积中的个体数量，是生态学研究的重要参数', 'B', 'assets/img/Decks/B卡/种群密度.png', 100, 0.35),
            ('B002', '协助扩散', '物质在载体蛋白帮助下顺浓度梯度跨膜运输的过程，不消耗能量', 'B', 'assets/img/Decks/B卡/协助扩散.png', 100, 0.35),
            ('B003', '核糖体', '细胞中蛋白质合成的场所，由rRNA和蛋白质组成', 'B', 'assets/img/Decks/B卡/核糖体.png', 100, 0.35),
            ('B004', '细胞学说奠基', '施莱登和施旺提出的细胞学说，奠定了现代生物学的基础', 'B', 'assets/img/Decks/B卡/细胞学说奠基.png', 100, 0.35),
            
            # A级卡牌 (A) - 重要生物学概念
            ('A001', '赤霉素', '植物激素，促进植物生长和发育，影响种子萌发和茎的伸长', 'A', 'assets/img/Decks/A卡/赤霉素.png', 300, 0.25),
            ('A002', '酸碱平衡', '生物体内pH值的相对稳定状态，对生命活动至关重要', 'A', 'assets/img/Decks/A卡/酸碱平衡.png', 300, 0.25),
            ('A003', '单基因遗传病', '由单个基因突变引起的遗传性疾病，如白化病、血友病等', 'A', 'assets/img/Decks/A卡/单基因遗传病.png', 300, 0.25),
            ('A004', '点突变', 'DNA分子中单个碱基对的改变，可能导致基因功能的改变', 'A', 'assets/img/Decks/A卡/点突变.png', 300, 0.25),
            ('A005', '程序性死亡', '细胞在特定信号诱导下的主动死亡过程，对生物发育很重要', 'A', 'assets/img/Decks/A卡/程序性死亡.png', 300, 0.25),
            ('A006', '主动运输', '物质逆浓度梯度跨膜运输的过程，需要载体蛋白和能量', 'A', 'assets/img/Decks/A卡/主动运输.png', 300, 0.25),
            ('A007', '生物催化剂', '酶，生物体内催化各种生化反应的蛋白质，具有高效性和专一性', 'A', 'assets/img/Decks/A卡/生物催化剂.png', 300, 0.25),
            ('A008', '细胞膜', '细胞的基本保护屏障，控制物质进出，维持细胞内环境稳定', 'A', 'assets/img/Decks/A卡/细胞膜.png', 300, 0.25),
            ('A009', '磷脂双分子层', '细胞膜的基本骨架，由磷脂分子排列成双层结构', 'A', 'assets/img/Decks/A卡/磷脂双分子层.png', 300, 0.25),
            ('A010', '蛋白质', '生命活动的主要承担者，参与细胞结构、代谢调节、免疫等多种功能', 'A', 'assets/img/Decks/A卡/蛋白质.png', 300, 0.25),
            ('A011', '叶绿体', '植物细胞中进行光合作用的细胞器，含有叶绿素', 'A', 'assets/img/Decks/A卡/叶绿体.png', 300, 0.25),
            
            # R级卡牌 (R) - 进阶生物学概念
            ('R001', '食物链', '生物之间通过捕食关系形成的营养关系链，体现能量流动', 'R', 'assets/img/Decks/R卡/食物链.png', 600, 0.20),
            ('R002', '生长素', '植物激素，促进细胞伸长和分化，影响植物向光性', 'R', 'assets/img/Decks/R卡/生长素.png', 600, 0.20),
            ('R003', '激素调节', '生物体内通过激素进行的信息传递和生理调节机制', 'R', 'assets/img/Decks/R卡/激素调节.png', 600, 0.20),
            ('R004', '反射弧', '神经调节的基本结构，包括感受器、传入神经、神经中枢、传出神经和效应器', 'R', 'assets/img/Decks/R卡/反射弧.png', 600, 0.20),
            ('R005', '染色体异常遗传病', '由染色体结构或数目异常引起的遗传性疾病，如唐氏综合征', 'R', 'assets/img/Decks/R卡/染色体异常遗传病.png', 600, 0.20),
            ('R006', '多基因遗传病', '由多个基因共同作用引起的遗传性疾病，如高血压、糖尿病等', 'R', 'assets/img/Decks/R卡/多基因遗传病.png', 600, 0.20),
            ('R007', '染色体结构变异', '染色体发生断裂、缺失、重复、倒位、易位等结构改变', 'R', 'assets/img/Decks/R卡/染色体结构变异.png', 600, 0.20),
            ('R008', '分离定律', '孟德尔第一定律，控制一对相对性状的基因在形成配子时分离', 'R', 'assets/img/Decks/R卡/分离定律.png', 600, 0.20),
            ('R009', '细胞全能性', '细胞具有发育成完整个体的潜在能力，是克隆技术的基础', 'R', 'assets/img/Decks/R卡/细胞全能性.png', 600, 0.20),
            ('R010', '无氧呼吸', '在无氧条件下，有机物不完全氧化分解产生能量的过程', 'R', 'assets/img/Decks/R卡/无氧呼吸.png', 600, 0.20),
            ('R011', '线粒体', '细胞进行有氧呼吸的主要场所，被称为细胞的能量工厂', 'R', 'assets/img/Decks/R卡/线粒体.png', 600, 0.20),
            ('R012', '能量货币', 'ATP，细胞中储存和传递能量的主要分子', 'R', 'assets/img/Decks/R卡/能量货币.png', 600, 0.20),
            
            # SR级卡牌 (SR) - 高级生物学概念
            ('SR001', '翻译', '以mRNA为模板，在核糖体上合成蛋白质的过程', 'SR', 'assets/img/Decks/SR卡/翻译.png', 1200, 0.15),
            ('SR002', '食物网', '多个食物链相互交织形成的复杂营养关系网络', 'SR', 'assets/img/Decks/SR卡/食物网.png', 1200, 0.15),
            ('SR003', '现代生物进化理论', '综合了自然选择、遗传变异、基因频率变化等内容的进化理论', 'SR', 'assets/img/Decks/SR卡/现代生物进化理论.png', 1200, 0.15),
            ('SR004', '染色体数目变异', '染色体数目发生改变，如多倍体、单倍体等', 'SR', 'assets/img/Decks/SR卡/染色体数目变异.png', 1200, 0.15),
            ('SR005', '转录', '以DNA为模板，在RNA聚合酶催化下合成RNA的过程', 'SR', 'assets/img/Decks/SR卡/转录.png', 1200, 0.15),
            ('SR006', '半保留复制', 'DNA复制时，每条子链都保留一条母链的复制方式', 'SR', 'assets/img/Decks/SR卡/半保留复制.png', 1200, 0.15),
            ('SR007', '伴X遗传', '基因位于X染色体上的遗传方式，如红绿色盲、血友病等', 'SR', 'assets/img/Decks/SR卡/伴X遗传.png', 1200, 0.15),
            ('SR008', '自由组合定律', '孟德尔第二定律，控制不同性状的基因在形成配子时自由组合', 'SR', 'assets/img/Decks/SR卡/自由组合定律.png', 1200, 0.15),
            ('SR009', '有丝分裂', '真核细胞进行细胞分裂的主要方式，保证遗传物质的准确分配', 'SR', 'assets/img/Decks/SR卡/有丝分裂.png', 1200, 0.15),
            ('SR010', '暗反应', '光合作用中不依赖光的化学反应，固定CO2合成有机物', 'SR', 'assets/img/Decks/SR卡/暗反应.png', 1200, 0.15),
            ('SR011', '光反应', '光合作用中依赖光的反应，将光能转化为化学能', 'SR', 'assets/img/Decks/SR卡/光反应.png', 1200, 0.15),
            ('SR012', '有氧呼吸', '在氧气参与下，有机物彻底氧化分解产生大量能量的过程', 'SR', 'assets/img/Decks/SR卡/有氧呼吸.png', 1200, 0.15),
            
            # UR级卡牌 (UR) - 顶级生物学概念
            ('UR001', '物质循环', '生物圈中物质在生物与非生物环境之间的循环过程，维持生态系统的物质平衡', 'UR', 'assets/img/Decks/UR卡/物质循环.png', 2500, 0.05),
            ('UR002', '生物多样性', '地球上所有生物种类、基因和生态系统的丰富程度，是生命进化的宝贵财富', 'UR', 'assets/img/Decks/UR卡/生物多样性.png', 2500, 0.05),
            ('UR003', '能量流动', '生态系统中能量从生产者到消费者的单向流动过程，驱动整个生命系统的运转', 'UR', 'assets/img/Decks/UR卡/能量流动.png', 2500, 0.05),
            ('UR004', '自然选择', '达尔文进化论的核心机制，适者生存，不适者被淘汰的自然过程', 'UR', 'assets/img/Decks/UR卡/自然选择.png', 2500, 0.05),
            ('UR005', '减数分裂', '生殖细胞形成过程中的特殊细胞分裂方式，产生单倍体配子', 'UR', 'assets/img/Decks/UR卡/减数分裂.png', 2500, 0.05),
        ]
        
        cursor.executemany('''
            INSERT INTO card_definitions_new (card_id, name, description, rarity, image_url, points_cost, drop_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', new_cards)
        print(f"   ✓ 插入了 {len(new_cards)} 张新卡牌")
        
        # 6. 插入新的稀有度概率配置
        new_rarity_rates = [
            ('B', 0.35),
            ('A', 0.25),
            ('R', 0.20),
            ('SR', 0.15),
            ('UR', 0.05)
        ]
        
        print("   ✓ 稀有度概率配置:")
        print("      • B级: 35% (4张)")
        print("      • A级: 25% (11张)")
        print("      • R级: 20% (12张)")
        print("      • SR级: 15% (12张)")
        print("      • UR级: 5% (5张)")
        
        cursor.executemany('INSERT INTO rarity_drop_config (rarity, rate) VALUES (?, ?)', new_rarity_rates)
        print("   ✓ 更新了稀有度概率配置")
        
        # 7. 替换旧表
        cursor.execute('DROP TABLE IF EXISTS card_definitions')
        cursor.execute('ALTER TABLE card_definitions_new RENAME TO card_definitions')
        print("   ✓ 更新了卡牌定义表")
        
        # 8. 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_card_rarity ON card_definitions(rarity)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_card_id ON card_definitions(card_id)')
        print("   ✓ 创建了数据库索引")
        
        conn.commit()
        print("\n✅ 卡牌系统更新完成！")
        
        # 显示更新后的统计信息
        cursor.execute('SELECT COUNT(*) FROM card_definitions')
        card_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        
        print(f"\n📊 更新统计:")
        print(f"   - 卡牌总数: {card_count}")
        print(f"   - 用户总数: {user_count}")
        print(f"   - 稀有度分布:")
        print(f"     • B级卡牌: 4张 (35%) - 基础生物学概念")
        print(f"     • A级卡牌: 11张 (25%) - 重要生物学概念")
        print(f"     • R级卡牌: 12张 (20%) - 进阶生物学概念")
        print(f"     • SR级卡牌: 12张 (15%) - 高级生物学概念")
        print(f"     • UR级卡牌: 5张 (5%) - 顶级生物学概念")
        print(f"   - 抽卡费用: 单抽100积分, 十抽900积分")
        print(f"   - 总计: 42张生物学主题卡牌")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ 更新失败: {str(e)}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    try:
        init_card_system_update()
    except Exception as e:
        print(f"初始化失败: {str(e)}")
        sys.exit(1) 