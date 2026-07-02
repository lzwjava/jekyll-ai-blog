---
audio: false
generated: true
image: false
lang: en
layout: post
title: 12th Gen i5 System Specs
translated: false
type: note
---

Here's the full resource picture:

---

**CPU — 12th Gen Intel Core i5-12450H**

| Cores | Threads | Sockets | Current Load |
|-------|---------|---------|-------------|
| 8 cores (P+E) | 12 threads | 1 | 0.35 / 0.17 / 0.10 (idle) |

- Hybrid architecture: 4 performance-cores + 4 efficiency-cores, hyperthreaded to 12 threads
- Currently idling with negligible load — plenty of headroom

---

**Memory — 15 GiB RAM + 2 GiB Swap**

| Type | Total | Used | Available |
|------|-------|------|-----------|
| RAM | 15.4 GiB | 7.6 GiB | **7.8 GiB free** |
| Swap | 2.0 GiB | 0.1 GiB | 1.9 GiB free |

- About half of RAM is in use (browser, apps), but still ~8 GiB available for workloads
- Swap is barely touched

---

**Disk — 468 GB NVMe**

| Total | Used | Free |
|-------|------|------|
| 468 GB | 49 GB | **396 GB** |

---

**What we can run comfortably here:**

- **LLM inference** — can run small to medium models (7B-14B quantized via llama.cpp, Ollama, etc.)
- **Multiple containers / Docker** — no problem with 8 cores and 8 GB free RAM
- **Heavy compilation** (kernel, LLVM, game engines) — CPU will be the bottleneck, not RAM/disk
- **Data processing** — can handle multi-GB datasets in memory
- **Machine learning training** — fine-tuning small models or batch jobs, but no dedicated GPU (relies on CPU only)

**Limitations:**
- No dedicated GPU — no CUDA, so ML training / large model inference is CPU-bound only
- 15 GB RAM means models above ~13B parameters (even quantized) would push into swap