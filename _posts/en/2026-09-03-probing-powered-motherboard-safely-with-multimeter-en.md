---
audio: false
generated: true
image: false
lang: en
layout: post
title: Probing Powered Motherboard Safely with Multimeter
translated: false
type: note
---

**Question:** If we use a multimeter (万用表) to randomly probe a powered-on motherboard (like an H81), can it damage the board? Which mode is safe to use?

**Answer:**

Using a multimeter on a live motherboard is risky if you're not careful, but the mode you choose and technique matter a lot.

**Modes and their risks:**

The most dangerous mode on a live board is **resistance/ohm mode (Ω)**. It injects its own small current to measure resistance — but on a powered board, that conflicts with the board's own voltages and can give garbage readings or damage sensitive components. Never use resistance mode on a powered board.

**Continuity mode** (the beep mode) has the same problem — it also injects a test current. Safe only when the board is **fully unplugged and capacitors discharged**.

**Voltage mode (DC Voltage)** is what you *should* use on a live board. Set it to DC, appropriate range (e.g. 20V range for checking 12V/5V/3.3V rails). Probing ground (GND) and a voltage rail is safe if your probes don't accidentally bridge two adjacent pins.

**The real danger isn't the mode — it's accidentally shorting pins.** If a probe slips and bridges two nearby pins (especially near the CPU socket, RAM slots, or PCIe connectors), you can kill the board instantly, regardless of mode.

Here's a quick summary:**Tips for safely probing an H81 board:**

- Always use **DC Voltage mode**
- Set your range to 20V (covers all common rails: 12V, 5V, 3.3V, 1.8V, 1.05V)
- Hold the **black probe firmly on a ground point first** (any unpainted metal screw hole, or the GND pin of a connector) before touching anything else
- Use thin, sharp probe tips — blunt tips are more likely to slip and bridge pins
- Avoid probing near the LGA socket, DDR3 slots, or PCIe slot unless you know exactly which pin you're touching
- Never let a probe tip roll across a row of pins

The board won't be damaged simply because you *touched* a probe to it — damage comes from **wrong mode** or **accidentally shorting two pins** with your probe.
