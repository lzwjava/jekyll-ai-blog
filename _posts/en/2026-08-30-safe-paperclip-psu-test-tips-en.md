---
audio: false
generated: true
image: false
lang: en
layout: post
title: Safe Paperclip PSU Test Tips
translated: false
type: note
---

Question: Is it safe to use your hand on the paperclip when doing a PSU paperclip test?

Answer: **Yes, your understanding is basically right, but there is one important distinction.**

For a standard ATX PSU paperclip test:

1. **Turn the PSU OFF and unplug it.**
2. Insert the paperclip between **PS_ON (usually green)** and **GND (usually black)** on the 24-pin connector.
3. Ideally, **do not hold/touch the exposed paperclip while powering the PSU.**
4. Make sure the paperclip is firmly inserted and won't fall out or short another pin.
5. Plug the PSU into AC power and switch it ON.
6. **Don't touch or reposition the paperclip while the PSU is powered.**
7. Turn the PSU **OFF and unplug it** before removing the paperclip.

### Why?

The paperclip itself isn't normally carrying a dangerous voltage on the **green-to-black PS_ON connection**. PS_ON is a low-voltage control signal.

However, once the PSU is running, there are **lethal voltages inside the PSU** (the primary side can be around 325 VDC after rectification from 230 VAC, and even higher transiently). The dangerous part is **not the exposed paperclip itself**, but the possibility of touching something else, slipping, or accidentally bridging contacts.

Also, a metal paperclip is easy to accidentally move and short adjacent pins.

### Best practice

Instead of holding a loose paperclip:

```text
24-pin ATX
┌──────────────────────────┐
│ ... [GREEN] [BLACK] ...  │
│        ↑       ↑         │
│       PS_ON    GND       │
└──────────────────────────┘
       └── paperclip ──┘
```

Use a **proper ATX PSU jumper/tester** or insulate most of the paperclip so only the two insertion ends are exposed.

**And never open the PSU enclosure just to perform this test.** That's where the genuinely dangerous mains/high-voltage circuitry is exposed.

For GPU repair work, I'd strongly recommend using a **PSU tester + multimeter** rather than repeatedly doing the paperclip trick.