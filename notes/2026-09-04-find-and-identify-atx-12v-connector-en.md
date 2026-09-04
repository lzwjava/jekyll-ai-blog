---
audio: false
generated: true
image: false
lang: en
layout: post
title: Find and Identify ATX 12V Connector
translated: false
type: note
---

**Question:** How do I find and identify the ATX 12V connector on a 航嘉 (Huntkey) Super 500W PSU?

---**Answer:**

On a **航嘉 (Huntkey) Super 500W** PSU, the ATX 12V connector is called the **CPU Connector**. Here's how to find and identify it:

---

**How to identify it physically:**

| Feature | Description |
| --- | --- |
| **Shape** | Small square connector, 2×2 pins |
| **Pin count** | 4 pins (sometimes 4+4 = 8 pin split) |
| **Cable label** | Usually printed: `CPU`, `ATX12V`, or `+12V` |
| **Cable color** | Typically **yellow** (+12V) and **black** (GND) wires |
| **Connector size** | Much smaller than the big 24-pin main connector |

---

**Steps to find it:**

1. **Look at all cables** coming out of the PSU
2. **Find the small 4-pin square plug** — it is NOT the big 24-pin one
3. Check for a label on the cable or connector that says **`CPU`** or **`ATX12V`**
4. It may come as a **4+4 pin** (two halves that clip together) — for the H81M-K, you only need **one half (4 pins)**
5. Route it to the **top-left area** of the H81M-K motherboard where the ATX12V socket is located

---

**Visual guide:**

```
Big connector = 24-pin  →  goes to motherboard EATXPWR
Small connector = 4-pin →  goes to motherboard ATX12V (CPU power)
```

The Huntkey Super 500W ships with this cable included — it is **not a separate purchase**. Just look for the **smallest multi-pin connector** in the cable bundle labeled CPU or +12V.

---

**References:**

- [Huntkey ECO500 500W Specs – CPU Connector listed as (4+4)P](https://en.huntkey.com/product/eco500-power-supply/)
- [Huntkey CP5000 500W ATX Power Supply](https://en.huntkey.com/product/cp5000-power-supply/)
