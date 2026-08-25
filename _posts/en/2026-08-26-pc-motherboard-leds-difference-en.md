---
audio: false
generated: true
image: false
lang: en
layout: post
title: PC Motherboard LEDs Difference
translated: false
type: note
---

Question: What is the difference between HDD LED and Power LED on a PC motherboard?

Answer:

**Power LED** indicates whether the computer is on, off, or in sleep mode. It's usually solid when on, off when shut down, and blinking when in sleep/standby.

**HDD LED** (Hard Disk Drive LED) flashes whenever the storage drive (HDD or SSD) is being actively read from or written to. It gives you a real-time indicator of disk activity.

| Feature | Power LED | HDD LED |
| --- | --- | --- |
| What it shows | System power state | Storage activity |
| Behavior | Solid on / blinks in sleep | Flashes during disk read/write |
| Connector pins | `PWR LED+` / `PWR LED−` | `HDD LED+` / `HDD LED−` |
| Works with SSD? | N/A | Yes, still flickers on SSD activity |

A practical tip: if your system seems frozen, glancing at the HDD LED tells you whether it's still doing something (busy) or truly hung.
