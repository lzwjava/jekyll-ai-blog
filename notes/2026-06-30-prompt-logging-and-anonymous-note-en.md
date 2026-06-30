---
audio: false
generated: true
image: false
lang: en
layout: post
title: Prompt logging and anonymous note
translated: false
type: note
---

All done. Here's what changed:

**server.py** — each request now logs a JSONL record to `/workspace/model/prompts.jsonl`:

```json
{
  "id": "chatcmpl-2a01cc93",
  "model": "sec-edgar-gpt-124m",
  "endpoint": "chat_completions",
  "timestamp": "2026-06-30T05:28:33.957161Z",
  "prompt": "user: What risk factors are disclosed in 10-K filings?",
  "response": "to the University of San Francisco, Michigan...",
  "usage": {"prompt_tokens": 13, "completion_tokens": 1000, "total_tokens": 1013},
  "latency_ms": 21328.5
}
```

**index.html** — system message now includes: *"Note: prompts and responses are logged anonymously for quality analysis."*

**Server restarted** with new code (PID 7167), healthy and responding. First test prompt already logged to `prompts.jsonl` (1 line, verified).

**Committed** to git as `cc10fe3`.
