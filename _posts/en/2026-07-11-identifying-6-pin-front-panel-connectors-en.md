---
audio: false
generated: true
image: false
lang: en
layout: post
title: Identifying 6-Pin Front Panel Connectors
translated: false
type: note
---

Good question — "6 pins" usually means your case bundles the front-panel connectors differently than the raw 9-pin JFP1 header expects. A couple of common configurations exist, so let me get this right rather than guess.

Can you check what's printed on the wires/connector housing? Look for small text like `PWR SW+`, `PWR SW-`, `RESET SW`, `H.D.D. LED`, `POWER LED`, or `+`/`-` symbols molded into the plastic. Usually each function comes as a separate small connector (2-pin), and "6 pins total" likely means you're missing one function (e.g. no HDD LED cable) — three 2-pin connectors × 2 pins = 6.

Most likely breakdown for 6 pins = 3 connectors:
- **Power Switch** (2 pins, unlabeled polarity, momentary switch) → **JFP1 pins 6 + 8**
- **Reset Switch** (2 pins, unlabeled polarity, momentary switch) → **JFP1 pins 5 + 7**
- **Power LED** (2 pins, has polarity: usually white wire = ground/−, colored wire = +) → **JFP1 pins 2 + 4** (align the + lead with pin 2)

If that's your case, you're just missing an HDD LED cable, or your case combined it into the case's SATA/NVMe activity detection elsewhere (some cases skip HDD LED entirely on modern builds since M.2 activity isn't always wired to a header).

If instead your 6 pins are a **single connector block** (one plastic housing, 6 pins in a row, not 3 separate 2-pin clips), that's a different story — some cases (Fractal, Corsair, some NZXT) mold Power SW + Reset SW + Power LED into one connector meant to straddle specific pins directly. In that case, tell me:
- Is it one connector or three separate ones?
- Any text printed on the connector (even faint)?
- Wire colors (e.g. white/black pair, blue/white pair)?

That'll tell me exactly which JFP1 pins each wire needs, since guessing wrong on the switches won't hurt anything but guessing wrong on LED polarity just means it won't light up until you flip it.
