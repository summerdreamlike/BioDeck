# 卡牌抽奖系统 API 文档

## 概述

卡牌抽奖系统提供生物学主题的卡牌收集游戏功能。用户使用签到获得的积分进行抽奖，收集不同稀有度的生物学卡牌。

## 基础信息

- **基础URL**: `http://localhost:5000/api/v1`
- **认证方式**: JWT Token (需要在请求头中添加 `Authorization: Bearer <token>`)
- **数据格式**: JSON

## 卡牌系统说明

### 卡牌稀有度
- **B级卡牌 (B)**: 35%掉落率，100积分价值
- **A级卡牌 (A)**: 25%掉落率，300积分价值
- **R级卡牌 (R)**: 20%掉落率，600积分价值
- **SR级卡牌 (SR)**: 15%掉落率，1200积分价值
- **UR级卡牌 (UR)**: 5%掉落率，2500积分价值

### 抽奖费用
- **单抽**: 100积分
- **十连抽**: 900积分（优惠100积分）

## 接口列表

### 1. 获取用户卡牌收集

**接口地址**: `GET /cards/collection`

**功能描述**: 获取用户拥有的卡牌和收集统计信息

**请求参数**: 无

**请求示例**:
```bash
curl -X GET "http://localhost:5000/api/v1/cards/collection" \
  -H "Authorization: Bearer <your_jwt_token>"
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "cards": [
      {
        "id": 1,
        "user_id": 1,
        "card_id": "C001",
        "obtained_at": "2024-01-15T08:30:00",
        "obtained_method": "draw",
        "name": "细胞膜",
        "description": "细胞的基本保护屏障",
        "rarity": "common",
        "image_url": "/images/cards/cell_membrane.jpg"
      },
      {
        "id": 2,
        "user_id": 1,
        "card_id": "R001",
        "obtained_at": "2024-01-14T15:20:00",
        "obtained_method": "draw",
        "name": "DNA双螺旋",
        "description": "生命的密码",
        "rarity": "rare",
        "image_url": "/images/cards/dna.jpg"
      }
    ],
    "stats": {
      "total_cards": 2,
      "total_definitions": 20,
      "completion_rate": 10.0,
      "rarity_stats": {
        "common": 1,
        "rare": 1
      }
    }
  },
  "message": "获取成功"
}
```

**响应字段说明**:
- `cards`: 用户拥有的卡牌列表
  - `card_id`: 卡牌ID
  - `name`: 卡牌名称
  - `description`: 卡牌描述
  - `rarity`: 稀有度
  - `image_url`: 卡牌图片URL
  - `obtained_at`: 获得时间
  - `obtained_method`: 获得方式
- `stats`: 收集统计
  - `total_cards`: 拥有卡牌数量
  - `total_definitions`: 总卡牌定义数量
  - `completion_rate`: 收集完成度百分比
  - `rarity_stats`: 按稀有度统计

### 2. 获取所有卡牌定义

**接口地址**: `GET /cards/all`

**功能描述**: 获取系统中所有卡牌的定义信息

**请求参数**: 无

**请求示例**:
```bash
curl -X GET "http://localhost:5000/api/v1/cards/all" \
  -H "Authorization: Bearer <your_jwt_token>"
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "cards": [
      {
        "id": 1,
        "card_id": "C001",
        "name": "细胞膜",
        "description": "细胞的基本保护屏障",
        "rarity": "common",
        "image_url": "/images/cards/cell_membrane.jpg",
        "points_cost": 50,
        "drop_rate": 0.4,
        "created_at": "2024-01-01T00:00:00"
      },
      {
        "id": 6,
        "card_id": "R001",
        "name": "DNA双螺旋",
        "description": "生命的密码",
        "rarity": "rare",
        "image_url": "/images/cards/dna.jpg",
        "points_cost": 200,
        "drop_rate": 0.25,
        "created_at": "2024-01-01T00:00:00"
      }
    ],
    "total": 20
  },
  "message": "获取成功"
}
```

### 3. 单抽

**接口地址**: `POST /cards/draw/single`

**功能描述**: 消耗100积分进行单次抽奖

**请求参数**: 无

