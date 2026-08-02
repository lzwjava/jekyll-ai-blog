---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Sglang 服务器完全运行
translated: true
type: note
---

sglang 进程运行正常。以下是总结：

## sglang 服务器状态 ✅

**进程：** `python3.12 -m sglang.launch_server --model-path Qwen/Qwen2.5-0.5B-Instruct --port 30010`（PID 2170342，以及 `sglang::scheduler` 和 `sglang::detokenizer` 工作进程）

**端点：** `http://127.0.0.1:30010`（仅本地访问，未对外暴露）

**模型：** `Qwen/Qwen2.5-0.5B-Instruct` — 最大上下文 32768 个 token

## 已验证功能

| 功能 | 结果 |
|---|---|
| `/v1/chat/completions` | ✅ 正确生成文本 |
| `/v1/completions` | ✅（相同 API） |
| 流式传输 (SSE) | ✅ 逐个 token 增量 |
| `/v1/models` | ✅ 列出模型 |
| `/get_model_info`、`/get_server_info` | ✅ 均有响应 |
| 吞吐量 | 5 个并发请求合计约 **615 tok/s**（0.67 秒，412 个 token） |

## 可直接使用的代码片段

**简单请求（curl）：**
```bash
curl -s http://127.0.0.1:30010/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct",
       "messages":[{"role":"user","content":"Hello!"}],
       "max_tokens":100}'
```

**从任何兼容 OpenAI 的客户端（Python、llama.cpp、LiteLLM 等）：**
```python
from openai import OpenAI
client = OpenAI(base_url="http://127.0.0.1:30010/v1", api_key="EMPTY")
resp = client.chat.completions.create(
    model="Qwen/Qwen2.5-0.5B-Instruct",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100,
)
print(resp.choices[0].message.content)
```

注意：`sglang` Python 客户端模块无法从系统 Python 中导入（只能从启动服务器的环境导入），但兼容 OpenAI 的 HTTP API 完全可用——无需特殊客户端。

你打算用它做什么？例如我可以：
- **更全面地测试性能**（延迟与并发扫描）
- **通过 `/v1/batches` 测试批量/离线处理**
- **探测 tokenizer 端点**（`/tokenize`、`/detokenize`）
- **流式传输到演示**或围绕它构建一个小脚本（例如聊天 CLI）