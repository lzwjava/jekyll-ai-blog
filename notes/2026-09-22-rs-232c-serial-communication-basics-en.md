---
audio: false
generated: true
image: false
lang: en
layout: post
title: RS-232C Serial Communication Basics
translated: false
type: note
---

Question: **Introduction to RS-232C in electrical/electronics engineering**

Answer:

**RS-232C** is a standard for **serial communication** between electronic devices. It defines mainly **electrical signal levels, connector/pin conventions, and communication behavior**.

A simple mental model:

```text
Computer / Controller                  Device
┌───────────────┐                    ┌───────────────┐
│ UART          │                    │ UART          │
│               │                    │               │
│ TX ───────────┼────────────────────┼── RX           │
│ RX ───────────┼────────────────────┼── TX           │
│ GND ──────────┼────────────────────┼── GND          │
└───────────────┘                    └───────────────┘
       │                                      │
       └──── RS-232 voltage driver ───────────┘
```

### 1. What does "serial" mean?

Instead of sending many bits simultaneously:

```text
Parallel:
D7 D6 D5 D4 D3 D2 D1 D0
 │  │  │  │  │  │  │  │
 └──┴──┴──┴──┴──┴──┴──┘
```

RS-232 sends bits **one after another** on a wire:

```text
TX: ──┐ ┌───┐   ┌─┐ ┌────
      │ │   │   │ │ │
      └─┘   └───┘ └─┘
       1 0 0 1 0 1 ...
```

This is why it is called **serial communication**.

### 2. The important electrical difference

This is the part that often confuses people.

Normal MCU UART:

```text
Logic 1 ≈ 3.3 V
Logic 0 ≈ 0 V
```

RS-232 uses **positive and negative voltages**:

```text
RS-232:

Logic 0 → positive voltage
Logic 1 → negative voltage

typically:
+3 V ... +15 V  → 0
-3 V ... -15 V  → 1
```

So:

```text
MCU UART                 RS-232

3.3V ──┐
       │                 -12V ──┐
       └── TX                    └── TX
0V   ──┘                 +12V ──┘
```

**Do not directly connect a 3.3 V UART pin to an RS-232 port.**

You normally need a transceiver such as a **MAX232/MAX3232**:

```text
MCU                    RS-232 device

UART TX ──> MAX3232 ───────────> RX
UART RX <── MAX3232 <─────────── TX
GND ──────────────────────────── GND
```

The transceiver converts:

```text
3.3V/0V UART
      ↓
  MAX3232
      ↓
positive/negative RS-232 voltage
```

### 3. What does the "C" mean?

**RS-232** is the standard; **RS-232C** refers to a revision of that standard.

You will often see equipment labeled:

```text
RS-232
RS-232C
```

In practical engineering discussions, people commonly use "RS-232" to refer to the interface.

### 4. Typical communication parameters

RS-232 itself does not simply mean "9600 baud." The communication normally has parameters such as:

```text
Baud rate:   9600
Data bits:   8
Parity:      None
Stop bits:   1
```

This is commonly written:

```text
9600 8N1
```

For example, transmitting the ASCII character `A`:

```text
A = 0x41 = 01000001
```

UART framing sends something approximately like:

```text
       start       data bits          stop
          ↓            ↓                ↓
TX: ────┐ ┌─┐ ┌─────────────────────┐ ┌────
        └─┘ └─┴─────────────────────┴─┘
         0   1 0 0 0 0 0 1 0           1
```

The actual wire polarity is then converted by the RS-232 transceiver.

### 5. DB-9 connector

A classic PC RS-232 interface uses a **DE-9 connector** (often incorrectly called DB-9).

Common pins:

```text
DE-9

  1 2 3 4 5
   6 7 8 9

Pin 2 = RXD
Pin 3 = TXD
Pin 5 = GND
```

For basic communication, you often only need:

```text
Device A          Device B

TXD ───────────── RXD
RXD ───────────── TXD
GND ───────────── GND
```

This is called a **3-wire connection**.

### 6. RS-232 vs UART

These are related but **not the same thing**.

Think of it as layers:

```text
Application
    │
    │  "send temperature = 25.3"
    ↓
Protocol / data format
    │
    ↓
UART
    │  framing + baud rate + bits
    ↓
RS-232 transceiver
    │  electrical voltage conversion
    ↓
Physical wires
```

A microcontroller might have:

```text
STM32 UART
     │
     │  3.3V logic
     ↓
MAX3232
     │
     │  ± voltage
     ↓
RS-232 cable
     │
     ↓
PC / PLC / instrument
```

So the key distinction is:

| Technology | Main purpose                             |
| ---------- | ---------------------------------------- |
| UART       | Serial data/framing mechanism            |
| RS-232     | Electrical interface standard            |
| RS-485     | Differential electrical interface        |
| USB        | Much more complex host/device serial bus |

### 7. Why RS-232 was useful

RS-232 was designed for relatively simple point-to-point communication and became extremely common for:

* PCs
* PLCs
* industrial instruments
* CNC machines
* modems
* oscilloscopes
* power supplies
* embedded controllers

For example:

```text
PC ───── RS-232 ───── Power Supply
                         │
                         ├── "VOLT 12"
                         │
                         └── "MEAS:VOLT?"
```

The electrical interface doesn't define what `"VOLT 12"` means. The device manufacturer defines that **higher-level command protocol**.

### The 5 things to remember

```text
1. RS-232 = serial communication interface

2. It uses positive/negative voltage levels,
   unlike ordinary 3.3V UART.

3. TX connects to RX.
   RX connects to TX.
   GND connects to GND.

4. MAX232/MAX3232 converts MCU UART ↔ RS-232.

5. "9600 8N1" describes common UART communication settings,
   not the RS-232 electrical standard itself.
```

If you're learning this from an **electrical engineering / industrial controls** perspective, the next useful step is to build a tiny **UART → MAX3232 → RS-232 circuit** and walk through the voltage waveform for one byte with an oscilloscope/logic analyzer. I can do that next.
