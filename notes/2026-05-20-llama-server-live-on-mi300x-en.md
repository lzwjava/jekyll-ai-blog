---
audio: false
generated: true
image: false
lang: en
layout: post
title: Llama Server Live on MI300X
translated: false
type: note
---

**Server is live!** Here's the full status:

---

## llama-server: Running on Port 8080

**Model:** Qwen3.5-122B-A10B-UD-IQ1_M (122B total / ~10B active MoE)
**File size:** 37 GB (IQ1_M quantization)
**VRAM:** 196,288 MiB total / 194,606 MiB free — plenty of room

### Performance

| Metric | Speed |
|---|---|
| Prompt processing | **77.4 t/s** |
| Token generation | **91.2 t/s** |

### Server Config

| Setting | Value |
|---|---|
| Context | 32,768 tokens (4 slots) |
| GPU layers | 99 (all on MI300X) |
| Threads | 16 |
| Memory | mlocked (no swapping) |
| API | OpenAI-compatible at `http://165.245.137.138:8080/v1` |
| Process PID | 292080 |

### API Usage

```bash
curl http://165.245.137.138:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "Qwen3.5-122B-A10B-UD-IQ1_M",
    "messages": [{"role": "user", "content": "Your prompt here"}],
    "max_tokens": 500
  }'
```

The model loaded with reasoning/thinking capability enabled (Qwen3.5's default) — you'll get chain-of-thought in `reasoning_content` before the final answer. With 91 t/s generation on a 122B MoE, the MI300X is running very strong here.
