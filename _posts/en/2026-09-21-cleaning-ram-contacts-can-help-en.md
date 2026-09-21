---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cleaning RAM Contacts Can Help
translated: false
type: note
---

Question: Is rubbing the DDR4 RAM’s gold contacts with an eraser useful if the RAM is not recognized and the CPU/DRAM debug LEDs alternate?

Answer: **Yes, it can help, but only as a cleaning step—not as the primary diagnosis.**

If the motherboard alternates between **CPU and DRAM debug LEDs**, a bad electrical connection between the DIMM and slot can absolutely cause this. Lightly cleaning the DDR4 gold contacts can remove oxidation/contamination.

However, I would do it this way:

1. **Power off completely**

   * Shut down.
   * PSU switch → OFF.
   * Unplug power.
   * Press the case power button once to discharge.

2. **Remove the DIMM.**

3. **Inspect the gold contacts.**

   * Look for dirt, oxidation, scratches, or obvious damage.
   * Also inspect the DIMM slot for dust/debris.

4. **Preferably clean with 90%+ isopropyl alcohol and lint-free material.**

   * If you use an eraser, use a **clean, soft white eraser**.
   * Rub **very gently along the contacts**, not aggressively.
   * Remove all eraser residue afterward.
   * Don't use a rough/pink abrasive eraser.

5. **Reinstall the RAM firmly.**

   * Make sure the locking tabs actually click into position.
   * For one DIMM, use the motherboard's recommended slot, usually **A2**.

6. **Test systematically:**

   ```text
   DIMM #1 → A2 → boot
   DIMM #1 → B2 → boot
   DIMM #2 → A2 → boot
   DIMM #2 → B2 → boot
   ```

   If you have two sticks, this is much more useful than repeatedly cleaning them.

Also, after changing RAM configuration, give the motherboard **a few minutes for DDR4 memory training**, especially after clearing CMOS or changing DIMMs. Don't immediately assume it's dead if the debug LEDs cycle for a while.

### Important clue

If the LEDs go:

```text
CPU → DRAM → CPU → DRAM → ...
```

that can indicate the system is repeatedly failing POST rather than simply "bad RAM." Possible causes include:

* DIMM not seated correctly
* dirty/damaged DIMM contacts
* bad DIMM
* bad DIMM slot
* incompatible/incorrect memory configuration
* CMOS/BIOS configuration problem
* CPU/socket contact problem — the CPU's memory controller is on the CPU
* motherboard problem

So **cleaning the contacts is worth trying**, but the **one-stick / one-slot matrix** above will tell you much more about what's actually failing.
