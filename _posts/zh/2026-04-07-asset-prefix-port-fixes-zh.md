---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 资产前缀与端口修复
translated: true
type: note
---

以下是两个仓库的全部变更总结：

### live-mobile-web（3处变更）

1. **`vite.config.js`** — 添加了 `base: process.env.VITE_BASE_URL || '/'`，使构建输出使用正确的资源路径前缀
2. **`.env.production`** — 添加了 `VITE_BASE_URL=/static/`，让生产环境构建的资源解析路径位于 `/static/` 下
3. **`src/router/index.js`** — 修复 Vue Router 4 的全匹配路由：`'*'` 改为 `'/:pathMatch(.*)*'`

### live-server（2处变更）

1. **`docker-compose.yml`（前端服务）** — 添加环境变量 `VITE_BASE_URL=/static/`，使其在 Docker 构建期间可用
2. **`docker-compose.yml`（应用服务）** — 端口映射从 `8081:80` 改为 `8082:80`（8081 已被 llama-server 占用）

需要我提交并推送这两个仓库吗？🦞