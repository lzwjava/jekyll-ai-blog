---
audio: false
generated: true
image: false
lang: en
layout: post
title: Arduino Uno ICSP Header Guide
translated: false
type: note
---

**Question:** What is ICSP on the Arduino Uno board?

**Answer:**

**ICSP** stands for **In-Circuit Serial Programming**. It is a 6-pin (2×3) header connector found on the Arduino Uno board used to program AVR microcontrollers directly — bypassing the normal USB/bootloader method.

**Physical Location**
On the Arduino Uno, there are actually **two** ICSP headers:
- **ICSP** — connects to the main **ATmega328P** (the primary microcontroller)
- **ICSP2** — connects to the **ATmega16U2** chip that handles USB-to-serial communication

**Pin Layout (2×3)**

| MISO | VCC |
|------|-----|
| SCK  | MOSI |
| RST  | GND |

MISO, MOSI, and SCK are available at a consistent physical location on the ICSP header, and this connector is also used by shields that rely on the SPI interface, allowing shields to be designed that work across every board.

**Main Use Cases**

1. **Burning a bootloader** — If your bootloader gets corrupted or you want to install a custom one, ICSP lets you flash it directly using an external programmer or another Arduino.
2. **Bypassing the bootloader** — Uploading firmware directly to the chip for faster uploads and more flash memory usage.
3. **SPI communication** — The SPI interface, and therefore these pins, is the interface used to program AVR microcontrollers.
4. **Fallback programming** — ICSP pins are especially useful when your Arduino's USB port is broken or damaged, since they allow coding and booting from an external source.

**Normal vs. ICSP Programming**

| Method | Via USB (normal) | Via ICSP |
|---|---|---|
| Uses bootloader | ✅ Yes | ❌ No |
| Requires extra hardware | ❌ No | ✅ Programmer needed |
| Flash memory used by bootloader | ~0.5 KB consumed | None wasted |
| Speed | Slower | Faster |

In everyday Arduino projects you rarely need ICSP — it's primarily for advanced use like bootloader recovery or direct chip programming.

---

**References:**
- [Arduino as ISP and Arduino Bootloaders – Arduino Docs](https://www.arduino.cc/en/Tutorial/ArduinoISP)
- [Installing an Arduino Bootloader – SparkFun](https://learn.sparkfun.com/tutorials/installing-an-arduino-bootloader/hardware-hookup)
- [Hex File and ICSP Pins of Arduino – C# Corner](https://www.c-sharpcorner.com/article/hex-file-and-icsp-pins-of-arduino/)
