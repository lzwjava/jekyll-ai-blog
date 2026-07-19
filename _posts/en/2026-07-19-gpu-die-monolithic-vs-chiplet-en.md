---
audio: false
generated: true
image: false
lang: en
layout: post
title: "GPU Die: Monolithic vs Chiplet"
translated: false
type: note
---

Question: What is a GPU die?

Answer: A die is the actual piece of silicon cut from a wafer that contains the fabricated circuits — the physical chip before packaging. "GPU die" = the silicon implementing the GPU's compute units (SMs on NVIDIA, CUs on AMD), memory controllers, L2 cache, and interconnect fabric.

Key mechanics:

**Wafer → die**

- Fabs pattern a ~300mm silicon wafer with thousands of copies of a design, then cut (dice) it into individual chips
- Die size is bounded by the reticle limit (~858mm² max for current EUV lithography) — this is why huge GPU dies (H100 ~814mm², MI300X compute die smaller due to chiplets) push against that ceiling
- Larger die = fewer dies per wafer + lower yield (defect probability scales with area) = more expensive per good die

**Monolithic vs chiplet**

- Monolithic: one large die does everything (older GPUs, still true for NVIDIA H100/B200 compute die)
- Chiplet: multiple smaller dies connected via interposer/package (AMD MI300X is exactly this — it's XCDs (compute dies, CDNA3) + IODs (I/O dies) + HBM stacks, all fused together with CoWoS-style packaging)
- MI300X specifically: 8 XCD chiplets + 4 IOD chiplets + 8 HBM3 stacks, ~153B transistors total across the package — no single die does that alone

**Why this matters for you training on MI300X**

- Cross-XCD communication (Infinity Fabric) has different bandwidth/latency than intra-XCD — this affects how your training framework should place tensor-parallel shards. If you're doing manual NCCL/RCCL tuning, die topology is why some GPU pairs are "closer" than others on the same physical package.
- Die yield economics is also why AMD/NVIDIA price large-die parts (H100, MI300X) at a premium — bad dies get binned into cut-down SKUs (e.g., fewer active SMs/CUs).

**Quick check**: run this to see your actual die/package topology on MI300X:

```bash
rocm-smi --showtopo
```

or for NVIDIA:

```bash
nvidia-smi topo -m
```

References:

- [AMD Instinct MI300X Data Sheet](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html)
- [Chiplet Architecture — AMD CDNA3 Whitepaper](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/white-papers/amd-cdna-3-white-paper.pdf)
- [Reticle limit explanation — SemiAnalysis](https://semianalysis.com/)
