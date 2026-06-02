---
audio: false
generated: true
image: false
lang: en
layout: post
title: Arduino Serial Port Detection Report
translated: false
type: note
---

Here's the full report:

---

## Arduino Connection Report

### How I Checked

1. **`ls /dev/cu.* /dev/tty.*`** — Listed all serial/character devices on macOS and filtered for `usb`/`arduino`/`serial` patterns. This is the primary detection method.
2. **`ioreg -c IOSerialBSDClient`** — Queried the macOS I/O Registry to get kernel-level driver info about the serial device.
3. **`stat`** + **`lsof`** — Checked device file metadata and whether any process is currently using the port.

---

### Findings

| Property | Value |
|---|---|
| **Callout device** | `/dev/cu.usbserial-1110` |
| **Dialin device** | `/dev/tty.usbserial-1110` |
| **TTY suffix** | `1110` (last 4 digits of USB serial number) |
| **Connected at** | 2026-05-03 23:30:19 |
| **Permissions** | `crw-rw-rw-` (readable/writable by all users) |
| **Driver** | `IOSerialBSDClient` (Apple serial family) |
| **Port status** | **Not in use** (no process has it open) |
| **Chip type** | Likely **CH340** (clone Uno) or **FTDI** — suffix `usbserial` indicates a USB-to-UART bridge |

### Notes

- Use `/dev/cu.usbserial-1110` to upload sketches or read serial output
- Default Arduino baud rate is `9600`
- `tty.*` is for incoming connections; `cu.*` (call-up) is what you use for outgoing/Arduino communication
- `system_profiler SPUSBDataType` returned empty — likely an M-series Mac limitation with the USB subsystem reporting
