---
audio: false
generated: true
image: false
lang: en
layout: post
title: EMI Shielding Cans Explained
translated: false
type: note
---

**Question:** What are those steel/metal shield-shaped things found on circuit boards in GPU cards and convenience store refrigerator control boards? Are they related to lithium (锂) or something else?

**Answer:**

Those metal "shield" shapes on PCBs are called **EMI shielding cans** (also known as RF shields or shielding cages) — and they have nothing to do with lithium. Here's what they do:

**What they are:**
They are metal cans — a type of Faraday cage — used to enclose electronic circuits on a PCB. They limit the amount of electromagnetic interference (EMI) radiation from the external environment that can disrupt components, and also prevent EMI generated inside from escaping outward.

**What they're made of:**
They are closed metal cans made from materials like brass, nickel silver, or stainless steel, connected to the ground of the PCB. They effectively reduce loop antenna sizes, and absorb and/or reflect electromagnetic radiation.

**Why they look the way they do:**
These very thin sheet metal enclosures are soldered onto the PCB — they can be quickly and reliably placed on an SMT (surface-mount technology) assembly line. They come in standardized form factors with a specific footprint, headroom, and shape.

**Why they're on refrigerators and GPUs:**
Modern electronics are full of EMI concerns — with clock speeds in the GHz and switching regulators in the megahertz, and wireless radios appearing everywhere, the electromagnetic noise within and around a PCB is extremely cluttered. Without shielding, a device may fail regulatory tests (FCC, CE, CISPR), experience self-interference, or cause interference with surrounding equipment.

In short: they're **electromagnetic shields**, not batteries or anything lithium-related. They protect sensitive circuits from radio/electromagnetic noise — essential in any modern appliance or computer component.

**References:**
- [EMI Shielding for PCBs: Best Practices – JLCPCB](https://jlcpcb.com/blog/emi-shielding-pcb)
- [Shield: Using Metal Shield Cans on PCB for EMI Shielding – MADPCB](https://madpcb.com/glossary/shield/)
- [EMI Basics and Board Level Shielding Design – Interference Technology](https://interferencetechnology.com/emi-basics-and-board-level-shielding-design/)
