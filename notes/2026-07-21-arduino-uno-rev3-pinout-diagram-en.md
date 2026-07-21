---
audio: false
generated: true
image: false
lang: en
layout: post
title: Arduino UNO Rev3 Pinout Diagram
translated: false
type: note
---

Question: what's this PDF? ([https://docs.arduino.cc/resources/pinouts/A000066-full-pinout.pdf](https://docs.arduino.cc/resources/pinouts/A000066-full-pinout.pdf))

Answer:

This is the **Arduino UNO Rev3 (SKU A000066) full pinout diagram**. It is basically a **map showing every pin on the Arduino board and what each pin connects to internally**. ([Arduino Documentation][1])

![Image](https://images.openai.com/static-rsc-4/LWeyio-9Fb_NjWkei2BssmUiuoCgqPlsiDKeEB1nF5Jb7zg3tiatX_z6Z4WRvbw0aBMBoB7Xf2QMgIq4AvDgpi1hSvWgIcuIR1_PuM2A7T22Jj_fL5e07VaI4mJegDIb05NLygFT8tkvIq_GSKRvZcSX5MJIxQ9nQ_ycvB32oNlfIpTHkWJqcJ_AsH9t5KgD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/U-KZVzBfa4XxhQ8LCZkhOuSZzW2UJuly651Gu6ZQ0IwwiIqSSfjNLi6be8igOQkFLm5gHVmvXKq1bSs8Td6yQC68yMXEHHiKTmm5iDCh8MrjqV9mWO6T3Sv8sIaRDU4N1NQ5nFvq8OBp9TtzWto5Rle_dSpsvkoQq5LT96j9Xc3jz3otfbDGaYRZ1ZVPjl0e?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/VhAPgmy9BwKrtPTgefnojVyqF_WdhkscPAv__2GDO2NbakygyXaQsNZC_IjGTU4fwOkUa4QPW5iTuiwIY911tfu_Bj1274zhm1WsNAzzbd6YaGUUNT4rLIJy5GkCrj8fr8rSMJ2OfuuByButH45ue9Lx1v2oaEBuWWOSY8oDKIlYYgr6TqJTPXC11oOVafnO?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/yLgtOwt910YYWkN1evIc1ET-LVkXHX7QdybnptJ-xcjkKZHQE99lvctZkr8zzHOVBjQmAlOv_c4DMMFcPV3m9aY2_jLr2YRunzj9QEeHpEqJzNsbtUknnTA_FBc2Jg-ZQnobh3EJBjHaMXq82rSSJJ96OMdpeBW-B4a3J93ed-A1NTZqG69w4tSse3lPmBW1?purpose=fullsize)

Think of it like the "motherboard manual" for a tiny microcontroller board.

The board:

* MCU: **ATmega328P**
* Clock: **16 MHz**
* Logic voltage: **5V**
* Digital GPIO: **14 pins (D0-D13)**
* Analog inputs: **6 pins (A0-A5)**
* Flash: **32 KB**
* SRAM: **2 KB**
* EEPROM: **1 KB**
  ([Arduino Official Store][2])

---

## Main sections in the pinout

### 1. Digital pins (D0-D13)

These are general-purpose input/output pins.

Example:

```
D13 ---- LED_BUILTIN
D12 ---- GPIO
D11 ---- PWM / SPI MOSI
D10 ---- PWM / SPI SS
D9  ---- PWM
D8  ---- GPIO
...
D0  ---- UART RX
D1  ---- UART TX
```

You can write:

```cpp
pinMode(13, OUTPUT);

digitalWrite(13, HIGH);
```

to turn on the onboard LED.

---

### 2. Analog pins (A0-A5)

These connect to the ADC inside ATmega328P.

Example:

```
Sensor output
      |
      v
     A0
      |
      v
10-bit ADC
      |
      v
0 ~ 1023 value
```

Code:

```cpp
int value = analogRead(A0);
```

If voltage is:

```
0V    -> 0
5V    -> 1023
```

---

### 3. Power pins

The PDF shows:

```
VIN
5V
3.3V
GND
RESET
IOREF
```

Typical usage:

```
External 7-12V
       |
       v
      VIN

Arduino regulator

       |
       +---- 5V rail
```

---

### 4. Communication pins

Arduino exposes several hardware protocols.

#### UART

```
D0 RX
D1 TX
```

Used for serial communication:

```
Arduino <---- USB serial ----> PC
```

---

#### SPI

Pins:

```
D10 SS
D11 MOSI
D12 MISO
D13 SCK
```

Used for:

* SD cards
* displays
* fast sensors

Example:

```
Arduino
  |
 SPI
  |
SD card
```

---

#### I2C

Pins:

```
A4 SDA
A5 SCL
```

Used for:

* OLED displays
* IMU sensors
* RTC modules

Example:

```
Arduino

A4 SDA -------- Sensor SDA
A5 SCL -------- Sensor SCL
```

---

## The interesting part: Arduino pin numbers vs MCU pins

The Arduino abstraction hides the actual chip pins.

Example:

Arduino:

```
D13
```

actually maps to:

```
ATmega328P PB5
```

The PDF helps translate:

```
Arduino pin
      |
      v
ATmega328P register
      |
      v
hardware port
```

For low-level programming:

```c
PORTB |= (1 << PB5);
```

is the same as:

```cpp
digitalWrite(13, HIGH);
```

but much faster.

---

## Why this PDF matters

For beginners:

```
Arduino pin
      |
      v
Connect LED / sensor / motor
```

For embedded engineers:

```
Arduino pin
      |
      v
ATmega328P GPIO
      |
      v
AVR register
      |
      v
hardware peripheral
```

It is the equivalent of a **GPU block diagram or motherboard PCIe lane diagram**, but for a microcontroller.

For your AI hardware background, the analogy:

```
Arduino pinout PDF
        ≈
NVIDIA GPU architecture diagram
        ≈
server motherboard block diagram
```

It tells you the physical resource map.

---

References:

* Arduino UNO R3 documentation ([Arduino Documentation][1])
* Arduino UNO Rev3 technical specifications ([Arduino Official Store][2])
* Arduino UNO R3 datasheet ([Arduino Documentation][3])

[1]: https://docs.arduino.cc/hardware/uno-rev3/?utm_source=chatgpt.com "UNO R3 | Arduino Documentation"
[2]: https://store.arduino.cc/products/arduino-uno-rev3?utm_source=chatgpt.com "Arduino UNO Rev3 – Reliable ATmega328P Board with Digital & Analog I/O — Arduino Official Store"
[3]: https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf?hkey=EF798316E3902B6ED9A73243A3159BB0&utm_source=chatgpt.com "Arduino® UNO R3"
