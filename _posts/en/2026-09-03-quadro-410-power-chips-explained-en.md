---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quadro 410 Power Chips Explained
translated: false
type: note
---

Question: What are the **APW8720 P57F (8-pin)** and **V5F20 (5-pin)** chips on a Quadro 410?

Answer: They are most likely **power-management / voltage-regulation components**, not connectors.

* **APW8720 / P57F — 8-pin:** likely a **buck regulator / power-controller or power MOSFET-related power IC** used to generate one of the GPU board's lower-voltage rails.
* **V5F20 — 5-pin:** likely a **voltage regulator / power-management IC** serving another rail, but the exact function depends on the board revision and the marking package.

On a Quadro 410, these components are part of the board's **VRM/power tree**. The important thing when repairing/testing is not just the chip name, but **which rail each one generates**.

If you upload a clear photo of the **front and back of your Quadro 410 PCB**, I can trace the surrounding inductors/capacitors and identify **which pins are VIN, VOUT, GND, EN, etc.**, then tell you exactly where to put the multimeter probes.
