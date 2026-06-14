---
audio: false
generated: true
image: false
lang: en
layout: post
title: Serving Fine-Tuned Model via llama.cpp
translated: false
type: note
---

Here's the full story of serving your fine-tuned model:

**Problem:** Your ollama binary was corrupted (segfaulting, missing ELF section headers). Reinstalling ollama fixed it, but you wanted llama.cpp instead.

**What I did:**

1. **Found llama.cpp** already built at ~/projects/llama.cpp/ with both `llama-server` and `llama-cli` binaries ready.

2. **Started llama-server** with these flags:
   - `--model` — your Q4_K_M GGUF (2.4GB)
   - `--host 0.0.0.0 --port 8080` — accessible on all interfaces
   - `--n-gpu-layers 999` — offload everything to your RTX 4070
   - `--ctx-size 4096` — matching your training max_seq_len
   - `--threads $(nproc)` — use all CPU cores for any non-GPU work

3. **Verified it works** — health check returns `{"status":"ok"}`, and a test prompt ("The Art of Slow Living") produced a coherent blog-style article at ~140 tokens/sec.

**Your serving setup:**

```
GGUF file (2.4GB, Q4_K_M)
    → llama-server on localhost:8080
    → OpenAI-compatible API
    → Full GPU offload on RTX 4070
```

**Endpoints:**

- `POST http://localhost:8080/v1/chat/completions` — drop-in OpenAI replacement
- `POST http://localhost:8080/completion` — raw text completion
- `GET http://localhost:8080/health` — status check

**How to use it:**

```bash
# Chat completion (like OpenAI API)
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Your blog title here"}],"max_tokens":500}'

# Or point any OpenAI-compatible client at http://localhost:8080/v1
```

**To stop:** `kill 1838246`
