---
audio: false
generated: true
image: false
lang: en
layout: post
title: Whine vs Buzz in Electronics
translated: false
type: note
---

Question: What does the word "whine" mean in this context?

Answer:

"Whine" here is being used in its literal, non-figurative sense — a **high-pitched, continuous sound**, similar to the noise a small child makes when complaining ("whining"), or a mosquito's buzz, or a small motor running at high RPM. In audio/electronics terminology, "coil whine" specifically describes:

- **Pitch**: high frequency, often 1 kHz–10 kHz range (whistling/singing quality), as opposed to a "hum" or "buzz" which implies lower frequency (50-500 Hz, more of a vibration-you-can-feel quality)
- **Character**: steady/tonal, sometimes with a warbling or pulsing quality that tracks CPU/GPU load changes

Your original description was 滋滋 (zī zī) — in English this maps more to **"buzzing"** or **"crackling"** rather than "whine." Zī zī suggests a lower, more textured/electrical-sounding noise (like static or a faint sizzle), whereas "whine" suggests a cleaner, higher singing tone (like a jet engine spooling down, or a dog whimpering).

This distinction actually matters diagnostically:

| Term | Sound quality | Typical cause |
|---|---|---|
| **Whine** | Clean, high-pitched, tonal | Inductor coil vibrating at its switching frequency — classic "coil whine" |
| **Buzz / crackle (滋滋)** | Lower, textured, electrical-sounding | Could be coil whine too, but also: loose component vibrating against something, a failing capacitor, or even a fan bearing issue as your friend suggested |
| **Hum** | Low, steady, droning | Usually mains-frequency (50/60 Hz) related — transformer hum, ground loop |
| **Click/tick** | Discrete, repeating | Relay switching (some PSUs click when protection circuits engage), or mechanical fan contact |

Since forum posts (which I cited) use "whine," "buzz," and "crackle" almost interchangeably when people describe electronic noise in English, I've been treating your 滋滋 as covering the same general phenomenon — but if you want to nail down the exact mechanism, it's worth describing more precisely whether it's a clean tone or a grainy/textured sound, since that would help distinguish "definitely an inductor" from "possibly something else mechanical or electrical that just happens to also come from near the VRM."
