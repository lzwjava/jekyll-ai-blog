---
audio: false
generated: true
image: false
lang: en
layout: post
title: ATX_PWR1 on MSI B760M MORTAR
translated: false
type: note
---

Question: What does the ATX_PWR1 connector mean on the MSI MAG B760M MORTAR WIFI motherboard?

Answer:

`ATX_PWR1` is the **main 24-pin ATX power connector** on the board — the primary power feed from your PSU to the motherboard (chipset, RAM, I/O, PCIe slots, fans, etc.). It's distinct from the `CPU_PWR1`/`CPU_PWR2` connectors (the 8+8-pin EPS12V connectors near the CPU socket that feed the VRM/CPU directly).

On this board:

- CPU_PWR1~2 and ATX_PWR1 are the power connectors that allow you to connect an ATX power supply
- CPU_PWR1/2 are 8-pin each, carrying `+12V` and `Ground` pins for CPU power
- ATX_PWR1 is the 24-pin connector, with pin 1 being `+3.3V` (ATX_PWR1 Pin 1 Signal Name 1 +3.3V) and the rest following the standard ATX24 pinout (+5V, +12V, PS_ON, PWR_OK, etc. — the manual only shows pins 1-2 in the excerpt I found, but it's the standard 24-pin ATX spec)

**Where it is physically**: it's located along the right edge of the board near the DIMM slots — in the component overview it sits near JUSB3, JUSB4, and PUMP_FAN1, adjacent to the 24-pin edge connector you'd expect.

**Practically for your build**: plug your PSU's 24-pin cable into `ATX_PWR1`, and the 8-pin (or dual 8-pin if you have a higher-end CPU) EPS cable into `CPU_PWR1` (+`CPU_PWR2` if populated). If you're flashing BIOS via the Flash BIOS Button before installing CPU/RAM, MSI's instructions confirm you only need the power supply connected to CPU_PWR1 and ATX_PWR1 — no CPU or memory required for that step, which is handy if you want to update BIOS before finishing the build (e.g., to make sure a newer CPU is supported day one).

References:

- [MSI MAG B760M MORTAR WIFI II User Guide (PDF)](https://download-2.msi.com/archive/mnu_exe/mb/MAGB760MMORTARII_MAGB760MMORTARWIFIII_EN.pdf)
- [MSI MAG B760M MORTAR WIFI II Manual (manua.ls)](https://www.manua.ls/msi/mag-b760m-mortar-wifi-ii/manual)
- [MSI MAG B760M MORTAR WIFI Product Page](https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI)
