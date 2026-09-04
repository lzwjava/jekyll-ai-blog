---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quadro 4000 Power Connectors Guide
translated: false
type: note
---

**Question:** On the Quadro 4000 card, which side is the 6-pin PCIe power connector — and what is the 4-pin connector on the right?**Question:** On the Quadro 4000, which side is the 6-pin PCIe power connector — left or right? And what is the 4-pin connector on the right?

**Answer:**

The **6-pin PCIe power connector is on the left side** (toward the top/rear of the card). That is the one you need to plug your PSU cable into.

The **4-pin connector on the right** is a **Molex-style adapter port** — it is part of the **included Y-adapter cable** that NVIDIA provides in the box. It looks like this:

```
Card top edge:
┌─────────────────────────────────┐
│  [6-pin PCIe] ←PLUG HERE   [4-pin] ← Molex adapter (ignore if PSU has 6-pin)
└─────────────────────────────────┘
```

**Summary:**

| Connector | Purpose | Use it? |
| --- | --- | --- |
| **6-pin (left)** | Main PCIe power input | ✅ Yes — plug PSU cable here |
| **4-pin (right)** | Molex adapter port | ❌ Only if PSU has NO 6-pin cable |

The card comes with a 6-pin connector that splits into two 4-pin connectors — this adapter is intended for PSUs that do not have a dedicated PCIe power connector. If your PSU already has a 6-pin (or 8-pin with detachable 2-pin) PCIe cable, **skip the 4-pin side entirely** and plug directly into the 6-pin port.

**References:**

- [How to connect Quadro 4000 to PSU – Tom's Hardware Forum](https://forums.tomshardware.com/threads/how-to-connect-quadro-4000-to-psu.791303/)
- [Quadro 4000 specs – eBay listing](https://www.ebay.com/itm/167837856419)
