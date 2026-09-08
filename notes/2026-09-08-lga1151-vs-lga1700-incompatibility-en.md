---
audio: false
generated: true
image: false
lang: en
layout: post
title: LGA1151 vs LGA1700 Incompatibility
translated: false
type: note
---

**Question:** Can an Intel Core i5-7400 work in the MSI B760M-E DDR5?

**Answer:** **No. ❌**

The **i5-7400** is a **7th-gen Kaby Lake** CPU and uses **LGA1151**.

Your **MSI B760M-E DDR5** uses **LGA1700**.

```text
i5-7400
  └── 7th Gen
      └── LGA1151 ❌

B760M-E DDR5
  └── 12th/13th/14th Gen
      └── LGA1700 ✅
```

So don't buy these for the B760 board:

```text
i5-7400   ❌
i5-7500   ❌
i7-7700   ❌
i5-8400   ❌
i5-9400   ❌
```

Even though some of them are physically similar, **LGA1151 ≠ LGA1700**.

For the B760M-E, search Xianyu for:

```text
G6900
G7400
i3-12100
i3-12100F
i5-12400
i5-12400F
i5-13400
```

If you're trying to build the **absolute cheapest PC around that B760M-E**, I'd target a **used G6900/G7400**. If you want something substantially more capable, **i5-12400/F** is the sweet spot.