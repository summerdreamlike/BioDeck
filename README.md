# BioDeck

# 高中生物后台管理系统

一个基于前后端分离架构的现代化高中生物后台管理系统，用于学情监控、在线教学与资源管理（生物学科专用）。

## 技术栈

### 前端

- Vue 3
- Vue Router
- Pinia (状态管理)
- Element Plus (UI 组件库)
- ECharts (图表可视化)
- Axios (HTTP 请求)

### 后端

- Python Flask (Web 框架)
- SQLite (数据库)
- JWT (JSON Web Token 认证)
- 分层架构:
  - API 层: 路由和请求处理
  - 服务层: 业务逻辑实现
  - 模型层: 数据访问和操作
  - 工具层: 通用功能支持

## 项目结构

```
BCDMT/
├── frontend/               # 前端项目
│   ├── src/
│   │   ├── assets/         # 静态资源
│   │   ├── components/     # 可复用组件
│   │   ├── views/          # 页面视图
│   │   ├── router/         # 路由配置
│   │   ├── store/          # Pinia状态管理
│   │   ├── api/            # API接口
│   │   ├── utils/          # 工具函数
│   │   ├── App.vue         # 根组件
│   │   └── main.js         # 入口文件
│   ├── public/             # 公共资源
│   └── package.json        # 依赖配置
│
└── backend/                # 后端项目
    ├── app.py              # 应用主入口
    ├── api/                # API层
    │   └── v1/             # API版本1
    │       ├── api.py      # API路由注册
    │       └── endpoints/  # API端点
    │           ├── auth.py          # 认证相关路由
    │           ├── students.py      # 学生相关路由
    │           ├── questions.py     # 题目相关路由
    │           ├── study.py         # 学习数据路由
    │           ├── papers.py        # 试卷相关路由
    │           └── ...              # 其他功能路由
    ├── core/               # 核心功能
    │   ├── errors.py       # 错误处理
    │   ├── responses.py    # 响应格式化
    │   ├── auth.py         # 认证中间件
    │   └── helpers.py      # 辅助函数
    ├── models/             # 数据模型层
    │   ├── base.py         # 基础模型
    │   ├── user.py         # 用户模型
    │   ├── student.py      # 学生模型
    │   ├── question.py     # 题目模型
    │   └── ...             # 其他数据模型
    ├── services/           # 业务逻辑层
    │   ├── auth_service.py      # 认证服务
    │   ├── student_service.py   # 学生服务
    │   ├── question_service.py  # 题目服务
    │   ├── study_service.py     # 学习数据服务
    │   ├── paper_service.py     # 试卷服务
    │   └── ...                  # 其他业务服务
    ├── utils/              # 工具函数
    │   ├── date_utils.py   # 日期处理工具
    │   └── file_utils.py   # 文件处理工具
    ├── config/             # 配置文件
    ├── database.db         # SQLite数据库文件
    └── requirements.txt    # 依赖列表
```

## 功能模块（面向高中生物）

### 用户认证与权限管理

- 多角色支持：管理员、教师、学生
- JWT 令牌认证机制
- 基于角色的权限控制
- 教师/学生注册功能

### 学情监控

- 首页展示学生学习指数加权排名
- 学生详情页，展示学习情况与图表分析（如知识点掌握：细胞、遗传、生态等）
- 按知识点统计学习数据，生成掌握程度分析
- 错题本管理，自动收集错误作答

### 组卷中心（生物）

- 题型：单选、多选、填空、简答
- 按题型、知识点（细胞与分子、遗传与进化、生态与稳态、生命活动的调节）、难度系数筛选题目
- 智能推荐题目，基于学生薄弱知识点进行个性化推荐
- 灵活组卷功能，支持设置分值与总分

### 在线课堂

- 实时消息交流功能（基于 Socket.IO）
- 课程管理（创建、更新、删除）
- 学生举手互动功能
- 直播功能规划（支持 RTMP/HLS/WebRTC 协议，教师推流与学生观看）
- 课件同步展示

### 教学课件（生物）

- 上传与浏览教学资源（PDF、视频、音频、图片、H5 课件等）
- 分类：高一生物/高二生物/高三生物，专题如细胞与分子、遗传与进化、生态与稳态
- 标签：实验、图解、遗传图谱、显微图、生态案例、错题本等
- 资源浏览量统计
- 文件上传限制与安全控制

### 消息中心

- 学校公告、教师私信、学生留言
- 消息已读未读状态管理
- 按用户筛选消息

### 任务发布

- 发布作业/测试，设置截止时间
- 支持晚交设置
- 按班级分配任务
- 图形化统计分析（提交时间分布、分数分布、班级完成率）

### 反馈收集

- 学生满意度评价与主观建议
- 统计分析（满意度分布、按班级均值）
- 关键词提取与分析

### 考勤管理

- 多种签到方式（包括考勤码系统）
- 考勤数据导出
- 按课程筛选考勤记录
- 考勤统计分析

## 快速开始

### 前端启动

```bash
cd frontend
npm install
npm run serve
```

### 后端启动

```bash
cd backend
pip install -r requirements.txt
python app.py
```

**注意**: 确保在 backend 目录下运行，系统已修复导入路径问题，支持直接运行。

访问 http://localhost:8080 即可使用系统。

## API 文档

主要 API 端点：

- `/api/students` - 学生信息
- `/api/students/rankings` - 学生排名
- `/api/questions` - 生物题目管理
- `/api/papers` - 试卷管理
- `/api/classroom/live` - 在线课堂
- `/api/materials` - 教学资源
- `/api/messages` - 消息中心
- `/api/tasks` - 任务管理
- `/api/feedbacks` - 反馈收集
- `/api/attendance` - 考勤管理

## 数据库设计

系统使用 SQLite 数据库，包含以下主要表结构：

- `users` - 用户信息
- `students` - 学生信息
- `study_data` - 学习数据（支持按知识点维度统计：细胞、遗传、生态等）
- `questions` - 题目库（生物）
- `papers` - 试卷
- `courses` - 课程
- `materials` - 教学资源
- `messages` - 消息
- `tasks` - 任务
- `feedbacks` - 反馈
- `attendance` - 考勤记录

## 可视化图表

系统使用 ECharts 实现丰富的数据可视化功能：

- 学生学习指数趋势图
- 知识点掌握雷达图（生物知识点）
- 作业完成率统计图
- 学习时间分布热力图
- 考勤数据柱状图
- 反馈满意度饼图

## 项目亮点

1. 现代化 UI 设计：采用 Element Plus 组件库
2. 数据可视化：利用 ECharts 创建直观的数据图表
3. 状态管理：使用 Pinia 进行高效的状态管理
4. 响应式设计：适配不同屏幕尺寸的设备
5. 模块化结构：代码组织清晰，便于维护和扩展（已面向高中生物适配）
6. 分层后端架构：API 层、服务层、模型层和工具层清晰分离，提高代码可维护性
7. 统一错误处理：标准化的错误码和响应格式，提升 API 使用体验
8. 权限控制：基于 JWT 和 RBAC 的细粒度权限管理
9. 导入路径优化：修复了模块导入路径问题，确保项目可直接运行
