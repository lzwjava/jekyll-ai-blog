---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 保持后端与前端分离
translated: true
type: note
---

现在我完全理解了。我的看法是：

---

**保持二者独立**。理由如下：

**它们在本质上是不同的东西：**

- **live-server** = PHP 后端 (CodeIgniter 4) —— 负责 REST API、数据库、微信集成、RTMP 挂钩、支付
- **live-mobile-web** = Vue 3 前端 —— 移动端网页界面，通过 `/api` 代理调用后端 API

**当前的协作方式：**

- `live-mobile-web` 通过 `/api` 代理到开发环境的 `api.quzhiboapp.com`（通过 Vite 代理）
- 生产环境中，nginx 负责提供 Vue 静态构建产物，并将 `/api` 请求代理到 PHP 后端
- 它们已经解耦 —— 前端构建不需要后端代码

**为何合并会带来问题：**

- 在同一个代码仓库混合 PHP 和 Node.js 会导致依赖管理混乱、构建过程不清晰
- 它们有不同的部署周期（更新 UI 时无需重新部署后端）
- 不同的运行环境、不同的 Docker 镜像、不同的扩展需求

**你应该采取的做法：**

1. **在更高层级（或 `live-server` 中）使用一个 `docker-compose.yml`** 来编排两者：
   - `live-server` 已经具备 nginx 配置，可以托管 Vue 静态构建产物
   - 只需添加一个构建步骤：构建 `live-mobile-web` → 输出到 `live-server/public/` → nginx 统一提供服务

2. **或者维持现有仓库结构，分别部署：**
   - `live-server` → Docker：PHP-FPM + nginx + MySQL + Redis（已配置）
   - `live-mobile-web` → 构建静态产物 → 复制到 nginx 静态目录（或通过 CDN 分发）

最简单的路径是：**扩展 `live-server` 的 Docker 配置，使其构建并包含前端** —— 在 Dockerfile 中添加一个阶段，或在 docker-compose 中添加一个 `frontend` 服务来构建 Vue 应用，并通过卷共享输出。无需合并仓库。

需要我来设置这个方案吗？
