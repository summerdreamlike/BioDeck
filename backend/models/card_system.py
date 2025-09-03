from .base import BaseModel
from datetime import datetime
import sqlite3
import random

class CardSystem(BaseModel):
    @classmethod
    def get_db(cls):
        from .base import DATABASE
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    
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
        
        # 稀有度概率配置表（控制各稀有度总体掉落概率）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rarity_drop_config (
                rarity TEXT PRIMARY KEY,
                rate   REAL NOT NULL
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
        # 初始化默认稀有度概率
        cls._initialize_default_rarity_rates()
    
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
            # B级卡牌 (B)
            ('B001', '细胞膜', '细胞的基本保护屏障', 'B', '/images/cards/cell_membrane.jpg', 100, 0.35),
            ('B002', '线粒体', '细胞的能量工厂', 'B', '/images/cards/mitochondria.jpg', 100, 0.35),
            ('B003', '细胞核', '细胞的指挥中心', 'B', '/images/cards/nucleus.jpg', 100, 0.35),
            ('B004', '叶绿体', '植物细胞的绿色工厂', 'B', '/images/cards/chloroplast.jpg', 100, 0.35),
            ('B005', '高尔基体', '细胞的包装中心', 'B', '/images/cards/golgi.jpg', 100, 0.35),
            
            # A级卡牌 (A)
            ('A001', 'DNA双螺旋', '生命的密码', 'A', '/images/cards/dna.jpg', 300, 0.25),
            ('A002', '蛋白质合成', '生命的制造过程', 'A', '/images/cards/protein.jpg', 300, 0.25),
            ('A003', '细胞分裂', '生命的延续', 'A', '/images/cards/division.jpg', 300, 0.25),
            ('A004', '光合作用', '阳光的能量转换', 'A', '/images/cards/photosynthesis.jpg', 300, 0.25),
            ('A005', '呼吸作用', '能量的释放', 'A', '/images/cards/respiration.jpg', 300, 0.25),
            
            # R级卡牌 (R)
            ('R001', '基因突变', '进化的源泉', 'R', '/images/cards/mutation.jpg', 600, 0.20),
            ('R002', '自然选择', '适者生存', 'R', '/images/cards/selection.jpg', 600, 0.20),
            ('R003', '生态系统', '生命的网络', 'R', '/images/cards/ecosystem.jpg', 600, 0.20),
            ('R004', '生物多样性', '地球的财富', 'R', '/images/cards/biodiversity.jpg', 600, 0.20),
            ('R005', '进化论', '生命的历史', 'R', '/images/cards/evolution.jpg', 600, 0.20),
            
            # SR级卡牌 (SR)
            ('SR001', '生命起源', '最初的奇迹', 'SR', '/images/cards/origin.jpg', 1200, 0.15),
            ('SR002', '智慧生命', '意识的觉醒', 'SR', '/images/cards/intelligence.jpg', 1200, 0.15),
            ('SR003', '宇宙生命', '无限的可能', 'SR', '/images/cards/universe.jpg', 1200, 0.15),
            ('SR004', '永恒生命', '不灭的传说', 'SR', '/images/cards/eternal.jpg', 1200, 0.15),
            ('SR005', '创世神卡', '生物学的终极奥秘', 'SR', '/images/cards/creator.jpg', 1200, 0.15),
            
            # UR级卡牌 (UR) - 已移至初始化脚本中
            # ('UR001', '物质循环', '生物圈中物质循环过程', 'UR', '/assets/img/Decks/UR卡/物质循环.png', 2500, 0.05),
            # ('UR002', '生物多样性', '地球生物多样性', 'UR', '/assets/img/Decks/UR卡/生物多样性.png', 2500, 0.05),
            # ('UR003', '能量流动', '生态系统能量流动', 'UR', '/assets/img/Decks/UR卡/能量流动.png', 2500, 0.05),
        ]
        
        # 注意：默认卡牌数据已移至初始化脚本中
        # 这里不再插入默认卡牌，由 init_card_system_update.py 脚本统一管理
        pass
        
        conn.commit()
        conn.close()

    @classmethod
    def _initialize_default_rarity_rates(cls):
        """初始化默认稀有度概率（若未配置）"""
        conn = cls.get_db()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT COUNT(*) FROM rarity_drop_config')
            if cursor.fetchone()[0] == 0:
                default_rates = [
                    ('B', 0.35),
                    ('A', 0.25),
                    ('R', 0.20),
                    ('SR', 0.15),
                    ('UR', 0.05)
                ]
                cursor.executemany('INSERT INTO rarity_drop_config (rarity, rate) VALUES (?, ?)', default_rates)
                conn.commit()
        finally:
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
            # 读取稀有度概率配置
            cursor.execute('SELECT rarity, rate FROM rarity_drop_config')
            rarity_rows = cursor.fetchall()

            if rarity_rows:
                rarity_rates = [(row[0], float(row[1])) for row in rarity_rows]
            else:
                # 若未配置，则根据卡牌定义中的drop_rate聚合出稀有度概率
                cursor.execute('SELECT rarity, SUM(drop_rate) FROM card_definitions GROUP BY rarity')
                rarity_rates = [(row[0], float(row[1])) for row in cursor.fetchall()]

            if not rarity_rates:
                raise Exception('未找到稀有度配置或卡牌定义')

            # 先按稀有度概率抽取稀有度
            total_rarity_rate = sum(rate for _, rate in rarity_rates)
            if total_rarity_rate <= 0:
                raise Exception('稀有度概率配置无效')

            rand_rarity = random.uniform(0, total_rarity_rate)
            chosen_rarity = None
            acc = 0.0
            for rarity, rate in rarity_rates:
                acc += rate
                if rand_rarity <= acc:
                    chosen_rarity = rarity
                    break
            if not chosen_rarity:
                chosen_rarity = rarity_rates[-1][0]

            # 在选中的稀有度中选择具体卡牌（按该稀有度下的卡牌drop_rate归一，若无则均匀）
            cursor.execute('SELECT * FROM card_definitions WHERE rarity = ?', (chosen_rarity,))
            rarity_cards = [dict(row) for row in cursor.fetchall()]
            if not rarity_cards:
                raise Exception(f'所选稀有度无卡牌：{chosen_rarity}')

            per_card_total = sum(card.get('drop_rate') or 0 for card in rarity_cards)
            if per_card_total and per_card_total > 0:
                rand_card = random.uniform(0, per_card_total)
                current = 0.0
                selected_card = None
                for card in rarity_cards:
                    current += card.get('drop_rate') or 0
                    if rand_card <= current:
                        selected_card = card
                        break
                if not selected_card:
                    selected_card = rarity_cards[-1]
            else:
                selected_card = random.choice(rarity_cards)
            
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
    def get_rarity_drop_config(cls):
        """获取稀有度概率配置"""
        conn = cls.get_db()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT rarity, rate FROM rarity_drop_config')
            rows = cursor.fetchall()
            config = {row[0]: float(row[1]) for row in rows}
            return config
        finally:
            conn.close()

    @classmethod
    def update_rarity_drop_config(cls, config):
        """更新稀有度概率配置。
        参数示例: { 'B': 0.35, 'A': 0.25, 'R': 0.20, 'SR': 0.15, 'UR': 0.05 }
        """
        conn = cls.get_db()
        cursor = conn.cursor()
        try:
            # 简单校验
            allowed = {'B', 'A', 'R', 'SR', 'UR'}
            for key in config.keys():
                if key not in allowed:
                    raise ValueError(f'未知稀有度: {key}')
                if config[key] is None or float(config[key]) < 0:
                    raise ValueError(f'稀有度概率无效: {key}')

            # 覆盖写入
            for rarity in allowed:
                if rarity in config:
                    cursor.execute('REPLACE INTO rarity_drop_config (rarity, rate) VALUES (?, ?)', (rarity, float(config[rarity])))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
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
