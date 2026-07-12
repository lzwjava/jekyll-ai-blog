---
audio: false
generated: true
image: false
lang: en
layout: post
title: Paperclip PSU Test Guide
translated: false
type: note
---

Question: How do I use the paperclip method to test whether my Great Wall (长城) 85W power supply is functioning, and how does the pin-4/pin-5 procedure work?

Answer:

The pinout note you pasted is describing the standard **ATX PS_ON# jumper test** — the trick works because on any ATX-spec 24-pin connector, shorting the green wire (**PS_ON#**, pulled to 5V internally) to a black wire (**COM/ground**) tells the PSU's control IC "motherboard says start up," bypassing the need for an actual motherboard.

**Why pin 4/5 works (electrically):**

The 24-pin connector has two rows of 12 pins. If you orient the connector with the plastic retention clip facing up and count left-to-right along the *top* row, PS_ON# and an adjacent ground land on positions 4 and 5. This is the same physical wire as "pin 16 → pin 17" in guides that count all 24 pins sequentially instead of by row — all of the 24 pin cables have the same pinout, even if the wires are not color-coded, so starting on the left side with the clip up and counting 4 pins to the right gets you there. Different vendors just document the count differently (sequential 1–24 vs row-relative). Your pasted instructions and the English-language guides describe the identical two pins.

**Procedure (clean version):**

```
1. Power off PSU, unplug from wall.
2. Disconnect every cable except the 24-pin main connector (and AC cable stays unplugged).
3. Orient 24-pin connector: latch/clip facing UP, pins facing you.
4. Count 4th and 5th pin, top row, left to right.
5. Bend a paperclip into a U-shape (strip any coating), insert both ends
   into pin 4 and pin 5 to bridge them.
6. Plug AC cable back in, flip PSU switch to "I" / ON.
7. Fan spins -> PSU can produce power and its self-protection/control IC works.
   Fan silent -> PSU is dead, or in zero-RPM idle mode with no load.
```

**Important caveat for your case:** a genuine ATX 24-pin connector is used on PSUs rated ~300W and up (that's what a full ATX motherboard needs). An 85W "Great Wall" (长城) unit is almost certainly **not** a standard desktop ATX PSU with a 24-pin connector — 85W is in the range of:

- A flex-ATX / mini-ITX embedded PSU (some do use a 24-pin or a 4/6/8-pin subset)
- A power brick / adapter for a specific device (NAS, thin client, POS terminal, industrial board)

Before doing the paperclip test, check:

```bash
# quick sanity check — does the label say "24-pin ATX", "Flex-ATX", or something proprietary?
# look for: model number printed on the PSU casing, then search datasheet
```

If your unit really does have a 24-pin main connector, the procedure above applies unchanged — the ATX spec is fixed regardless of wattage. If it's a proprietary DC brick instead, the paperclip trick doesn't apply at all; in that case, the actual test is a multimeter across output pins:

```
Expected rails (if standard ATX pinout is present):
+3.3V (orange), +5V (red), +12V (yellow), -12V (blue, legacy),
+5VSB (purple, always live even when PSU is "off"),
PS_ON# (green, ~5V floating, 0V when triggered),
COM (black, ground reference for all measurements)

multimeter test:
- Black probe -> any black/COM pin
- Red probe -> the rail you're checking
- Before jumper: PS_ON# should read ~+5V, all main rails ~0V
- After jumper (PSU "on"): PS_ON# should drop near 0V,
  +5V/+12V/+3.3V should be within ~5% of nominal, +5VSB always ~5V
```

If you can tell me the exact model number printed on the Great Wall unit (or share a photo), I can confirm whether it's ATX-pinout-compatible or a proprietary brick, and give you exact pin assignments instead of the generic spec.

References:

- [PSU Test, All cords are black — Tom's Hardware Forum](https://forums.tomshardware.com/threads/psu-test-all-cords-are-black.2583369/)
- [Testing your Power Supply Unit (Paperclip Test) — NZXT Support](https://support.nzxt.com/hc/en-us/articles/1260802863490-Testing-your-Power-Supply-Unit-Paperclip-Test)
- [Is my power supply dead?: The Paperclip Test — Antec Support](https://bobteam.freshdesk.com/support/solutions/articles/1000015319-is-my-power-supply-dead-the-paperclip-test)
