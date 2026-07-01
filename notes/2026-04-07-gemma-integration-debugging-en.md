---
audio: false
generated: true
image: false
lang: en
layout: post
title: Gemma Integration Debugging Steps
translated: false
type: note
---

## Root cause summary

There were three layered issues preventing Gemma from working in OpenClaw:

### 1. llama-server not running

The OpenClaw config referenced `llama-server` provider at `http://192.168.1.36:8081/v1`, but no process was listening. The old `~/llama.sh` starts a different model on port 8000.

### 2. Gemma 4's thinking mode

Once started, llama-server's `--reasoning auto` detected Gemma 4's thinking template and split output into `reasoning_content` (with the actual text) and `content` (empty). OpenClaw reads `content`, so it got blank responses. Fixed with `--reasoning off`.

### 3. llama-server binding + proxychains routing (the real blocker)

This was the tricky one. Two things combined:

- llama-server defaults to binding on `127.0.0.1` only, so `http://192.168.1.36:8081` was unreachable even from the same machine
- OpenClaw gateway runs under `proxychains4` (routing through mihomo/Clash at `127.0.0.1:7891`). Even after enabling `localnet 192.168.0.0/255.255.0.0`, the connection still failed because the destination port wasn't actually open on that interface

We couldn't use `localnet 127.0.0.0/255.0.0.0` to bypass loopback because that would break the SOCKS5 proxy itself (mihomo listens on `127.0.0.1:7891`).

The fix: start llama-server with `--host 0.0.0.0` so it listens on all interfaces, keep the baseUrl as `http://192.168.1.36:8081/v1`, and let the proxychains localnet exclusion bypass the proxy for `192.168.x.x` traffic.

### Final working command

```bash
nohup /home/lzw/projects/llama.cpp/build/bin/llama-server \
  -m /home/lzw/projects/llama.cpp/models/gemma-4-26B-A4B-it-UD-IQ3_S.gguf \
  --port 8081 --host 0.0.0.0 -c 32768 --reasoning off \
  >> /home/lzw/llama-server.log 2>&1 &
```

### Changes made on the server

| What | Change |
| ------ | -------- |
| `/etc/proxychains4.conf` | Uncommented `localnet 192.168.0.0/255.255.0.0` |
| `~/.openclaw/openclaw.json` | baseUrl was temporarily changed to `127.0.0.1`, reverted back to `192.168.1.36` |
| openclaw-gateway | Restarted via systemctl |

### Still not persistent

llama-server was started manually with `nohup`. It won't survive a reboot. Consider updating `~/llama.sh` or creating a systemd user service for it.
