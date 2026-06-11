---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Chip Creation: Design and Manufacture"
translated: false
type: note
---

**Question:** What do Lam Research (LRCX), Cadence (CDNS), and Synopsys (SNPS) actually do?

**Answer:**

These three sit at different points of the chip creation pipeline. Think of it as: design the chip (Cadence/Synopsys) → manufacture the chip (Lam's machines inside TSMC/Samsung/Intel fabs).

**Lam Research (LRCX) — wafer fabrication equipment**

Lam builds the machines that physically carve chips out of silicon. Its two core specialties are *etch* and *deposition*:

- **Etch**: removing material with atomic precision. After lithography (ASML's domain) projects a circuit pattern onto a wafer, Lam's plasma etch tools selectively strip away material to actually create the 3D structures — transistor fins, contact holes, the deep vertical channels in 3D NAND.
- **Deposition**: the inverse — laying down ultra-thin films of materials (oxides, nitrides, metals) layer by layer, often just a few atoms thick.

Lam is especially dominant in memory manufacturing. 3D NAND is basically an etch/deposition problem: you stack 200+ layers of film, then etch holes through the entire stack with aspect ratios like drilling a perfectly straight 1-meter hole the width of a human hair. SK Hynix, Micron, Samsung, Kioxia — all heavy Lam customers. The HBM boom directly drives Lam's revenue because more memory layers and advanced packaging (TSVs, hybrid bonding) mean more etch/dep steps per wafer.

Its main peers are Applied Materials (broader portfolio) and Tokyo Electron. ASML does lithography; Lam does almost everything around it.

**Cadence (CDNS) and Synopsys (SNPS) — EDA (Electronic Design Automation)**

These two form a near-duopoly in chip design software. A modern chip like an H100 has ~80 billion transistors — no human places those by hand. EDA tools are the compilers of hardware:

- **Logic synthesis**: you write the chip in an HDL (Verilog/SystemVerilog) describing behavior — registers, ALUs, control logic. Synthesis tools (Synopsys Design Compiler/Fusion Compiler, Cadence Genus) compile that RTL into a netlist of actual logic gates mapped to a foundry's standard cell library, analogous to GCC turning C into machine code for a specific ISA.
- **Place and route**: deciding where each of billions of gates physically sits on the die and routing the wires between them, while meeting timing closure (signals arriving within a clock cycle), power, and area constraints. This is a massive constrained optimization problem — Cadence Innovus, Synopsys IC Compiler.
- **Verification and simulation**: simulating the design before taping out, since one logic bug after fabrication costs tens of millions and months. Verification is often >50% of a chip project's effort.
- **IP licensing**: Synopsys in particular sells pre-designed blocks — PCIe, DDR/HBM PHYs, USB, Arm-alternative interfaces — so design teams don't reinvent commodity components. Synopsys also acquired Ansys (2025), adding multiphysics simulation.

Practically every chip you've heard of — NVIDIA GPUs, Apple silicon, the MI300X you train on — was designed using Cadence and Synopsys tools, usually both, since teams mix and match. That's why they're considered "picks and shovels": when hyperscalers like Google, Amazon, Meta, and OpenAI all start designing custom ASICs, every new design team becomes a new EDA license customer, regardless of whose chip ultimately wins.

The mental model for the whole stack:

```
Synopsys/Cadence (design software + IP)
        ↓ GDSII layout file
TSMC/Samsung fabs
        ↓ using
ASML (lithography) + Lam/AMAT/TEL (etch, deposition) + KLA (inspection)
        ↓
finished wafer → packaging (HBM stacking, CoWoS) → your MI300X
```

Business-wise, EDA (Cadence/Synopsys) is software-margin, subscription-like, and less cyclical; equipment (Lam) is capex-driven and swings with fab spending cycles — which is the trade-off between the two if you're comparing them as investments.
