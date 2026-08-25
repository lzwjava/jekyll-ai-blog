---
audio: false
generated: true
image: false
lang: en
layout: post
title: Two Power Connectors on Arduino Uno
translated: false
type: note
---

**Question: What are the two power connectors on an Arduino Uno?**

**Answer:**

On an **Arduino Uno**, the two common power connectors are:

1. **USB connector (usually USB-B)**
2. **DC barrel jack (battery/power adapter connector)**

![Image](https://images.openai.com/static-rsc-4/fV9WOLEzti8jngCI4K0AHfglYuZ3vZHdI3EWlasth5hxJkqS3Le0WlKOuBq3DLH8-X9CHNNQ-n6xHsbEgFAJj1qs-d6Fzr7fcQ1h1IGAAVXK0wkTP4YYJvRW_pyrmJHq1keNYCClmYpBpjn6D8dccdjZir4FdZsb_YcsPJlYuXbjj1OymvBAfx3VyeQPVQST?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/UEgTUIPnUyTEGl54Ya7BvI5lgYOs9Qydtd5EmwMdlM-v5evHk0MjsmHapoL4qJsPlA5sV6KeWey7E1sF1OFCz-3vO4-PfXdu4dbQcd9W3XvPRyOV-48PSvFRK5KEzCcH_F3Ef7ehl7JY2e5VYvIefvWR0j0RTus7pxV1g14eqqPk3FYqF1iESqi9yHRkM69G?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/mSYnD211t5TDyoHlXw7FCybCnPsDtfokc7a7L3wO0-1CH0u_JARjJYZLSENrx_5IZ4Kc1Is97cJPn9VKruDHGoNbjUjgFTd0Q0Yaz4uqoVLklBsBuNg4VrQPVENtaDe5PwReISuxPAnK6YFpdl1LSfmpxgZSU8KADz6TGaxkXGfWRkNO0JRvhfatGgbD4v3h?purpose=fullsize)

### 1. DC barrel jack — external power

The barrel jack accepts an external power supply:

* Recommended: **7–12V DC**
* Center positive
* Goes through a voltage regulator
* Produces **5V** for the Arduino board

Examples:

```
9V battery
    |
    v
[DC barrel jack]
    |
[Voltage regulator]
    |
+5V Arduino
```

You can use:

* 9V wall adapter
* Battery pack
* Li-ion battery + regulator

---

### 2. USB connector — programming + power

The USB connector does two jobs:

#### A. Upload code

Your computer:

```
Arduino IDE
     |
 USB cable
     |
ATmega328P bootloader
     |
new firmware
```

#### B. Supply power

USB provides:

```
USB 5V
 |
polyfuse
 |
Arduino 5V rail
```

Usually up to around 500mA (depending on the USB port).

---

### How does Arduino choose power source?

The Uno has automatic power selection.

Example:

```
USB connected + DC jack connected

       9V adapter
           |
           v
      voltage regulator
           |
           +---- 5V rail
                    |
USB 5V ------------+
```

The board detects the higher/appropriate source and prevents back-feeding USB.

---

### There are also other power pins

Near the pin headers:

```
POWER HEADER

VIN  ---- external input voltage
GND
5V   ---- regulated 5V output
3.3V ---- 3.3V output
RESET
IOREF
```

`VIN` is basically the same voltage as the DC jack input.

Example:

```
Battery + ---- VIN
Battery - ---- GND
```

works without using the barrel jack.

---

### Engineering perspective

Arduino Uno is a simple embedded system:

```
                 USB
                  |
                  v
PC -----> USB-UART chip -----> ATmega328P
                                  |
                                  |
                             GPIO / ADC / PWM
                                  |
                              Sensors
                              Motors


Battery
  |
  v
Power regulator
  |
  +---- 5V logic
```

The barrel jack exists because embedded devices often run **without a computer**. During development you use USB; in a deployed device you remove the computer and use battery/DC power.

This same pattern appears everywhere:

* ESP32 dev boards → USB + battery pin
* Raspberry Pi → USB-C power
* GPUs → PCIe slot + auxiliary power connectors
* Servers → redundant power supplies

The separation is fundamental: **one connector is for development/debugging, one is for standalone operation.**
