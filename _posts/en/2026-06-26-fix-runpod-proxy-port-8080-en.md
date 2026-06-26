---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix RunPod Proxy Port 8080
translated: false
type: note
---

The proxy isn't reaching the server — no proxy requests appear in the log (only localhost). Port 8080 needs to be exposed in RunPod pod settings.

**Fix:** In RunPod dashboard → your pod → Settings → edit "Exposed HTTP Ports" → add `8080` → save. Then the proxy URL will work.

**Quick workaround** — use SSH tunnel from your Mac:

```bash
ssh -p 28484 -i ~/.ssh/id_ed25519 -L 8080:localhost:8080 root@213.173.110.200 -N
```

Then access `http://localhost:8080/health` in your browser.
