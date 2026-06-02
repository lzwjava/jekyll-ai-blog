---
audio: false
generated: true
lang: en
layout: post
title: USB Cable Guide for Raspberry Pi Pico on Ubuntu
translated: false
type: note
---

For your **Raspberry Pi Pico (with headers)** from the **Raspberry Pi Foundation** (assuming "duistou" is a typo or a reseller brand), you need the right USB cable to set it up with Ubuntu. Here's what you need:

### USB Cable Requirements

1. **Type**: USB to Micro-USB cable
   - The Raspberry Pi Pico (original, with headers) uses a **Micro-USB** port for power and data.
   - Ensure the cable supports **data transfer**, not just charging. Some cheap Micro-USB cables are power-only and won’t work for programming or communication.

2. **Cable Specifications**:
   - **Connector**: USB-A (or USB-C, depending on your computer’s ports) to Micro-USB.
   - **Quality**: Use a high-quality cable to avoid connection issues. A cable from a reputable brand (e.g., Anker, Belkin, or the one included with devices like phones or tablets) works well.
   - **Length**: A 1-3 ft (30-100 cm) cable is ideal to minimize signal issues.

3. **Computer Port**:
   - If your Ubuntu machine has **USB-A ports**, use a USB-A to Micro-USB cable.
   - If it only has **USB-C ports**, use a USB-C to Micro-USB cable or a USB-C hub/adapter with a USB-A to Micro-USB cable.

### Setup Notes

- **Connection**: Plug the Micro-USB end into the Pico’s Micro-USB port and the other end into your Ubuntu computer.
- **Mode**:
  - **Normal Mode**: Plug in the Pico directly to connect for programming (e.g., MicroPython, C/C++).
  - **BOOTSEL Mode**: Hold the **BOOTSEL** button on the Pico while plugging it in to enter mass storage mode for firmware updates (it appears as a drive named `RPI-RP2`).
- **Verification**: After connecting, use the steps from my previous response to confirm Ubuntu detects the Pico (e.g., `lsusb`, `ls /dev/tty*`, or `lsblk`).

### Troubleshooting Cable Issues

- If the Pico isn’t detected (no `/dev/ttyACM0` or `RPI-RP2` drive), try a different cable or USB port.
- Avoid using USB hubs, as they can sometimes cause detection issues.
- Check the cable by testing it with another device (e.g., a phone) to confirm it supports data transfer.

If you’re unsure about your cable or still face issues, describe your setup (e.g., computer ports, cable type, what you see when plugging in), and I can guide you further!
