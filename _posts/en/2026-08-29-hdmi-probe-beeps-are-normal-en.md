---
audio: false
generated: true
image: false
lang: en
layout: post
title: HDMI Probe Beeps Are Normal
translated: false
type: note
---

Question: When one probe is on the HDMI port and the other probe randomly touches various points within 3–5cm on the GPU board, sometimes beeping and sometimes not — what does this mean?

Answer:

**This is completely normal behavior.** It simply means some nearby points are electrically connected to the HDMI port, and some are not.

---

**Why Some Points Beep and Some Don't:**

The GPU board is made up of **hundreds of separate electrical networks (nets)**. Each net is a group of points connected together by copper traces inside the PCB.

```
HDMI Port
    │
    ├──── beeps ──→ capacitor on same signal line  ✅ connected
    ├──── beeps ──→ resistor on same trace         ✅ connected
    ├──── beeps ──→ GND pad (if HDMI pin is GND)  ✅ connected
    │
    ├──── silent ──→ VRM coil (different net)      ○ not connected
    ├──── silent ──→ unrelated capacitor           ○ not connected
    └──── silent ──→ GPU core power pad            ○ not connected
```

---

**What the Pattern Tells You:**

| Result | Meaning |
| --- | --- |
| **Beep** | That point shares the same electrical net as your HDMI probe point |
| **No beep** | That point belongs to a **different** net, isolated from HDMI |
| **Beeps everywhere** | Possible **GND short** — almost everything connects to ground |
| **Never beeps** | Broken trace, lifted pin, or truly isolated net |

---

**Think of it Like a Map:**

> Imagine the HDMI port as a **city**. The copper traces are **roads**.
>
> - Points that **beep** = locations connected by roads to that city
> - Points that **don't beep** = different cities, no road connection

---

**Is This a Problem?**

- **Random beep / no-beep pattern = Normal**, just mapping different nets
- **Beeps at almost every point you touch = Suspicious**, possible short to GND
- **Never beeps at all, even on obvious GND pads = Suspicious**, possible open circuit or broken trace

---

**If You Are Doing Fault Diagnosis:**

1. Put **one probe firmly on a GND point** (metal shield or known GND pad)
2. Touch the **other probe to each HDMI pin one by one**
3. Signal pins should **NOT beep** to GND — if they do, that pin is **shorted to ground (对地短路)**
4. GND pins on HDMI **should beep** to GND — that is normal

References:

- [Understanding PCB Nets and Traces](https://resources.altium.com/p/what-is-a-net-in-pcb-design)
- [How to Find Short Circuits on a PCB with a Multimeter](https://www.electroschematics.com/using-multimeter-for-pcb-fault-finding/)
- [GPU Board Repair – Continuity Testing Basics](https://www.youtube.com/results?search_query=gpu+pcb+repair+continuity+test+hdmi)
