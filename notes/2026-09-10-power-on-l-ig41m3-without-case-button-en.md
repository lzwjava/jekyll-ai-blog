---
audio: false
generated: true
image: false
lang: en
layout: post
title: Power On L-IG41M3 Without Case Button
translated: false
type: note
---

Question: You want to start the **Lenovo L-IG41M3** on a workbench without connecting the case's power-button board, by briefly shorting the correct two pins on `F_PANEL`.

Answer: **Yes. You can do exactly that.** A normal PC power button is just a momentary switch: it briefly connects the two power-button pins.

For your **L-IG41M3**, the schematic gives the `F_PANEL` pinout explicitly. ([ManualMachine][1])

```text
             F_PANEL
       ┌───────────────────┐
       │  1  3  5  7  9  11  13 │
       │  o  o  o  o  o   o   x  │
       │  o  o  o  o  o   o   o  │
       │  2  4  6  8 10  12  14 │
       └───────────────────┘

       9  = PS / Power Switch
      11  = GND
```

So for **power-on**:

```text
Pin 9 ─────────┐
               │  ← briefly short
Pin 11 ────────┘
```

### Easiest workbench method

You **don't need a switch board**.

Use a small **flat-head screwdriver**:

1. Connect PSU → motherboard.
2. Install CPU + RAM, etc.
3. Turn PSU on.
4. Touch the screwdriver tip to **pin 9 and pin 11 simultaneously** for about **0.5 second**.
5. Remove it.

That's electrically equivalent to pressing the PC's power button.

A screwdriver is actually convenient for GPU repair/testing benches because you don't need to keep a case switch attached.

### If you want a permanent easy connector

You can buy a cheap **2-pin Dupont jumper / 2-pin JST-style switch**, or simply make a tiny cable:

```text
          momentary switch
       ┌──────────────────┐
pin 9 ─┤                  ├─ pin 11
       └──────────────────┘
```

The switch **doesn't have polarity**. Either wire can go to either pin.

You can also buy a generic **2-pin PC Power SW cable** and plug it directly onto pins 9/11.

**Important:** don't confuse this with the common modern ATX 9-pin front-panel layout. The L-IG41M3 uses a Lenovo-specific **2×7 F_PANEL header**, and its schematic explicitly identifies `PS` at pin 9 and `GND` at pin 11. ([ManualMachine][1])

If you upload a clear photo of your actual `F_PANEL` header, I can mark **exactly which two physical pins are 9 and 11** so you don't have to worry about orientation.

I can also give you a **minimal workbench wiring setup for this L-IG41M3**—PSU + power-on pins + speaker + CMOS + GPU test—so you can use it as your GPU repair test board.

[1]: https://manualmachine.com/ecs/lig41m3/24375062-schematics--rev-1/?utm_source=chatgpt.com "ECS L-IG41M3 Schematics REV 1.1 - ManualMachine.com"
