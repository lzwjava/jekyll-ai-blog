---
audio: false
generated: true
image: false
lang: en
layout: post
title: Inference Backend Detection Tool
translated: false
type: note
---

Done. Here's what was built:

**`ww inference test`** — SGLang vs vLLM backend detection

**Detection logic** (based on the info you shared):
| Signal | SGLang | vLLM |
|--------|--------|------|
| `id` field | Bare 32-char hex string | `chatcmpl-...` prefix |
| Streaming `delta` | `reasoning` key (deep thinking models) | `reasoning_content` key |
| Server header | `sglang` or absent | `uvicorn` (typical) |

**Tests run:**
1. **Streaming detection** — inspects first chunk's `id`, `delta` keys, and TTFT
2. **Server header** — checks `Server` and `X-Powered-By` headers
3. **Prefix cache** — two requests with shared 200-line prefix, compares TTFT drop

**Usage:**
```
ww inference test                          # default: tencent/hy3-preview
ww inference test --no-prefix-cache        # skip prefix cache test
ww inference test --model openai/gpt-4o-mini
```

The code is committed (153a1b4). Run it from your terminal where `OPENROUTER_API_KEY` is available to get real results.