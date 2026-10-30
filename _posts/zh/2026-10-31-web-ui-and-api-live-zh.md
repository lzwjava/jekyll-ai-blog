---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Web UI与API直播
translated: true
type: note
---

Web UI 已启动，API 也已有响应。以下是访问方式：

## 访问

| 位置 | URL |
|-------|-----|
| **本机** | http://localhost:8080 |
| **局域网（其他设备）** | **http://192.168.1.209:8080** |

只需在浏览器中打开它 — llama.cpp 自带一个内置的 chat UI 在根路径。无需额外的 frontend。

**API endpoints**（OpenAI 兼容）：
- `POST http://192.168.1.209:8080/v1/chat/completions`
- `POST http://192.168.1.209:8080/v1/completions`
- `GET  http://192.168.1.209:8080/v1/models`

## 当前状态

```
model     : Qwen2.5-7B-Instruct-Q4_K_M.gguf
backend   : ROCm / gfx900 (WX 9100), ngl=99
ctx       : 32768  (4 slots, unified KV)
listening : http://0.0.0.0:8080   (/health -> ok)
```
经过实时的 chat completion 验证 → `Hello there!`

## 管理服务器

```bash
# log
tail -f ~/projects/llama.cpp/server.log

# stop
pkill -f llama-server

# start again (detached, survives logout)
cd ~/projects/llama.cpp
setsid nohup ./build/bin/llama-server \
  -m models/Qwen2.5-7B-Instruct-Q4_K_M.gguf \
  -ngl 99 --host 0.0.0.0 --port 8080 --ctx-size 32768 \
  > server.log 2>&1 < /dev/null &
```

## ⚠️ 安全注意事项

日志警告：**未设置 API key 且 CORS 允许所有来源**。由于它绑定到 `0.0.0.0`，您局域网上的任何人都可以使用它。要锁定它，请向启动命令添加 `--api-key YOUR_SECRET`（客户端之后发送 `Authorization: Bearer YOUR_SECRET`）。如果您只需要本地访问，请改用 `--host 127.0.0.1`。