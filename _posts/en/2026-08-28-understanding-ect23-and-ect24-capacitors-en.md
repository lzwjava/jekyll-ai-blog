---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding ECT23 and ECT24 Capacitors
translated: false
type: note
---

Good — now the picture is much clearer. Here's the corrected answer:

---

**Question:** What do ECT23 and ECT24 mean on the top of the capacitor (820µF, 2.5V) on the Quadro 410 GPU board?

**Answer:**

Those are **solid polymer aluminum electrolytic capacitors** from **NCC (Nippon Chemi-Con)**. The markings break down like this:

| Marking | Meaning |
|---|---|
| **E** | Voltage code — "E" in NCC's system = **2.5V** rated voltage |
| **CT** | **Series name** — the internal NCC product series (like how NCC also uses PSE, PSA, PSC, etc.) |
| **23** | **Capacitance code** — encodes **820µF** in NCC's abbreviated format |
| **24** | **Second line** — likely a **lot/date code** or a second marking line (year or batch) |

NCC's solid polymer capacitor families — like PSE, PSC, and PSA — are super low ESR, high ripple current designs rated for 2.5V to 16V, operating at 105°C for 15,000 to 20,000 hours. The ECT series follows the same family of conductive polymer aluminum solid capacitors.

**In plain terms**, on a Quadro 410 board:
- The capacitor is **820µF / 2.5V**, a **solid (non-liquid) polymer capacitor**
- It's used in the **VRM (voltage regulator module)** near the GPU die to smooth and stabilize the very low GPU core voltage (typically 0.9–1.1V range)
- **ECT** is simply the NCC series designation for that specific product line
- **23 / 24** refer to lot/date codes or the capacitance encoding within NCC's numbering system

The two different numbers (ECT23 vs ECT24) you see on the board just indicate **different production lots or sub-variants** of the same 820µF / 2.5V capacitor — electrically they are equivalent.

**References:**
- [Nippon Chemi-Con Product Catalogue (NCC 2020)](https://chemi-con.com/wp-content/uploads/2021/04/Nippon-Chemi-Con-Product-Catalogue.pdf)
- [NCC Group Chart – Aluminum Electrolytic Capacitors](https://www.chemi-con.co.jp/en/products/aluminum/chart/)
