---
audio: false
generated: true
image: false
lang: en
layout: post
title: CS 4725 V Arduino Uno Capacitors
translated: false
type: note
---

**Question:** What is the component labeled "CS 4725 V" on the Arduino Uno board?

**Answer:**

"CS 4725 V" (sometimes read as "CS47 25V") is the markings printed on the two **electrolytic aluminum capacitors** on the Arduino Uno board, referenced as **PC1** and **PC2** in the official schematic.

Here's what those markings mean:

| Marking | Meaning |
|---|---|
| **CS** | Component series / manufacturer code (Panasonic "CS" series) |
| **47** | Capacitance: **47 µF** |
| **25V** | Voltage rating: **25 Volts** |

According to the Arduino Uno board topology, PC1 and PC2 are listed as **electrolytic aluminum capacitors rated 47µF, 20%, 25V SMD**, with part number `EEE-1EA470WP`.

**Role on the board:** These capacitors are located in the power section of the Arduino Uno. They act as **bulk decoupling / filter capacitors**, smoothing out voltage ripple from the power supply to ensure stable power delivery to the board's components.

**References:**
- [Arduino Uno Board Parts – VideotronicMaker](https://videotronicmaker.com/arduino-uno-board-parts/)
- [Arduino Uno Rev3 – Official Store Page](https://store-usa.arduino.cc/products/arduino-uno-rev3)
- [Overview of Arduino UNO Components – Arduino Docs](https://docs.arduino.cc/tutorials/uno-rev3/intro-to-board)
