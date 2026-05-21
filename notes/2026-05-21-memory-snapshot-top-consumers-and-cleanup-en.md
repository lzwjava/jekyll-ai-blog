---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Memory Snapshot: Top Consumers and Cleanup"
translated: false
type: note
---

Here's your current memory snapshot on this 16 GB Mac:

**Free pages**: ~80 MB (very low, swapping is active)

**Top consumers now:**

| App | Memory | Action |
|-----|--------|--------|
| **Safari + WebKit** | **~3.4 GB** (15 WebContent procs) | ⚠️ Quit or close tabs |
| **WeChat** | **~1.2 GB** (16 processes) | ❌ Kill for +1.2 GB |
| Docker / nginx / Redis / PG | ~0.8 GB | Minor |
| GitHub Desktop | ~0.2 GB | Minor |
| Zed | ~0.2 GB | Minor |
| Ghostty + Python | ~0.4 GB | Your current session |
| Spotlight | ~0.1 GB (idle) | ✅ Already tamed |

**Next cleanup, ranked by impact:**

1. **Quit Safari** — closable tabs alone freed ~13.5 GB before. Currently 3.4 GB in WebKit. If you Safari (or close heavy tabs), biggest single gain.

2. **Kill WeChat** — 1.2 GB. Command:
   ```bash
   pkill -9 WeChat
   pkill -9 WeChatAppEx
   ```

3. **GitHub Desktop** — small but if unused:
   ```bash
   pkill -9 GitHub
   ```

4. **Docker** — if no containers are actively needed, `killall Docker` frees background processes too but remember Docker daemon + VM uses more than the 0.8 GB shown here (the VM allocation isn't in RSS).

The low-hanging fruit is **WeChat (1.2 GB)** and **Safari (3.4 GB)**. Want me to kill any of these?