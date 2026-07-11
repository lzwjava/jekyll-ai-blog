---
audio: false
generated: true
image: false
lang: en
layout: post
title: JFP1 Wiring Errors Are Safe
translated: false
type: note
---

Good news: JFP1 is about as low-risk as motherboard connectors get. Here's exactly what happens for each possible mistake:

**Power Switch / Reset Switch wired wrong (swapped, reversed, or even mixed up with each other)**
- Zero risk. These are just simple momentary contact switches — no polarity, no signal direction that matters electrically.
- Worst case: pressing "power" does nothing, or pressing "reset" acts like a power switch instead. Nothing gets damaged. You just swap the connector around until it does what you expect.

**Power LED wired backwards (+ and − swapped)**
- Zero risk to hardware. An LED is a diode — current only flows one direction.
- Worst case: the LED simply stays dark when the PC is on. No board damage, no fire risk, nothing burns out. Flip the connector and it lights up.

**Plugging into completely the wrong pins (e.g., landing on pins 1/3/10 which are unused, or straddling the missing pin 9 by accident)**
- If you land on unused/reserved pins: nothing happens — no short, no damage, the switch/LED just won't function until you find the right pins.
- If you literally can't seat the connector because of the missing pin 9 (the key), that's actually a safety feature — it physically prevents you from plugging in backwards in the first place, since standard front-panel connector housings are shaped to match that gap.

**What genuinely would be risky (but isn't relevant here):**
- Shorting a 12V rail to ground with a stray wire touching pins outside the connector's housing — that's a general "loose wire touching board" risk, not specific to JFP1 wiring choices.
- JFP1 itself carries only low-current logic-level signals (not power delivery), so even a dead-wrong connection can't take out your CPU, RAM, or GPU.

Bottom line: wire it, power on, see what works. If power switch does nothing, try reset instead (or vice versa). If the LED is dark, flip that 2-pin connector. Worst case is a 30-second re-seat, not a damaged board.
