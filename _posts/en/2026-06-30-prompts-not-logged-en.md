---
audio: false
generated: true
image: false
lang: en
layout: post
title: Prompts Not Logged
translated: false
type: note
---

No, the prompts are **not saved.** The server receives them in memory, processes, returns, and forgets. The only logs are uvicorn's default HTTP line — method, path, IP, status code. No request body, no prompt text, no output.

```
INFO: 100.64.1.99:57138 - "POST /v1/chat/completions HTTP/1.1" 200 OK
```

That's all that's recorded. No idea what they typed.

The 2 `400 Bad Request` also don't show the body — just `400` status, no detail logged.

---

Want me to add prompt logging? I can patch `server.py` to log the user's message text (and the generated output) to a file. That way next time you'll know what people are actually asking. Something like:

- `prompts.log` — timestamp + user message + first ~200 chars of output
- Or a JSONL file with full request/response pairs

Privacy call: since you shared this to company WeChat groups, logging prompts means you'd be storing what colleagues typed. Up to you.
