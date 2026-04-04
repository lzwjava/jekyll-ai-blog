---
audio: false
generated: true
image: false
lang: en
layout: post
title: Weibo.com MTR Result Summary
translated: false
type: note
---

Here's the mtr result to **weibo.com** (49.7.37.74), 20 cycles:

| Hop | Host | Loss% | Avg (ms) | Worst (ms) |
|-----|------|-------|----------|------------|
| 1 | _gateway (local) | 0% | 9.5 | 36.8 |
| 2 | 100.69.0.1 | **30%** | 11.2 | 33.5 |
| 3–7 | ??? (no ICMP reply) | 100% | — | — |
| 8 | 36.110.248.126 | **50%** | 39.4 | 47.0 |
| 9 | 180.149.128.198 (Beijing backbone) | 0% | 40.3 | 47.5 |
| 10 | ??? | 100% | — | — |
| 11 | 180.149.137.242 | 10% | 38.5 | 41.1 |
| 12–13 | ??? | 100% | — | — |
| 14 | **49.7.37.74** (weibo.com) | 0% | 46.3 | 79.5 |

**Summary:**
- **Final hop is healthy** — 0% loss, ~46ms avg, which is reasonable to weibo.com's Beijing server.
- Hop 2 shows 30% loss and hop 8 shows 50%, but those are **router-level ICMP rate-limiting**, not real packet loss — the 0% on the destination confirms traffic gets through fine.
- The ??? hops just don't respond to ICMP (common on Chinese backbone routers).

Overall network to weibo.com looks solid. 🦞