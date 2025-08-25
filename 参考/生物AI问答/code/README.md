# 数学问答系统

这是一个基于 Vue.js 和 Flask 的前后端分离数学问答系统。

## 项目结构

```
code/
├── backend/           # Python Flask后端
│   ├── api/          # API实现
│   ├── templates/    # 模板文件
│   └── requirements.txt
│
├── frontend/         # Vue.js前端
│   ├── src/         # 源代码
│   ├── public/      # 静态资源
│   └── package.json # 依赖配置
│
└── README.md
```

## 运行说明

### 后端启动

1. 进入 backend 目录

```bash
cd backend
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 启动 Flask 服务器

```bash
python app.py
```

### 前端启动

1. 进入 frontend 目录

```bash
cd frontend
```

2. 安装依赖

```bash
npm install
```

3. 启动开发服务器

```bash
npm run dev
```

## 环境变量配置

- 后端需要设置 `MOONSHOT_API_KEY` 环境变量
- 前端的 API 地址配置在 `.env` 文件中

## 功能特性

- 数学问题解答
- 图片识别
- 历史记录管理
- 实时对话
