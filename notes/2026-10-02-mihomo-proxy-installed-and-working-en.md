---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mihomo Proxy Installed and Working
translated: false
type: note
---

Done! Here's what happened:

1. **Downloaded and installed** `mihomo-linux-amd64-v1.19.32` (60MB, x86_64, statically linked) on `192.168.1.34`
2. **Started mihomo** with your existing config at `~/.config/mihomo/config.yaml`
3. **All ports are up**:
   - `7890` — HTTP proxy ✅
   - `7891` — SOCKS proxy ✅
   - `7892` — Mixed proxy ✅
   - `9090` — External controller ✅

The proxy is working — HTTP test through port 7890 returned `200`. Logs show it's loading your rule sets and routing traffic.
