---
audio: false
generated: true
image: false
lang: en
layout: post
title: CPU Fan Connector Faces Rear I/O
translated: false
type: note
---

**Question:** On the ASUS H81M-K motherboard, when installing a CPU fan/heatsink, which direction should the fan connector face — toward the PCIe slot, the RAM slots, the USB headers, or elsewhere?

**Answer:**

Based on the official ASUS H81M-K layout, here's what you need to know:

**CPU_FAN Connector Location**

According to the H81M-K motherboard layout, the `CPU_FAN` connector is located at the **top-left area** of the board, near the ATX12V power connector, above the LGA1150 CPU socket — which places it closest to the **rear I/O side** of the board (the side with video/USB ports).

**Which direction should the fan connector face?**

The fan connector cable on most Intel stock coolers (push-pin type) is short. Since `CPU_FAN` is positioned at the **top-left corner** (near the rear I/O panel / ATX12V power header), you should:

- **Orient the fan so its cable faces toward the top-left / rear I/O side** — that's where the `CPU_FAN` header sits.
- This means the connector will generally face **away from the PCIe slot** (which is at the bottom), **away from the RAM/DIMM slots** (which are to the right of the CPU), and **away from the internal USB headers** (which are at the bottom-right area).

**Visual orientation summary for H81M-K:**

| Board Edge | What's there |
|---|---|
| Top (rear I/O) | CPU_FAN header ← **aim cable here** |
| Right | DDR3 RAM slots |
| Bottom | PCIe x16 slot, USB headers, SATA |
| Left | ATX 24-pin power |

**Practical tip:** With push-pin Intel coolers, the cable is fixed to one corner of the fan. Before pressing in the push pins, rotate the entire heatsink/fan assembly so that the cable corner is closest to the `CPU_FAN` header. Then lock the pins down. The CPU_FAN connector supports a CPU fan of maximum 1A (12W), and only the 4-pin CPU fan supports the ASUS Fan Xpert feature.

**References:**
- [ASUS H81M-K User Manual – Motherboard Layout (ManualsLib)](https://www.manualslib.com/manual/565354/Asus-H81m-K.html)
- [ASUS H81M-K – Fan Connectors Page 24 (ManualsLib)](https://www.manualslib.com/manual/565354/Asus-H81m-K.html?page=24)
- [H81M-K Layout Contents – ManualOwl](https://www.manualowl.com/m/Asus/H81M-K/Manual/372249?page=12)
