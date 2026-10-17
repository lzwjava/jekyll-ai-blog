---
audio: false
generated: true
image: false
lang: en
layout: post
title: UEFI and Legacy Boot Modes
translated: false
type: note
---

**Question:** What do UEFI and Legacy (BIOS) mean in the context of computer boot modes?

---

**Answer:**

## Legacy (BIOS)

- The **old** way computers have started up since the 1980s
- Stands for **Basic Input/Output System**
- Simple, limited — only supports hard drives up to **2 TB**
- Uses **MBR** (Master Boot Record) partition style
- Text-based interface, mouse usually doesn't work
- Slower boot time

## UEFI

- The **modern** replacement for Legacy BIOS
- Stands for **Unified Extensible Firmware Interface**
- Supports drives larger than **2 TB**
- Uses **GPT** (GUID Partition Table) partition style
- Graphical interface, mouse works
- **Faster boot** (supports Fast Boot / Secure Boot)
- Required for Windows 11 and modern Linux installs

---

## Simple Analogy

| | Legacy BIOS | UEFI |
|--|-------------|------|
| Like... | An old flip phone | A modern smartphone |
| Speed | Slow | Fast |
| Disk size limit | 2 TB max | 9 ZB (no real limit) |
| Security | None | Secure Boot ✓ |
| Interface | Text only | Graphical (mouse works) |

---

## Which Should You Use for Ubuntu?

✅ **Use UEFI** — it's what modern Dell laptops use by default, and Ubuntu installs best with it.

> When you flash your USB drive with Rufus, make sure to select:
> - Partition scheme: **GPT**
> - Target system: **UEFI (non CSM)**

"CSM" (Compatibility Support Module) is the option that allows Legacy mode — **leave it off** for a modern Ubuntu install.

---

**References:**
- [UEFI vs Legacy BIOS – How-To Geek](https://www.howtogeek.com/56958/htg-explains-how-uefi-will-replace-the-bios/)
- [Ubuntu UEFI Install Guide](https://help.ubuntu.com/community/UEFI)
