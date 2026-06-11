---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why 32 Workers Is Ideal
translated: false
type: note
---

## Why 32 is the sweet spot on your M2 Air

### The workload anatomy

Each `git fetch` does this:

```
Thread idle (99% of time)
├── DNS lookup → GitHub
├── TCP handshake → GitHub
├── SSH key exchange / TLS handshake
├── Git protocol: "what refs do you have?"
├── Git protocol: "here's a thin pack"
├── Write packfile to .git/objects/pack/
└── Thread idle again
```

The CPU does almost nothing — just SHA-1 hash verification at the end. The thread spends 99% of its time **waiting** on two things:

1. **Network round-trip to GitHub** — ~50-200ms per request from Guangzhou (through your Los Angeles proxy via DMIT/hysteria2). That's 50-200ms of pure wait where the thread is sleeping and the CPU core is free.

2. **Disk write** — your SSD writes packfiles in microseconds. Negligible.

### Why CPU cores don't matter here

Your M2 has 8 cores (4P + 4E). If this were a CPU-bound task (like video encoding), 8 threads would already saturate all cores, and 32 threads would just add context-switching overhead.

But for I/O-bound work, a thread waiting on a network packet uses **0% CPU**. It's parked in the kernel's epoll/kqueue — no scheduling, no burning cycles. So you can have 32 or 64 threads all "active" simultaneously while using maybe 2-3% total CPU.

### The math on your machine

```
160 repos × ~150ms avg network RTT (Guangzhou → LA proxy → GitHub)

With 8 workers:
  160 / 8 = 20 batches × 150ms = 3.0s theoretical minimum
  Actual: 24.1s (includes SSH setup, DNS, some slow repos)

With 32 workers:
  160 / 32 = 5 batches × 150ms = 0.75s theoretical minimum
  Actual: 9.9s (4 batches hit the slow tail)

With 64 workers:
  160 / 64 = 2.5 batches → 3 batches × 150ms = 0.45s theoretical
  Actual: 9.6s — only 0.3s faster than 32
```

### Why 64 doesn't help much

Three walls:

1. **GitHub connection throttling** — GitHub limits concurrent SSH connections per IP. Beyond ~30-40, new connections start getting queued server-side. You're hitting that wall at 32.

2. **DMIT proxy bottleneck** — your traffic routes through hysteria2 → Los Angeles → GitHub. The proxy has its own connection pool and bandwidth limits. 32 concurrent streams already saturate it.

3. **macOS file descriptor overhead** — each git process opens ~5-10 FDs (socket, packfile, index, etc.). At 32 workers that's ~200-300 FDs, well within your `ulimit -n 2560`. At 64 you're still fine, but the kernel's kqueue starts doing more work polling them.

### Why not 128 or 256?

```
Workers   Batches   GitHub queuing   Net benefit
───────   ───────   ──────────────   ───────────
   8        20         none           baseline
  32         5         minimal        2.4x faster
  64         3         moderate       2.5x faster
 128         2         heavy          ~2.5x (no gain)
 256         1         severe         possibly slower
```

At 128+, you're opening connections faster than GitHub accepts them, so they queue in the kernel's TCP backlog. You're not fetching faster — you're just moving the queue from "your thread pool" to "GitHub's rate limiter." Same wall, different queue.

### The bottom line

On a CPU-bound task, optimal workers = CPU cores (8 on your M2). On an I/O-bound task like git fetch, optimal workers = **how many concurrent network requests the remote server and your network path can handle**. For GitHub through a Los Angeles proxy from Guangzhou, that number is ~32.
