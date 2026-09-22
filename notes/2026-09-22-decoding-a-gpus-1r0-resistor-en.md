---
audio: false
generated: true
image: false
lang: en
layout: post
title: Decoding a GPU's 1R0 Resistor
translated: false
type: note
---

Got it — **"1R0 2103"** is one component, likely a **1.0 Ω resistor** marked `1R0` with a `2103` date/batch code. And it reads **0 V**.

Here's the key: **0 V on a 1 Ω resistor is only meaningful if I know which circuit it's in.** A 1 Ω resistor on a GPU is almost always one of these:

## What a 1R0 resistor usually does on a GPU

| Location | Role | 0 V means |
| ---------- | ------ | ----------- |
| **Near VCore inductors / MOSFETs** | **Bootstrap** or **current-sense** resistor in the VRM phase | VRM is not switching (fault) |
| **Near the VRM controller chip** | **VCC feed** resistor (feeds 5V/12V into the controller) | Controller has no supply |
| **On a small signal line** | series resistor on **EN/PGOOD/SDA** | that signal is low |

## How to tell which one it is — check both ends

The fastest test: measure **each side of the 1R0 resistor to ground**, one at a time (black probe on ground):

| Reading | Meaning |
| --------- | --------- |
| **Both sides 0 V** | The rail feeding it is dead → go upstream |
| **One side 12V, other 0V** | Resistor open, OR the load after it is shorted |
| **One side 5V/3.3V, other 0V** | Same — resistor blown or downstream short |
| **Both sides 5V/3.3V** | Rail is fine — the 0V you saw was a measurement setup issue |

## What I need from you

1. **Where is this 1R0 physically?** Near the die/coils? Near a small IC? Near the power connector?
2. **What's on each side of it to ground?** (red probe on one end → note V, then the other end → note V)

That tells us if the **rail feeding it is dead** (upstream problem) or if the **resistor/load is bad**.

---

## Meanwhile — don't skip the main test

The most direct measurement is still the **VCore inductor** (grey coils around the die). Red probe on the inductor, black on ground:

- **0 V** → VRM dead/not enabled → we hunt the controller
- **12 V** → shorted high-side MOSFET
- **0.6–1.1 V** → VCore works, die itself is the suspect

Grab those two numbers (VCore inductor + each side of the 1R0) and I'll pinpoint the fault.
