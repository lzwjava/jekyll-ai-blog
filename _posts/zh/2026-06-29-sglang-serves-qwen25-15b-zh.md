---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang 服务 Qwen2.5-1.5B
translated: true
type: note
---

SGLang 正在运行 Qwen2.5-1.5B-Instruct 模型。以下是完整的情况说明：

**工作原理：** SGLang 在 30000 端口提供 OpenAI 兼容的 API。它不仅仅是原始模型——它是一个完整的推理服务器，使用与 OpenAI 相同的 `/v1/chat/completions`、`/v1/models` 等 API 协议。

**可用的端点（全部兼容 OpenAI）：**
- `POST /v1/chat/completions` — 聊天（消息数组）
- `POST /v1/completions` — 原始文本补全
- `GET  /v1/models` — 列出已加载的模型
- `GET  /health` — 健康检查

**使用方法：**

1. 通过 Mac 的 SSH 隧道（这样可以在本地访问）：
```bash
ssh -N -L 30000:localhost:30000 lzw@192.168.1.36
# 然后在另一个终端中：
curl http://localhost:30000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-1.5B-Instruct","messages":[{"role":"user","content":"你好"}],"max_tokens":100}'
```

2. 通过 Python（使用 OpenAI SDK）：
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:30000/v1", api_key="未使用")
resp = client.chat.completions.create(
    model="Qwen/Qwen2.5-1.5B-Instruct",
    messages=[{"role":"user","content":"用三句话解释Transformer"}],
    max_tokens=200
)
print(resp.choices[0].message.content)
```

3. 流式模式（添加 `"stream": true`）：
```bash
curl -N http://localhost:30000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-1.5B-Instruct","messages":[{"role":"user","content":"写一首诗"}],"max_tokens":200,"stream":true}'
```

**SGLang 相比普通 API 的增强功能：**
- RadixAttention — 跨请求的 KV 缓存复用（前缀缓存）
- CUDA 图形捕获 — 更低延迟（已为 bs 1/2/4/8 捕获）
- 连续批处理 — 高并发请求的高吞吐量
- 快速约束生成（JSON/正则表达式解码）

**当前配置：** Qwen2.5-1.5B-Instruct，12K 上下文（最大 32K），占用约 3 GB 显存，RTX 4070 上剩余约 9 GB 可用。如果您想要更高品质，可以换成更大的模型，如 Qwen2.5-7B（将占用约 8 GB 显存）。

需要我帮您从 Mac 设置 SSH 隧道，或者测试更大的模型吗？