---
audio: false
generated: true
image: false
lang: en
layout: post
title: Budget Vega 20 Cluster for Training
translated: false
type: note
---

Question: Is a 10x AMD Radeon Pro VII (16GB, ~600 RMB each, sold mislabeled as MI50) cluster for ~6000 RMB a good bet for local training, and does 10 cards → 100 cards scale?

Answer:

**The mislabeling story checks out.** Radeon Pro VII and MI50 are the same Vega 20 die, differing mainly in branding, firmware, and physical packaging — MI50 has display outputs disabled and passive cooling stripped off, while Pro VII keeps the mini-DisplayPort 1.4a output and active cooling. Sellers on 闲鱼/转转 flash MI50 cards with Pro VII vbios (or vice versa) constantly because they're electrically identical. You didn't get scammed on compute — you got scammed on the label, and the seller undercharged you if anything. Let him keep selling.

**ROCm status — this is the real constraint, not PCIe.** gfx906 GPUs (MI50, Radeon Pro VII, Radeon VII) entered maintenance mode in ROCm 6.0. ROCm 5.7 was the final release for gfx906 in a fully supported state. Practically:

```bash
# Last officially-built ROCm for gfx906 with vendor binaries: 5.7
# Beyond that, you self-compile or use community builds:
# mi50 works with ROCm 6.4.3 + a small rocblas package hack from Arch's rocblas
# https://github.com/nlzy/vllm-gfx906 is the go-to community fork for inference
```

MI50 is still well supported by the code, but AMD doesn't build binaries for it anymore. You either build ROCm for gfx906 yourself or use community-maintained packages. So: inference (vLLM fork, llama.cpp with HIP backend) — fine. Training with the full PyTorch+ROCm+RCCL stack on latest ROCm — expect breakage, pin to 5.7 or the community 6.4.3 hack.

**PCIe expansion for 10 cards — don't use mining risers.** For actual training (gradient all-reduce every step), x1 mining risers (250MB/s) will bottleneck you badly. Real options, cheapest to most capable:

```bash
# Option 1: Used server board with real lane count (best value)
# AMD EPYC Rome/Milan (SP3) — 128 PCIe4 lanes per socket, single socket enough
# e.g. used Supermicro H11/H12 boards, ~1500-3000 RMB used
# Gives you 6-8x real x8/x16 slots without a switch

# Option 2: PCIe bifurcation + retimers if you're stuck on a consumer board
# x16 slot -> 4x x4 via bifurcation riser (needs BIOS bifurcation support)
# check: lspci -vvv | grep -i "LnkCap\|LnkSta"  # verify negotiated width/speed post-install

# Option 3: PCIe switch card (ASM2824-based, ~4x x4 from one x8) if bifurcation unsupported
```

Check RCCL/P2P support once assembled:

```bash
rocminfo | grep -A5 "Pool Info"
rocm-smi --showtopo   # shows P2P link matrix between GPUs
```

gfx906 does **not** support PCIe P2P the way MI50 pairs with xGMI bridges do standalone — without xGMI bridge cards between adjacent pairs, all-reduce traffic goes GPU→CPU→GPU over PCIe, which is your actual training bottleneck, not the riser.

**Cost math is real but not apples-to-apples:**

| | Pro VII (10x) | A6000 Pro |
| --- | --- | --- |
| VRAM | 160GB | 96GB |
| Cost | ~6000 RMB | ~50-60k RMB |
| FP16 | ~26.8 TFLOPS/card, 268 total | dense, higher per-card |
| Bandwidth/card | 1.02 TB/s HBM2 | ~960GB/s GDDR6 |
| Interconnect | PCIe only, no NVLink | PCIe only (Pro also no NVLink on A6000 non-Ada) |
| Software risk | high (ROCm EOL, self-build) | low (CUDA, current) |
| Power | 300W x10 = 3kW | 300W x1 |

VRAM/RMB favors you by ~15x, but that ignores software stack maintenance time (which for you, running an AI company, is not free) and the all-reduce bottleneck once you go past 2-4 GPUs on plain PCIe. Where this genuinely wins: **large-batch inference / serving, or data-parallel fine-tuning of small-medium models where each GPU holds a full replica** (embarrassingly parallel, minimal sync) — not tensor-parallel training of a single large model across all 10.

**On "10 cards solved → 100 cards not far":** push back on that. 10→100 isn't a multiply, it's a different problem — power (30kW+, needs 3-phase), rack/cooling, network fabric (RDMA/RoCE if you want real multi-node throughput), and ROCm's gfx906 EOL means you're maintaining your own fork at that scale, which is a real ongoing cost. If the actual goal is "cheap local training capacity," a used 4x-8x A100/A6000 node with real NVLink or good PCIe4 x16 lanes will get you more usable training throughput per RMB than 10x Pro VII once you count engineering time. Pro VII cluster makes sense as an inference/experimentation rig or for RL/agent rollout workloads where you need lots of parallel small-model instances, not as a dense pretraining cluster.

References:

- [Radeon VII vs MI50 branding](https://www.aliexpress.com/s/wiki-ssr/article/radeon-vii-vs-mi50)
- [ROCm 6.0 gfx906 maintenance mode](https://rocm.docs.amd.com/en/docs-6.0.0/about/release-notes.html)
- [ROCm 5.7 release notes — gfx906 EOS](https://rocm.docs.amd.com/en/docs-5.7.0/release.html)
- [community gfx906 ROCm 6.4.3 workaround thread](https://github.com/ROCm/ROCm/discussions/4276)
- [vllm-gfx906 fork](https://github.com/nlzy/vllm-gfx906)
