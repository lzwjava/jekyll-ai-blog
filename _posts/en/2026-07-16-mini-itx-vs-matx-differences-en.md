---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mini-ITX vs mATX Differences
translated: false
type: note
---

Question: What's a Mini-ITX board, and how does it differ from mATX?

Answer:

**Form factor sizes:**

- Mini-ITX: 170mm × 170mm (square)
- microATX (mATX): 244mm × 244mm (square, but larger)
- ATX: 305mm × 244mm (for reference)

**Practical differences:**

| | Mini-ITX | mATX |
| --- | --- | --- |
| PCIe slots | 1 (x16, for GPU) | 2-4 (usually 1x16 + 2-3x1) |
| RAM slots | 2 (max ~64-128GB depending on chipset) | 4 (max ~128-256GB) |
| Case size | Smallest, SFF builds | Small-mid tower |
| Expansion | None beyond the one GPU slot | Can add capture cards, extra NICs, HBAs |
| Cost | Often pricier per-feature (niche market) | Cheaper, mainstream |

**Why it matters for your use case (GPU/ML boxes):**

If you're building anything with multiple GPUs or need PCIe bifurcation for NVMe/networking, mATX (or full ATX) is the only sane choice — Mini-ITX gives you exactly one x16 slot, full stop. Mini-ITX makes sense for a single-GPU inference box you want physically small (e.g. a home server or edge deployment), or a NAS.

Also check:

- **VRM quality** — Mini-ITX boards often skimp on power delivery since they target lower-power SFF builds. If you're running a 300W+ GPU or a high-TDP CPU for local training, check VRM temps/reviews carefully.
- **M.2 slots** — Mini-ITX boards sometimes only have 1 M.2 slot due to space; mATX usually has 2+.
- **Cooling clearance** — ITX cases are notoriously tight, which matters if you're stuffing in a workstation GPU + big cooler for a home dev rig.

For your MI300X-adjacent home setup or any multi-GPU experiments, mATX/ATX is the practical choice. ITX is for "I want this thing to be small and it only needs one card."
