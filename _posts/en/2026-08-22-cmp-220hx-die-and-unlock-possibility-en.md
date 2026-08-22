---
audio: false
generated: true
image: false
lang: en
layout: post
title: CMP 220HX Die and Unlock Possibility
translated: false
type: note
---

**Question:** What die does the CMP 220HX use, and can it be unlocked with cmpunlocker like the CMP 170HX?

**Answer:**

---

### The Die: GA100 (Ampere A100)

The CMP 220HX uses the same **GA100** die as the CMP 170HX — NVIDIA's flagship Ampere data center chip, manufactured on **TSMC's 7nm** process. The GA100 die measures 826 mm² and packs 54.2 billion transistors.

The key difference between the 170HX and the rumored 220HX is the degree of chip harvesting:
- The CMP 170HX enables only 4,480 CUDA cores — just 54% of GA100's full design — and uses 8 GB HBM2e across two stacks with a 4096-bit bus and ~1,493 GB/s bandwidth.
- The 220HX was expected to enable more SMs (closer to a full GA100), which is how it would push 210 MH/s vs. the 170HX's 165 MH/s.

NVIDIA also intentionally crippled several things beyond CUDA core count. They throttled FP32/BF16 floating-point performance to roughly 0.39 TFLOPS, and the PCIe link was limited to Gen 1.1 x4 — only 250 MB/s, compared to modern PCIe 4.0 x16 at 32 GB/s.

---

### Can It Be Unlocked?

**Short answer: cmpunlocker only officially supports the CMP 170HX, not the 220HX.**

The cmpunlocker tool is explicitly designed for the **NVIDIA CMP 170HX (GA100)** and restores full SM compute throughput, unlocked HBM2e memory geometry, PCIe Gen 2 speeds, and full 64 GB BAR1 size — persisting across reboots via patched kernel modules.

The unlock mechanism is deeply technical. It works via a Falcon firmware exploit: a signed firmware buffer overflow → canary bypass → hypervisor-level (HS) code execution → unlocking privilege level masks (PLMs) → overriding fuse-derived settings for SM rate, framebuffer, and PCIe registers.

Since the **CMP 220HX was never officially released** (it remained a rumor — NVIDIA shipped the 170HX instead), there's no real hardware to target. If a 220HX unit did exist, it would share the same GA100 die and likely the same firmware lock architecture, meaning the exploit *could* theoretically apply — but no one has confirmed this in practice.

**What cmpunlocker unlocks on the 170HX:**

| Feature | Status |
|---|---|
| Full SM compute throughput | ✓ Working |
| Memory: 64 GB (8 GB card) / 40 GB (10 GB card) | ✓ Working |
| PCIe Gen 2 | ✓ Working |
| Full 64 GB BAR1 | ✓ Working |
| Reboot persistence | ✓ Working |

Requirements: Linux x86-64, root access, `nvidia-open 610.43.0x`, secure boot disabled.

---

**References:**
- [cmpunlocker GitHub — amoghmunikote](https://github.com/amoghmunikote/cmpunlocker)
- [The almost A100 – NVIDIA CMP 170HX — DevQuasar](https://devquasar.com/hardware/the-almost-a100-nvidia-cmp-170hx/)
- [NVIDIA CMP 170HX Mining Monster Spotted — Tom's Hardware](https://www.tomshardware.com/news/nvidias-cmp170hx-in-the-wild-with-164-mhps-ethereum-mining-performance)
