---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI ReBarUEFI CPU Support Guide
translated: false
type: note
---

**Question:** What CPUs do those MSI ReBarUEFI-compatible boards support?

**Answer:** The key distinction is **Z170 = 6th-gen Skylake**, while **Z270 = 6th/7th-gen Skylake/Kaby Lake**.

### MSI boards from the list

| Motherboard         | Socket  | Official CPU generations | Good CPU choices                 |
| ------------------- | ------- | ------------------------ | -------------------------------- |
| **Z170-A PRO**      | LGA1151 | 6th Gen                  | i7-6700K, i7-6700, i5-6600K      |
| **Z170A Gaming M5** | LGA1151 | 6th Gen                  | i7-6700K, i7-6700, i5-6600K      |
| **Z270-A PRO**      | LGA1151 | 6th + 7th Gen            | **i7-7700K**, i7-6700K, i5-7600K |
| **Z270 Gaming M5**  | LGA1151 | 6th + 7th Gen            | **i7-7700K**, i7-6700K, i5-7600K |

MSI explicitly lists the Z170-A PRO as supporting 6th-gen Core i3/i5/i7, Pentium and Celeron CPUs. ([MSI][1])

The **Z270 boards are more interesting**: MSI officially lists both 6th- and 7th-gen Core i3/i5/i7 CPUs.

So if you're buying an old platform **specifically for an Intel Arc GPU + ReBarUEFI**, I'd look for:

```text
MSI Z270-A PRO
       +
Core i7-7700K
       +
Intel Arc A770 / A750 / B-series
       +
ReBarUEFI
```

The **i7-7700K + Z270** is the top-end mainstream CPU combination for that platform.

One important catch: **don't assume every LGA1151 CPU works in every LGA1151 board**. Z170/Z270 use the same physical socket, but their officially supported CPU generations differ.

If you're considering buying a **used MSI board + cheap CPU specifically to run an Arc B580/B570**, tell me your target Arc GPU and budget—I can narrow it down to the cheapest viable CPU/board combination.

[1]: https://us.msi.com/Motherboard/Z170-A-PRO/Specification?utm_source=chatgpt.com "Specification Z170-A PRO | MSI USA"
