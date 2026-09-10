---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 嵌入在llama-server中的Web UI
translated: true
type: note
---

在此构建版本（b10894）中，没有单独的 `llama-web` 二进制文件——Web UI 现在直接嵌入在 `llama-server` 中。因此运行服务器 *就是* 运行 Web UI。

**现已上线：** http://127.0.0.1:8080

```
模型      : models/Qwen3-8B-abliterated-q4_k_m.gguf (Q4_K_M)
GPU        : llama-server 使用了 5896 MiB 显存（完全卸载，-ngl 99）
上下文    : 8192（4个 slots）
健康检查  : {"status":"ok"}
Web UI    : HTTP 200（从 / 提供嵌入式 UI）
```

已验证 API 和 UI：
- `POST /v1/chat/completions` -> `{"content":"hi"}` 正确
- `GET /` -> HTTP 200，提供 Svelte 包

如果单独运行 `curl http://127.0.0.1:8080/` 返回 **415**，请不要惊慌——这是预期的。UI 仅支持 gzip；普通浏览器总会发送 `Accept-Encoding: gzip`，因此它能正常加载。使用 `curl --compressed` 也可以。

管理方式：
```bash
# 日志
tail -f /tmp/llama-server.log
# 停止
kill 3981052
# 重启
cd /mnt/data/llama.cpp && ./build/bin/llama-server -m models/Qwen3-8B-abliterated-q4_k_m.gguf -ngl 99 -c 8192 --host 127.0.0.1 --port 8080
```

要从另一台机器访问，请绑定 `--host 0.0.0.0`（注意：日志警告 CORS 为 `*` 且没有 API 密钥——在公开之前请设置 `--api-key`）。