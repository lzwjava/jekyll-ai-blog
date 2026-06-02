---
audio: false
date: 2025-09-09
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Setting OPENAI_REVERSE_PROXY in LibreChat
translated: false
type: note
---

Got it 👍 You’re editing LibreChat’s `.env`.
That file is exactly where you set `OPENAI_REVERSE_PROXY`.

---

### 1. What the variable does

`OPENAI_REVERSE_PROXY` is used if you want LibreChat to route OpenAI API requests through a proxy server (for example, if you run a self-hosted reverse proxy to add logging, caching, regional routing, or to bypass restrictions).

---

### 2. How to set it

In your `.env`, just assign it the base URL of your reverse proxy. For example:

```ini
OPENAI_REVERSE_PROXY=https://your-proxy.example.com/v1
```

Notes:

* The URL should point to your proxy endpoint that mimics OpenAI’s `/v1` API.
* Don’t include trailing `/` unless your proxy requires it.
* Keep it empty (`OPENAI_REVERSE_PROXY=`) if you don’t use a proxy.

---

### 3. Apply the changes

After editing `.env`, restart your LibreChat containers so they pick up the new value:

```bash
docker compose down
docker compose up -d --force-recreate
```

---

### 4. Verify

You can check inside the running container:

```bash
docker compose exec librechat env | grep OPENAI_REVERSE_PROXY
```

It should show the value you set.

---

Do you already have a reverse proxy URL (like `https://openrouter.ai/api/v1` or your own Nginx instance), or do you want me to show you how to **set one up** for LibreChat?
