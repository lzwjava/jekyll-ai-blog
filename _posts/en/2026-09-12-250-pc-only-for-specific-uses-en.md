---
audio: false
generated: true
image: false
lang: en
layout: post
title: "¥250 PC: Only for Specific Uses"
translated: false
type: note
---

Question: Is this **¥250 used PC** worth buying?

Answer: **For ¥250, yes — but only for very specific use cases.**

The hardware is ancient:

* **Xeon L5640** — 6C/12T, Westmere, ~2010. Fine for basic Linux/server work, but very weak single-core performance.
* **16 GB RAM** — actually useful for a cheap home server.
* **GT 620** — basically irrelevant today; don't buy it for GPU compute.
* **2×120 GB SSD** — this is the biggest red flag. The seller explicitly says the second SSD is dying.
* **1×100 Mbps + 1×1 Gbps NIC** — surprisingly useful for a cheap router/NAS/lab box.
* **¥250 shipped** — low enough that the machine itself is almost disposable.

### What I'd use it for

**Good:**

* Proxmox / Linux homelab
* Docker with small services
* Git server / CI runner
* Tailscale / VPN gateway
* DNS, reverse proxy, monitoring
* Network experiments
* Lightweight NAS, **after replacing the disks**

**Bad:**

* Modern Docker-heavy development
* Large Java/Node/Rust/C++ projects
* Local LLM inference
* GPU workloads
* Anything where build time matters

The CPU's **single-thread performance is the real problem**, not the 12-thread headline. And I'd treat both SSDs as temporary/e-waste-grade storage.

### My verdict

**¥250: buy, if you want a cheap lab/server.**

I'd actually consider the **1 Gbps NIC + 16 GB RAM + L5640 platform** worth ¥250 by itself, provided the motherboard/PSU are healthy.

But if your goal is **"cheap development PC that can run Docker + big projects"**, **don't buy it**. Spend more on a newer used Intel platform (e.g. 8th-gen+ Core/i5 or Ryzen) and you'll get dramatically better compilation and container performance.

If you send me the **motherboard model + PSU model** (or a photo of the listing), I can sanity-check whether there are any hidden deal-breakers.
