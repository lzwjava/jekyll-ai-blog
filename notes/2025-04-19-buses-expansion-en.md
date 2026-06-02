---
audio: false
generated: true
lang: en
layout: post
title: 'Part 5: Buses and Expansion'
translated: false
type: note
---

### 1. System Bus Standards

#### What is a System Bus?

A system bus is a communication pathway that connects the CPU with memory and peripheral devices. It facilitates data transfer, address signaling, and control signals between these components, enabling the CPU to interact with other parts of the computer system efficiently[^3].

---

### 2. ISA Bus Overview

- **ISA (Industry Standard Architecture)** is one of the earliest system bus standards, introduced with the IBM PC AT in the 1980s.
- It is a 16-bit bus running at 4.77 MHz, capable of data transfer rates up to approximately 9 MB/s[^5].
- ISA supports multiple expansion cards, each with its own interrupt request line, enabling devices like network cards, serial ports, and video cards to be connected.
- The bus is backward-compatible with older 8-bit PC XT systems and uses a 98-pin connector combining two edge connectors into a single slot.
- ISA uses asynchronous signaling and bus mastering, but only accesses the first 16 MB of main memory directly[^5].
- Due to its age, ISA is largely obsolete but important historically as the foundation for later bus designs.

---

### 3. PCI Bus Overview

- **PCI (Peripheral Component Interconnect)** is a more modern, synchronous, parallel bus standard designed to overcome ISA limitations[^1][^3].
- PCI buses run at 33 MHz with a 32-bit multiplexed address/data bus, offering a base bandwidth of 44 to 66 MB/s.
- For sequential memory accesses, PCI can achieve up to 132 MB/s by transferring one 32-bit word per clock cycle without needing to resend addresses[^1].
- PCI uses a bridge interface to connect to the CPU bus, which buffers data and optimizes memory access, allowing the CPU to continue execution without wait states during peripheral communication[^1].
- PCI supports bus mastering and DMA (Direct Memory Access), where devices can take control of the bus to transfer data directly.
- There is a 64-bit extension of PCI to increase bandwidth further.
- PCI devices are identified by bus number, device number, and function, with configuration registers specifying vendor, device type, memory and I/O addresses, and interrupts[^3].
- PCI transactions include address phases and data phases, supporting various commands like memory read/write and I/O read/write[^3].

---

### 4. Modern Interface Technologies

Modern peripheral communication has shifted towards serial interfaces that are simpler and more flexible than parallel buses.

---

#### USB (Universal Serial Bus)

- USB is a widely used high-speed serial interface designed for connecting peripherals like keyboards, mice, storage devices, and more.
- It supports plug-and-play and hot-swapping, allowing devices to be connected and disconnected without powering down.
- USB uses a tiered star topology and supports data rates from 1.5 Mbps (Low Speed) up to 10 Gbps (USB 3.1 and beyond).
- It provides power to devices and supports multiple device classes with standardized protocols.
- USB controllers manage data transfers using endpoints and pipes, with different transfer types such as control, bulk, interrupt, and isochronous transfers.

---

#### SPI (Serial Peripheral Interface)

- SPI is a synchronous serial communication bus commonly used for short-distance communication with peripheral devices like sensors, EEPROMs, and displays[^4].
- It uses four signals: SCLK (clock), MOSI (Master Out Slave In), MISO (Master In Slave Out), and CS (Chip Select).
- SPI is full-duplex, allowing simultaneous data transmission and reception.
- It is simple and fast but requires one chip select line per device, which can limit scalability.
- SPI mode settings include clock polarity and phase, which define when data is sampled and shifted[^6].
- SPI is typically used in embedded systems and microcontroller applications.

---

#### I²C (Inter-Integrated Circuit)

- I²C is a two-wire serial bus used for communication between microcontrollers and peripherals like sensors and EEPROMs[^4].
- It uses two bidirectional lines: SDA (data) and SCL (clock).
- I²C supports multiple masters and slaves on the same bus, with devices addressed by unique 7- or 10-bit addresses.
- It supports half-duplex communication and uses open-drain/open-collector outputs with pull-up resistors.
- I²C is slower than SPI but requires fewer pins and supports multi-device communication with simple wiring.
- Typical speeds are 100 kHz (Standard mode), 400 kHz (Fast mode), and higher in newer specifications.

---

### Summary Table: ISA vs PCI vs USB vs SPI vs I²C

| Feature | ISA | PCI | USB | SPI | I²C |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Bus Type | Parallel, asynchronous | Parallel, synchronous | Serial, asynchronous | Serial, synchronous | Serial, synchronous |
| Data Width | 8 or 16 bits | 32 or 64 bits multiplexed | Serial (1 bit) | 1 bit per line, full duplex | 1 bit per line, half duplex |
| Clock Speed | 4.77 MHz | 33 MHz (base PCI) | Up to 10 Gbps (USB 3.1) | Typically up to several MHz | Typically up to 400 kHz+ |
| Max Bandwidth | ~9 MB/s | 44-132 MB/s | Varies by USB version | Depends on clock speed | Lower than SPI |
| Number of Wires | Many (address, data, ctrl) | Many (multiplexed lines) | 4 (power, ground, D+, D-) | 4 (SCLK, MOSI, MISO, CS) | 2 (SDA, SCL) |
| Device Addressing | Slot-based | Bus/device/function number | Device enumeration | Chip select per device | Addressed devices |
| Typical Use Cases | Legacy expansion cards | Modern expansion cards | External peripherals | Embedded peripherals | Embedded peripherals |
| Bus Mastering | Yes | Yes | Managed by host controller | Master/slave | Multi-master supported |

---

### Practical Notes on Using SPI and I²C

- On platforms like Raspberry Pi, SPI and I²C interfaces are not enabled by default and require configuration via system settings (e.g., `raspi-config`)[^4].
- Libraries such as `wiringPi`, `spidev` (for SPI), and `smbus` (for I²C) provide programming interfaces in C/C++ and Python to communicate with devices on these buses.
- SPI configuration involves setting mode (clock polarity and phase), bit order (MSB or LSB first), and selecting the correct chip select pin[^6].
- I²C communication involves specifying device addresses and handling start/stop conditions for data transfer.

---

This tutorial outlines the fundamental concepts and practical aspects of system buses and modern peripheral interfaces, providing a solid foundation for understanding microcomputer bus architectures and expansion technologies.

<div style="text-align: center">⁂</div>

[^1]: <https://people.ece.ubc.ca/~edc/464/lectures/lec17.pdf>

[^3]: <https://home.mit.bme.hu/~rtamas/rendszerarchitekturak/eloadas/08_bus_introduction.pdf>

[^4]: <https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/all>

[^5]: <https://www.techtarget.com/searchwindowsserver/definition/ISA-Industry-Standard-Architecture>

[^6]: <https://www.ratocsystems.com/english/download/pdffiles/usb61_e_10.pdf>
