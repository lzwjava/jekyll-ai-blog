---
audio: false
generated: true
image: false
lang: en
layout: post
title: SXM vs PCIe GPU Performance
translated: false
type: note
---

Question: Why are SXM-form-factor GPUs (H100/H200/MI300X SXM) better than PCIe versions?

Answer:

**1. Interconnect bandwidth — the big one**

- PCIe card: GPU-to-GPU traffic goes through NVLink Bridge (limited, only pairs) or falls back to PCIe itself.
  - H100 PCIe: NVLink bridge only bonds 2 GPUs at ~600 GB/s bidirectional, everything else routes through PCIe Gen5 x16 (~64 GB/s each direction, shared with host).
- SXM card: plugs into a proprietary socket wired to a full NVSwitch fabric on the baseboard.
  - H100 SXM: 18 NVLink 4.0 links = **900 GB/s** bidirectional per GPU, all-to-all, non-blocking via NVSwitch.
  - MI300X OAM (same idea, AMD's SXM-equivalent): Infinity Fabric ~896 GB/s aggregate.

For training with tensor/pipeline parallelism, all-reduce and all-to-all ops dominate step time. 900 GB/s all-to-all vs ~64 GB/s PCIe-routed is not a small delta — it's the difference between GPUs actually acting like one big accelerator vs. 8 islands bottlenecked by a bus also serving host DMA.

**2. Power delivery**

- PCIe form factor capped by slot power spec: H100 PCIe = 300-350W.
- SXM baseboard delivers power directly: H100 SXM = 700W, MI300X SXM(OAM) = 750W.
- More power headroom → higher sustained clocks → PCIe H100 has ~15-20% lower FP16/BF16 throughput than SXM H100 at the chip level alone, before even counting interconnect effects.

**3. Topology / scaling**

- SXM boards (HGX/UBB) are designed as 4 or 8-GPU units with NVSwitch already wired, no bridge cables, no host CPU in the hot path for peer traffic.
- PCIe cards need switch topology, NVLink bridges (only pairs on H100 PCIe), and host CPU/root-complex mediates cross-socket transfers, adding latency and stealing PCIe lanes from NICs/NVMe.

**4. Practical impact on your workloads**

For your GPT-2 760M training on MI300X — if you're on OAM/SXM MI300X (8-GPU UBB), all-reduce cost for gradient sync scales far better than PCIe MI300X would. At small model scale (760M) this matters less since compute/comm ratio is favorable, but once you scale toward the models you're training at 2B tokens/mo across bigger architectures, interconnect becomes the bottleneck first, not FLOPs.

**Rule of thumb:** PCIe = fine for inference / single-GPU / small fine-tunes. SXM = mandatory once you're doing multi-GPU pretraining with tensor parallelism, because comm-bound ops (all-reduce, all-to-all) are where PCIe cards fall off a cliff.

References:

- [NVIDIA H100 Datasheet](https://www.nvidia.com/en-us/data-center/h100/)
- [NVLink and NVSwitch Overview](https://www.nvidia.com/en-us/data-center/nvlink/)
- [AMD Instinct MI300X Datasheet](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html)
