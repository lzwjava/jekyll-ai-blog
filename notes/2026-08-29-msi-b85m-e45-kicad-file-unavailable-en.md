---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI B85M-E45 KiCad File Unavailable
translated: false
type: note
---

**Question:** Where can I find a KiCad PCB file for the MSI B85M-E45 motherboard?

**Answer:**

Unfortunately, **this does not exist and cannot exist publicly** — and here's why:

---

**Why there is no KiCad (or any open-source PCB) file for this board:**

MSI is a commercial company. The PCB design files (schematics, layout, Gerbers) for the B85M-E45 are **proprietary, closed-source, and trade secret**. MSI has never released them, and they never will for a commercial product like this. No KiCad file, no Altium file, no Eagle file exists publicly for this board.

What does exist publicly:

- The **user manual** (connector pinout diagrams, basic layout overview)
- Some users on repair forums like Badcaps.net have requested the **boardview** (`.BRD` file, used for repair tracing) and **schematic**, but these are hard to find even there and are shared informally in repair communities

---

**What you might actually be looking for — and where to find it:**

| Goal | What to look for | Where |
| --- | --- | --- |
| Repair / trace power rails | Boardview (`.BRD`) file | Badcaps.net, eevblog forums |
| Understand circuit design | Schematic PDF | Badcaps.net schematic request threads |
| Component locations | User manual with connector map | ManualsLib, MSI support page |
| Reference Intel B85 platform design | Intel B85 PCH reference schematic | Intel ARK / developer resources |

---

**The closest you can get:**

The Badcaps.net community has threads specifically requesting the MSI B85M-E45 schematic and boardview for repair purposes. That's realistically the only place where unofficial copies sometimes surface.**Bottom line:** A KiCad PCB file for the MSI B85M-E45 simply does not exist in the public domain. Commercial motherboard designs are never open-sourced. Your best bet for repair/tracing work is the Badcaps.net community for boardview files, or the official manual for connector layout reference.