**请求示例**:
```bash
curl -X POST "http://localhost:5000/api/v1/cards/draw/single" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json"
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "card": {
      "id": 1,
      "card_id": "C001",
      "name": "细胞膜",
      "description": "细胞的基本保护屏障",
      "rarity": "common",
      "image_url": "/images/cards/cell_membrane.jpg",
      "points_cost": 50,
      "drop_rate": 0.4
    },
    "is_duplicate": false,
    "message": "恭喜获得新卡牌：细胞膜！",
    "points_spent": 100,
    "remaining_points": 50
  },
  "message": "抽卡成功！"
}
```

**响应字段说明**:
- `card`: 抽到的卡牌信息
- `is_duplicate`: 是否为重复卡牌
- `message`: 抽奖结果消息
- `points_spent`: 消耗的积分
- `remaining_points`: 剩余积分

**重复卡牌响应示例**:
```json
{
  "success": true,
  "data": {
    "card": {
      "id": 1,
      "card_id": "C001",
      "name": "细胞膜",
      "description": "细胞的基本保护屏障",
      "rarity": "common",
      "image_url": "/images/cards/cell_membrane.jpg",
      "points_cost": 50,
      "drop_rate": 0.4
    },
    "is_duplicate": true,
    "message": "抽到了重复的卡牌：细胞膜",
    "points_spent": 100,
    "remaining_points": 50
  },
  "message": "抽卡成功！"
}
```

### 4. 十连抽

**接口地址**: `POST /cards/draw/ten`

**功能描述**: 消耗900积分进行十次抽奖

**请求参数**: 无

**请求示例**:
```bash
curl -X POST "http://localhost:5000/api/v1/cards/draw/ten" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json"
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "draws": [
      {
        "card": {
          "id": 1,
          "card_id": "C001",
          "name": "细胞膜",
          "rarity": "common"
        },
        "is_duplicate": false,
        "message": "恭喜获得新卡牌：细胞膜！"
      },
      {
        "card": {
          "id": 6,
          "card_id": "R001",
          "name": "DNA双螺旋",
          "rarity": "rare"
        },
        "is_duplicate": false,
        "message": "恭喜获得新卡牌：DNA双螺旋！"
      }
    ],
    "points_spent": 900,
    "remaining_points": 100,
    "new_cards_count": 2,
    "duplicate_cards_count": 8
  },
  "message": "十连抽成功！"
}
```

**响应字段说明**:
- `draws`: 十次抽奖结果数组
- `points_spent`: 消耗的积分
- `remaining_points`: 剩余积分
- `new_cards_count`: 新卡牌数量
- `duplicate_cards_count`: 重复卡牌数量

### 5. 获取抽奖历史

**接口地址**: `GET /cards/draw/history`

**功能描述**: 获取用户抽奖历史记录

**请求参数**:
- `limit` (可选): 返回记录数量，默认50，最大200

**请求示例**:
```bash
curl -X GET "http://localhost:5000/api/v1/cards/draw/history?limit=100" \
  -H "Authorization: Bearer <your_jwt_token>"
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "history": [
      {
        "id": 1,
        "user_id": 1,
        "card_id": "C001",
        "points_spent": 100,
        "draw_type": "new",
        "created_at": "2024-01-15T08:30:00",
        "name": "细胞膜",
        "rarity": "common"
      },
      {
        "id": 2,
        "user_id": 1,
        "card_id": "C001",
        "points_spent": 100,
        "draw_type": "duplicate",
        "created_at": "2024-01-14T15:20:00",
        "name": "细胞膜",
        "rarity": "common"
      }
    ],
    "total_draws": 2
  },
  "message": "获取成功"
}
```

### 6. 获取抽奖费用

**接口地址**: `GET /cards/draw/costs`

**功能描述**: 获取抽奖费用信息

**请求参数**: 无

**请求示例**:
```bash
curl -X GET "http://localhost:5000/api/v1/cards/draw/costs" \
  -H "Authorization: Bearer <your_jwt_token>"
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "single_draw": 100,
    "ten_draw": 900,
    "ten_draw_discount": 100
  },
  "message": "获取成功"
}
```

## 管理员接口

### 7. 添加新卡牌

**接口地址**: `POST /cards/admin/add`

**功能描述**: 管理员添加新的卡牌定义

**权限要求**: 管理员权限

