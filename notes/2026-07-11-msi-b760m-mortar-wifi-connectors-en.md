---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI B760M Mortar WiFi Connectors
translated: false
type: note
---

I have enough verified data from the official MSI datasheet (this covers the base MAG B760M MORTAR WIFI, not the "II" or "MAX" variants — those are different SKUs with extra M.2 slots and headers).

Question: What connectors does the MSI MAG B760M Mortar WiFi motherboard (LGA 1700, DDR5) have?

Answer:

This is the original **MAG B760M MORTAR WIFI** (not the "II" or "MAX" refresh — those have a 3rd M.2 slot and different header layout, so don't mix specs from those reviews). Per MSI's official datasheet:

**Rear I/O panel**
| Connector | Spec |
|---|---|
| USB 3.2 Gen 2x2 Type-C | 1x, 20 Gbps |
| USB 3.2 Gen 2 Type-A | 3x, 10 Gbps |
| USB 3.2 Gen 1 Type-A | 2x, 5 Gbps |
| USB 2.0 | 1x (rear, rest are internal headers) |
| DisplayPort | 1.4 |
| HDMI | 2.1 (4K@60Hz, needs iGPU) |
| LAN | Realtek RTL8125BG, 2.5Gbps RJ45 |
| Wi-Fi/BT antenna | 2x (Intel Wi-Fi 6E + BT 5.3) |
| Audio jacks | 5x 3.5mm + optical S/PDIF out |

**Storage**
- 2x M.2 Gen4 x4 (64 Gbps) slots — one from CPU, one from chipset (M.2 Shield Frozr covered)
- 4x SATA 6Gb/s ports

**Expansion slots**
- 1x PCIe 5.0 x16 (CPU, Lightning Gen 5, up to 128GB/s)
- 1x PCIe 4.0 x16 (physically x16, electrically x4, chipset)
- 1x PCIe 3.0 x1 (chipset)

**Memory**
- 4x DDR5 DIMM slots, dual-channel, up to 7000+ MT/s (OC)

**Internal headers (from the shared MSI MAG-series header layout — worth confirming against your specific board's silkscreen, since MSI doesn't publish a full internal-header table for this exact non-II SKU in the datasheet)**
- 1x 24-pin ATX_PWR1, 2x 8-pin CPU_PWR
- CPU_FAN1, PUMP_FAN1, SYS_FAN1~4 (6 total fan headers)
- JFP1/JFP2 front panel (power/reset/HDD LED, speaker)
- JAUD1 front audio
- JUSB4 (USB 3.2 Gen2 Type-C front panel), JUSB3 (USB 3.2 Gen1 header, 2 ports), JUSB1~2 (USB 2.0 headers, 4 ports)
- JTPM1 (TPM 2.0 header)
- JRGB1 (12V RGB), JARGB_V2_1~2 (5V addressable ARGB Gen2)
- JCI1 (chassis intrusion)
- JBAT1 (clear CMOS jumper)

For your workstation build context — this board caps you at 2 M.2 Gen4 slots and PCIe 4.0 x4 for a second GPU/NIC lane, which matters if you're planning to add a second NVMe for model checkpoints/datasets or pass through a network card for your AMD dev cloud setup. If you're routinely juggling large local datasets, the 2-slot M.2 limit (vs 3 on the "II" variant) is the one spec here worth double-checking against your actual use case before buying.

References:

- [MSI MAG B760M MORTAR WIFI Official Datasheet](https://storage-asset.msi.com/datasheet/mb/us/MAG-B760M-MORTAR-WIFI.pdf)
- [Tom's Hardware Review — MSI MAG B760M Mortar](https://www.tomshardware.com/reviews/msi-mag-b760m-mortar-wifi-review)
