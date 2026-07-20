---
audio: false
generated: true
image: false
lang: en
layout: post
title: Is PCIe 3.0 Riser Enough?
translated: false
type: note
---

**Question: Is this PCIe 3.0 x16 riser cable OK for MSI MAG B760M Mortar + RTX GPUs?**

**Answer: Yes, it will work, but I would choose the PCIe 5.0 Fenvi riser if the price difference is small.**

This NZXT original PCIe 3.0 x16 riser is actually a decent cable. The important point is:

> PCIe 3.0 x16 bandwidth is enough for many AI inference workloads, but it is not ideal for newer GPUs.

---

## Bandwidth comparison

```
PCIe 3.0 x16  ≈ 15.8 GB/s
PCIe 4.0 x16  ≈ 31.5 GB/s
PCIe 5.0 x16  ≈ 63 GB/s
```

Your GPUs:

```
RTX 4070:
PCIe 4.0 x16

RTX 3090:
PCIe 4.0 x16
```

With this riser:

```
RTX 4070
    |
    |
PCIe 3.0 x16 riser
    |
    |
B760M PCIe slot

Result:
PCIe 3.0 x16
```

The GPU will downgrade to PCIe 3.0.

---

## Performance impact

### Gaming

Noticeable sometimes:

```
RTX 4090:
PCIe 3.0 x16 loses little

RTX 4060:
PCIe 3.0 x8 can lose more
```

For RTX 4070/3090:

small impact.

---

### AI inference

Usually fine:

Example:

```
Qwen / Llama inference

GPU VRAM:
24GB RTX3090

Model weights:
stay in VRAM

PCIe traffic:
low
```

So:

```
RTX3090 + PCIe3.0 x16
= OK
```

For agents / local LLM:

✅ good

---

### Multi-GPU model split

Example:

```
RTX3090 24GB
+
RTX4070 12GB

Total VRAM:
36GB
```

The riser is not the biggest issue.

The bottleneck is:

```
B760M:

GPU1:
PCIe4 x16

GPU2:
PCIe4 x4
```

Even if the riser is PCIe5, the second slot is still x4.

---

## Important: "PCIe 3.0 x16" vs physical x16

Many cheap risers advertise:

```
PCIe 3.0 x16
```

but internally only wire:

```
x4
```

For AI, check:

* 16 lanes connected
* shielded cable
* short length

This NZXT-based one is probably genuine because NZXT risers are normally high quality.

---

## My ranking for your B760M AI workstation

### Best

```
PCIe 5.0 x16 20cm Fenvi
★★★★★
```

Reason:

* future proof
* RTX 50 series ready
* better signal margin

---

### This NZXT PCIe 3.0 x16

```
★★★★☆
```

Good if:

* price is much cheaper
* only RTX3090/4070
* inference workload

---

### Cheap no-name PCIe riser

```
★★☆☆☆
```

Avoid.

---

For your use case (local LLM, agents, vLLM, experimenting with 2 GPUs):

I would buy the **PCIe 5.0 Fenvi** if it is only ¥20-50 more.

The riser cable is not where you should save money; a bad riser causes random CUDA crashes, GPU disappearing, and BIOS PCIe negotiation problems.
