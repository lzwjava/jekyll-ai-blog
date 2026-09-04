---
audio: false
generated: true
image: false
lang: en
layout: post
title: CPU Power Connector 4+4 Pin Design
translated: false
type: note
---

**Question:** Why is the CPU power connector designed as 4+4 pin (two halves) instead of just one solid 4-pin? What is the second half for?

---

**Answer:**

The **4+4 pin design** is purely about **backwards compatibility and flexibility**. Here's the full explanation:

---

**The history behind it:**

| Era | Standard | Connector |
| --- | --- | --- |
| Old boards (Pentium 4 era) | ATX12V 1.x | **4-pin** only |
| Newer boards (Core 2 / i-series) | ATX12V 2.x | **8-pin** (EPS12V) |
| PSU solution | Universal | **4+4 pin** (fits both!) |

---

**Why two halves?**

- Some motherboards (like your **H81M-K**) only have a **4-pin socket** → you plug in **only one half**
- High-end motherboards (X99, Z-series, server boards) have an **8-pin socket** → you **clip both halves together** and plug in the full 8-pin
- This way, **one PSU cable works for all boards** — no need to make two different cables

---

**Visual explanation:**

```
4-pin half A  +  4-pin half B
      ↓                ↓
 [■ ■ ■ ■]      [■ ■ ■ ■]

Use ONLY half A          Clip A+B together
 for H81M-K (4-pin)      for high-end boards (8-pin)
```

---

**So for YOUR setup (H81M-K):**

- Plug in **only ONE 4-pin half** into the ATX12V socket
- Leave the **other half dangling / tucked away** — it is simply unused
- The two halves are usually **keyed differently** so only the correct half fits the 4-pin socket

---

**Why not just make two separate cables?**

Because it would mean:

- More cables cluttering the case
- PSU manufacturers needing to include both types
- Users buying the wrong PSU for their board

The **4+4 design solves all of this** with one elegant split connector.

---

**References:**

- [ATX Standard – Wikipedia (ATX12V / EPS12V connector history)](https://en.wikipedia.org/wiki/ATX)
- [Tom's Hardware – 4-pin ATX12V connector explained](https://forums.tomshardware.com/threads/4-pin-atx12v-connector.1429321/)
