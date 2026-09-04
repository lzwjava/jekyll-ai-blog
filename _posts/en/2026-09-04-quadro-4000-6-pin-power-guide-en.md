---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quadro 4000 6-Pin Power Guide
translated: false
type: note
---

**Question:** What PCIe power cable does the Quadro 4000 require, and how do I connect it?

**Answer:**

The NVIDIA Quadro 4000 requires a **single 6-pin PCIe power connector**. The card's power cable requirement is a 6-pin PCI-E connector.

Here's what to do:

**Step-by-step:**

1. **Power down the PC completely** — shut down the OS, flip the PSU switch to OFF (if it has one), and unplug the power cord from the wall.
2. **Locate the 6-pin PCIe cable** on your PSU — it's a 6-hole connector, sometimes labeled "VGA" or "PCIe" on the cable.
3. **Check if your PSU has an 8-pin (6+2) connector** — many power supplies have a cable with an 8-pin (6+2) connector; if you only need 6 pins, just detach the 2-pin part.
4. **Plug the 6-pin end firmly into the card** — it will only go in one way (keyed connector). You should hear/feel a click.
5. **Do NOT use SATA-to-PCIe adapters** — SATA-to-PCIe and Molex-to-PCIe adapters cannot supply enough current; a new PSU is safer.
6. Reconnect the power cord and power on.

**Regarding the included adapter cable** (if the card came with a dual 4-pin Molex adapter): that adapter is intended for PSUs that do not have a dedicated PCIe power connector — use it only as a last resort, and prefer a native PCIe cable from your PSU if available.

**References:**

- [NVIDIA Quadro Power Guidelines (PNY)](https://www.pny.com/file%20library/company/support/product%20brochures/nvidia%20quadro/quadro-power-guidelines.pdf)
- [How to connect Quadro 4000 to PSU – Tom's Hardware Forum](https://forums.tomshardware.com/threads/how-to-connect-quadro-4000-to-psu.791303/)
- [Quadro K4000 power connector guide – BleepingComputer](https://www.bleepingcomputer.com/forums/t/795216/nvidia-quadro-k4000-power-connector-needed/)
