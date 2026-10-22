---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disk Fully Set Up and Verified
translated: false
type: note
---

Done — the disk is fully set up and verified. ✅

## Summary — `192.168.1.137` TOSHIBA DT01ACA050 (500 GB)

| Step | Status |
|---|---|
| Detection | `sda` now enumerated after reboot (was: hotplug-invisible on Q170 AHCI) |
| Old data | Was empty NTFS (3 partitions, 94 MB metadata only) — wiped safely |
| Partitioning | GPT, single partition `/dev/sda1` |
| Format | ext4, label `MODELS` |
| Mount | `/mnt/models` — **458 GB total, 435 GB free** |
| Persistence | `/etc/fstab` UUID entry with `nofail` (boot safe even if disk missing) |
| Ownership | `lzw:lzw` |
| Performance | **167 MB/s write / 168 MB/s read** (healthy 7200 rpm drive; SATA link at 6 Gbps) |
| Layout | `/mnt/models/{comfy, models/{diffusion_models,text_encoders,vae,loras,embeddings}, hf-cache}` — staged for ComfyUI + H3 |

## Where that leaves MiniMax-H3

✅ **Storage wall — solved.** The smallest H3 set (int8: 27.1 GB encoder + 21 GB diffusion + 3.4 GB VAEs ≈ 51.5 GB) now fits with ~380 GB to spare — even the full `text_encoder` + `fl2va` int8 + ComfyUI comfortably.

⚠️ **But the other three walls are unchanged** — be clear-eyed before we download ~52 GB:
1. **VRAM**: int8 Qwen3-VL encoder alone = 27 GB > 24 GB on the M40 (H3's official flow wants 4×80 GB GPUs)
2. **RAM**: 7.7 GB — no room for CPU-offload of a 32B encoder
3. **Compute**: H3's runtime is torch cu130 (Comfy ships `int8_convrot` for exactly that); CUDA ≥12 has zero Maxwell kernels — and we empirically proved this driver family hangs (not just fails) when torch touches the M40. You'd likely wedge `.137`'s driver the same way and need another reboot.

So my recommendation stands: **keep the 435 GB disk ready** (it's also great for SD1.5/legacy experiments or a future GPU swap), but don't download the H3 weights yet unless you're prepared for a guaranteed driver hang on this card.

**Next options:**
- **(a)** I verify the actual ComfyUI + torch cu130 hang risk empirically on `.137` (short, time-boxed, but expects a reboot afterwards) — up to you
- **(b)** Start pulling the H3 files anyway as a staging exercise (downloads work; inference won't)
- **(c)** Mark this box as storage-ready and move on — still pending: `.34`'s wedged NVIDIA driver needs its own reboot whenever convenient
