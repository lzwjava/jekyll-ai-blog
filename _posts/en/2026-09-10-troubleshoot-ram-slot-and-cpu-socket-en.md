---
audio: false
generated: true
image: false
lang: en
layout: post
title: Troubleshoot RAM Slot and CPU Socket
translated: false
type: note
---

Question: **One RAM slot causes CPU↔DRAM cycling, while another slot stays on DRAM. What should you do next?**

Answer: This pattern makes me suspect **RAM slot / memory-channel / CPU socket contact** more than Debian or the HDD.

Do this systematically:

```text
1. Power off + unplug PSU
2. Clear CMOS
3. Remove the GAMER II stick
4. Inspect/clean the RAM contacts
5. Install ONE stick in the slot that previously behaved differently
6. Try POST
```

Then test **both slots with the same RAM stick**:

| Test                        | Result        |
| --------------------------- | ------------- |
| Stick → Slot A              | CPU ↔ DRAM    |
| Stick → Slot B              | DRAM stays on |
| Another DDR4 stick → Slot A | ?             |
| Another DDR4 stick → Slot B | ?             |

The key experiment is **another known-good DDR4 DIMM**. If both sticks fail in exactly the same way, the RAM itself becomes much less likely.

### Then inspect the LGA1151 socket

On the i5-6500, the memory controller is inside the CPU. **Bent/misaligned LGA1151 socket pins can cause DRAM initialization failure.**

Remove the cooler and CPU and inspect the socket under magnification:

```text
LGA1151 socket
       ↓
  tiny contact pins
       ↓
CPU memory controller
       ↓
DDR4
```

Look for a pin that is visibly different in angle/orientation from its neighbors.

Also check that the CPU cooler isn't excessively tight or causing the CPU to sit unevenly.

### One important correction

Don't conclude that the slot where the LED stays on **DRAM is necessarily the bad slot**. The two slots may correspond to different memory channels, and the different LED behavior tells us the POST process is failing at slightly different points.

**Best next experiment: another known-good DDR4 stick in each slot.** That will give us much more information than repeatedly trying the Debian HDD.

If you can upload a clear photo of the **RAM slots and LGA1151 socket**, I can inspect the physical setup with you.