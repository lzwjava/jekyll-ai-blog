---
audio: false
date: 2025-09-09
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 在LibreChat中设置OPENAI_REVERSE_PROXY
translated: true
type: note
---

明白了 👍 你正在编辑 LibreChat 的 `.env` 文件。
这个文件正是你设置 `OPENAI_REVERSE_PROXY` 的地方。

---

### 1. 该变量的作用

`OPENAI_REVERSE_PROXY` 用于让 LibreChat 将 OpenAI API 请求通过代理服务器路由（例如，如果你运行了一个自托管的反向代理来添加日志记录、缓存、区域路由，或绕过某些限制）。

---

### 2. 如何设置

在你的 `.env` 文件中，只需将其分配为你的反向代理的基础 URL。例如：

```ini
OPENAI_REVERSE_PROXY=https://your-proxy.example.com/v1
```

注意事项：

* URL 应指向模拟 OpenAI `/v1` API 的代理端点。
* 除非你的代理要求，否则不要包含末尾的 `/`。
* 如果不使用代理，请保持为空（`OPENAI_REVERSE_PROXY=`）。

---

### 3. 应用更改

编辑 `.env` 后，重启你的 LibreChat 容器以使新值生效：

```bash
docker compose down
docker compose up -d --force-recreate
```

---

### 4. 验证

你可以在运行的容器内检查：

```bash
docker compose exec librechat env | grep OPENAI_REVERSE_PROXY
```

它应该显示你设置的值。

---

你是否已经有了一个反向代理 URL（例如 `https://openrouter.ai/api/v1` 或你自己的 Nginx 实例），或者需要我为你展示如何为 LibreChat **设置一个反向代理**？
