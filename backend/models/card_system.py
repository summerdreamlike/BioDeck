from .base import BaseModel
from datetime import datetime
import sqlite3
import random

class CardSystem(BaseModel):
    @classmethod
    def get_db(cls):
        return sqlite3.connect(cls.db_path)
    
    @classmethod
    def ensure_tables(cls):
        """确保数据库表存在"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 创建卡牌定义表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS card_definitions (
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
        
        # 创建用户卡牌收集表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                card_id TEXT NOT NULL,
                obtained_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                obtained_method TEXT NOT NULL DEFAULT 'draw',
                UNIQUE(user_id, card_id)
            )
        ''')
        
        # 创建抽奖记录表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS draw_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                card_id TEXT,
                points_spent INTEGER NOT NULL,
                draw_type TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # 初始化默认卡牌
        cls._initialize_default_cards()
    
    @classmethod
    def _initialize_default_cards(cls):
        """初始化默认卡牌"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 检查是否已有卡牌
        cursor.execute('SELECT COUNT(*) FROM card_definitions')
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # 插入默认卡牌
        default_cards = [
            # 普通卡牌 (Common)
            ('C001', '细胞膜', '细胞的基本保护屏障', 'common', '/images/cards/cell_membrane.jpg', 50, 0.4),
            ('C002', '线粒体', '细胞的能量工厂', 'common', '/images/cards/mitochondria.jpg', 50, 0.4),
            ('C003', '细胞核', '细胞的指挥中心', 'common', '/images/cards/nucleus.jpg', 50, 0.4),
            ('C004', '叶绿体', '植物细胞的绿色工厂', 'common', '/images/cards/chloroplast.jpg', 50, 0.4),
            ('C005', '高尔基体', '细胞的包装中心', 'common', '/images/cards/golgi.jpg', 50, 0.4),
            
            # 稀有卡牌 (Rare)
            ('R001', 'DNA双螺旋', '生命的密码', 'rare', '/images/cards/dna.jpg', 200, 0.25),
            ('R002', '蛋白质合成', '生命的制造过程', 'rare', '/images/cards/protein.jpg', 200, 0.25),
            ('R003', '细胞分裂', '生命的延续', 'rare', '/images/cards/division.jpg', 200, 0.25),
            ('R004', '光合作用', '阳光的能量转换', 'rare', '/images/cards/photosynthesis.jpg', 200, 0.25),
            ('R005', '呼吸作用', '能量的释放', 'rare', '/images/cards/respiration.jpg', 200, 0.25),
            
            # 史诗卡牌 (Epic)
            ('E001', '基因突变', '进化的源泉', 'epic', '/images/cards/mutation.jpg', 500, 0.15),
            ('E002', '自然选择', '适者生存', 'epic', '/images/cards/selection.jpg', 500, 0.15),
            ('E003', '生态系统', '生命的网络', 'epic', '/images/cards/ecosystem.jpg', 500, 0.15),
            ('E004', '生物多样性', '地球的财富', 'epic', '/images/cards/biodiversity.jpg', 500, 0.15),
            ('E005', '进化论', '生命的历史', 'epic', '/images/cards/evolution.jpg', 500, 0.15),
            
            # 传说卡牌 (Legendary)
            ('L001', '生命起源', '最初的奇迹', 'legendary', '/images/cards/origin.jpg', 1000, 0.05),
            ('L002', '智慧生命', '意识的觉醒', 'legendary', '/images/cards/intelligence.jpg', 1000, 0.05),
            ('L003', '宇宙生命', '无限的可能', 'legendary', '/images/cards/universe.jpg', 1000, 0.05),
            ('L004', '永恒生命', '不灭的传说', 'legendary', '/images/cards/eternal.jpg', 1000, 0.05),
            ('L005', '创世神卡', '生物学的终极奥秘', 'legendary', '/images/cards/creator.jpg', 1000, 0.05),
        ]
        
        cursor.executemany('''
            INSERT INTO card_definitions (card_id, name, description, rarity, image_url, points_cost, drop_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', default_cards)
        
        conn.commit()
        conn.close()
    
    @classmethod
    def get_all_cards(cls):
        """获取所有卡牌定义"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM card_definitions ORDER BY rarity, card_id')
        cards = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return cards
    
    @classmethod
    def get_user_cards(cls, user_id):
        """获取用户拥有的卡牌"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT uc.*, cd.name, cd.description, cd.rarity, cd.image_url
            FROM user_cards uc
            JOIN card_definitions cd ON uc.card_id = cd.card_id
            WHERE uc.user_id = ?
            ORDER BY cd.rarity, cd.card_id
        ''', (user_id,))
        
        cards = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return cards
    
    @classmethod
    def draw_card(cls, user_id, points_cost=100):
        """抽卡"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        try:
            # 获取所有卡牌及其掉落率
            cursor.execute('SELECT * FROM card_definitions')
            all_cards = [dict(row) for row in cursor.fetchall()]
            
            if not all_cards:
                raise Exception('没有可用的卡牌')
            
            # 根据掉落率随机选择卡牌
            total_rate = sum(card['drop_rate'] for card in all_cards)
            rand = random.uniform(0, total_rate)
            
            selected_card = None
            current_rate = 0
            
            for card in all_cards:
                current_rate += card['drop_rate']
                if rand <= current_rate:
                    selected_card = card
                    break
            
            if not selected_card:
                selected_card = all_cards[-1]  # 保底
            
            # 检查用户是否已有此卡
            cursor.execute('SELECT id FROM user_cards WHERE user_id = ? AND card_id = ?', 
                         (user_id, selected_card['card_id']))
            
            if cursor.fetchone():
                # 已有此卡，记录抽奖但返回重复信息
                cursor.execute('''
                    INSERT INTO draw_history (user_id, card_id, points_spent, draw_type)
                    VALUES (?, ?, ?, 'duplicate')
                ''', (user_id, selected_card['card_id'], points_cost))
                
                conn.commit()
                conn.close()
                
                return {
                    'card': selected_card,
                    'is_duplicate': True,
                    'message': f'抽到了重复的卡牌：{selected_card["name"]}'
                }
            
            # 添加卡牌到用户收集
            cursor.execute('''
                INSERT INTO user_cards (user_id, card_id, obtained_method)
                VALUES (?, ?, 'draw')
            ''', (user_id, selected_card['card_id']))
            
            # 记录抽奖历史
            cursor.execute('''
                INSERT INTO draw_history (user_id, card_id, points_spent, draw_type)
                VALUES (?, ?, ?, 'new')
            ''', (user_id, selected_card['card_id'], points_cost))
            
            conn.commit()
            conn.close()
            
            return {
                'card': selected_card,
                'is_duplicate': False,
                'message': f'恭喜获得新卡牌：{selected_card["name"]}！'
            }
            
        except Exception as e:
            conn.rollback()
            conn.close()
            raise e
    
    @classmethod
    def get_draw_history(cls, user_id, limit=50):
        """获取用户抽奖历史"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT dh.*, cd.name, cd.rarity
            FROM draw_history dh
            LEFT JOIN card_definitions cd ON dh.card_id = cd.card_id
            WHERE dh.user_id = ?
            ORDER BY dh.created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return history
    
    @classmethod
    def get_user_collection_stats(cls, user_id):
        """获取用户收集统计"""
        conn = cls.get_db()
        cursor = conn.cursor()
        
        # 总卡牌数
        cursor.execute('SELECT COUNT(*) FROM user_cards WHERE user_id = ?', (user_id,))
        total_cards = cursor.fetchone()[0]
        
        # 按稀有度统计
        cursor.execute('''
            SELECT cd.rarity, COUNT(*) as count
            FROM user_cards uc
            JOIN card_definitions cd ON uc.card_id = cd.card_id
            WHERE uc.user_id = ?
            GROUP BY cd.rarity
        ''', (user_id,))
        
        rarity_stats = {row[0]: row[1] for row in cursor.fetchall()}
        
        # 总卡牌定义数
        cursor.execute('SELECT COUNT(*) FROM card_definitions')
        total_definitions = cursor.fetchone()[0]
        
        # 收集完成度
        completion_rate = (total_cards / total_definitions * 100) if total_definitions > 0 else 0
        
        conn.close()
        
        return {
            'total_cards': total_cards,
            'total_definitions': total_definitions,
            'completion_rate': round(completion_rate, 2),
            'rarity_stats': rarity_stats
        }
