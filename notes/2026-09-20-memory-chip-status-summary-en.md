---
audio: false
generated: true
image: false
lang: en
layout: post
title: Memory Chip Status Summary
translated: false
type: note
---

Now I have all the data needed. Let me provide a comprehensive summary of findings.

---

## Memory Chip Status for `lzw@192.168.1.53`

### System Overview

| Item | Value |
|------|-------|
| **Hostname** | `lzw-MS-7996` (MSI MS-7996 motherboard) |
| **CPU** | Intel Core i5-4460 @ 3.20 GHz (4 cores, Haswell) |
| **Kernel** | Ubuntu 7.0.0-31-generic (x86_64) |
| **Graphics** | NVIDIA Tesla M40 (GM200) + Intel HD Graphics (iGPU) |

---

### Current Memory Status

| Metric | Value |
|--------|-------|
| **Total RAM (available)** | **3.2 GiB** (3399592 kB) |
| **Used** | ~827 MiB (24%) |
| **Free** | ~2.4 GiB |
| **Available** | ~2.4 GiB |
| **Swap Total** | 3.7 GiB |
| **Swap Used** | 592 MiB (16%) |

> ℹ️ Total physical memory is ~4 GiB, but ~1 GiB is reserved for the Intel iGPU / BIOS / DMA, leaving **3.2 GiB usable**.

---

### Memory Chip (SPD decode from I²C EEPROM @ 0x50)

| Field | Value |
|-------|-------|
| **Memory Type** | **DDR3 SDRAM** |
| **Module Type** | **UDIMM** (Unbuffered DIMM) |
| **Part Number** | **`KB256082G`** |
| **Slots Populated** | **2/2** (both slots occupied) |
| **Per Module Size** | ~**2 GB** (256M×64) |
| **Total Physical** | **~4 GB** (2 × 2GB) |
| **SDRAM Width** | ×8 (8-bit per chip) |
| **Bus Width** | 64-bit |
| **Number of Ranks** | **2** (dual-rank modules) |
| **Supported CAS Latencies** | 5, 6, 7, 8, 9, 10, 11 (from SPD) |
| **Manufacturing Date** | Year 2025 or later, week 19 |
| **SPD Revision** | 1.1 |
| **Module Revision** | 0x06 |

**Speed Grade:** Likely **DDR3-1333** (PC3-10600) or **DDR3-1600** (PC3-12800) based on the CPU's IMC support.

**Manufacturer:** The JEDEC manufacturer bytes decode to **0x04 0x51** — likely a **Kingston** module or a generic/third-party branded module ("KB256082G" — could be Kingston/Kingbox).

**All memory blocks are `online`** — no offline or faulty memory detected.

---

### Health / Errors

- **EDAC/MCE:** No memory error counters found (EDAC subsystem not loaded).
- **Memory State:** All 32 × 128 MB blocks are **online** ✅
- **NVIDIA driver:** Not loaded (Tesla M40 present but not running, likely needs driver reinstall)
- **Swap:** 16% used — moderate swap usage, but system is not under memory pressure.

**Overall Status:** ✅ **Healthy** — memory is fully online, no errors detected, ~76% free.
