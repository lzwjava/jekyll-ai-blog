---
audio: false
generated: true
image: false
lang: en
layout: post
title: CH340 Arduino Nano Clone Guide
translated: false
type: note
---

Here's the full picture based on what I found:

### Your connected device: CH340 USB-serial (`1a86:7523`)

The CH340 chip is a **generic USB-to-serial converter**, not a specific board's native USB. This means:

| Board | Uses CH340? | VID:PID |
|-------|------------|---------|
| **Arduino Nano (clone)** | ✅ **Most common** | `1a86:7523` |
| **Arduino Uno (clone)** | ⚠️ Sometimes | `1a86:7523` |
| **Circuit Playground** (Adafruit) | ❌ No — native USB | `0x239A:0x8011` |
| **Arduino BT** | ❌ No — Bluetooth | — |

**Circuit Playground** and **Arduino BT** are ruled out — their hardware is completely different (ATmega32u4 native USB, and Bluetooth respectively).

### What you almost certainly have: **Arduino Nano clone** (ATmega328P)

The CH340 is the hallmark of cheap Arduino Nano clones. Select:

> **Board: `Arduino Nano`**
> **Processor: `ATmega328P`**

### One gotcha — old vs new bootloader

Nano clones sold in the last ~5 years use the **new bootloader** (115200 baud). But if yours is older or from a random cheap batch, you might need:

> **Processor: `ATmega328P (Old Bootloader)`** (57600 baud)

**Try the new one first** (`ATmega328P`). If upload fails with a timeout/avrdude error, switch to `ATmega328P (Old Bootloader)`.

### If it's actually an Uno

If the board is physically larger with the USB port and power jack on one end, it's an **Arduino Uno** — select `Arduino UNO` instead. But the CH340 is less common on Unos (most use the original FTDI or the 16U2).