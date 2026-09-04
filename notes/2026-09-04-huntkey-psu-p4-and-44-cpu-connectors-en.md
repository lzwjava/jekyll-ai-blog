---
audio: false
generated: true
image: false
lang: en
layout: post
title: Huntkey PSU P4 and 4+4 CPU Connectors
translated: false
type: note
---

**Question:** On the Huntkey 航嘉 Super 500W PSU, what does the "P4 cable" (the 4-pin connector) mean, and what does the nearby second set of 4 pins mean?

---

**Answer:**

Here's a clear breakdown of both connectors:

---

### 1. The P4 Cable (4-pin CPU power connector)

The 4-pin ATX connector — officially known as the **ATX12V P4 connector** — is a standardized power delivery interface introduced with the ATX12V 1.0 specification in 2000. It supplies **+12V DC directly to the motherboard's CPU VRM (Voltage Regulator Module)**, decoupling high-current CPU loads from the main rails.

The P4 cable has **two black wires (ground)** and **two yellow wires (+12V DC)**. These attach to a 4-pin connector on the motherboard. It is a standard power connector used with both Intel and AMD motherboards.

The name "P4" came from the Intel **Pentium 4** era, but it's now universal across all modern CPUs.

---

### 2. The "Nearby" Second Set of 4 Pins — The 4+4 (EPS12V) Connector

Many PSUs ship an **8-pin EPS12V CPU cable that can be split into two 4-pin connectors**. If your motherboard only has a 4-pin CPU socket, you simply pull the two halves apart and plug in one half.

So what you're seeing on the Huntkey Super 500W is a **4+4 pin design** — two 4-pin pieces clipped together side by side:

| Configuration | When to use it |
|---|---|
| **Use just one 4-pin half** | Your motherboard has only a 4-pin CPU power socket (older or budget boards) |
| **Clip both together to make 8-pin** | Your motherboard has an 8-pin EPS CPU power socket (most modern boards) |

One half of the 4+4 EPS12V connector is a mirror image of the other. The pins are keyed (some square, some with clipped/rounded corners), so **only the correct half will fit into a 4-pin motherboard socket without forcing it**.

---

### Summary

- **P4 / 4-pin** = CPU power connector, delivers +12V to the CPU. **Must be plugged in** or the CPU gets no power.
- **The nearby 4 pins** = the second half of the **4+4 EPS12V** connector. Clip both halves together for an **8-pin socket**, or use just one half for a **4-pin socket**.
- The best choice is to plug a 4-pin cable into a 4-pin connector, an 8-pin cable into an 8-pin connector, or a 4+4 cable into either kind of connector.

---

**References:**
- [What Is P4? – ComputerHope](https://www.computerhope.com/jargon/p/p4.htm)
- [All About PSU Cables and Connectors – PlayTool](https://www.playtool.com/pages/psuconnectors/connectors.html)
- [How to Connect a PSU to a 4-pin CPU Port – Corsair](https://help.corsair.com/hc/en-us/articles/360043469632-PSU-How-to-connect-a-PSU-to-a-4-pin-CPU-port)
- [ATX Compatibility Guide – PlayTool](http://www.playtool.com/pages/psucompat/compat.html)
