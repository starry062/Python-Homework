# 管理系统

一个基于Flask的管理系统，包含用户管理、帖子管理和管理员功能。

## 技术栈

- **后端**:
  - Python 3.x
  - Flask框架
  - Flask-RESTful (API开发)
  - Flask-WTF (CSRF保护)
  - SQLite数据库

- **前端**:
  - Bootstrap 5 (CSS框架)
  - Jinja2 (模板引擎)
  - JavaScript (交互功能)

## 功能特性

### 管理员功能
- 管理员注册/登录
- 管理员信息管理

### 用户管理
- 用户数据增删改查
- 用户数据导入/导出(JSON格式)
- 用户搜索功能

### 帖子管理
- 帖子列表展示
- 帖子删除功能

## 项目结构

```
.
├── src/                    # 源代码目录
│   ├── api/                # API接口
│   ├── dao/                # 数据访问层
│   ├── po/                 # 持久化对象
│   ├── util/               # 工具类
│   ├── app.py              # 主应用文件
│   └── db.sqlite3          # 数据库文件
├── templates/              # HTML模板
│   ├── base.html           # 基础模板
│   ├── admin.html          # 管理后台
│   ├── login.html          # 登录页面
│   └── register.html       # 注册页面
└── test/                   # 测试代码
```

## 安装运行

1. 克隆仓库:
```bash
git clone [仓库地址]
cd [项目目录]
```

2. 安装依赖:
```bash
pip install -r requirements.txt
```

3. 启动服务:
```bash
python src/app.py
```

4. 访问应用:
```
http://localhost:5000
```

## API文档

### 管理员相关
- `POST /api/admin_login` - 管理员登录
- `POST /api/register` - 管理员注册
- `GET /admin_dashboard` - 管理后台

### 用户相关
- `GET /user` - 获取用户列表
- `DELETE /user` - 删除用户
- `POST /user_import_export` - 导入用户数据
- `GET /user_import_export` - 导出用户数据

### 帖子相关
- `GET /post` - 获取帖子列表
- `DELETE /post` - 删除帖子

## 前端说明

### 模板结构
- **base.html**: 基础模板，包含导航栏和公共资源
- **admin.html**: 管理后台，包含用户和帖子管理功能
- **login.html**: 登录页面
- **register.html**: 注册页面

### 主要功能
- 用户数据表格展示
- AJAX删除操作
- 表单验证
- 消息提示系统

## 截图示例

