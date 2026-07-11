---
audio: false
generated: true
image: false
lang: en
layout: post
title: Locating JFP1 Pin 1
translated: false
type: note
---

Looking at your photo — I can see the **JFP1** label printed vertically next to the connector block (rotated 90° along with the board, same as "MORTAR" and "SYS_FAN4 / SATA-5~6" text nearby). The header itself does show the 2×5 layout with one position missing/keyed, consistent with the standard 9-pin JFP1.

Here's the honest limitation: the photo is too blurry/dark at that specific connector for me to reliably read a printed "1" or spot a notch on the plastic housing itself — that text would be extremely small (sub-1mm silkscreen), and camera focus is on the wider "MORTAR" branding, not the header.

What I can tell you reliably:
- The **missing pin (the key)** is your best anchor — find that gap physically with your finger/eye on the actual board (much easier in person than in a photo).
- Once you have the gap located, **pin 1 is the pin on the same row as the gap, at the far end of that row** (i.e., diagonally opposite the missing pin across the whole connector).
- MSI boards specifically print a tiny **"1"** right at that corner in silkscreen — worth looking with a flashlight and maybe your phone's macro mode if it has one, directly on the board rather than through this photo.

If you want a definitive read, take a **straight-on, well-lit, close-up shot** of just the JFP1 connector (fill the frame with just that header, not the whole board) — ideally with a flashlight angled across it so the silkscreen text casts a shadow and becomes legible. I can then tell you exactly which physical corner is pin 1.
