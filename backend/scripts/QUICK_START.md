# 🚀 卡牌系统快速启动指南

## 📋 系统概述

这是一个完整的生物学主题卡牌收集游戏系统，包含：
- 前端：Vue.js + Element Plus
- 后端：Flask + SQLite
- 功能：积分系统、抽卡系统、卡组管理

## 🛠️ 快速启动步骤

### 1. 初始化数据库
```bash
cd backend/scripts
python init_card_system_update.py
```

**预期输出**:
```
✅ 卡牌系统更新完成！
📊 更新统计:
   - 卡牌总数: 42
   - 稀有度分布: B(4张) A(11张) R(12张) SR(12张) UR(3张)
```

### 2. 测试核心功能
```bash
python test_core_functions.py
```

**预期输出**:
```
🎉 所有核心功能测试通过！
✅ 数据库结构完整
✅ 卡牌系统正常
✅ 积分系统正常
✅ 抽卡逻辑正常
```

### 3. 启动后端服务
```bash
cd backend
python app.py
```

**预期输出**:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 4. 启动前端服务
```bash
cd frontend
npm run serve
```

**预期输出**:
```
  App running at:
  - Local:   http://localhost:8080/
  - Network: http://192.168.x.x:8080/
```

## 🎮 功能测试

### 积分系统
- ✅ 用户默认100积分
- ✅ +1000积分按钮
- ✅ 抽卡自动扣除积分
- ✅ 实时积分更新

### 抽卡系统
- ✅ 单抽：100积分
- ✅ 十抽：900积分
- ✅ 真实概率：B(35%) A(25%) R(20%) SR(15%) UR(5%)
- ✅ 抽卡动画和结果展示

### 卡组管理
- ✅ 自动保存抽卡结果
- ✅ 用户卡组库
- ✅ 卡牌详细信息显示

## 🔧 故障排除

### 常见问题

#### 1. 数据库连接错误
```bash
# 检查数据库文件
ls -la backend/database.db

# 重新初始化
python init_card_system_update.py
```

#### 2. 前端API错误
```bash
# 检查后端服务状态
curl http://localhost:5000/api/v1/cards/all

# 检查CORS配置
# 确保后端允许前端域名访问
```

#### 3. 积分系统异常
```bash
# 检查用户表结构
python test_core_functions.py

# 手动修复积分
sqlite3 backend/database.db
UPDATE users SET points = 100 WHERE points IS NULL OR points < 100;
```

### 日志查看
```bash
# 后端日志
tail -f backend/app.log

# 前端控制台
# 打开浏览器开发者工具查看Console
```

## 📊 系统配置

### 稀有度配置
| 稀有度 | 概率 | 卡牌数量 | 积分价值 |
|--------|------|----------|----------|
| B级 | 35% | 4张 | 100 |
| A级 | 25% | 11张 | 300 |
| R级 | 20% | 12张 | 600 |
| SR级 | 15% | 12张 | 1200 |
| UR级 | 5% | 3张 | 2500 |

### 抽卡费用
- **单抽**: 100积分
- **十抽**: 900积分 (优惠100积分)

### 数据库表结构
- `users`: 用户信息和积分
- `card_definitions`: 卡牌定义
- `rarity_drop_config`: 稀有度概率
- `user_cards`: 用户卡组
- `draw_history`: 抽卡历史

## 🎯 下一步开发

### 短期目标
- [ ] 添加更多卡牌类型
- [ ] 实现卡牌合成系统
- [ ] 添加成就系统

### 长期目标
- [ ] 多人对战模式
- [ ] 卡牌交易系统
- [ ] 排行榜系统

## 📞 技术支持

如果遇到问题，请：
1. 运行测试脚本检查系统状态
2. 查看日志文件定位错误
3. 检查数据库连接和表结构
4. 确认前后端服务状态

---

**祝您使用愉快！** 🎉 