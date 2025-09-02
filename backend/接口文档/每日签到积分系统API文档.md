# 每日签到积分系统 API 文档

## 概述

每日签到积分系统提供用户每日签到、积分管理、历史记录查询等功能。用户通过每日签到获得积分，积分可用于卡牌抽奖等游戏化功能。

## 基础信息

- **基础URL**: `http://localhost:5000/api/v1`
- **认证方式**: JWT Token (需要在请求头中添加 `Authorization: Bearer <token>`)
- **数据格式**: JSON

## 接口列表

### 1. 获取用户签到状态

**接口地址**: `GET /daily-checkin/status`

**功能描述**: 获取用户今日签到状态、积分信息、连续签到天数等

**请求参数**: 无

**请求示例**:
```bash
curl -X GET "http://localhost:5000/api/v1/daily-checkin/status" \
  -H "Authorization: Bearer <your_jwt_token>"
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "has_checked_in_today": false,
    "today_checkin": null,
    "user_points": {
      "total_points": 150,
      "current_streak": 3,
      "longest_streak": 7,
      "points_earned_today": 0
    },
    "current_streak": 3,
    "today_points": 16,
    "next_checkin_time": "2024-01-16"
  },
  "message": "获取成功"
}
```

**响应字段说明**:
- `has_checked_in_today`: 今日是否已签到
- `today_checkin`: 今日签到记录（未签到时为null）
- `user_points`: 用户积分信息
  - `total_points`: 总积分
  - `current_streak`: 当前连续签到天数
  - `longest_streak`: 最长连续签到天数
  - `points_earned_today`: 今日获得积分
- `current_streak`: 当前连续签到天数
- `today_points`: 今日可获得的积分
- `next_checkin_time`: 下次可签到时间

### 2. 执行每日签到

**接口地址**: `POST /daily-checkin/checkin`

**功能描述**: 执行每日签到，获得积分奖励

**请求参数**: 无

**请求示例**:
```bash
curl -X POST "http://localhost:5000/api/v1/daily-checkin/checkin" \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json"
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "checkin_id": 123,
    "points_earned": 16,
    "current_streak": 4,
    "user_points": {
      "total_points": 166,
      "current_streak": 4,
      "longest_streak": 7,
      "points_earned_today": 16
    },
    "message": "签到成功！获得 16 积分 连续签到 4 天，继续加油！"
  },
  "message": "签到成功！"
}
```

**响应字段说明**:
- `checkin_id`: 签到记录ID
- `points_earned`: 本次获得的积分
- `current_streak`: 当前连续签到天数
- `user_points`: 更新后的用户积分信息
- `message`: 签到成功消息

**错误响应**:
```json
{
  "success": false,
  "error": {
    "message": "今日已签到，请明天再来",
    "code": 1001
  }
}
```

### 3. 获取签到历史

**接口地址**: `GET /daily-checkin/history`

**功能描述**: 获取用户签到历史记录

**请求参数**:
- `limit` (可选): 返回记录数量，默认30，最大100

**请求示例**:
```bash
curl -X GET "http://localhost:5000/api/v1/daily-checkin/history?limit=50" \
  -H "Authorization: Bearer <your_jwt_token>"
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "history": [
      {
        "id": 123,
        "user_id": 1,
        "checkin_date": "2024-01-15",
        "checkin_time": "2024-01-15T08:30:00",
        "points_earned": 16,
        "streak_days": 4,
        "created_at": "2024-01-15T08:30:00"
      },
      {
        "id": 122,
        "user_id": 1,
        "checkin_date": "2024-01-14",
        "checkin_time": "2024-01-14T09:15:00",
        "points_earned": 14,
        "streak_days": 3,
        "created_at": "2024-01-14T09:15:00"
      }
    ],
    "total_days": 2
  },
  "message": "获取成功"
}
```

### 4. 获取积分历史

