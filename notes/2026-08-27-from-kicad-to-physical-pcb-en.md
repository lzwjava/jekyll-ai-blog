---
audio: false
generated: true
image: false
lang: en
layout: post
title: From KiCad to Physical PCB
translated: false
type: note
---

**Question:** How do you manufacture a PCB from a design created in KiCad?

**Answer:**

Here's the full workflow from KiCad design to physical PCB:

---

### Step 1 — Generate Gerber Files (the standard manufacturing format)

In KiCad's **PCB Editor (Pcbnew)**:

1. Go to **File → Fabrication Outputs → Gerbers (.gbr)**
2. Select the layers you need:
   - `F.Cu` / `B.Cu` — front/back copper
   - `F.SilkS` / `B.SilkS` — silkscreen
   - `F.Mask` / `B.Mask` — solder mask
   - `Edge.Cuts` — board outline
3. Also generate the **Drill file**: **File → Fabrication Outputs → Drill Files (.drl)**

---

### Step 2 — Generate BOM & Pick-and-Place Files (if assembled)

- **BOM:** File → Fabrication Outputs → BOM
- **Component Placement (CPL/PnP):** File → Fabrication Outputs → Component Placement

These are needed if you want the manufacturer to also solder components.

---

### Step 3 — Verify with a Gerber Viewer

Before sending files, verify them visually:

- KiCad's built-in **GerbView**
- Online: [gerber.ucamco.com](https://gerber.ucamco.com) or **JLCPCB's Gerber Viewer**

---

### Step 4 — Choose a PCB Manufacturer

| Manufacturer | Notes |
| --- | --- |
| **JLCPCB** | Cheapest for prototypes; also offers SMT assembly |
| **PCBWay** | Good quality + assembly services |
| **OSH Park** | US-based; purple boards; great for hobbyists |
| **Eurocircuits** | Europe-based; high quality |
| **Seeed Fusion** | Good for low-volume production |

---

### Step 5 — Upload & Order

1. Zip all Gerber + drill files into one `.zip`
2. Upload to the manufacturer's website
3. Configure options: layers, board thickness (typically 1.6mm), copper weight (1oz), surface finish (HASL or ENIG)
4. If using assembly: upload BOM + CPL files, select components
5. Review the preview, then place your order

---

### Step 6 — Solder Components (if not using assembly service)

Once bare boards arrive:

- **Hand soldering** for through-hole and simple SMD
- **Reflow oven / hot plate** for SMD paste + reflow
- **Stencil** (can be ordered with the board) for applying solder paste evenly

---

**References:**

- [KiCad Official Docs — Generating Gerbers](https://docs.kicad.org/8.0/en/pcbnew/pcbnew.html#fabrication-outputs)
- [JLCPCB — How to Generate Gerber Files from KiCad](https://jlcpcb.com/help/article/how-to-generate-gerber-and-drill-files-in-kicad-7)
- [PCBWay KiCad Guide](https://www.pcbway.com/blog/PCB_Design_Tutorial/Generate_Gerber_file_from_Kicad.html)
- [KiCad Community Forum](https://forum.kicad.info)
