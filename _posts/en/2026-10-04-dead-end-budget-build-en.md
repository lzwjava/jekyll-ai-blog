---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dead End Budget Build
translated: false
type: note
---

The motherboard is an **ASUS A68HM-E**.

## Details

| Field | Value |
|-------|-------|
| **Manufacturer** | ASUSTeK COMPUTER INC. |
| **Model** | A68HM-E (Rev X.0x) |
| **Form factor** | Micro-ATX |
| **Socket** | FM2+ |
| **Chipset** | AMD A68H |
| **BIOS** | AMI v1301 (12/14/2015) |
| **Serial** | 160368661901125 |

## What this tells us

This is a **budget micro-ATX board from ~2014-2015**, part of the same low-cost FM2+ platform we identified earlier. It pairs with the Athlon X4 850 and confirms why the machine is slow:

- **2× DDR3 DIMM slots** — both are currently filled (2× 4 GB = 8 GB), so you're already at max unless you replace the sticks with 2× 8 GB
- **FM2+ socket** — the fastest CPU you could drop in is an Athlon X4 880K (still a weak 2015-era quad-core, marginal upgrade)
- **No M.2 slot** — SATA-only, so the WD Green SSD is as good as it gets storage-wise
- **A68H chipset** — entry-level, no USB 3.1, limited PCIe lanes

It's a classic ~2015 budget office/home build. Honestly, there's no worthwhile upgrade path — the whole platform (CPU, board, RAM) is a dead end. It's best used as-is for light server duty like your mihomo LAN proxy.