---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why GPU Leaves Gray Residue
translated: false
type: note
---

**Question:** Why does touching the GPU die on an old Quadro 410 leave a gray residue on my finger?

**Answer:**

That gray layer on your finger is almost certainly **dried, degraded thermal paste** that was originally applied between the GPU die and the heatsink's contact plate.

Here's what happened:

- **Thermal paste ages.** Over years of heat cycles, the compound dries out, cracks, and crumbles. The old factory paste dries and discolors on both the die and the heatsink's contact plate — and on an old workstation card like the Quadro 410, this paste can be over a decade old.

- **Most thermal pastes are gray.** Standard compounds use metal oxides (like zinc oxide or aluminum) or even silver particles as the thermally conductive filler, which gives them that characteristic gray/silver color.

- **It flakes off easily when dry.** Hardened, dried thermal paste comes off very easily, which is why just touching the die transfers it to your finger.

**What you should do:**

Since the paste is this degraded, it's doing a poor job of transferring heat. You should repaste the card:

1. Use high-concentration isopropyl alcohol (IPA) with a lint-free cloth or cotton swabs, using gentle circular motions to wipe away the dried paste.
2. Never use razor blades, metal scrapers, or abrasive materials on the GPU die — the die is exposed silicon and can be permanently scratched.
3. Apply a small pea-sized dot of fresh thermal paste (e.g., Arctic MX-4 or Thermal Grizzly Kryonaut) to the center of the die before reassembling the cooler.

This is completely normal for an old used GPU — nothing is broken, it just needs a repaste.

---

**References:**
- [How to remove old, hard thermal compound from GPU die – Overclock.net](https://www.overclock.net/threads/how-to-remove-old-hard-thermal-compound-from-gpu-die.1720856/)
- [How to Replace GPU Thermal Paste – computerinfobits.com](https://knowledge.computerinfobits.com/hardware/gpu/thermal-paste-replacement)
- [Repaste Your GPU – Gamer Hardware](https://gamerhardware.org/repaste-gpu-thermal-paste/)
