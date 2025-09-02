# 卡牌抽奖系统 API 文档

## 概述

卡牌抽奖系统提供生物学主题的卡牌收集游戏功能。用户使用签到获得的积分进行抽奖，收集不同稀有度的生物学卡牌。

## 基础信息

- **基础URL**: `http://localhost:5000/api/v1`
- **认证方式**: JWT Token (需要在请求头中添加 `Authorization: Bearer <token>`)
- **数据格式**: JSON

## 卡牌系统说明

### 卡牌稀有度
- **普通卡牌 (Common)**: 40%掉落率，50积分价值
- **稀有卡牌 (Rare)**: 25%掉落率，200积分价值
- **史诗卡牌 (Epic)**: 15%掉落率，500积分价值
- **传说卡牌 (Legendary)**: 5%掉落率，1000积分价值

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

### 8. 修改卡牌掉落率

**接口地址**: `PUT /cards/admin/drop-rate`

**功能描述**: 管理员修改卡牌的掉落率

**权限要求**: 管理员权限

**请求参数**:
```json
{
  "card_id": "C001",
  "new_drop_rate": 0.5
}
```

**请求示例**:
```bash
curl -X PUT "http://localhost:5000/api/v1/cards/admin/drop-rate" \
  -H "Authorization: Bearer <admin_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "card_id": "C001",
    "new_drop_rate": 0.5
  }'
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "message": "掉落率修改成功",
    "modification": {
      "card_id": "C001",
      "new_drop_rate": 0.5
    }
  },
  "message": "掉落率修改成功"
}
```

## 生物学主题卡牌列表

### 普通卡牌 (Common)
- C001: 细胞膜 - 细胞的基本保护屏障
- C002: 线粒体 - 细胞的能量工厂
- C003: 细胞核 - 细胞的指挥中心
- C004: 叶绿体 - 植物细胞的绿色工厂
- C005: 高尔基体 - 细胞的包装中心

### 稀有卡牌 (Rare)
- R001: DNA双螺旋 - 生命的密码
- R002: 蛋白质合成 - 生命的制造过程
- R003: 细胞分裂 - 生命的延续
- R004: 光合作用 - 阳光的能量转换
- R005: 呼吸作用 - 能量的释放

### 史诗卡牌 (Epic)
- E001: 基因突变 - 进化的源泉
- E002: 自然选择 - 适者生存
- E003: 生态系统 - 生命的网络
- E004: 生物多样性 - 地球的财富
- E005: 进化论 - 生命的历史

### 传说卡牌 (Legendary)
- L001: 生命起源 - 最初的奇迹
- L002: 智慧生命 - 意识的觉醒
- L003: 宇宙生命 - 无限的可能
- L004: 永恒生命 - 不灭的传说
- L005: 创世神卡 - 生物学的终极奥秘

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
