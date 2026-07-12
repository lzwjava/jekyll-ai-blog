---
audio: false
generated: true
image: false
lang: en
layout: post
title: Arduino Uno Three LEDs Lit Meaning
translated: false
type: note
---

The CH340 has been disconnected and **no new Arduino board is visible** on USB. So if you're looking at a physical Uno board with 3 LEDs lit, the board is either powered via USB from another cable or external power, and it's running whatever sketch was last uploaded to it.

Let me explain what the **3 lit LEDs** tell you:

### On the Arduino Uno R3 boards

| LED | Label | What controls it | Likely cause if ON |
| ----- | ------- | ----------------- | ------------------- |
| **1** | **ON** (green) | Power rail | Board has power — normal |
| **2** | **L** / pin 13 (yellow) | Your sketch (`LED_BUILTIN`) | Sketch has `digitalWrite(13, HIGH)` stuck on |
| **3** | **TX** (yellow) | ATmega16U2 serial chip | Serial data being transmitted — or 16U2 in noisy state |
| or | **RX** (yellow) | ATmega16U2 serial chip | Serial data being received — or 16U2 in noisy state |

### If you see ON + L + TX all steady

- **ON** = normal, power is OK
- **L** = your sketch set pin 13 HIGH and **isn't running the blink loop** — the 100ms blink at 5Hz is fast but still visible as rapid flashing, not steady-on. If it's **steady**, either:
  - The board froze / crashed after setting pin 13 HIGH
  - Or a different sketch was already on the board
- **TX** = the 16U2 is driving its TX line high (could be idle-line state with USB disconnected)

### What to try

1. **Press the RESET button** on the Uno — if it's a running sketch, it restarts: L should start blinking visibly
2. **Plug it back into USB** and check:

   ```bash
   ls /dev/ttyACM*
   ```

   Real Unos appear as `/dev/ttyACM0`, not `/dev/ttyUSB0`.
3. If it shows up, upload the standard Blink example (1s delay) to confirm the board is alive