**接口地址**: `GET /daily-checkin/point-history`

**功能描述**: 获取用户积分变化历史记录

**请求参数**:
- `limit` (可选): 返回记录数量，默认50，最大200

**请求示例**:
```bash
curl -X GET "http://localhost:5000/api/v1/daily-checkin/point-history?limit=100" \
  -H "Authorization: Bearer <your_jwt_token>"
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "history": [
      {
        "id": 456,
        "user_id": 1,
        "points_change": 16,
        "change_type": "daily_checkin",
        "description": "每日签到奖励",
        "created_at": "2024-01-15T08:30:00"
      },
      {
        "id": 455,
        "user_id": 1,
        "points_change": -100,
        "change_type": "card_draw",
        "description": "卡牌抽奖消耗",
        "created_at": "2024-01-14T15:20:00"
      }
    ],
    "total_records": 2
  },
  "message": "获取成功"
}
```

### 5. 获取积分排行榜

**接口地址**: `GET /daily-checkin/leaderboard`

**功能描述**: 获取用户积分排行榜

**请求参数**:
- `limit` (可选): 返回记录数量，默认20，最大100

**请求示例**:
```bash
curl -X GET "http://localhost:5000/api/v1/daily-checkin/leaderboard?limit=50" \
  -H "Authorization: Bearer <your_jwt_token>"
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "leaderboard": [
      {
        "user_id": 1,
        "username": "张三",
        "total_points": 500,
        "current_streak": 10,
        "rank": 1
      },
      {
        "user_id": 2,
        "username": "李四",
        "total_points": 450,
        "current_streak": 8,
        "rank": 2
      }
    ],
    "total_users": 2
  },
  "message": "获取成功"
}
```

## 管理员接口

### 6. 重置用户积分

**接口地址**: `POST /daily-checkin/reset-points/{user_id}`

**功能描述**: 管理员重置指定用户的积分

**权限要求**: 管理员权限

**请求参数**:
- `user_id`: 用户ID (路径参数)
- `points`: 新的积分值 (请求体)

**请求示例**:
```bash
curl -X POST "http://localhost:5000/api/v1/daily-checkin/reset-points/1" \
  -H "Authorization: Bearer <admin_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{"points": 100}'
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "new_points": 100
  },
  "message": "积分重置成功"
}
```

### 7. 获取签到统计

**接口地址**: `GET /daily-checkin/statistics`

**功能描述**: 获取系统签到统计信息

**权限要求**: 管理员权限

**请求示例**:
```bash
curl -X GET "http://localhost:5000/api/v1/daily-checkin/statistics" \
  -H "Authorization: Bearer <admin_jwt_token>"
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "total_users": 100,
    "today_checkins": 85,
    "total_points_distributed": 1500
  },
  "message": "获取成功"
}
```

## 积分规则

### 基础积分
- **每日签到**: 10积分
- **连续签到奖励**: 每天额外2积分（最多20积分）
- **周末奖励**: 额外5积分
- **月初奖励**: 额外20积分

### 积分计算示例
- 第1天签到: 10积分
- 第2天连续签到: 10 + 2 = 12积分
- 第3天连续签到: 10 + 4 = 14积分
- 周末连续签到: 10 + 4 + 5 = 19积分
- 月初连续签到: 10 + 4 + 20 = 34积分

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 1001 | 今日已签到，请明天再来 |
| 1002 | 签到时间还未开始 |
| 1003 | 获取签到状态失败 |
| 1004 | 签到失败 |
| 1005 | 获取签到历史失败 |
| 1006 | 获取积分历史失败 |
| 1007 | 获取排行榜失败 |
| 1008 | 积分不足 |
| 1009 | 权限不足 |

## 注意事项

1. 每个用户每天只能签到一次
2. 连续签到天数在断签后重置
3. 积分不能为负数
4. 所有时间均为服务器时间
5. 需要有效的JWT Token才能访问接口
