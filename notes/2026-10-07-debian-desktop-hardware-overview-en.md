---
audio: false
generated: true
image: false
lang: en
layout: post
title: Debian Desktop Hardware Overview
translated: false
type: note
---

Here's the full hardware report for **192.168.1.137 (Debian 13 trixie, hostname `debian`)**:

## 🖥️ System / Motherboard

| Component | Detail |
|---|---|
| Vendor | **MSI** |
| Motherboard | **MSI Z170A GAMING M3 (MS-7978)** v2.0 |
| Chassis | Desktop (type 3) |
| BIOS | American Megatrends Inc. **A.50** (2016-02-23) |

## 🧠 CPU

| Component | Detail |
|---|---|
| Model | **Intel Core i5-6500** @ 3.20GHz (Skylake, 6th gen) |
| Cores / Threads | **4 cores / 4 threads** (no hyperthreading), 1 socket |
| Turbo | up to 3.60 GHz, idle down to 0.80 GHz |

## 💾 Memory

| Component | Detail |
|---|---|
| Total RAM | **7.7 GiB** (8057 MB), ~6.5 GiB available |
| Swap | 2.9 GiB (unused) |

*(Note: memory module details from dmidecode weren't readable — `lzw` is not in sudoers. Let me know if you want the exact DDR4 speed/part numbers.)*

## 💽 Storage

| Device | Size | Model | Mount |
|---|---|---|---|
| sda | **55.9 GB** | **faspeed K5-60G** (SSD) | `/boot/efi` (976M), `/` (52.1G), swap (2.9G) |

## 🎮 GPU / Peripherals

| Device | Detail |
|---|---|
| GPU | **Intel HD Graphics 530** (integrated, rev 06) — no discrete GPU |
| Audio | Intel 100 Series/C230 HD Audio |
| NIC | **Qualcomm Atheros Killer E2400** Gigabit Ethernet |

## ⚙️ Kernel
`Linux debian 6.12.111+deb13-amd64` (2026-09-28 build)

**In short:** an MSI Z170A GAMING M3 desktop build — Skylake i5-6500, 8GB DDR4-class RAM (Z170 board capacity), and a 60GB faspeed SSD. It's a compact home-lab/server box. Want me to pull RAM module details (needs an admin account), check disk SMART health, or install something on it?
