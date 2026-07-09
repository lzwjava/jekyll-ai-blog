---
audio: false
generated: true
image: false
lang: en
layout: post
title: Controlling Arduino TX and RX LEDs
translated: false
type: note
---

**Question:** On an Arduino Uno, can I blink the TX, RX, or R9/R7/R8-labeled LEDs the way I blink `LED_BUILTIN`, and is the modified delay code correct?

**Answer:**

Short answer: **no, not directly** — TX/RX are hardware-driven, not GPIO-controlled.

**Why:**

On the Uno R3, there are 3 onboard LEDs near the USB port area:

| LED | Driven by | Controllable via sketch? |
|---|---|---|
| `L` (pin 13) | ATmega328P PB5, through a resistor (commonly silkscreened R9 depending on revision) | **Yes** — this is `LED_BUILTIN` |
| `TX` | ATmega16U2 (USB-to-serial bridge) TXD line, through a resistor (R7-ish) | **No** — hardware only |
| `RX` | ATmega16U2 RXD line, through a resistor (R8-ish) | **No** — hardware only |

The TX/RX LEDs are wired to the *USB-serial chip's* UART pins, not to any GPIO pin your sketch can address with `digitalWrite`. They light up automatically whenever bytes move across USB serial — including during `Serial.print()` calls, and during sketch upload. There's no pin number in the Arduino core that maps to them, so `digitalWrite(TX_LED, ...)` isn't a thing on stock Uno hardware.

If you want them to blink deliberately, the only lever you have is generating serial traffic:

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println("x");   // TX LED flickers on this
  delay(100);
}
```

That's indirect and flickery, not a clean on/off blink — don't use this as your "blink" LED. Use `LED_BUILTIN` for controlled blinking.

**Your code diff:**

The intent (100ms on / 100ms off instead of 3000/3000) is fine, but line 10's comment is stale (`// wait for 3 seconds` still, should say `100ms`). Corrected:

```cpp
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on
  delay(100);                       // wait 100ms
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED off
  delay(100);                       // wait 100ms
}
```

This gives you a 5Hz blink on pin 13 (`L`). If your goal was actually to have a visual indicator during serial/agent communication (e.g. blink LED when your CLI agent sends a command over serial to the board), that's a legit pattern — just drive it off `LED_BUILTIN` or an external LED on a free digital pin, triggered when you detect incoming serial bytes (`Serial.available()`), rather than trying to tap the TX/RX hardware LEDs.