---
audio: false
generated: true
image: false
lang: en
layout: post
title: Direct SGLang Query Without LibreChat
translated: false
type: note
---

Question: I'm already running SGLang on my GPU box. Do I need LibreChat to serve it / talk to it, or can I query it directly?

Answer:

No, you don't need LibreChat. SGLang already *is* the server. `python -m sglang.launch_server` exposes an OpenAI-compatible HTTP endpoint on `:30000` — that's the whole serving layer. LibreChat is just an optional chat UI on top; it's a client, not a requirement.

So from your Air, tunnel and hit it directly:

```bash
ssh -L 30000:localhost:30000 gpu
```

**Raw curl** (OpenAI-compatible `/v1`):

```bash
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "default",
    "messages": [{"role":"user","content":"explain KV cache in one line"}],
    "temperature": 0.7
  }'
```

**Python — just the OpenAI SDK pointed at SGLang:**

```python
from openai import OpenAI
c = OpenAI(base_url="http://localhost:30000/v1", api_key="none")  # key ignored
r = c.chat.completions.create(
    model="default",
    messages=[{"role": "user", "content": "explain KV cache in one line"}],
)
print(r.choices[0].message.content)
```

**SGLang's native endpoint** (more control over sampling than `/v1`):

```bash
curl http://localhost:30000/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "The capital of France is", "sampling_params": {"temperature": 0, "max_new_tokens": 16}}'
```

**Check what's loaded:**

```bash
curl http://localhost:30000/get_model_info
curl http://localhost:30000/v1/models
```

---

When you'd actually *add* a UI like LibreChat / Open WebUI: only if you want a browser chat interface with history, multi-user, system-prompt presets, conversation branching — i.e. a ChatGPT-like frontend. It connects to SGLang via that same `base_url: http://gpu:30000/v1`. For your workflow (CLI, REPL, agents, scripts) it's pure overhead — curl and the OpenAI SDK are the leaner path.

One thing to expose it to your LAN without the tunnel: launch SGLang with `--host 0.0.0.0` so other machines can reach `http://192.168.x.x:30000/v1` directly. Default binds to localhost only, which is why you need the SSH forward.

If you want a lightweight local chat UI anyway, Open WebUI is one `docker run` and points at the same endpoint — say the word and I'll give you the exact command.
