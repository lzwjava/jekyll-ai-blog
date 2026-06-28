---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang Serves Qwen2.5-1.5B
translated: false
type: note
---

SGLang is running with Qwen2.5-1.5B-Instruct. Here's the full picture:

**How it works:** SGLang serves an OpenAI-compatible API on port 30000. It's not just a raw model — it's a full inference server with the same API contract as OpenAI's `/v1/chat/completions`, `/v1/models`, etc.

**Available endpoints (all OpenAI-compatible):**
- `POST /v1/chat/completions` — chat (messages array)
- `POST /v1/completions` — raw text completion
- `GET  /v1/models` — list loaded models
- `GET  /health` — health check

**How to use it:**

1. From your Mac via SSH tunnel (so you can hit localhost):
```bash
ssh -N -L 30000:localhost:30000 lzw@192.168.1.36
# Then in another terminal:
curl http://localhost:30000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-1.5B-Instruct","messages":[{"role":"user","content":"hello"}],"max_tokens":100}'
```

2. From Python (openai SDK):
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:30000/v1", api_key="unused")
resp = client.chat.completions.create(
    model="Qwen/Qwen2.5-1.5B-Instruct",
    messages=[{"role":"user","content":"Explain transformers in 3 sentences"}],
    max_tokens=200
)
print(resp.choices[0].message.content)
```

3. Stream mode (add `"stream": true`):
```bash
curl -N http://localhost:30000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"Qwen/Qwen2.5-1.5B-Instruct","messages":[{"role":"user","content":"Write a poem"}],"max_tokens":200,"stream":true}'
```

**What SGLang adds over plain API:**
- RadixAttention — KV cache reuse across requests (prefix caching)
- CUDA graph capture — lower latency (already captured for bs 1/2/4/8)
- Continuous batching — high throughput for concurrent requests
- Fast constrained generation (JSON/regex decoding)

**Current setup:** Qwen2.5-1.5B-Instruct, 12K context (32K max), ~3 GB VRAM, leaves ~9 GB free on your RTX 4070. You could swap to a bigger model like Qwen2.5-7B if you want more quality (would use ~8 GB).

Want me to set up the SSH tunnel from your Mac, or test with a bigger model?
