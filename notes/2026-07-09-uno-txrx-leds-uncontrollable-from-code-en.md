---
audio: false
generated: true
image: false
lang: en
layout: post
title: Uno TX/RX LEDs Uncontrollable from Code
translated: false
type: note
---

Here's what the **actual source code** on your system confirms:

---

## 1. LED_BUILTIN definition — confirmed

**File:** `~/.arduino15/packages/arduino/hardware/avr/1.8.8/variants/standard/pins_arduino.h` (line 54)

```c
#define LED_BUILTIN 13
```

This is **pin 13 (PB5)** on the ATmega328P — the `L` LED. It's a GPIO you own fully via `digitalWrite`.

## 2. TX/RX LED definitions — NOT present for Uno

The Uno's `pins_arduino.h` has **zero** TX/RX LED macros. Every other pin definition (SPI, I2C, analog) is there — but not TX/RX.

Boards that **do** define `TX_RX_LED_INIT` are all **native-USB (ATmega32u4)** based:

| Board | File | TX LED | RX LED |
|-------|------|--------|--------|
| Leonardo | `variants/leonardo/pins_arduino.h:94` | PD5 (D5) | PB0 (D8) |
| Micro | `variants/micro/pins_arduino.h:35` | PD5 | PB0 |
| Robot Control | `variants/robot_control/pins_arduino.h:31` | PD5 | PB0 |
| Circuit Playground | `variants/circuitplay32u4/pins_arduino.h:100` | handled separately | |

**Uno = not in that list.** Because the Uno's TX/RX LEDs are on the **ATmega16U2** (the separate USB bridge chip), not on the main ATmega328P. No pin number on the 328P maps to them.

## 3. USBCore.cpp — only compiled for native USB

**File:** `~/.arduino15/packages/arduino/hardware/avr/1.8.8/cores/arduino/USBCore.cpp` (line 24–29)

```c
#if defined(USBCON)   // ← NOT defined on Uno's ATmega328P
#define TX_RX_LED_PULSE_MS 100
volatile u8 TxLEDPulse;
volatile u8 RxLEDPulse;
```

The TX/RX LED pulse system exists, but it's guarded by `USBCON` — only boards with native USB (Leonardo, Micro, etc.) compile this code. The Uno's 328P does not.

## 4. The delay code — no automatic modification in IDE

I searched the entire Arduino IDE source (`arduino-ide-extension/`) for "blink", "delay", "example" — the IDE is just a GUI shell. It ships built-in examples via the `ExamplesService` protocol, but it does **not** auto-generate or auto-modify delay values in user sketches. The 3000ms → 100ms change was something you did manually in your sketch.

---

## Bottom line from source code

The previous answer was **correct**:

| Claim | Source Verified? |
|-------|:---:|
| `LED_BUILTIN` = pin 13 | ✅ `pins_arduino.h` line 54 |
| TX/RX LEDs not controllable from sketch on Uno | ✅ No `TX_RX_LED_INIT` in `variants/standard/` |
| TX/RX LEDs driven by 16U2, not 328P | ✅ Confirmed by architecture — no `USBCON` on 328P |
| `delay(100)` is valid Arduino code | ✅ No IDE-level modification exists; it's a manual sketch edit |
| Circuit Playground uses ATmega32u4 native USB | ✅ `circuitplay32u4` variant has its own TX_RX_LED_INIT = 0 |