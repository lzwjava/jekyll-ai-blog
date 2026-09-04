---
audio: false
generated: true
image: false
lang: en
layout: post
title: Finding the 6+2 Pin GPU Cable
translated: false
type: note
---

**Question:** How do I find the correct PCIe power connector on a Huntkey 航嘉 Super 500W PSU for the Quadro 4000?

**Answer:**

Good news — Huntkey 500W PSUs typically include a **(6+2 — 6+2)P GPU connector**, which means you have what you need.

Here's how to find it physically:

**Step 1 — Look at the cables coming out of the PSU**

The cable bundle from the PSU includes several different cables. Look for the one labeled or shaped like this:

| Cable | Appearance | Use |
|---|---|---|
| 24-pin | Wide flat connector | Motherboard |
| 4+4 pin | Two 4-pin blocks | CPU |
| **6+2 pin** ← | **6 holes + 2 extra holes on side** | **GPU ← This one!** |
| SATA | Flat L-shaped | Hard drives |

**Step 2 — Identify the 6+2 pin PCIe cable**

It looks like this:
```
[  6-pin body  ][+2 extra pins]
```
The "+2" part can be **detached** — for the Quadro 4000 you only need the **6-pin** portion. Simply **separate the 2-pin clip** from the side and only plug in the 6-pin end into the card.

**Step 3 — Plug into the card**

- Insert the **6-pin end** into the **left connector** on top of the Quadro 4000
- It only fits one way — push until you hear a **click**
- Leave the right 4-pin port on the card alone

**Summary:**
> Find the cable with the **6+2 connector** → detach the 2-pin side → plug only the 6-pin into the Quadro 4000. Done. ✅

**References:**
- [Huntkey CP5000 500W specs](https://en.huntkey.com/product/cp5000-power-supply/)
- [Huntkey WD500K connector details – VillMan](https://villman.com/Product-Detail/huntkey_wd500k-500w-80plus-gold-power-supply-)
