---
audio: false
generated: true
image: false
lang: en
layout: post
title: ATX 12V Connector Identification Guide
translated: false
type: note
---

**Question:** How do I identify and insert the correct half of the 4+4 pin ATX 12V connector?

---

**Answer:**

The connector is **physically designed so only the correct half can fit** — it is foolproof by design. Here's how to identify it:

---

**Method 1 — Look at the CLIP/LATCH side:**

```
Correct half:        Wrong half:
┌─────────┐          ┌─────────┐
│ ■ ■ ■ ■ │          │ ■ ■ ■ ■ │
│  [CLIP] │          │ no clip │
└─────────┘          └─────────┘
     ↓                    ↓
fits the socket      will NOT insert
                     fully / feels loose
```

- The **correct half has a plastic latch/clip** on the side
- It will click and lock into the motherboard socket
- The wrong half **physically cannot fully insert** — it will feel loose or won't go in at all

---

**Method 2 — Look at the shape of the plastic housing:**

Each half has a **chamfered corner (beveled/cut edge)** on one side:

```
Correct half looks like:

 ___________
|           |
| ■ ■ ■ ■  |
|_______   /   ← cut corner here
        \_/
```

- Match the cut corner to the matching notch inside the motherboard socket
- If corners don't align → wrong half

---

**Method 3 — Read the cable label:**

Most PSU cables including 航嘉 (Huntkey) are labeled directly on the connector or cable:

| Label on connector | Meaning |
|---|---|
| `CPU` | This is the ATX12V cable |
| `ATX12V` | Correct label |
| `+12V` | Same cable |
| One half may say `1` | Use this half for 4-pin boards |
| Other half may say `2` | Only used when combining into 8-pin |

---

**Method 4 — Look at wire colors:**

The correct 4-pin half for ATX12V always has:
```
Pin 1 = Yellow (+12V)
Pin 2 = Yellow (+12V)
Pin 3 = Black  (GND)
Pin 4 = Black  (GND)
```

If the half you picked has these 4 wires → it is correct.

---

**Simplest real-world test:**

> Just gently try to insert each half into the motherboard ATX12V socket.
> **The correct half slides in smoothly and clicks.**
> **The wrong half will not fit — do NOT force it.**

The plastic keying makes it nearly impossible to insert the wrong half. So if it goes in and clicks → you have the right one. ✅

---

**References:**
- [ASUS H81M-K User Manual – ATX Power Connectors (Page 25)](https://www.manualslib.com/manual/565354/Asus-H81m-K.html?page=25)
- [Tom's Hardware – 4-pin ATX12V connector identification](https://forums.tomshardware.com/threads/atx-12v-connector.1664339/)
