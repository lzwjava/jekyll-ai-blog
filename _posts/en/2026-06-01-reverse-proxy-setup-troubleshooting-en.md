---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reverse Proxy Setup Troubleshooting
translated: false
type: note
---

There it is:

```
Caddy config: /etc/caddy/Caddyfile
──────────────────────────────────────
:80 {
    reverse_proxy localhost:8888
}
```

Caddy is reverse proxying port 80 → `localhost:8888`. Port 8888 is the classic **Jupyter Notebook** port. The 502 means Jupyter isn't running right now.

So the flow would be:
```
Internet → :80 (Caddy) → localhost:8888 (Jupyter, currently dead)
```

This is standard AMD Dev Cloud setup — they give you Caddy as a front door to Jupyter. Not a big deal, but if you don't need Jupyter/web access, you can just stop it:

```
systemctl stop caddy && systemctl disable caddy
```

Or block port 80 with UFW. For GPT-2 training you don't need any of this — SSH is enough.
