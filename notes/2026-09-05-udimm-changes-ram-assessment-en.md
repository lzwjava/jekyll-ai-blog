---
audio: false
generated: true
image: false
lang: en
layout: post
title: UDIMM Changes RAM Assessment
translated: false
type: note
---

## Question: If the seller says it is UDIMM, does that change the assessment?

**Answer: Yes — significantly.** If it is genuinely **UDIMM**, then `2Rx4` does **not** automatically mean RDIMM.

For Samsung DDR3L:

* **PC3L** = DDR3L, usually 1.35V
* **2Rx4** = 2 ranks, ×4 DRAM organization
* **UDIMM** = Unbuffered DIMM
* **RDIMM** would normally have an `R` in the module specification, e.g. `PC3L-12800R`

So something like:

```text
Samsung 8GB 2Rx4 PC3L
DDR3L
UDIMM
ECC? ← important
```

could be a perfectly legitimate **DDR3L ECC UDIMM**.

### But there's one thing I would verify

Ask the seller for the **exact Samsung model number printed on the sticker**, something like:

```text
M391B1G73BH0-YK0
M378B1G73DB0-YK0
...
```

The model number tells us exactly whether it is:

```text
UDIMM / RDIMM
ECC / non-ECC
DDR3 / DDR3L
1333 / 1600 MHz
```

**¥160 for 2×8GB is reasonable only if your motherboard supports that exact type.** For ordinary DDR3L non-ECC UDIMM, I'd consider ¥160 somewhat high; for ECC UDIMM, compatibility becomes the main question.

If you upload a **photo of the RAM sticker**, I can decode the exact module before you buy it.
