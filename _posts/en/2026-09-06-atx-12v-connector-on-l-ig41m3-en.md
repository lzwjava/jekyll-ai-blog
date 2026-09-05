---
audio: false
generated: true
image: false
lang: en
layout: post
title: ATX 12V Connector on L-IG41M3
translated: false
type: note
---

**Question:** What does the ATX 12V connector mean on the Lenovo L-IG41M3 motherboard?

---

**Answer:**

The **ATX 12V connector** is a **separate small power connector** on the motherboard, completely different from the main 20/24-pin ATX connector. Here's what you need to know:

---

### 🔌 What it is

It is a **4-pin or 8-pin square connector** that delivers **+12V power exclusively to the CPU**. On the L-IG41M3 (an older board), it is typically a **4-pin ATX12V** connector, also called the **"P4 connector"**.

```
[ +12V ][ +12V ]
[ GND  ][ GND  ]
```

---

### ⚡ Why it exists

The main 24-pin connector powers the whole motherboard (RAM slots, PCIe, chipset, etc.), but the **CPU needs a dedicated, clean 12V line** for the VRM (Voltage Regulator Module) to convert down to the CPU's actual operating voltage (around 1.1V–1.4V). Without this connector plugged in, the CPU gets **no power** and the PC will not boot at all.

---

### 🔧 On your Huntkey 280W PSU

Your Huntkey 280W PSU should have a **4-pin ATX12V cable** coming out of it — it is a small square 4-pin plug, **separate from the main 20-pin cable**. You must plug this into the small square socket near the CPU socket on the L-IG41M3 board.

| Connector | Purpose | Pins |
| --- | --- | --- |
| Main ATX | Powers whole board | 20-pin (your PSU) |
| ATX 12V | Powers CPU only | 4-pin square |

---

### ⚠️ Do not skip it

If you only plug in the main 20-pin and forget the ATX 12V 4-pin, the system will power on (fans may spin) but **will not POST or boot** — a very common mistake.

---

**References:**

- [ATX 12V Power Connector Explained — computerhope.com](https://www.computerhope.com/jargon/a/atx.htm)
- [What is the ATX 12V connector? — Tom's Hardware](https://www.tomshardware.com/reviews/psu-buying-guide,4229.html)
