---
audio: false
generated: true
image: false
lang: en
layout: post
title: Server Outbound HTTPS Traffic Blocked
translated: false
type: note
---

Here's what happened, Boss:

**Root Cause:**
The server's direct HTTPS outbound traffic is blocked (firewall DROP policy). Only ICMP (ping) and HTTP through the proxy works. The connection to HuggingFace goes through a SOCKS5 proxy at `127.0.0.1:7891` (proxychains).

**Why it kept stopping:**
1. **Unstable proxy connection** — The proxy link between your server and HuggingFace isn't stable for large files. It kept timing out or getting dropped.
2. **No connection persistence** — Each resume started fresh but hit the same instability. Around 2-3GB in, something would break (proxy timeout, connection reset, etc.).
3. **Single-threaded download** — `curl` doesn't handle proxy failures gracefully. No auto-retry logic built in.

**Possible fixes if you want to download on server:**
- Use `axel` or `lftp` for multi-threaded downloads with better retry
- Use `wget` with a persistent proxy session
- Or download on your side and `scp` the file over

For now, since the download is failing repeatedly from here, your best bet is to download it wherever you have good connectivity (your laptop, etc.) and transfer it via `scp`:

```bash
scp gemma-4-26B-A4B-it-UD-IQ3_S.gguf lzw@192.168.1.36:/tmp/
```

Want me to prepare the install steps so we can move fast once the file arrives?
