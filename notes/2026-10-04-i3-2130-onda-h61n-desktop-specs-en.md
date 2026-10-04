---
audio: false
generated: true
image: false
lang: en
layout: post
title: i3-2130 Onda H61N Desktop Specs
translated: false
type: note
---

Here's the hardware breakdown for `192.168.1.45` (Onda H61N desktop):

## 🧠 CPU — Intel Core i3-2130 @ 3.40 GHz

- **Socket**: LGA1155 · **Generation**: Sandy Bridge (2nd gen, 2011)
- **Cores**: 2 physical / 4 threads (Hyper-Threading) · **TDP**: 65W
- L2 512KB, L3 3MB · Max mem bandwidth: DDR3-1333

## 🧩 Motherboard — Onda Technology **H61N**

- **Chipset**: Intel **H61 Express** (confirmed in lspci: `H61 Express Chipset LPC Controller`)
- Socket LGA1155, 2nd/3rd gen Core support, 2× DDR3 DIMM slots, max 16 GB, 1× PCIe x16, SATA II
- This is the platform's defining spec: **H61 = DDR3 only, up to 1333 MT/s**

## 💾 Memory chip — DDR3, ~8 GiB

- **Total physical**: **8320 MiB** (~8.1 GiB, from SMBIOS via lshw)
- **Linux sees**: 7.1 GiB (`MemTotal 7,486,648 kB`) — the ~0.8 GiB gap is reserved for the **Intel HD Graphics iGPU shared memory** (Sandy Bridge steals system RAM for VRAM, typical 512 MB–1.7 GB)
- Platform dictates: **DDR3-1333** (H61's rated spec)

**⚡ Caveat**: exact module details (manufacturer, part number, speed grade like PC3-10600, single 8G vs 2×4G sticks) are in SMBIOS SPD, but `dmidecode` needs **root** and this box has no passwordless sudo. If you want the full SPD dump, tell me to run `sudo dmidecode -t memory` interactively — or from the machine's own terminal run:

```
sudo dmidecode -t memory | grep -E "Size|Speed|Manufacturer|Part Number|Locator"
```

**TL;DR**: 2011-era Sandy Bridge desktop — **i3-2130** CPU on an **Onda H61N** (H61 chipset, LGA1155) motherboard with **~8 GB DDR3** system memory, DDR3-1333 class.
