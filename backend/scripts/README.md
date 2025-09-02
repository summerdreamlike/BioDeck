# 脚本工具包

这个目录包含了项目的各种初始化、测试和管理脚本。

## 目录结构

```
scripts/
├── __init__.py              # 包初始化文件
├── README.md               # 本说明文档
├── init_user_profile.py    # 用户画像功能初始化脚本
├── init_auth_update.py     # 认证系统更新初始化脚本
├── init_avatar.py          # 头像功能初始化脚本
├── test_user_profile.py    # 用户画像功能测试脚本
├── test_auth_update.py     # 认证系统更新测试脚本
├── test_avatar.py          # 头像功能测试脚本
├── export_db.py            # 导出 SQLite 为 dump.sql
└── import_db.py            # 导入 dump.sql 到 database.db
```

## 脚本说明

### 初始化脚本

#### `init_user_profile.py`

- **作用**: 初始化用户画像功能，创建必要的数据库表
- **运行方式**: `python scripts/init_user_profile.py`
- **功能**:
  - 创建用户画像表
  - 设置相关索引
  - 显示可用的 API 接口

#### `init_auth_update.py`

- **作用**: 更新认证系统，添加新字段和功能
- **运行方式**: `python scripts/init_auth_update.py`
- **功能**:
  - 添加学号、教职工号、班级编号字段
  - 创建刷新令牌表
  - 优化数据库索引
  - 支持多种登录方式

#### `init_avatar.py`

- **作用**: 初始化头像功能，创建必要的数据库表和目录
- **运行方式**: `python scripts/init_avatar.py`
- **功能**:
  - 添加avatar_url字段到users表
  - 创建avatar_files表记录文件信息
  - 创建头像存储目录
  - 设置相关索引

### 测试脚本

#### `test_user_profile.py`

- **作用**: 测试用户画像相关 API 功能
- **运行方式**: `python scripts/test_user_profile.py`
- **测试内容**:
  - 分析用户画像
  - 生成用户画像
  - 获取用户画像
  - 更新用户画像

#### `test_auth_update.py`

- **作用**: 测试认证系统的新功能
- **运行方式**: `python scripts/test_auth_update.py`
- **测试内容**:
  - 学生/教师注册
  - 多种方式登录
  - 自动班级分配

#### `test_avatar.py`

- **作用**: 测试头像相关API功能
- **运行方式**: `python scripts/test_avatar.py`
- **测试内容**:
  - 获取头像URL
  - 获取头像详细信息
  - 删除头像
  - 创建测试图片

## 使用流程

1. **初始化系统**:

   ```bash
   # 更新认证系统
   python scripts/init_auth_update.py

   # 初始化用户画像功能
   python scripts/init_user_profile.py
   
   # 初始化头像功能
   python scripts/init_avatar.py
   ```

2. **启动后端服务**:

   ```bash
   python app.py
   ```

3. **运行测试**:

   ```bash
   # 测试认证系统
   python scripts/test_auth_update.py

   # 测试用户画像功能
   python scripts/test_user_profile.py
   
   # 测试头像功能
   python scripts/test_avatar.py
   ```

4. **导出/导入数据库**:

   - 导出当前数据库为 SQL：

     ```bash
     python backend/scripts/export_db.py
     ```

     生成文件：`backend/scripts/dump.sql`

   - 在目标机器导入 SQL：
     ```bash
     python backend/scripts/import_db.py
     ```
     将覆盖/创建 `backend/database.db`。

## 优势

将脚本放在 `scripts/` 目录下的好处：

1. **项目结构清晰**: 根目录不再混乱
2. **职责分离**: 脚本与主程序代码分离
3. **易于维护**: 所有脚本集中管理
4. **符合规范**: 遵循 Python 项目最佳实践
5. **便于扩展**: 可以轻松添加新的脚本

## 注意事项

- 所有脚本都添加了项目根目录到 Python 路径，确保能正确导入项目模块
- 数据库路径使用相对路径，确保在不同环境下都能正常工作
- 测试脚本需要后端服务运行才能正常工作
