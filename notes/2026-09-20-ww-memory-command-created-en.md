---
audio: false
generated: true
image: false
lang: en
layout: post
title: ww memory command created
translated: false
type: note
---

Everything is working. Here's a summary of what was created:

---

## ✅ Done — `ww memory {host}` command created

### Files modified

| File | Action |
|------|--------|
| `ww/machine/memory.py` | **Created** — full memory diagnostics module |
| `ww/main.py` | **Edited** — added `memory` group dispatch + help text |

### Usage

```bash
ww memory lzw@192.168.1.53
ww memory root@server -i ~/.ssh/key.pem
ww memory --help
```

### What it does

| Feature | Description |
| --------- | ------------- |
| **Memory usage** | `free -h` + `/proc/meminfo` (total, free, available, swap) |
| **SPD EEPROM decode** | Reads DRAM module info from I²C (DDR3/DDR4/DDR5): type, part number, manufacturer, ranks, voltage, speed, CAS latencies, manufacturing date |
| **Hardware slots** | From dmesg — shows populated/total slots |
| **CPU / platform** | lscpu output |
| **Kernel messages** | memory-related dmesg/journalctl |
| **Health summary** | Usage %, SPD status, memory block online status |

### Tested output for `lzw@192.168.1.53`

```
Memory Type:    DDR3 SDRAM
Module Type:    UDIMM
Part Number:    KB256082G
Manufacturer:   Fujitsu  (ID: 0x04 0x51)
Ranks:          2
Speed:          ~1330 MT/s
Grade:          DDR3-1330 (PC3-10640)
Module Size:    2.0 GB (from SPD)
Mfg Date:       2018 week 25
Slots populated: 2/2
Usage:  27%  (2.4 GB free / 3.2 GB total)
✅ SPD readable, all 32 memory blocks online
```
