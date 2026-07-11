---
audio: false
generated: true
image: false
lang: en
layout: post
title: Two Power-On Failure Diagnoses
translated: false
type: note
---

Question: Explain the two diagnoses given for why the computer wouldn't power on — one being a loose motherboard power connector, the other a loose front-panel power-button connector.

Answer:

These are two distinct failure points in the power-on chain, and they matter because they sit at opposite ends of the circuit — one supplies power, the other triggers power. Worth understanding both precisely since you're about to assemble this exact system.

**1. Motherboard power supply connector (loose) — power delivery failure**

This refers to the **24-pin ATX main connector** (and possibly the **4+4 pin EPS12V / CPU power connector**) between your PSU (Corsair CX650F) and motherboard (MSI MAG B760M Mortar).

- The 24-pin feeds the board's VRMs, chipset, and peripheral rails.
- The 8-pin EPS12V feeds the CPU directly — critical for your i9-13900KF, which pulls significant transient current.
- If either is **loose or not fully seated**, you get one of these symptoms:
  - Completely dead system (no fans, no LEDs, no beep) — most common if 24-pin is loose, since the board never gets standby power (5VSB) to even respond to the power button.
  - System powers on for a split second then shuts off — classic symptom of a loose/partial EPS12V connection: board gets 5VSB and starts the boot sequence, but VRM can't sustain CPU power draw.
  - Random reboots under load — a semi-seated connector that works at idle but fails when current draw spikes (e.g., gaming, benchmarks).

Diagnostic clue: if the board doesn't even show a "standby power" LED (most MSI boards have one near the 24-pin), you're not getting 5VSB at all — reseat the 24-pin fully until you hear/feel the clip latch.

**2. Front panel start button connector (loose) — trigger circuit failure**

This is the **JFP1 header** (or dedicated 2-pin `PWR_SW` header) on the motherboard, connected via a tiny 2-pin connector from the case's front panel wiring (your Aigo Yueguangbaohe Mini case).

- This connector carries no real power — it's just a momentary switch closure that pulls a GPIO-like pin to ground, telling the board's power-on logic (via Super I/O chip) to assert `PS_ON#` to the PSU.
- If this connector is loose or misaligned (very easy on cramped mATX cases with tiny pin headers), pressing the power button does **nothing** — no fans spin, no LEDs, because the board never receives the signal to begin the power sequence, even though the PSU and 24-pin are fine and standby power is present.

Diagnostic clue: if the board's standby LED **is** lit (meaning 24-pin is fine and 5VSB is present) but pressing the power button does nothing, the fault is almost certainly the front-panel connector, not the PSU or main power link. You can confirm this by shorting the two `PWR_SW` pins directly with a screwdriver (a standard bench test) — if the system boots, the case button/connector is the culprit, not the PSU/24-pin.

**Why experts check both, in this order**

| Check | Symptom if faulty | Root cause layer |
| --- | --- | --- |
| 24-pin / EPS12V loose | No standby LED, totally dead | Power delivery |
| Front panel PWR_SW loose | Standby LED on, but button does nothing | Trigger/signal path |

These are the two most common "won't power on" root causes precisely because they're the two connectors most likely to be **partially seated but not fully clicked in** during a first build — especially in a compact case like your Aigo Mini, where cable routing is tight and front-panel headers are small (often just 1-2mm pins) and easy to misalign by one row.

**Practical tip for your build**

Given your parts list:

- The **MSI MAG B760M Mortar** typically groups front-panel pins as a single **JFP1** block (not individual pins), which reduces this exact loose-connector risk compared to older boards with separate pin headers — but it's still easy to shift the block by one pin row in a cramped mATX case.
- Push the 24-pin and 8-pin EPS12V connectors until you feel/hear the latch **click** — don't just seat by feel, since a "close enough" connection is often enough for standby power but fails under CPU load (matches symptom #2 above), which would present as a mysterious instability issue days into using the system rather than an obvious dead-on-arrival.

References:

- [MSI MAG B760M Mortar WiFi manual — front panel connector pinout](https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/support)
