---
audio: false
generated: true
image: false
lang: en
layout: post
title: X99-AD4 Supports Tesla P100 PCIe
translated: false
type: note
---

Question: Can the ¥200 X99-AD4 + E5-2680 v4 system run an NVIDIA Tesla P100?

Answer: **Yes, absolutely — if it's the PCIe version of the P100.** This is actually a pretty natural pairing.

The X99-AD4 has **2× PCIe 3.0 x16 slots**, while the Tesla P100 PCIe uses **PCIe 3.0 x16**. ([Huananzhi][1])

### The important part: P100 power

The **Tesla P100 PCIe is a 250 W passive GPU** and requires an auxiliary **8-pin CPU-style power connector**. ([NVIDIA][2])

So your setup should be:

```text
E5-2680 v4
     │
     ▼
X99-AD4
     │ PCIe 3.0 x16
     ▼
Tesla P100 16GB
     │
     └── 8-pin PCIe power

PSU: preferably 650–750W+
```

The motherboard itself has **24-pin ATX + 8-pin CPU power**, and Huananzhi specifies a 500 W minimum for the platform. But because the P100 alone can consume 250 W, I'd personally use a **good-quality 650–750 W PSU**, not a cheap 500 W unit. ([Manuals+][3])

### One BIG catch: P100 is passive

This matters.

The PCIe P100 doesn't have its own active fan; NVIDIA specifies a **passive thermal solution that requires chassis airflow**. ([NVIDIA][4])

So don't just throw it into an open-air desktop and run CUDA workloads indefinitely.

I'd do:

```text
[front intake]
     ↓↓↓
┌─────────────────────┐
│       P100          │ →→→ strong rear exhaust
│   █████████████     │
│                     │
│ E5-2680v4           │
└─────────────────────┘
```

A strong fan directly in front of the P100 heatsink is a good idea.

### For AI specifically

The P100 is still interesting because it's **16 GB HBM2 / 732 GB/s memory bandwidth / 3584 CUDA cores**. ([NVIDIA][4])

But remember:

**P100 = Pascal (compute capability 6.0).**

That means the modern CUDA/PyTorch ecosystem can be more annoying than with newer GPUs. Some recent software stacks increasingly drop support for older architectures.

For example, if your goal is:

```text
LLM inference
LoRA training
CUDA experiments
custom CUDA kernels
old-school ML
```

then **P100 16 GB + E5-2680 v4 for ¥200 platform cost is a pretty fun cheap machine**.

If you're buying the P100 separately, though, **tell me its price**. The GPU price is much more important than the ¥200 motherboard/CPU price, and I can tell you whether the *whole* setup makes sense.

[1]: https://www.huananzhi.com/list_6/48.html?utm_source=chatgpt.com "X99-AD4 V2.0-华南金牌"
[2]: https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com "SPECIFICATIONS"
[3]: https://manuals.plus/ko/ae/1005008645142129?utm_source=chatgpt.com "HUANANZHI X99-AD4 Motherboard User Manual"
[4]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-p100/pdf/nvidia-tesla-p100-PCIe-datasheet.pdf?utm_source=chatgpt.com "Data Sheet: Tesla P100"
