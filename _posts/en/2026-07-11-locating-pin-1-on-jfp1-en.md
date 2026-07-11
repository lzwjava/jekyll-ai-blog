---
audio: false
generated: true
image: false
lang: en
layout: post
title: Locating Pin 1 on JFP1
translated: false
type: note
---

Not necessarily — "edge-most" isn't a reliable rule since header orientation varies by board layout. What you want to look for instead:

1. **A printed "1" on the PCB silkscreen** right next to the header — MSI almost always marks pin 1 this way, usually in tiny white text.
2. **A square/rectangular solder pad** — pin 1's solder pad on the underside (or sometimes visible from top as a slightly different pad shape) is typically square while all others are round. This is a very reliable convention across virtually all motherboard headers, not just JFP1.
3. **The missing pin 9** — since JFP1 is a 2×5 block with pin 9 physically absent, once you find that gap, pin 1 is on the *same row* as the gap, at the *opposite end* of that row from the gap. So if the missing pin (9) is on the far end of one row, pin 1 is the near end of that same row.

Concretely: the header is two rows of 5. One row is 1-3-5-7-9(missing), the other is 2-4-6-8-10. Pin 1 and pin 9 are on the same row; pin 1 is the end of the row furthest from where the gap sits, pin 2 sits directly across from pin 1 on the other row.

If you can get a clear photo of the header (even a phone pic), I can confirm pin 1's exact position for you rather than you having to guess from silkscreen text, which can be tiny and easy to misread.
