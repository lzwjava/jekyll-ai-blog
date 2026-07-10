---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD MI50 vs RTX 4070 Power Connectors
translated: false
type: note
---

Question: AMD MI50 power connector vs RTX 4070 power connector — are they different?

Answer:

Yes, they are different. You are talking about the **power connector on the GPU**, not a "battery port".

![Image](https://images.openai.com/static-rsc-4/zafhnHpK3Z_GYG-_LUG0Z3gypX3iGT8fq0XcwgNgcA6_TG46Mz2Qfj6mHaRyhPgUUjbTP9yfEoJpbYpneJWe2Taptb0uXZOXKfJPJHlzmnxZS2Lxmoq4rEECb8Hf18Epsh5qxOYiCtcX-F4Ub-5Qi0OiFR24clqjuwk5linNbEH84hC-Ta9dfm6I7K4Cn_nr?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/KGTtBnG4aFza-JlG-28pzslFHcV1aXsaCfbymzpYA6FrWs9-y5qzM9QI_0QeHH8tVcEWHoPdXSU148mTtygUcWuQ7d0pWRyDazHVEl7rjy8S-acnFD9arTmGKWBjZ_DmYE5JRmqvpg7jRxYRkfXuVNRMBIZ1m2lEyIJoF1bwec57Mh0X0ZZGqGhkfSOSQD4j?purpose=fullsize)

### RTX 4070 (MSI Gaming)

Many RTX 4070 cards use the newer:

* **12VHPWR / 12V-2x6 connector**
* Looks like a **12-pin main connector + 4 small sense pins** (often called "12 pin")
* Can provide up to ~600W depending on implementation
* Requires either:

  * native PSU 12VHPWR cable, or
  * adapter from 2×/3× 8-pin PCIe power cables

Example:

```
RTX 4070
GPU socket:

[■■■■■■■■■■■■]
[■■■■]
12VHPWR
```

---

### AMD MI50

The MI50 is a datacenter GPU from the Vega architecture.

It uses:

* **2 × 8-pin PCIe power connectors**

```
MI50

[8-pin] [8-pin]

PCIe power
```

Each 8-pin PCIe connector provides up to ~150W, so:

```
2 × 150W = 300W
+
PCIe slot 75W

≈ 375W available
```

MI50 TDP is around **300W**, so two 8-pin connectors are normal.

---

### Important for your build

Your RTX 4070 PSU cable **cannot directly plug into MI50**.

You need:

```
PSU
 |
 +---- 8-pin PCIe ---- MI50
 |
 +---- 8-pin PCIe ---- MI50
```

A normal gaming PSU usually has these cables:

* CPU EPS 8-pin ❌ (not same)
* GPU PCIe 8-pin ✅
* 12VHPWR ✅ (for RTX 40 series)

Make sure you use **PCIe VGA cables**, not CPU/EPS cables.

---

Also, MI50 is not like RTX 4070:

|               | MI50           | RTX 4070                 |
| ------------- | -------------- | ------------------------ |
| Architecture  | Vega 20        | Ada Lovelace             |
| VRAM          | 16GB HBM2 ECC  | 12GB GDDR6X              |
| Power         | ~300W          | ~200W                    |
| Connector     | 2×8-pin PCIe   | 12VHPWR / 8-pin variants |
| Gaming driver | poor           | excellent                |
| AI/Linux      | good ROCm card | better CUDA ecosystem    |

For your AI workstation idea: the MI50's **16GB HBM2 + ECC** is interesting, but the motherboard/PSU needs to be prepared for the **two 8-pin connectors and ~300W power draw**. It is much closer to a datacenter accelerator than a gaming GPU.
