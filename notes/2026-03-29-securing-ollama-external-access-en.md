---
audio: false
generated: true
image: false
lang: en
layout: post
title: Securing Ollama External Access Guide
translated: false
type: note
---

## 🦞 Review: Ollama External Access

**What we did:**
1. Set `OLLAMA_HOST=0.0.0.0:11434` in the systemd service
2. Restarted Ollama — now listening on `*:11434`
3. Confirmed firewall is inactive (no blocks)

**The good:**
- Simple, one-line config change
- Works immediately — no proxy layer to maintain
- Direct API access from anywhere

**The risks:**
- **No authentication** — anyone who finds the port can use your H100 for free. GPU time isn't cheap.
- **No TLS** — traffic is plaintext. Prompts/responses visible to anyone on the wire.
- **No rate limiting** — a bad actor could max out your GPU and spike your cloud bill.
- **Port scanning** — bots will find 11434 fast. It's a known Ollama default.

**What I'd recommend (sooner, not later):**
1. **Quick fix** — `ufw allow from <your-ip> to any port 11434` to whitelist just your IPs
2. **Better** — nginx reverse proxy with basic auth + HTTPS (Let's Encrypt)
3. **Best** — Cloudflare Tunnel or Tailscale. Zero open ports, encrypted, authenticated

For personal dev work over the next few hours? You're probably fine. For anything longer-term or production? Lock it down.

Want me to set up any of those?
