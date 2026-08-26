---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 3090 PCB Layout for KiCad
translated: false
type: note
---

Question: How do I find an RTX 3090 PCB layout/schematic for use in KiCad?

Answer:

Finding an official RTX 3090 PCB layout for KiCad is very difficult because NVIDIA keeps their GPU board designs proprietary. However, here are your realistic options:

**1. Community / Open-Source Repositories**

- Search GitHub for terms like `RTX 3090 PCB`, `GA102 PCB`, or `GPU PCB KiCad`
- Check [Hackaday.io](https://hackaday.io) for GPU-related hardware hacks
- Browse [EEVblog Forums](https://www.eevblog.com/forum/) — hardware teardown threads sometimes include traced schematics

**2. Reverse-Engineered Schematics**

- Sites like **schematics.com** or **elektrotanya.com** occasionally host GPU board schematics uploaded by repair technicians
- Search for `RTX 3090 schematic PDF` — some repair-focused communities share partial schematics
- YouTube GPU repair channels (e.g., *northridgefix*) sometimes reference or link to board-level docs

**3. Convert Existing Files to KiCad**

- If you find an Altium, Eagle, or PDF schematic, you can:
  - Use **KiCad's Altium importer** (built-in since KiCad 6)
  - Use **Eagle-to-KiCad converter** via KiCad's import tool
  - Trace a PDF schematic manually into KiCad's schematic editor

**4. GPU Repair / Boardview Files**

- Search for `.brd` or `.bdv` boardview files for the RTX 3090 (used by repair techs)
- Tools like **OpenBoardView** can read these, and you can reference them while building in KiCad
- Search: `RTX 3090 boardview` or `GA102 boardview`

**5. Start from Reference Designs**

- NVIDIA publishes **PCIe x16 reference guidelines** — useful if you're designing a carrier board
- Use KiCad's built-in PCIe connector footprints as a starting point

> ⚠️ **Note:** Redistributing NVIDIA's proprietary PCB designs may violate their IP. Use community-traced schematics at your own discretion, and verify the accuracy of any files you find.

---

References:

- [KiCad EDA Official Site](https://www.kicad.org/)
- [OpenBoardView (boardview viewer)](https://github.com/OpenBoardView/OpenBoardView)
- [EEVblog Hardware/Repair Forum](https://www.eevblog.com/forum/repair/)
- [Hackaday.io Projects](https://hackaday.io)
