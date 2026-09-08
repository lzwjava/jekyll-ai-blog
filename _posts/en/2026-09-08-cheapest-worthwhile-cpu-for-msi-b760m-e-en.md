---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cheapest worthwhile CPU for MSI B760M-E
translated: false
type: note
---

**Question:** How do you find the cheapest worthwhile CPU for the MSI B760M-E DDR5?

**Answer:** Search specifically for **LGA1700 CPUs**. For a cheap build, I'd prioritize the used market like this:

| CPU               | Typical target | My take                       |
| ----------------- | -------------: | ----------------------------- |
| **Celeron G6900** |     very cheap | 🟢 Cheapest functional option |
| **Pentium G7400** |          cheap | 🟢 Better budget CPU          |
| **i3-12100F**     |          cheap | ⭐ Best cheap performance      |
| **i3-12100**      |  slightly more | ⭐ Has iGPU                    |
| **i5-12400F**     |           more | ⭐⭐⭐ Best value                |
| **i5-12400**      |           more | ⭐⭐⭐ iGPU + 6 cores            |
| i5-13400F         |         higher | Good if used price is right   |

### My strategy for Xianyu

Search these exact terms:

```text
G6900
G7400
12100F
12100
12400F
12400
```

**Don't search by GHz.** Search by **socket + generation + model**.

For example:

```text
MSI B760M-E DDR5
        ↓
     LGA1700
        ↓
12th / 13th / 14th Gen
        ↓
G6900 / G7400 / i3-12100 / i5-12400...
```

If your goal is simply **"get this motherboard running as cheaply as possible"**, I'd look for a **G6900**.

If your goal is **"cheap but actually useful for LLM/AI development"**, skip the Celeron/Pentium and hunt for a **used i3-12100F or i5-12400F**. The 12400F's 6C/12T is much more useful for compilation, preprocessing, Docker, etc.

**One important detail:** `F` CPUs have **no integrated GPU**. If you don't have a discrete GPU, get the non-F version.

If you tell me your **maximum CPU budget (e.g. ¥100 / ¥200 / ¥300)**, I can give you a very specific Xianyu search strategy.