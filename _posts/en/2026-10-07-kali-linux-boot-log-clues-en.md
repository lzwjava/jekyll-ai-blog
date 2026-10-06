---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kali Linux Boot Log Clues
translated: false
type: note
---

**Question:** Is this system actually running Kali Linux, and how can you tell?

**Answer:**

Yes, this is almost certainly **Kali Linux**. Here are the clues visible in the boot messages:

---

**Clue 1: `file:/cdrom resolute`**
```
Ign:1 file:/cdrom resolute InRelease
Get:2 file:/cdrom resolute Release [664 B]
Get:4 file:/cdrom resolute/restricted amd64 Packages
Get:5 file:/cdrom resolute/main amd64 Packages
```
- **"resolute"** is the codename for **Kali Linux 2024.4**
- This is Kali's APT package source being read from the ISO/cdrom

---

**Clue 2: `/dev/disk/by-label/writable` → `/log-persistence`**
- This is **100% Kali Live USB persistence** setup
- Kali names its persistence partition **"writable"** by default
- No other distro uses this exact label/mount combination

---

**Clue 3: `passwd: password changed`**
- Kali Live automatically resets the default `kali/kali` credentials on boot

---

**In Summary:**

| What you're running | Details |
|---|---|
| OS | Kali Linux |
| Version | 2024.4 ("resolute") |
| Mode | Live USB with Persistence |
| Persistence partition | `/dev/sdb4` labeled `writable` |

This is a **bootable USB drive** running Kali Linux, not a traditionally installed OS on the SSD.

---

**References:**
- [Kali Linux releases — "resolute"](https://www.kali.org/blog/kali-linux-2024-4-release/)
- [Kali Live USB Persistence](https://www.kali.org/docs/usb/usb-persistence/)
