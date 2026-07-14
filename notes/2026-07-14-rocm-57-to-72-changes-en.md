---
audio: false
generated: true
image: false
lang: en
layout: post
title: ROCm 5.7 to 7.2 Changes
translated: false
type: note
---

Question: What changed in ROCm between 5.7.0 (the last version that "fully supported" your MI50/gfx906) and the current release?

Answer:

Current stable is **ROCm 7.2.4** (May 2026), with 7.10.0 as the active technology-preview stream. Here's what matters for you specifically:

**1. gfx906 (MI50/MI60/Radeon VII) has gone from "maintenance mode" to actively removed**

- ROCm 5.7 → 6.0: gfx906 entered maintenance (bug fixes only, no new features) — this is where you left off.
- ROCm 7.0: AMD removed MI50/MI60-specific YAML data from ROCm Compute Profiler entirely — not just "stopped optimizing," actively deleted device support in tooling. A Phoronix report on this triggered enough community pushback that AMD said they'd consider reverting it, but the direction is clear: gfx906 is being phased out of the toolchain, not just deprioritized.
- Current official compatibility matrices (7.9.0, 7.10.0) list only CDNA2/3/4 (MI210/250/300/350) and RDNA3/4 consumer cards — gfx906 doesn't appear at all anymore.

**2. What still works (community-maintained, not AMD-shipped)**

- MI50 runs fine on ROCm 6.4.3 with a small rocblas package swap pulled from Arch's `extra` repo — confirmed working as of the active GitHub discussion.
- `vllm-gfx906` (community fork) plus Ubuntu 24.04 LTS + ROCm 6.4.3 is the currently-recommended stack for gfx906 inference serving.
- Arch Linux packages ROCm for gfx906 without extra hacking via pacman — better path than Ubuntu's official ROCm packages if you want less friction.
- llama.cpp ROCm backend has open regressions on gfx906 (crashes on newer model architectures like Qwen3.5) — Vulkan backend is the safe fallback on the same hardware.

**3. Bigger structural changes 5.7 → 7.2 that also affect you indirectly**

- ROCTracer, ROCProfiler, rocprof, and rocprofv2 are deprecated — migrate to rocprofv3 (built on ROCprofiler-SDK). EOS expected end of Q2 2026.
- ROCm SMI is being phased into maintenance mode — AMD SMI is the successor and gets ongoing feature work.
- ROCm 7.2 unified Windows + Linux into a single release stream, plus a big consumer-hardware push (Ryzen AI 300/400, Radeon RX 7000+) with ComfyUI integration — AMD's current investment is clearly consumer/APU + MI300-class datacenter, not legacy CDNA1/GCN5.1 cards like yours.
- Each major version bump (5→6→7) breaks backward compatibility (HIP runtime API changes, repackaged rocRAND/hipRAND, restructured file layout) — so pinning to 6.4.3 for gfx906 means you're stuck there; there's no clean upgrade path to 7.x for MI50.

**Practical takeaway for your card:** treat ROCm 6.4.3 as the ceiling for this MI50, run it on Ubuntu 24.04 or Arch, use `vllm-gfx906` for serving, and don't expect any new ROCm feature (Triton kernel improvements, FlashAttention updates, newer PyTorch ROCm builds) to land for gfx906 going forward — you're on a frozen, community-patched stack from here.

References:

- [AMD Hardware Would Ideally Be Supported ~10 Years — Phoronix (ROCm 7.0 profiler removal)](https://www.phoronix.com/news/AMD-ROCm-Hardware-Length)
- [ROCm Device Support Wishlist — gfx906 community status](https://github.com/ROCm/ROCm/discussions/4276)
- [ROCm 7.2.4 Release Notes — rocprofv3/AMD SMI deprecations](https://github.com/ROCm/ROCm/releases)
- [ROCm 7.10.0 Compatibility Matrix](https://rocm.docs.amd.com/en/7.10.0-preview/compatibility/compatibility-matrix.html)
- [ROCm 7.2.2 at CES 2026 — VideoCardz](https://videocardz.com/newz/amd-highlights-rocm-7-2-2-at-ces-2026-with-ryzen-ai-400-support-and-a-single-windows-plus-linux-release)
