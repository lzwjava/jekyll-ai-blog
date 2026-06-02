---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 面向后端与前端的 Docker Compose
translated: true
type: note
---

### 运行方式

**常规开发**（仅后端）：

```bash
cd live-server && docker compose up -d
```

→ 启动 PHP + nginx + MySQL + Redis，前端部分将被忽略。

**完整构建**（包含前端）：

```bash
cd live-server && docker compose --profile frontend up -d
```

→ 同时构建 `live-mobile-web`，将静态文件输出至共享存储卷，并由 nginx 通过 `/static/` 路径提供服务。

**本地前端开发**（热重载）：

```bash
cd live-mobile-web && npm run dev
```

→ 启动 Vite 开发服务器，默认代理至 `api.quzhiboapp.com`（或通过设置 `VITE_API_PROXY=http://localhost:8080` 以连接本地后端）。

### 关键变更

| 文件 | 说明 |
|---|---|
| `live-server/docker-compose.yml` | 新增 `frontend` 服务（按配置文件启用）、挂载至 nginx 的 `frontend-dist` 共享存储卷 |
| `live-server/nginx.conf` | 新增 `/static/` 路径配置，附带不可变缓存头设置 |
| `live-mobile-web/.env.production` | 设置 `VITE_API_BASE_URL=/api` 使生产版本请求指向 nginx |
| `live-mobile-web/vite.config.js` | 代理目标现使用 `VITE_API_PROXY` 环境变量（默认值为 `api.quzhiboapp.com`） |

代码库保持独立，通过单一编排文件协调两端。🦞
