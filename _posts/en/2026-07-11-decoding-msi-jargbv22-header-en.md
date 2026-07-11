---
audio: false
generated: true
image: false
lang: en
layout: post
title: Decoding MSI JARGBV2_2 Header
translated: false
type: note
---

**Question:** What does `JARGBV2_2` mean on the MSI MAG B760M Mortar WiFi motherboard?

**Answer:**

Breaking down the label the same way as `JAUD1`:

- `J` = header/jumper (generic MSI prefix)
- `ARGB` = **Addressable RGB** — each LED on the strip/fan can be individually addressed and controlled (vs. plain RGB where the whole strip is one color)
- `V2` = **Version 2** of MSI's ARGB header spec — this matters a lot, don't skip it
- `_2` = the **second** instance of this header type on the board (so there's also a `JARGBV2_1` elsewhere)

**Why the V2 matters (electrical, not cosmetic):**

MSI has shipped two incompatible ARGB header generations:

| | Pins | Voltage | Pin order |
|---|---|---|---|
| Old ARGB (`JRGB`, no V2 tag) | 4-pin | 12V | +12V, G, R, B (non-addressable) |
| ARGB V2 (`JARGBV2`) | 3-pin | **5V** | +5V, Data, GND |

These are **not interchangeable**. If you plug a 12V ARGB device into a 5V header (or vice versa), worst case you fry the LEDs or the header itself. MSI added the `V2` suffix specifically so you don't confuse the two when wiring — always match the header type printed on the device's own cable/box to the header type on the board.

**Practical use:**
1. Find `JARGBV2_2` on the board (B760M Mortar typically has two of these headers — one near the 24-pin ATX connector, one lower near the PCIe slots — hence `_1` and `_2`).
2. Connect any 3-pin 5V addressable RGB fan/strip/AIO pump here — the connector is keyed so it only seats one way.
3. Control the lighting via MSI Mystic Light software, or sync it to motherboard RGB profiles in BIOS.
4. If you have a non-addressable single-color 12V RGB strip instead, you need the separate 4-pin `JRGB1` header (also present on this board) — not this one.

Same decoding rule applies board-wide: once you know MSI's `J + function + version + instance` scheme, you can read `JAUD1`, `JARGBV2_1/2`, `JUSB4` (front panel USB-C), `JFP1` (power/reset switches + LEDs) etc. straight off the silkscreen without opening the manual PDF.
