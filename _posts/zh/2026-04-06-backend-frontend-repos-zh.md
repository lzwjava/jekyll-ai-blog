---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 后端与前端独立代码库
translated: true
type: note
---

问题：考虑到所描述的架构，你认为将 `live-server`（PHP/CodeIgniter 4 后端）和 `live-mobile-web`（Vue 3 前端）保持为独立的代码库，还是将它们合并，哪种方式更好？

答案：

我完全赞同这个分析。以下是我的结构化看法：

---

## ✅ 保持分离 — 正确的选择

### 为何分离是正确的

**不同的运行时，不同的关注点：**
- `live-server` = PHP 8 + CodeIgniter 4 — 有状态、连接数据库、处理业务逻辑
- `live-mobile-web` = Node.js/Vite + Vue 3 — 无状态构建工具，输出纯静态资源

将这两者混合在同一个代码库中会带来最糟糕的结果：PHP 开发者会因 `node_modules` 而困扰，前端开发者则对 Composer 文件感到困惑。

**独立的部署周期很重要：**
- 修复一个 UI 错误 → 重新构建 Vue → 推送静态文件。后端无需变动。
- 修补支付 API → 重新部署 PHP。前端无需变动。
- 这正是解耦的全部意义所在。

**设计上已经解耦：**
- Vite 代理（`/api → api.quzhiboapp.com`）证明前端并不关心后端运行在何处
- 生产环境中的 nginx 是唯一的“粘合剂” — 并且这属于 `live-server` 的配置，而非前端代码库

---

## 🏗️ 推荐的架构

最简洁的生产环境设置：

```
live-server/
├── docker-compose.yml        ← 协调所有服务
├── nginx/
│   └── default.conf          ← 提供静态文件 + 将 /api 代理至 php-fpm
├── public/
│   └── (Vue 构建输出存放于此)
└── ...PHP/CI4 应用...
```

**docker-compose.yml** 添加一个前端构建阶段：

```yaml
services:
  frontend-builder:
    image: node:20-alpine
    working_dir: /app
    volumes:
      - ../live-mobile-web:/app          # 挂载同级代码库
      - ./public:/app/dist               # 输出至 live-server/public
    command: sh -c "npm ci && npm run build"

  php-fpm:
    build: .
    depends_on:
      - mysql
      - redis

  nginx:
    image: nginx:alpine
    volumes:
      - ./public:/var/www/html/public    # 提供 Vue 静态文件
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - php-fpm
      - frontend-builder
```

这样做的优势：
- **代码库保持分离** — 无需合并代码
- **一个 `docker-compose up`** 即可构建所有内容并相互连接
- **nginx 同时提供** 静态 Vue 资源和代理的 PHP API — 来自同一个容器

---

## 🚫 应避免的做法

| 诱惑 | 为何不佳 |
|---|---|
| 合并为单体代码库 | 依赖地狱，CI/CD 混乱，单点故障 |
| 在生产环境中通过单独的 Node.js 服务器提供 Vue | 不必要的额外进程 — nginx 已经能完美处理静态文件 |
| 在 Vue 生产构建中硬编码 `api.quzhiboapp.com` | 应使用环境变量（`VITE_API_BASE_URL`），在构建时注入 |

---

## 💡 值得添加的一项改进

确保你的 Vue 构建正确使用环境变量：

```env
# live-mobile-web/.env.production
VITE_API_BASE_URL=/api
```

```javascript
// vite.config.js — 仅在开发环境需要
proxy: {
  '/api': { target: 'http://localhost:8080', changeOrigin: true }
}
```

在生产环境中，`/api` 由 nginx 直接处理 — 无需 Vite 代理介入。这保持了清晰的分离。

---

**总结：** 该架构是合理的。采用 Docker 编排方案（构建前端 → 放入 `live-server/public` → nginx 提供所有服务）是务实的最佳选择 — 一个部署命令，无需合并代码库，保持清晰的分离。