**请求参数**:
```json
{
  "card_id": "C006",
  "name": "核糖体",
  "description": "蛋白质合成的场所",
  "rarity": "common",
  "image_url": "/images/cards/ribosome.jpg",
  "points_cost": 50,
  "drop_rate": 0.4
}
```

**请求示例**:
```bash
curl -X POST "http://localhost:5000/api/v1/cards/admin/add" \
  -H "Authorization: Bearer <admin_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "card_id": "C006",
    "name": "核糖体",
    "description": "蛋白质合成的场所",
    "rarity": "common",
    "image_url": "/images/cards/ribosome.jpg",
    "points_cost": 50,
    "drop_rate": 0.4
  }'
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "message": "卡牌添加成功",
    "card_data": {
      "card_id": "C006",
      "name": "核糖体",
      "description": "蛋白质合成的场所",
      "rarity": "common",
      "image_url": "/images/cards/ribosome.jpg",
      "points_cost": 50,
      "drop_rate": 0.4
    }
  },
  "message": "卡牌添加成功"
}
```

### 8. 查询稀有度掉落概率（管理员）

**接口地址**: `GET /cards/admin/drop-rate`

**功能描述**: 查询各稀有度的总体掉落概率配置

**权限要求**: 管理员权限

**请求参数**: 无

**请求示例**:
```bash
curl -X GET "http://localhost:5000/api/v1/cards/admin/drop-rate" \
  -H "Authorization: Bearer <admin_jwt_token>"
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "config": {
      "common": 0.4,
      "rare": 0.25,
      "epic": 0.15,
      "legendary": 0.05
    },
    "total_rate": 0.85
  }
}
```

> 说明：`total_rate` 为配置值求和（用于归一化）。若不等于 1，系统会按比例归一使用。

### 9. 更新稀有度掉落概率（管理员）

**接口地址**: `PUT /cards/admin/drop-rate`

**功能描述**: 更新各稀有度的总体掉落概率（允许部分更新）

**权限要求**: 管理员权限

**请求参数**:
```json
{
  "common": 0.45,
  "rare": 0.25,
  "epic": 0.2,
  "legendary": 0.1
}
```

> 说明：键仅支持 `B`、`A`、`R`、`SR`、`UR`，可部分提供；非负即可，不要求和为 1。

**请求示例**:
```bash
curl -X PUT "http://localhost:5000/api/v1/cards/admin/drop-rate" \
  -H "Authorization: Bearer <admin_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "B": 0.35,
    "A": 0.25,
    "R": 0.20,
    "SR": 0.15,
    "UR": 0.05
  }'
```

**响应示例**:
```json
{
  "success": true,
  "data": {
      "config": {
    "B": 0.35,
    "A": 0.25,
    "R": 0.20,
    "SR": 0.15,
    "UR": 0.05
  },
    "total_rate": 0.95
  },
  "message": "稀有度概率已更新"
}
```

## 生物学主题卡牌列表

### B级卡牌 (B) - 基础生物学概念
- B001: 种群密度 - 种群在单位面积或单位体积中的个体数量，是生态学研究的重要参数
- B002: 协助扩散 - 物质在载体蛋白帮助下顺浓度梯度跨膜运输的过程，不消耗能量
- B003: 核糖体 - 细胞中蛋白质合成的场所，由rRNA和蛋白质组成
- B004: 细胞学说奠基 - 施莱登和施旺提出的细胞学说，奠定了现代生物学的基础

### A级卡牌 (A) - 重要生物学概念
- A001: 赤霉素 - 植物激素，促进植物生长和发育，影响种子萌发和茎的伸长
- A002: 酸碱平衡 - 生物体内pH值的相对稳定状态，对生命活动至关重要
- A003: 单基因遗传病 - 由单个基因突变引起的遗传性疾病，如白化病、血友病等
- A004: 点突变 - DNA分子中单个碱基对的改变，可能导致基因功能的改变
- A005: 程序性死亡 - 细胞在特定信号诱导下的主动死亡过程，对生物发育很重要
- A006: 主动运输 - 物质逆浓度梯度跨膜运输的过程，需要载体蛋白和能量
- A007: 生物催化剂 - 酶，生物体内催化各种生化反应的蛋白质，具有高效性和专一性
- A008: 细胞膜 - 细胞的基本保护屏障，控制物质进出，维持细胞内环境稳定
- A009: 磷脂双分子层 - 细胞膜的基本骨架，由磷脂分子排列成双层结构
- A010: 蛋白质 - 生命活动的主要承担者，参与细胞结构、代谢调节、免疫等多种功能
- A011: 叶绿体 - 植物细胞中进行光合作用的细胞器，含有叶绿素

