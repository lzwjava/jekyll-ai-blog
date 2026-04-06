---
audio: false
generated: true
image: false
lang: en
layout: post
title: Troubleshooting Llama.cpp Segfaults
translated: false
type: note
---

From the syslog review, here's the full picture:

**OOM Kill (03:39)**
The IQ3_S instance was OOM-killed — 37.5B virtual, ~14.9GB RSS. Standard systemd-oomd behavior. Not a crash, just memory exhaustion.

**Segfaults (all in `libllama.so`)**
Three segfaults across different processes, all at the same address offset `+231000` in `libllama.so`, all on CPU 31 (core 47). That's a consistent code path — likely in attention or KV cache handling.

The segfaults happened with:
- `llama-server` (79686) — before the OOM
- `llama-server` (79767) — right after
- `llama-cli` (125576 / 125666) — the IQ2_M runs at 04:15

**Root cause suspicion:** The repeated segfaults at the same offset suggest a real bug in this build, not hardware. Could be related to the MoE expert indexing in gemma4's architecture or Flash Attention with the SWA/non-SWA mixed layers.

**Recommendations:**
1. **Rebuild llama.cpp** — `git pull && cmake --build .` to get latest fixes
2. **Or try** `--no-flash-attn` to see if that避开 the crash
3. **Watch for recurrence** — if it crashes again, the segfault is the real problem, not memory

Want me to rebuild, or try starting with `--no-flash-attn` first?