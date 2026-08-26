---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD GPU PCB Layouts KiCad
translated: false
type: note
---

Question: How do I find AMD GPU PCB layouts/schematics for KiCad?

Answer:

AMD GPUs are **slightly more accessible** than NVIDIA's due to their open-source GPU driver efforts, but full PCB layouts are still largely proprietary. Here's what's available:

**1. AMD's Open-Source Resources**

- AMD open-sources their **GPU drivers and firmware** but NOT board-level PCB designs
- However, the open nature of AMD's ecosystem means more community documentation exists
- Check [AMD's GitHub](https://github.com/RadeonOpenCompute) for any hardware reference material

**2. Reference Board Designs (Best Bet)**

- AMD releases **reference card designs** to AIB partners (ASUS, MSI, Sapphire, etc.)
- Search GitHub for:
  - `RX 6900 XT PCB`
  - `Navi 21 schematic`
  - `AMD reference card boardview`

**3. Boardview Files for AMD GPUs**

- AMD cards are more commonly found in repair databases
- Search these terms:
  - `RX 6800 XT boardview .brd`
  - `Navi 21 .bdv`
  - `AMD GPU boardview`
- Tools to open them:

| Tool | Format Supported |
| --- | --- |
| OpenBoardView | `.brd`, `.bdv`, `.obv` |
| FlexBV | `.brd`, `.bv2`, `.fbv` |

**4. Community Traced Schematics**

- **Louis Rossmann's community** and GPU repair forums often share AMD board traces
- [Badcaps Forums](https://www.badcaps.net/forum/) — GPU repair section has AMD-specific threads
- Search: `AMD RX 6000 schematic repair PDF`

**5. Sapphire / PowerColor AIB Schematics**

- Some AIB partner repair depots occasionally leak or share partial schematics
- Sapphire (AMD's closest AIB partner) cards are most commonly documented
- Search: `Sapphire RX 6900 XT schematic`

**6. Convert to KiCad Workflow**

```
Boardview (.brd/.bdv)  →  OpenBoardView  →  Reference while tracing in KiCad
PDF Schematic          →  KiCad Schematic Editor  →  Manual re-entry
Altium file            →  KiCad built-in Altium importer  →  KiCad native
```

> ⚠️ AMD's actual PCB Gerber/KiCad files are not publicly released. What's available is mostly reverse-engineered by repair technicians. Always verify accuracy before using in any design.

---

References:

- [OpenBoardView GitHub](https://github.com/OpenBoardView/OpenBoardView)
- [FlexBV Boardview Tool](https://www.fluxeng.com/flexbv/)
- [Badcaps GPU Repair Forum](https://www.badcaps.net/forum/)
- [AMD Open Source GPU GitHub](https://github.com/RadeonOpenCompute)
- [KiCad Altium Importer Docs](https://docs.kicad.org/7.0/en/eeschema/eeschema.html#importing-schematics)
