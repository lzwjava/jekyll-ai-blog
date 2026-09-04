---
audio: false
generated: true
image: false
lang: en
layout: post
title: R68 Resistor on ASUS H81M-K
translated: false
type: note
---

**Question:** On the ASUS H81M-K motherboard, what is the component labeled **R68** located near the 4-pin ATX 12V connector?

**Answer:**

The component **R68** is a **resistor** — specifically a small SMD (surface-mounted) resistor placed near the **ATX12V** 4-pin power connector on the ASUS H81M-K board. Based on typical H81-series ASUS motherboard design practices:

- **What it is:** R68 is a pull-down or filtering resistor. On ASUS H81M-series boards, resistors in the R60–R70 range near the ATX12V connector are commonly used for **12V rail voltage sensing, filtering, or current limiting** on the power delivery circuit to the CPU VRM (Voltage Regulator Module).
- **Its role:** It helps stabilize or filter the 12V input signal before it reaches the CPU power delivery stage, or acts as part of a voltage divider for the PWM controller feedback loop.
- **Physical appearance:** Typically a tiny 0402 or 0603 SMD resistor with a value that varies by board revision (commonly in the range of a few ohms to several kΩ depending on its function).

> ⚠️ **Important note:** The ASUS H81M-K schematics and boardview files are not publicly released by ASUS. The exact value and circuit function of **R68 specifically** requires the boardview/schematic file (which exists in repair-community archives). Without access to the actual schematic, the exact resistance value cannot be confirmed definitively.

If you need the precise value for a board repair, I'd recommend:

1. Checking the **Badcaps.net** repair guide for H81M-K (a PDF repair guide exists there).
2. Using a boardview tool (like OpenBoardView) with the H81M-K `.brd` file if available.

---

**References:**

- [ASUS H81M-K User Manual – ManualsLib (Page 25, ATX Power Connectors)](https://www.manualslib.com/manual/565354/Asus-H81m-K.html?page=25)
- [ASUS H81M-K Motherboard Layout (Page 12)](https://www.manualowl.com/m/Asus/H81M-K/Manual/372249?page=12)
- [ASUS H81M-K Repair Guide – Badcaps.net](https://www.badcaps.net/forum/document-software-archive/schematics-and-boardviews/3483342-asus-h81m-k-motherboard-repair-guide)