### R级卡牌 (R) - 进阶生物学概念
- R001: 食物链 - 生物之间通过捕食关系形成的营养关系链，体现能量流动
- R002: 生长素 - 植物激素，促进细胞伸长和分化，影响植物向光性
- R003: 激素调节 - 生物体内通过激素进行的信息传递和生理调节机制
- R004: 反射弧 - 神经调节的基本结构，包括感受器、传入神经、神经中枢、传出神经和效应器
- R005: 染色体异常遗传病 - 由染色体结构或数目异常引起的遗传性疾病，如唐氏综合征
- R006: 多基因遗传病 - 由多个基因共同作用引起的遗传性疾病，如高血压、糖尿病等
- R007: 染色体结构变异 - 染色体发生断裂、缺失、重复、倒位、易位等结构改变
- R008: 分离定律 - 孟德尔第一定律，控制一对相对性状的基因在形成配子时分离
- R009: 细胞全能性 - 细胞具有发育成完整个体的潜在能力，是克隆技术的基础
- R010: 无氧呼吸 - 在无氧条件下，有机物不完全氧化分解产生能量的过程
- R011: 线粒体 - 细胞进行有氧呼吸的主要场所，被称为细胞的能量工厂
- R012: 能量货币 - ATP，细胞中储存和传递能量的主要分子

### SR级卡牌 (SR) - 高级生物学概念
- SR001: 翻译 - 以mRNA为模板，在核糖体上合成蛋白质的过程
- SR002: 食物网 - 多个食物链相互交织形成的复杂营养关系网络
- SR003: 现代生物进化理论 - 综合了自然选择、遗传变异、基因频率变化等内容的进化理论
- SR004: 染色体数目变异 - 染色体数目发生改变，如多倍体、单倍体等
- SR005: 转录 - 以DNA为模板，在RNA聚合酶催化下合成RNA的过程
- SR006: 半保留复制 - DNA复制时，每条子链都保留一条母链的复制方式
- SR007: 伴X遗传 - 基因位于X染色体上的遗传方式，如红绿色盲、血友病等
- SR008: 自由组合定律 - 孟德尔第二定律，控制不同性状的基因在形成配子时自由组合
- SR009: 有丝分裂 - 真核细胞进行细胞分裂的主要方式，保证遗传物质的准确分配
- SR010: 暗反应 - 光合作用中不依赖光的化学反应，固定CO2合成有机物
- SR011: 光反应 - 光合作用中依赖光的反应，将光能转化为化学能
- SR012: 有氧呼吸 - 在氧气参与下，有机物彻底氧化分解产生大量能量的过程

### UR级卡牌 (UR) - 顶级生物学概念
- UR001: 物质循环 - 生物圈中物质在生物与非生物环境之间的循环过程，维持生态系统的物质平衡
- UR002: 生物多样性 - 地球上所有生物种类、基因和生态系统的丰富程度，是生命进化的宝贵财富
- UR003: 能量流动 - 生态系统中能量从生产者到消费者的单向流动过程，驱动整个生命系统的运转

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 1008 | 积分不足，需要 100 积分 |
| 1010 | 获取卡牌收集失败 |
| 1011 | 获取卡牌列表失败 |
| 1012 | 抽卡失败 |
| 1013 | 获取抽奖历史失败 |
| 1014 | 获取抽奖费用失败 |
| 1015 | 添加卡牌失败 |
| 1016 | 修改掉落率失败 |
| 1009 | 权限不足 |

## 注意事项

1. 抽奖需要消耗积分，请确保积分充足
2. 重复卡牌不会重复添加到收集，但会记录在抽奖历史中
3. 十连抽比单抽更优惠，建议优先选择十连抽
4. 卡牌稀有度影响掉落率，传说卡牌最难获得
5. 所有时间均为服务器时间
6. 需要有效的JWT Token才能访问接口
7. 管理员接口需要管理员权限
