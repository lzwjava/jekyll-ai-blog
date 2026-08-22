---
audio: false
generated: true
image: false
lang: en
layout: post
title: CMP 170HX Unlockable Alternatives
translated: false
type: note
---

**Question:** What other cards are similar to the NVIDIA CMP 170HX that can be unlocked like the `cmpunlocker` tool does — including other GA100 variants or cards from other vendors like the AMD BC-250?

**Answer:**

The `cmpunlocker` project exploits a Falcon BootROM firmware bug to remove artificial software/OTP restrictions on hardware that was deliberately crippled for product segmentation. As of mid-2026, here's the landscape of similar "unlockable" repurposed cards:

---

### NVIDIA CMP 170HX (GA100) — the target card

The CMP 170HX is physically a complete GA100 die — the same silicon as the A100 datacenter GPU — with compute throughput, memory capacity, and other features artificially restricted via OTP fuses and firmware-enforced register locks.

There are now **two separate unlock tools** for it:

- **`amoghmunikote/cmpunlocker`** — patches the open kernel modules, survives reboots via a persistent service. Targets `nvidia-open 610.43.0x`.
- **`d3dx9/cmpunlocker`** — exploits the Falcon BootROM `.fwsignature_ga100` load bug, targeting `nvidia-open` driver `580.x`. The unlock is volatile (lost on power cycle) but reapplied automatically by a daemon every second.

In June 2026, ASU researcher Jon Pry published a paper revealing a stack protection vulnerability in NVIDIA's Falcon security co-processor, enabling pure-software removal of all restrictions on the CMP 170HX's compute limits, memory locks, and PCIe bandwidth.

**Memory unlock results:**

- The 8 GB model can be unlocked to 64 GB, and the 10 GB model can reach 80 GB — though results are not guaranteed. Reported stable results are often lower, with 32 GB to 40 GB described as more realistic.

**Price caveat:**

- The 170HX was going for around $250 on eBay before this, but since the exploit started spreading, it has shot past $1,000.

---

### AMD BC-250 — the closest equivalent from AMD

The BC-250 was originally designed for Ethereum mining and features a cut-down PS5 APU: 6x Zen 2 cores (all 8 unlockable), 24 RDNA2 Compute Units ("Cyan Skillfish"), and 16 GB of shared GDDR6 memory.

Like the CMP 170HX, it has software-unlockable compute units:

- The GPU has 24 CUs active (down from 36 in the full PS5 APU). The two disabled CPU cores are not fused off and can be re-enabled.
- When the CU unlock patch is applied, the system can recognize 40 CUs — exceeding the PS5's 36-unit spec — with confirmed performance improvements in benchmarks like Furmark. However, the standard cooler is designed only for 24 CUs, so thermal throttling is a real concern.
- As of August 2026, with kernel 7.1.5, a corrected TLB flush, hardware scheduling, the 40-CU unlock, and a flush-on-unmap workaround, ROCm compute reaches verified-correct GEMM, PyTorch matmul, FP64, and text-verified llama.cpp inference. Vulkan retains a roughly 10x prompt-processing advantage and remains the practical default for inference.

Community members are actively using it for AI: two BC-250s running llama.cpp RPC can run Qwen 27B at Q4 and 35B at Q4 for around $300 total.

---

### Summary comparison

| Card | Chip | Unlock Type | Memory | Est. Price (2026) |
| --- | --- | --- | --- | --- |
| NVIDIA CMP 170HX | GA100 (A100 die) | Falcon BootROM exploit (SW only) | 8/10 GB → up to 64/80 GB | $1,000–$2,000 |
| AMD BC-250 | PS5 APU (RDNA2) | Kernel patch (SW only) | 16 GB shared | ~$100–$200 |

Both cards share the same core story: it's a similar situation to another repurposed crypto device, AMD's BC-250 — hardware artificially crippled for a specific market, now being revived for AI inference workloads.

**No other GA100-based cards** are known to be in scope for `cmpunlocker` — the CMP 170HX is the only consumer-accessible GA100 SKU that ended up on the secondary market in volume.

---

**References:**

- [amoghmunikote/cmpunlocker (GitHub)](https://github.com/amoghmunikote/cmpunlocker)
- [d3dx9/cmpunlocker — alternate unlock tool (GitHub)](https://github.com/d3dx9/cmpunlocker)
- [Tom's Hardware — CMP 170HX unlock coverage](https://www.tomshardware.com/pc-components/gpus/nvidia-crypto-mining-gpus-hacked-to-restore-locked-away-vram-in-order-to-feed-ai-boom-software-mod-unlocks-64gb-of-vram-on-usd250-cmp-170hx)
- [AMD BC-250 community docs](https://elektricm.github.io/amd-bc250-docs/)
- [akandr/bc250 — BC-250 AI inference guide (GitHub)](https://github.com/akandr/bc250)
- [Hackaday — BC-250 compute unlock](https://hackaday.com/2026/06/09/re-enable-all-compute-units-on-the-ps5-like-bc-250-cryptomining-card/)
- [170th Street GitBook — CMP 170HX community resource](https://170th-street.gitbook.io/hx/unlock/current-unlock)
