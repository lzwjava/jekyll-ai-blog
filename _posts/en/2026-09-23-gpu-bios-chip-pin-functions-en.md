---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU BIOS Chip Pin Functions
translated: false
type: note
---

**Question:** What is the 8-pin BIOS chip on a GPU, and what does each pin do?

**Answer:**

The 8-pin BIOS chip on a GPU is an **SPI NOR Flash memory** IC (common models: Winbond W25Q128, MX25L series). It stores the GPU's firmware — VBIOS — which the GPU reads at power-on to initialize itself. The chip uses the **SPI (Serial Peripheral Interface)** protocol and comes in a tiny SOIC-8 package.

Here's what each pin does:

| Pin | Name | Function |
|-----|------|----------|
| 1 | CS# | Chip Select — pulls low to activate the chip |
| 2 | DO (MISO) | Data Out — sends data to the GPU |
| 3 | WP# | Write Protect — when pulled low, blocks any writes |
| 4 | GND | Ground |
| 5 | VCC | Power supply (1.8V or 3.3V depending on chip) |
| 6 | HOLD# | Pauses serial communication temporarily |
| 7 | CLK | Clock signal — drives data timing |
| 8 | DI (MOSI) | Data In — receives data from the GPU |

The **WP# pin** is particularly important for GPU BIOS modding — some boards tie it to ground permanently to prevent accidental overwrites. To flash a new BIOS, you sometimes need to bridge this pin to VCC, or use a clip programmer (like the CH341A) that overrides it.

**References:**
- [Winbond W25Q128 Datasheet](https://www.winbond.com/resource-files/w25q128jv%20spi%20revc%2011162016.pdf)
- [SPI Flash Programming — flashrom wiki](https://www.flashrom.org/Flashrom)
- [GPU BIOS modding guide — TechPowerUp](https://www.techpowerup.com/vgabios/)