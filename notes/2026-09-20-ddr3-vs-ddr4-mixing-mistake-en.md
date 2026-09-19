---
audio: false
generated: true
image: false
lang: en
layout: post
title: DDR3 vs DDR4 Mixing Mistake
translated: false
type: note
---

Question: Can two DDR4 sticks of different brands and speeds (2400MHz vs 1600MHz) be used together in the same desktop?

Answer:

**Wait — DDR4 at 1600MHz doesn't exist as a standard.**

DDR4 starts at **2133MHz** as its minimum spec. **1600MHz is a DDR3 speed.** So you likely have:

- One **DDR4** stick at 2400MHz
- One **DDR3** stick at 1600MHz

---

**❌ DDR3 + DDR4 Cannot Work Together — Ever**

They are physically and electrically incompatible:

| Feature | DDR3 | DDR4 |
|---|---|---|
| Voltage | 1.5V | 1.2V |
| Notch position | Different | Different |
| Pin count | 240-pin | 288-pin |
| Socket | Incompatible | Incompatible |

The notch (key) on the stick is in a **different physical location**, so you literally **cannot insert the wrong type** into a slot — the motherboard will block it.

---

**If Both Are Actually DDR4 (Different Speeds)**

If you misread and both are DDR4 (e.g., 2133MHz + 2400MHz), then yes they *can* work together, but:

- Both sticks will **downclock to the slower speed** (2133MHz)
- You may need to set XMP/DOCP in BIOS manually
- Dual-channel may or may not activate depending on the motherboard
- Stability is not guaranteed — mixed brands can sometimes cause boot issues

---

**Bottom Line**

| Scenario | Compatible? |
|---|---|
| DDR3 (1600) + DDR4 (2400) | ❌ No — physically impossible |
| DDR4 (2133) + DDR4 (2400) | ✓ Yes — runs at 2133MHz |
| DDR4 different brands, same gen | ✓ Usually works |

Double-check the label on each stick — look for **"DDR3"** or **"DDR4"** printed directly on the sticker.