---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mixed GPU Training on GeForce
translated: false
type: note
---

Question: How do I train models across a mixed 10-GPU rig of RTX 3060/3090/4090 cards?

Answer:

**The core problem isn't compute, it's three things: no P2P/NVLink on GeForce, heterogeneous VRAM (12GB/24GB/24GB), and PCIe bandwidth.** Handle those and DDP/DeepSpeed just works.

### 1. P2P reality check first

NVIDIA disables P2P on the driver level for GeForce (30/40 series), confirmed as intentional product segmentation. NVIDIA blocks P2P on consumer 90-series cards purely as a product segmentation decision to push people toward professional cards, even though the hardware supports it. On 4090 specifically there's a real bug beyond just the artificial block — multi-GPU RTX 4090 setups had a broken CUDA UVA implementation where P2P transfers reported success but silently corrupted data (destination all zeros or NaN), fixed only in driver 525.105.17+. Bottom line: **always run with `NCCL_P2P_DISABLE=1` on GeForce cards, don't fight it.**

```bash
export NCCL_P2P_DISABLE=1
export NCCL_IB_DISABLE=1      # no infiniband on a consumer rig
export NCCL_SHM_DISABLE=0     # shared memory transport is your fallback, keep it on
export NCCL_DEBUG=WARN
```

There's a driver patch (`aikitoria/open-gpu-kernel-modules`) that force-enables P2P via BAR1/DMA if you want to fight for it, but for a 10-card mixed rig it's not worth the instability — your bottleneck will be PCIe lane count long before P2P matters.

### 2. Topology matters more than the cards

10 GPUs on one board means most slots run at x4 or x1 (risers). Check your actual lane allocation:

```bash
nvidia-smi topo -m
lspci -vv | grep -A2 "LnkSta:"    # actual negotiated width/speed per card
```

If you're bandwidth-starved, don't do tensor-parallel or naive DDP all-reduce across all 10 — you'll be network(PCIe)-bound. Instead:

### 3. Use DeepSpeed ZeRO-3 with per-GPU heterogeneous batch sizing

Since VRAM is 12/24/24GB, don't use identical micro-batch across ranks. DeepSpeed doesn't natively do per-rank batch override cleanly, so the practical move is a **rank-grouped hybrid**: pipeline-parallel across VRAM tiers, data-parallel within same-VRAM groups.

```python
# launch.py — group your ranks by VRAM tier
import os, torch.distributed as dist

RANK = int(os.environ["RANK"])
GPU_TIERS = {
    # rank: vram_gb
    0: 12, 1: 12, 2: 12,      # 3060s
    3: 24, 4: 24, 5: 24, 6: 24,  # 3090s
    7: 24, 8: 24, 9: 24,      # 4090s
}
# micro-batch scales with VRAM headroom
MICRO_BATCH = {12: 4, 24: 8}
micro_bs = MICRO_BATCH[GPU_TIERS[RANK]]
```

`deepspeed_config.json`:

```json
{
  "train_micro_batch_size_per_gpu": "auto",
  "gradient_accumulation_steps": "auto",
  "zero_optimization": {
    "stage": 3,
    "offload_optimizer": {"device": "cpu", "pin_memory": true},
    "overlap_comm": true,
    "contiguous_gradients": true,
    "reduce_bucket_size": 5e7,
    "stage3_prefetch_bucket_size": 5e7
  },
  "bf16": {"enabled": true},
  "comms_config": {
    "nccl_p2p_disable": true
  }
}
```

`"auto"` lets DeepSpeed's autotuning pick per-rank micro-batch, but honestly on 3 different VRAM tiers I'd just hardcode via `--per_device_train_batch_size` passed differently per rank group using a wrapper script rather than trust the autotuner — it optimizes for homogeneous clusters.

### 4. Simpler and often better for a mixed rig: split by tier entirely

Don't force all 10 into one training run. Two configs get you further:

- **3090+4090 group (7 cards, 24GB each)**: standard FSDP/DDP, homogeneous, no batch-size headaches.

```bash
NCCL_P2P_DISABLE=1 torchrun --nproc_per_node=7 --nnodes=1 train.py \
  --fsdp full_shard --bf16 --gradient_checkpointing
```

- **3060 group (3 cards, 12GB)**: use for eval/inference serving, data preprocessing, or small ablations, not the main training run. Trying to jam a 12GB card into the same ZeRO-3 shard group as 24GB cards means the whole group's shard size gets capped by the smallest card — you lose most of the extra 24GB headroom on the bigger cards.

This matches what you already do with MI300X clusters — homogeneous grouping beats forcing heterogeneity through software.

### 5. Practical gotchas for a 10-card single box

- **Power**: 3×170W (3060) + 4×350W (3090) + 3×450W (4090) ≈ 3260W GPU-only. Multi-PSU with staggered `nvidia-smi -pl <watts>` power-limiting per card is mandatory, or you'll trip breakers.
- **PCIe risers**: mining-style risers (x1) will tank all-reduce throughput. If serious, get a board with real x8 electrical per slot (WRX80/EPYC).
- **Driver version**: stick to 525.105.17+ minimum on any 4090s in the mix — earlier drivers silently corrupt data on multi-4090 P2P even when NCCL_P2P_DISABLE is set, per the confirmed NVIDIA forum thread.

References:

- [Cannot enable P2P communication in RTX3090 server · NVIDIA/nccl#1127](https://github.com/NVIDIA/nccl/issues/1127)
- [Standard nVidia CUDA tests fail with dual RTX 4090 Linux box](https://forums.developer.nvidia.com/t/standard-nvidia-cuda-tests-fail-with-dual-rtx-4090-linux-box/233202)
- [Patching NVIDIA's driver and vLLM to enable P2P on consumer GPUs](https://smcleod.net/2026/02/patching-nvidias-driver-and-vllm-to-enable-p2p-on-consumer-gpus/)
- [Problems With RTX4090 MultiGPU — Puget Systems](https://www.pugetsystems.com/labs/hpc/problems-with-rtx4090-multigpu-and-amd-vs-intel-vs-rtx6000ada-or-rtx3090/)
- [DeepSpeed ZeRO config docs](https://www.deepspeed.ai/docs/config-json/#zero-optimizations-for-fp16-training)
