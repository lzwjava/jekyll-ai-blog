---
audio: false
generated: true
image: false
lang: en
layout: post
title: Can Huanan X99 Fix M40 BAR Error
translated: false
type: note
---

**Question:** Will the Huanan (华南) X99-4 MT Plus + Xeon E5-2673v3 combination help resolve the M40 PCI/BAR error?

**Answer:**

**Short answer: Probably yes — better than the old Lenovo board — but not guaranteed.**

Here's the breakdown:

---

### Why it's an improvement

| | Old Lenovo (i5-4460) | 华南 X99-4 MT Plus + 2673v3 |
| --- | --- | --- |
| **Platform** | Consumer Haswell, 2016 BIOS | LGA2011-3 X99 platform |
| **PCIe lanes** | Limited | 40-lane Xeon (E5-2673v3) |
| **BIOS age** | Very old, no UEFI Tesla support | Chinese X99 boards often have modded/updated BIOS |
| **Above 4G Decoding** | Almost certainly absent | May be present or moddable |

The E5-2673v3 is a **40-lane Xeon** — it has full PCIe 3.0 x16 bandwidth and the CPU-side address space to support large BAR allocation, which is what the M40 needs.

---

### The real risk: 华南 X99-4 MT chipset

The X99-4 MT Plus often uses a **consumer-grade chipset (H81 or B85)** disguised in an X99-style board, **not a true Intel C612/X99 server chipset**. This is common for cheap Chinese X99 boards. There are real reports of M40 24GB failing on boards because BAR1 could not be assigned, even with Above 4G decoding enabled.

Key things to check:

- **Does your BIOS have "Above 4G Decoding"?** Enter BIOS and look under Advanced/PCIe settings. This is the single most important toggle.
- **Is CSM (Compatibility Support Module) disabled?** Tesla cards work better in pure UEFI mode.

---

### If Above 4G Decoding is missing

Some modded Chinese X99 BIOSes include Above 4G Decoding and Resizable BAR support — communities like Win-Raid have BIOS mods specifically for Chinese X99 boards. The ReBarUEFI project also provides a UEFI DXE driver to enable Resizable BAR on systems that don't support it officially, and without 4G Decoding you will be limited to 1GB BAR.

---

### Summary

```
华南 X99-4 MT Plus + 2673v3 + M40
        ↓
Step 1: Check BIOS for "Above 4G Decoding"
        ↓
Found → Enable it, disable CSM → likely works
        ↓
Not found → Flash modded BIOS or use ReBarUEFI
```

It's a **much better candidate** than your old Lenovo board, but the outcome depends on what's actually in that BIOS.

**References:**

- [ReBarUEFI - Enable Resizable BAR on unsupported systems](https://github.com/xCuri0/ReBarUEFI)
- [Win-Raid: Overclock BIOS mods for Chinese X99 boards](https://winraid.level1techs.com/t/guide-overclock-bios-mods-for-chinese-x99-mbs/104683)
- [Tesla M40 + Above 4G Decoding discussion (Tom's Hardware)](https://forums.tomshardware.com/threads/tesla-m40-and-dell-oem-board.3600010/)
