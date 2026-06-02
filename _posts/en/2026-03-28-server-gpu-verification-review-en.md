---
audio: false
generated: true
image: false
lang: en
layout: post
title: Server Hardware and GPU Verification Review
translated: false
type: note
---

### 📋 Review: How I Checked the Server

**What I did (single SSH command, chained):**

1. **`lscpu`** — pulls CPU architecture details from `/proc/cpuinfo`. Tells us cores, threads, model, flags (instruction sets like AVX-512).

2. **`free -h`** — reads `/proc/meminfo` and shows total/used/available memory in human-readable format.

3. **`nvidia-smi`** — NVIDIA's management tool. Reports GPU model, VRAM, driver version, temperature, utilization. *Failed* because driver isn't installed.

4. **`lspci | grep -i gpu`** — raw PCIe bus scan. Shows what hardware is physically connected, regardless of driver status. This is what caught the RTX 3090.

5. **`cat /proc/driver/nvidia/version`** — checks if the kernel module is loaded. *Failed* — confirming no driver.

---

**What I could've done better:**

- **`lshw` or `dmidecode`** — more detailed hardware inventory (BIOS, exact memory DIMMs, etc.)
- **`cuda-smi` or `glxinfo`** — alternative GPU checks if CUDA runtime exists without the full driver
- **`/proc/driver/nvidia/gpus/*/information`** — another driver-level check
- **Stress test** — `gpu-burn` or `cuda-samples` to actually benchmark the GPU once driver is up
- **VRAM size** — I inferred 24 GB from the RTX 3090 model name, but didn't actually verify it empirically (can't without driver)

**What went well:**

- Single-shot command — no unnecessary round trips
- `lspci` saved the day when `nvidia-smi` failed — good fallback
- Caught the discrepancy: Alibaba calls it "G39" but it's actually an RTX 3090

Want me to dig deeper with `lshw` or `dmidecode` for a more complete picture?
