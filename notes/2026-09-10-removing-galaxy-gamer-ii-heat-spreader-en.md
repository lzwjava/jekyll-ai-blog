---
audio: false
generated: true
image: false
lang: en
layout: post
title: Removing Galaxy GAMER II Heat Spreader
translated: false
type: note
---

Question: Can you remove the orange/black heat spreader from this Galaxy GAMER II DDR4 stick?

Answer: **Yes, it can usually be removed**, but it is not designed to be removed frequently. The heat spreader is typically held by **adhesive thermal pads + clips/pressure**, rather than being permanently attached to the PCB.

For a used DDR4 module, I'd do this:

1. **Power off and remove the DIMM.**
2. Let it reach room temperature.
3. Look carefully at the **top/bottom edges** for clips or tabs.
4. If adhesive is holding the two halves together, gently warm the heat spreader with a **hair dryer** for ~30–60 seconds. Don't use a heat gun at high temperature.
5. Start separating from an **edge**, using a plastic card/pick.
6. **Do not pry against the memory chips** or bend the PCB.
7. Slowly peel the spreader away. The thermal pads may stick strongly to the DRAM chips.
8. Remove residual thermal-pad adhesive gently with **90%+ isopropyl alcohol** if necessary.

The important thing: **don't simply yank the orange/black metal pieces apart**. If the thermal pad is strongly bonded, you can actually pull a DRAM package off the PCB or crack the PCB.

If your goal is **GPU/DRAM repair experimentation**, removing the heat spreader is actually useful because you can identify the DRAM chips and markings underneath.

If you send me a photo of the exact GAMER II module, I can point out **where I'd pry first and where not to pry**.