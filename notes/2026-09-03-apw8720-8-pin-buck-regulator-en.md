---
audio: false
generated: true
image: false
lang: en
layout: post
title: APW8720 8-Pin Buck Regulator
translated: false
type: note
---

Question: What does each of the 8 pins on the **APW8720 / P57F** chip do?

Answer: I can explain the typical 8-pin buck-regulator topology, but I **would not assign exact pin numbers yet** from the marking alone. `P57F` is likely a top-mark/lot code, while **APW8720** identifies the IC family. The exact package/pinout should be verified against the specific datasheet/board.

Conceptually, an 8-pin buck regulator looks like this:

```text
                 GPU power rail
                      │
                    L ──────── VOUT
                      │
                 ┌────┴────┐
                 │         │
             capacitor   GPU core/
                 │        memory/etc.
                GND

        ┌─────────────────────┐
 VIN ──►│                     │
 EN  ──►│     APW8720         │
 FB  ◄──│                     │
 GND ──►│                     │
        │                     │
        │   switching node ───┼────► L
        └─────────────────────┘
```

The pins generally fall into these roles:

| Function         | What it does                  | Multimeter meaning                |
| ---------------- | ----------------------------- | --------------------------------- |
| **VIN**          | Input supply to the regulator | Usually several volts             |
| **GND**          | Ground/reference              | 0 V                               |
| **EN**           | Enable/on-off control         | Low = off, high = on              |
| **FB**           | Feedback from output          | Usually a small reference voltage |
| **SW/LX**        | Switching node                | Rapidly switches between voltages |
| **COMP/PG/etc.** | Control/monitoring            | Depends on exact IC               |

### The interesting one: SW/LX

This is the pin connected toward the **inductor**.

For example:

```text
12 V
 │
 │
MOSFET / regulator
 │
 └──── SW ────┬──── L ────── 1.0 V
              │
          switching
            node
```

An oscilloscope would see a rapidly switching waveform here. A normal multimeter in DC mode will usually show an **average-ish voltage**, which can be misleading.

### For GPU repair, trace the inductor first

This is much more useful than trying to guess the IC pins:

```text
APW8720
   │
   │ SW
   ▼
 [ L ]
   │
   ├──────────────► GPU power rail
   │
  [C]
   │
  GND
```

If you find the large inductor immediately beside the APW8720, one side is usually the **switching side** and the other side is the **regulated output**.

With the GPU **powered off**, you can safely use continuity/resistance mode to map:

```text
APW8720 pin ── trace ── inductor ── capacitor ── GPU
```

Then with power **on**, measure the output side of that inductor to ground.

**If you send me a sharp close-up photo of the APW8720 and its surrounding components, I can map the actual 8 pins on your Quadro 410 one-by-one and tell you exactly where to put the red/black probes.**
