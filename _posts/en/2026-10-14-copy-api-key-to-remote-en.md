---
audio: false
generated: true
image: false
lang: en
layout: post
title: Copy API key to remote?
translated: false
type: note
---

Done — `settings.json` copied and verified on the remote:

```json
{
  "lastChangelogVersion": "1.2.0",
  "theme": "dark",
  "defaultProvider": "openrouter",
  "defaultModel": "xiaomi/mimo-v2.6-flash",
  "hideThinkingBlock": false,
  "defaultThinkingLevel": "high"
}
```

`pi --version` still reports 1.2.0 after the copy.

**Remaining: credentials.** Your local machine gets `OPENROUTER_API_KEY` from `~/.bashrc` (and `auth.json` is empty `{}` — so the key is the only credential). The remote has none, so `/model` will show no usable models until one of these exists:

1. **I copy the key** — I'd extract `OPENROUTER_API_KEY` from your local `~/.bashrc` and append it to `lzw@192.168.1.137:~/.bashrc` with `chmod 600` semantics (it's your key, your machine). Say the word.
2. **You set it yourself** over there: `echo 'export OPENROUTER_API_KEY=...' >> ~/.bashrc`
3. **Interactive `/login`** on the remote instead (stores it in `auth.json`).

Want me to do option 1?
