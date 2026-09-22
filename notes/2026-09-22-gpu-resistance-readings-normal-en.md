---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Resistance Readings Normal
translated: false
type: note
---

Both images copied and analyzed. Here's what the vision model found:

## `gpu1.jpg`

| Field | Result |
|-------|--------|
| **Meter display** | `0.630` |
| **Mode** | Resistance — **20 kΩ range** |
| **Reading** | **0.63 kΩ** (630 Ω) |
| **Probed area** | Top-edge test point / header, near fan/power connector |
| **GPU** | Unidentified discrete GPU, cooler removed, die exposed, PCB text "94-1G-85" |
| **Damage** | None visible — thermal paste residue around die |

## `gpu2.jpg`

| Field | Result |
|-------|--------|
| **Meter display** | `1.137` |
| **Mode** | Resistance — **200 kΩ range** |
| **Reading** | **1.137 kΩ** |
| **Probed area** | SMD passive (likely resistor), top-right PCB near VRM/aux circuits |
| **GPU** | **NVIDIA GA104** — RTX 3060 Ti / 3070 OEM (likely Dell/Alienware prebuilt) |
| **Damage** | None visible |

## Interpretation

- Both are **resistance (Ω) measurements, not voltage** — so this is continuity/short-checking, not a powered rail check.
- **0.63 kΩ and 1.137 kΩ are neither shorts nor opens.** They're moderate resistance-to-ground paths — normal for many nodes (pull-ups, resistor/cap paths, IC I/O pins). On a GPU these alone don't indicate a fault.
- A **short** would read near **0.0 Ω**; an **open** would read **OL/"1"**. These readings are in between.
- **No visible damage** in either photo — no burns, bulged caps, or blown parts.
- The board is **GA104-based (RTX 3060 Ti / 3070)**, looks like an OEM/prebuilt variant.

## Verdict

So far: **no fault found.** The readings are consistent with a healthy, unpowered board. To diagnose further I'd need to know:

1. **What symptoms** the card has (no display? artifacts? no power? fans spin?)
2. **Which exact points** these two probes were on — the 0.63 kΩ and 1.137 kΩ values only mean something when tied to a specific test point/rail.
3. Voltage readings would be far more informative — probe the **12V, 5V, 1.8V, VDDCI, VDDC, VMEM** rails with the board powered and meter on DC volts.

Want me to cross-check these two values against known GA104 boardview test-point resistances?