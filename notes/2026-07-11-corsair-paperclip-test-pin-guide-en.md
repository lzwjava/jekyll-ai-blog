---
audio: false
generated: true
image: false
lang: en
layout: post
title: Corsair Paperclip Test Pin Guide
translated: false
type: note
---

This matches Corsair's official jumper test procedure almost verbatim, so let me verify pin numbering precisely rather than rely on memory, since getting pin 4/5 wrong on a live 24-pin connector is exactly the kind of physical mistake you can't afford here.Question: Does this Corsair-style paperclip test procedure (using "pin 4 and pin 5" when counting from the left with clip/tab up) match the standard method, and is it safe to follow as written?

Answer:

Yes — this is Corsair's official jumper-test procedure, word-for-word close to their support doc. But there's one critical ambiguity in the wording that you need to resolve correctly before you touch anything, because getting it wrong shorts the wrong rail.

**The ambiguity: "pin 4 and pin 5" ≠ literal pin numbers 4 and 5**

Corsair's actual instructions say: "Locate pin 16 and pin 17 on your 24-pin cable. To find pin 16 and pin 17, count from the left with the clip facing up and the pins facing toward you. They will be the 4th and 5th pins when counting from left to right"

So "pin 4 and pin 5" in your transcription means the **4th and 5th physical slot positions you count to**, in that specific orientation — and those slot positions correspond to the **actual numbered pins 16 (PS_ON#) and 17 (GND)** on the standard ATX pinout, not to the literally-numbered pins 4 and 5 you'd find on a generic 24-pin pinout diagram.

This distinction matters a lot: on the standard ATX numbering, actual pin 4 = +5V and actual pin 5 = GND. If you cross-referenced a generic pinout chart and shorted *those*, you'd be shorting a live +5V rail to ground instead of triggering the PS_ON signal — not what you want.

**So the correct reading of your procedure is:**

1. PSU off, unplugged from wall.
2. Disconnect everything except you're about to test the bare 24-pin connector alone (no motherboard, no AC yet).
3. Hold the 24-pin connector with the **locking clip/tab facing up, pins facing you**.
4. Count **4 slots in from the left, then the 5th slot** — these two slots are where the real PS_ON# (pin 16) and GND (pin 17) wires sit. This still indicates that the PSU is functioning normally when the fan spins.
5. Bend paperclip, insert one end in slot 4, other end in slot 5, bare metal only touching those two slots and nothing else.
6. Plug AC cord in, flip PSU switch to On.
7. Watch fan.

**Interpreting the result — confirmed by Corsair:**

- Fan spins → the PSU is functioning normally
- Fan doesn't spin at all, even briefly → Many Corsair PSUs have a zero-RPM feature that results in the fan only spinning for a moment after the PSU is powered on, so don't panic on zero spin alone — wait and watch closely for even a brief spin-up pulse. If truly nothing happens (no spin at all, ever, not even a twitch) → PSU is dead.

**One practical tip to remove the ambiguity entirely:** don't count pins by eye at all. Buy a ~15-20 CNY 24-pin PSU jumper/tester plug (search "PSU 24pin 跳线帽" or "PSU tester 24针" on Taobao) — it's a small block that plugs into the 24-pin connector and internally bridges the correct pins for you, zero risk of miscounting. Given you're trying to minimize physical-iteration risk on a 15k rig, spending 15 CNY to eliminate a manual counting error is the correct trade — this is the hardware equivalent of writing a test instead of eyeballing the output.

References:

- [PSU: How to test a PSU (Power Supply Unit) – Corsair](https://help.corsair.com/hc/en-us/articles/360025085372-PSU-How-to-test-a-PSU-Power-Supply-Unit)
- [How to Test a PSU (Power Supply Unit) | CORSAIR](https://www.corsair.com/us/en/explorer/diy-builder/power-supply-units/how-to-test-a-psu-power-supply-unit/)
