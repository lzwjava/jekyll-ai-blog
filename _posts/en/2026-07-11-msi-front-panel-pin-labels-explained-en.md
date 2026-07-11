---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI Front Panel Pin Labels Explained
translated: false
type: note
---

**SW = Switch.**

So:

- **PWR SW** = **Power Switch** — the wire pair from your case's physical power button
- **RESET SW** = **Reset Switch** — the wire pair from your case's physical reset button

It's just an abbreviation MSI (and the industry generally) uses in the pin labeling — `PWR_SW+` / `PWR_SW-` on the header just mean "the two pins for the power switch's contact loop." When the button is pressed, it briefly bridges those two pins, which the motherboard's logic reads as "user pressed power" and triggers the ATX power-on sequence.
