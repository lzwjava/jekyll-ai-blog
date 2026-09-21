---
audio: false
generated: true
image: false
lang: en
layout: post
title: Skylake K vs Non-K CPUs
translated: false
type: note
---

**Question:** What's the difference between the Intel Core i5-6600 and i5-6600K?

**Answer:**

Both are **Skylake, 4-core / 4-thread, LGA1151** CPUs. The big difference is the **K = unlocked multiplier**.

|                 |   i5-6600 |     i5-6600K |
| --------------- | --------: | -----------: |
| Cores / threads |     4 / 4 |        4 / 4 |
| Base clock      |   3.3 GHz |  **3.5 GHz** |
| Max Turbo       |   3.9 GHz |  **3.9 GHz** |
| Multiplier      |    Locked | **Unlocked** |
| TDP             |      65 W |         91 W |
| Socket          |   LGA1151 |      LGA1151 |
| Integrated GPU  |    HD 530 |       HD 530 |
| Memory          | DDR4-2133 |    DDR4-2133 |

### For your ReBarUEFI + Intel Arc use case

I'd take the **6600K** if the price difference is small.

But don't expect the `K` itself to make much difference for Arc. The important part is that they're both Skylake CPUs and can work on the appropriate Z170/Z270 platform.

The 6600K's real advantage is:

```text
i5-6600
  3.3 → 3.9 GHz
  locked

i5-6600K
  3.5 → 3.9 GHz
  unlocked
       ↓
   overclock
       ↓
   ~4.4–4.6 GHz
```

On a **Z170/Z270 motherboard**, the 6600K can therefore be overclocked, assuming the BIOS/microcode configuration allows it.

If you're buying a **cheap used CPU purely to feed an Arc GPU**, though, the **6600 is often the better value** if it's substantially cheaper. The GPU/ReBAR configuration matters much more than the small stock-clock difference.
