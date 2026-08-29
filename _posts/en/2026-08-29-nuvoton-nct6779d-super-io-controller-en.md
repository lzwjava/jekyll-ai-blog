---
audio: false
generated: true
image: false
lang: en
layout: post
title: Nuvoton NCT6779D Super I/O Controller
translated: false
type: note
---

**Question:** What is the Nuvoton NCT6779D chip inside the MSI B85M-E45 motherboard?

**Answer:**

The Nuvoton NCT6779D is the motherboard's **Super I/O (Super Input/Output) controller** — essentially the chip responsible for monitoring and managing the health of your system in real time. It's one of the most important "behind the scenes" chips on any modern motherboard.

---

**What it does:**

**1. Hardware Monitoring**
The NCT6779D monitors several critical parameters in PC hardware, including power supply voltages, fan speeds, and temperatures. This is what allows software like HWiNFO, HWMonitor, or MSI's own utilities to show you live system readings.

**2. Temperature Sensing**
The chip supports up to 25 temperature monitoring sources. Up to 6 of those are direct temperature sensor inputs, the others are special sources such as PECI (for CPU temp), PCH, and SMBus.

**3. Fan Speed Control**
The NCT6779D features support for the Smart Fan control system, including SMART FAN I and SMART FAN IV, enhancing system stability and user-friendliness. It can monitor up to 5 fans and provides 3 fan speed control outputs. This is what drives the automatic fan speed curves you configure in BIOS.

**4. Voltage Monitoring**
There are 8 to 15 analog voltage sensors that track rails like 12V, 5V, 3.3V, and CPU VCore to make sure everything stays within safe limits.

**5. Legacy I/O Functions**
The NCT6779D provides two high-speed serial communication ports (UART) and supports the PC-compatible printer port (SPP), the bi-directional printer port (BPP), the enhanced parallel port (EPP), and the extended capabilities port (ECP). It also handles the **PS/2 keyboard and mouse** interface.

**6. Interface with the System**
It is a highly integrated LPC Super I/O controller designed for PC and embedded motherboard platforms, combining extensive hardware monitoring, fan control, and legacy I/O functions through an LPC bus, enabling comprehensive system management with minimal external components.

---

**In plain terms:** The NCT6779D is the chip that "watches over" your PC — reading temperatures, controlling fan speeds, and keeping legacy ports (like PS/2) alive. It's also what monitoring software reads when it shows you CPU/motherboard temperatures and voltages.

---

**References:**
- [NCT6779D Features & Applications – Avaq](https://www.avaq.com/technology/nct6779d-nuvoton-datasheet-pdf-features-and-application)
- [NCT6779D Datasheet – Datasheetgo](https://datasheetgo.com/NCT6779D-datasheet-pdf-788178/)
- [Linux Kernel hwmon Driver for NCT6779D](https://www.kernel.org/doc/Documentation/hwmon/nct6775)
- [NCT6779D Datasheet PDF – TheRetroWeb](https://theretroweb.com/chip/documentation/nct6779d-novoton-644e9adf2d0db520875332.pdf)
