# 麦粽-MyZone

> 我的地盘我做主 - 个人网站导航系统

一个现代化的个人网站导航系统，支持网站分类管理、图标自定义、搜索功能等特性。采用前后端分离架构，支持多种部署方式。

## 🚀 项目特性

- **现代化界面**：基于 Vue 3 + TypeScript + Tailwind CSS 构建的响应式界面
- **多数据库支持**：支持 PostgreSQL 和 SQLite 数据库
- **Docker 部署**：完整的 Docker 容器化部署方案
- **搜索集成**：可选的 SearXNG 搜索引擎集成
- **图标管理**：支持自定义网站图标
- **分类管理**：灵活的网站分类系统
- **用户认证**：基于 JWT 的用户认证系统
- **低消耗**: Docker Sqlite方案部署，大小约260MB, 运行占用内存约72MB(飞牛OS环境)

## 🏗️ 技术架构

### 后端技术栈

- **框架**：FastAPI (Python 3.11+)
- **数据库**：PostgreSQL 16 / SQLite 3
- **ORM**：Tortoise ORM
- **认证**：JWT (JSON Web Tokens)
- **异步支持**：asyncio + uvicorn
- **容器化**：Docker + Docker Compose

### 前端技术栈

- **框架**：Vue 3 + TypeScript
- **构建工具**：Vite
- **UI 框架**：Tailwind CSS
- **状态管理**：Pinia
- **路由**：Vue Router 4
- **拖拽功能**：SortableJS + VueDraggable

### 基础设施

- **Web 服务器**：Nginx
- **数据库**：Sqlite3 / PostgreSQL 16 (可2选1)
- **搜索引擎**：SearXNG (可选)
- **容器编排**：Docker Compose

## 📦 项目结构

```txt
MyNavi/
├── backend/                # 后端服务
│   ├── app/
│   │   ├── db/             # 数据库模型
│   │   ├── routers/        # API 路由
│   │   ├── tasks/          # 后台任务
│   │   └── main.py         # 应用入口
│   ├── icons/              # 图标资源
│   └── db_data/            # 数据库文件
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/     # Vue 组件
│   │   ├── views/          # 页面视图
│   │   ├── stores/         # Pinia 状态管理
│   │   └── api/            # API 接口
│   └── dist/               # 构建输出
├── depends/                # 依赖服务配置
│   ├── nginx/              # Nginx 配置
│   ├── searxng/            # SearXNG 配置
│   └── pgdata/             # PostgreSQL 数据
├── docker-compose.yml      # Docker 编排配置
├── DockerfileBackend       # 后端 Docker 镜像
├── DockerfileFrontend      # 前端 Docker 镜像
└── env.template            # 环境变量模板
```

## 🚀 快速开始

### 环境要求

- Docker & Docker Compose
- Node.js 18+ (本地开发)
- Python 3.11+ (本地开发)

### 1. 克隆项目

```bash
git clone <repository-url>
cd MyNavi
```

### 2. 配置环境变量

```bash
cp env.template .env
# 编辑 .env 文件，配置数据库和其他参数
```

### 3. 部署方式

#### 方式一：Docker Compose 部署（推荐）

**使用 SQLite 数据库（简单部署）：**

```bash
docker-compose up -d
```

**使用 PostgreSQL 数据库：**

```bash
docker-compose --profile postgres up -d
```

**启用搜索引擎功能：**

```bash
docker-compose --profile postgres --profile searxng up -d
```

#### 方式二：本地开发

**启动后端：**

```bash
cd backend
pip install -r requirements.txt
python main.py
```

**启动前端：**

```bash
cd frontend
npm install
npm run dev
```

### 4. 访问应用

- **主应用**：http://localhost:3000 # docker部署则端口号为.env中WEB_PORT
- **API 文档**：http://localhost:8000/docs
- **搜索引擎**：http://localhost:8080 (如果启用了 SearXNG)

## ⚙️ 配置说明

### 环境变量配置

主要配置项：

```bash
# 数据库配置
DB_TYPE=postgres                    # 数据库类型：postgres 或 sqlite
POSTGRES_DB=my_navi                 # PostgreSQL 数据库名
POSTGRES_USER=its_me                # PostgreSQL 用户名
POSTGRES_PASSWORD=itsmynavidb       # PostgreSQL 密码

# 应用配置
SECRET_KEY=your-secret-key          # JWT 密钥
DEBUG=false                         # 调试模式

# 管理员配置
SUPERADMIN_NAME=admin               # 管理员用户名
SUPERADMIN_PASSWORD=your-password   # 管理员密码

# 服务端口
WEB_PORT=80                         # Web 服务端口
SEARXNG_BIND_PORT=8080              # 搜索引擎端口
```

### 数据库选择

**SQLite（自用推荐）：**

- 无需额外配置
- 数据文件存储在 `backend/db_data/` 目录
- 适合个人使用足够

**PostgreSQL：**

- 需要启动 PostgreSQL 服务

## 🔧 开发指南

### 后端开发

```bash
cd backend
# 安装依赖
uv lock && uv sync --active  # Linux
# uv lock; uv sync --active # Windows Powershell

# 数据库迁移
aerich init -t app.db.config.db_settings.config
aerich init-db

# 启动开发服务器
python -m app.main
```

### 前端开发

```bash
cd frontend
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

### API 接口

后端提供 RESTful API 接口：

- `GET /api/websites` - 获取网站列表
- `POST /api/websites` - 创建网站
- `PUT /api/websites/{id}` - 更新网站
- `DELETE /api/websites/{id}` - 删除网站
- `GET /api/categories` - 获取分类列表
- `POST /api/auth/login` - 用户登录

## 📊 功能特性

### 网站管理

- ✅ 网站添加、编辑、删除
- ✅ 网站分类管理
- ✅ 自定义网站图标
- ✅ 网站排序（拖拽）
- ✅ 网站搜索

### 用户系统

- ✅ JWT 用户认证
- ✅ 管理员权限控制
- ✅ 会话管理

### 系统功能

- ✅ 响应式设计
- ✅ 暗色/亮色主题
- ✅ 数据备份
- ✅ 健康检查

## 🐳 Docker 部署

### 服务说明

- **api**：后端 API 服务
- **web**：前端 Web 服务（Nginx）
- **db**：PostgreSQL 数据库（可选）
- **searxng**：搜索引擎（可选）

## 🔍 搜索引擎集成

项目支持集成 SearXNG 搜索引擎：

1. 启用 SearXNG 服务：

```bash
docker-compose --profile searxng up -d
```

2. 配置搜索参数：

```bash
SEARXNG_BASE_URL=http://localhost:8080/
SEARXNG_BIND_PORT=8080
```

3. Proxy：

Searxng如果需要开启Proxy，修改depengs/searxng/settings.yml第192-196行

```yml
proxies:
    http:
      - http://your_proxy_ip:proxy_port
    https:
      - http://your_proxy_ip:proxy_port
```

## 📝 更新日志

### v1.0.0
- ✅ 基础网站导航功能
- ✅ 用户认证系统
- ✅ 响应式界面设计
- ✅ Docker 容器化部署
- ✅ 多数据库支持
- ✅ 浅色深色自动模式
- ✅ 图标常规迷你聚合模式


## 📄 许可证

本项目采用 MIT 许可证。

---

**麦粽-MyZone** - 让网站导航更简单、更高效！
