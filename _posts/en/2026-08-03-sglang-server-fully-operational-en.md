---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sglang Server Fully Operational
translated: false
type: note
---

The sglang process is fully functional. Here's the summary:

## sglang Server Status ✅

**Process:** `python3.12 -m sglang.launch_server --model-path Qwen/Qwen2.5-0.5B-Instruct --port 30010` (PID 2170342, plus `sglang::scheduler` and `sglang::detokenizer` workers)

**Endpoint:** `http://127.0.0.1:30010` (localhost only, not exposed externally)

**Model:** `Qwen/Qwen2.5-0.5B-Instruct` — max context 32768 tokens

## Verified Working

| Feature | Result |
| --- | --- |
| `/v1/chat/completions` | ✅ Generates text correctly |
| `/v1/completions` | ✅ (same API) |
| Streaming (SSE) | ✅ Token-by-token deltas |
| `/v1/models` | ✅ Lists the model |
| `/get_model_info`, `/get_server_info` | ✅ Both respond |
| Throughput | ~**615 tok/s** aggregate on 5 concurrent requests (0.67s, 412 tokens) |

## Ready-to-Use Snippets

**Simple request (curl):**

```bash
curl -s http://127.0.0.1:30010/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen/Qwen2.5-0.5B-Instruct",
       "messages":[{"role":"user","content":"Hello!"}],
       "max_tokens":100}'
```

**From any OpenAI-compatible client** (Python, llama.cpp, LiteLLM, etc.):

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

Note: the `sglang` Python client module isn't importable from the system Python (only from whatever env the server was launched in), but the OpenAI-compatible HTTP API is fully accessible — no special client needed.

What would you like to do with it? I can for example:

- **Benchmark** it more thoroughly (latency vs. concurrency sweeps)
- **Test batch/offline processing** via `/v1/batches`
- **Probe tokenizer endpoints** (`/tokenize`, `/detokenize`)
- **Stream to a demo** or build a small script around it (e.g., a chat CLI)
