---
audio: false
generated: true
image: false
lang: en
layout: post
title: Intel 6th Gen CPU Guide
translated: false
type: note
---

Question: **What is an Intel 6th-gen CPU?**

Answer: **Intel 6th generation = Skylake**, released mainly in **2015–2016**.

The common desktop CPUs are:

| CPU      | Cores / Threads | Base clock | Socket  |
| -------- | --------------: | ---------: | ------- |
| i3-6100  |           2 / 4 |    3.7 GHz | LGA1151 |
| i5-6500  |           4 / 4 |    3.2 GHz | LGA1151 |
| i5-6600K |           4 / 4 |    3.5 GHz | LGA1151 |
| i7-6700  |           4 / 8 |    3.4 GHz | LGA1151 |
| i7-6700K |           4 / 8 |    4.0 GHz | LGA1151 |

### For your motherboard hunting

**6th gen = Skylake = LGA1151 + DDR4/DDR3L**

Typical chipsets:

```text
H110
B150 / B250
H170 / H270
Z170 / Z270
```

One important detail: **6th and 7th gen both use LGA1151**, so a board advertised as:

> "Supports 6/7 generation CPU"

usually means something like **i5-6500 / i7-6700 + i5-7500 / i7-7700**.

For your GPU-lab use case, **Z170/Z270 boards are particularly interesting** because they tend to have more PCIe configuration options than cheap H110/B150 boards. But having multiple x16 physical slots does **not** automatically mean you can run multiple GPUs with enough PCIe resources or Above 4G Decoding.

I can also map **Intel 2nd → 14th gen to socket + chipset + RAM + PCIe generation** as a compact reference for your used-hardware shopping.
