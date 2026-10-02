---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mihomo is running now
translated: false
type: note
---

Mihomo is running now! 🎉

```bash
● mihomo.service - active (running)
   Main PID: 11130
```

**Status:**
| Port | Protocol | Status |
|------|----------|--------|
| 7890 | HTTP proxy | ✅ |
| 7891 | SOCKS proxy | ✅ |
| 7892 | Mixed proxy | ✅ |
| 9090 | API controller | ✅ |

**Note:** DNS on port 53 failed (needs root) — that's fine, proxy still works.

Try the download again:
```bash
wget "https://huggingface.co/unsloth/Qwen3.8-27B-GGUF/resolve/main/Qwen3.8-27B-UD-IQ1_M.gguf?download=true"
```

If that works with proxy, you can re-enable TUN mode later by undoing the config change (restoring `tun:` section from `~/.config/mihomo/config.yaml.bak`).
