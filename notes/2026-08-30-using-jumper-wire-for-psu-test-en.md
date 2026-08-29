---
audio: false
generated: true
image: false
lang: en
layout: post
title: Using Jumper Wire for PSU Test
translated: false
type: note
---

Question: Can I use a breadboard jumper wire instead of a paperclip for the PSU test?

Answer: **Yes.** If you used a standard **male-to-male Dupont/breadboard jumper wire** to bridge **PS_ON (green) → GND (black)** on the 24-pin ATX connector, and the PSU fan starts, that's a valid way to perform the test.

For your 航嘉 PSU:

```text
24-pin ATX
PS_ON (green) ───── jumper wire ───── GND (black)
```

A few important points:

* **Turn PSU OFF/unplugged before inserting/removing the wire.**
* Once powered on, **don't touch or move the jumper**.
* Make sure the jumper is **only between the green pin and one black GND pin**.
* Don't let the metal ends touch neighboring pins.
* A normal thin Dupont jumper is fine for the **PS_ON control signal**; it isn't carrying the PSU's main output current.
* **Fan spinning is a good sign, but doesn't prove the PSU is fully healthy.** You should still measure the rails with a multimeter: **+12 V, +5 V, +3.3 V**.

One subtle point: **some modern PSUs have semi-passive/hybrid fan modes**, so *fan not spinning* does not necessarily mean a PSU is dead. But if this particular 航嘉 model normally spins its fan immediately when started, seeing it spin confirms that the PS_ON test is working.

If you're testing PSUs for your GPU-repair work, the next useful step is learning how to **check all ATX rails with a multimeter safely**, rather than relying on the fan.