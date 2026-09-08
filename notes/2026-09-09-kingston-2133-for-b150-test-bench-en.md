---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kingston 2133 for B150 Test Bench
translated: false
type: note
---

Question: **Which 8GB DDR4 should you buy for the B150M + i5-6500 GPU test bench: Galaxy GAMER II 2666 or Kingston 2133?**

Answer: **I’d take the Kingston 8GB DDR4-2133 if the prices are similar.**

|                  | Galaxy GAMER II         | Kingston                          |
| ---------------- | ----------------------- | --------------------------------- |
| Capacity         | 8GB                     | 8GB                               |
| Speed            | 2666 → **2133** on B150 | **2133 native**                   |
| Voltage          | likely 1.2V             | **1.2V**                          |
| Desktop DIMM     | ✅                       | ✅                                 |
| Your B150M       | ✅                       | ✅                                 |
| RGB              | ✅                       | ❌                                 |
| Brand/reputation | Good                    | **Better for boring reliability** |
| Condition        | Used                    | Used                              |
| GPU test bench   | 👍                      | **⭐**                             |

### Why Kingston wins here

Your B150 + i5-6500 won't benefit from the 2666 rating:

```text
Galaxy DDR4-2666
       ↓
B150 + i5-6500
       ↓
DDR4-2133
```

So you're paying for speed you won't use.

For a **GPU diagnostic machine**, I actually prefer the boring option:

```text
Kingston 8GB
DDR4-2133
1.2V
single stick
       ↓
B150M + i5-6500
       ↓
stable test platform
```

No need for RGB, high frequency, or gaming-oriented memory.

### One caveat

The Kingston listing doesn't give the **exact model number**. That's worth checking. If the seller can send a photo of the label, I can identify whether it's a normal **8GB 1Rx8 / 2Rx8 desktop UDIMM** and check the exact IC/model.

**Bottom line:** if Kingston is around **¥40–60**, I'd buy it. If the Galaxy is substantially cheaper, the Galaxy is also perfectly fine. **For this workstation, 8GB matters; 2133 vs 2666 basically doesn't.**
