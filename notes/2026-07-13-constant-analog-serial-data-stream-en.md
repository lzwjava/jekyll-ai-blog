---
audio: false
generated: true
image: false
lang: en
layout: post
title: Constant Analog Serial Data Stream
translated: false
type: note
---

The board is alive and running at **9600 baud**. It's sending serial data — ASCII numbers like `47\r\n`, `52\r\n`, `53\r\n`... These look like **analog readings** (e.g., `Serial.println(analogRead(A0))`).

This means **your sketch is already on the board, but it's NOT the Blink sketch** — it's one that reads an analog pin and prints it continuously.

Here's what the 3 LEDs mean:

| LED | State | Why |
|-----|-------|-----|
| **ON** (green) | ✅ Steady | Board has power — normal |
| **L** (pin 13) | ✅ On or blinking | The sketch may be driving it, or leftover state |
| **TX** (yellow) | ✅ **Steady** | The sketch is printing serial data constantly with no delays — TX LED stays lit because bytes are streaming non-stop |
| **RX** | off | Nothing is sending TO the board |

The constant serial printing (no `delay()` between prints) is why the TX LED appears solidly lit — it's sending data as fast as the UART can go.

Do you want me to help you **upload a fresh sketch** to the board? For example, the standard **Blink** example to verify it works, or your modified blink with the 100ms delay?