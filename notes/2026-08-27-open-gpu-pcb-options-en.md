---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open GPU PCB Options
translated: false
type: note
---

Question: Are there any open-source GPU PCB layouts available for KiCad?

Answer:

Fully open-source GPU designs are **extremely rare** because GPU silicon itself is proprietary. However, here are the closest things that actually exist:

---

**1. RISC-V Based Open GPUs (Most Legitimate Open Source)**

| Project | Description | Link |
| --- | --- | --- |
| **Nyuzi** | Open-source GPGPU processor in Verilog | [GitHub](https://github.com/jbush001/NyuziProcessor) |
| **MIAOW** | AMD Southern Islands ISA-compatible open GPU | [GitHub](https://github.com/VerticalResearchGroup/miaow) |
| **VeriGPU** | Simple open-source GPU in Verilog | [GitHub](https://github.com/hughperkins/VeriGPU) |

> These are **RTL/HDL designs**, not KiCad PCB layouts — but they're the most open GPU work available.

---

**2. Open PCIe Card PCB Designs (KiCad-ready)**

These aren't GPUs but are open PCIe board designs you can learn from or adapt:

- **[Open-Source PCIe Carrier Board](https://github.com/enjoy-digital/litepcie)** — LitePCIe by Enjoy-Digital
- **[Glasgow Interface Explorer](https://github.com/GlasgowEmbedded/glasgow)** — Open hardware, KiCad source included
- **[LUNA USB Hardware](https://github.com/greatscottgadgets/luna)** — KiCad-based open PCB example

---

**3. FPGA-Based GPU Replacements (Closest to Real GPU PCB in KiCad)**

FPGAs can emulate GPU functions and many have open KiCad board designs:

- **ULX3S** — Open-source FPGA board with KiCad files
  - [GitHub](https://github.com/emard/ulx3s)
- **OrangeCrab** — Open FPGA in KiCad
  - [GitHub](https://github.com/orangecrab-fpga/orangecrab-hardware)
- **Colorlight 5A-75B** — Used for DIY GPU-like rendering projects
  - Community KiCad replicas exist on GitHub

---

**4. Closest Thing to an Open GPU PCB**

- **[TinyGPU](https://github.com/adam-maj/tiny-gpu)** — Minimal GPU architecture, educational
- **[Tiny Tapeout GPU Submissions](https://tinytapeout.com)** — Small GPU cores submitted for actual chip fabrication

---

**Honest Summary**

```
What you want:          Open RTX/RX-class GPU PCB in KiCad
What actually exists:   Open FPGA boards + open GPU RTL logic
Gap:                    No one has taped out + released a
                        discrete GPU PCB in KiCad format publicly
```

If your goal is **learning GPU PCB design**, the best path is:

1. Study open FPGA board KiCad files (ULX3S is excellent)
2. Reference boardview files of real AMD/NVIDIA cards
3. Combine with PCIe electrical specs from the PCIe standard

---

References:

- [Nyuzi Open GPGPU](https://github.com/jbush001/NyuziProcessor)
- [ULX3S Open FPGA Board (KiCad)](https://github.com/emard/ulx3s)
- [LitePCIe Open PCIe Framework](https://github.com/enjoy-digital/litepcie)
- [Tiny Tapeout Open Silicon](https://tinytapeout.com)
- [OrangeCrab FPGA Hardware](https://github.com/orangecrab-fpga/orangecrab-hardware)
