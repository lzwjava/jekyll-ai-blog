---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 3080端口冲突已解决
translated: true
type: note
---

完成。✅

**发生了什么：** 端口 3080 并不是被一个游离进程占用的——是 **LibreChat** Docker 容器发布了 `0.0.0.0:3080->3080/tcp`，与你的 `dsh-app-boot`（DeepSeek 应用）冲突。

**已应用的修复：** `docker stop LibreChat` — 端口 3080 现已释放。

**备注：**
- 要恢复 LibreChat：`docker start LibreChat`
- 如果你想同时运行两者，请修改 LibreChat 在 docker-compose 中的端口映射（例如 `3081:3080`）并重新创建容器：`docker compose up -d`
- 之前来自 Chrome 的 `CLOSE_WAIT` 条目只是与旧监听器的过时连接，没有危害。

你现在可以重新运行你的 DeepSeek 应用了。