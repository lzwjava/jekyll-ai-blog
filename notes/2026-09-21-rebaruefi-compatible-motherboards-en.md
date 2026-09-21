---
audio: false
generated: true
image: false
lang: en
layout: post
title: ReBarUEFI Compatible Motherboards
translated: false
type: note
---

**Question:** What motherboards does the ReBarUEFI project recommend or confirm as working?

**Answer:**

The ReBarUEFI project does not officially "recommend" specific motherboards to buy — rather, it maintains a community-sourced list of confirmed working boards. Here's a summary of the most commonly reported and well-supported motherboards from [the working boards issue](https://github.com/xCuri0/ReBarUEFI/issues/11):

**ASUS (most represented brand):**

- Z170 series: Z170-A, Z170-AR, Z170-DELUXE, Z170-WS, Z170-E, Z170I Pro Gaming, Z170-P, Z170 Sabertooth MARK 1
- Z97/Z270 series: Z97-Pro, Z97-DELUXE, Z97-K, Z270-A, Maximus VII/VIII/IX Hero/Gene
- X99 series: X99-A, X99-A II, X99-DELUXE, X99-DELUXE II, X99M-WS, ROG RAMPAGE V EDITION 10, Sabertooth X99, STRIX X99 GAMING
- Older: P8Z77-V PRO, P8H61-M LX2 R2.0, H110M-K/D, B150M-C, H170M-PLUS, EX-B150M-V3

**MSI:**

- Z97 Gaming 3/5, Z170-A PRO, Z170A Gaming M5, Z270-A PRO, Z270 GAMING M5
- B150M Bazooka/Plus, H110M Gaming, C236M WORKSTATION, H97M-G43

**ASRock:**

- Z97 Extreme9, Z97 Anniversary, Fatal1ty Z97 Killer
- Z170 Extreme4, Z270M Extreme4, H77 Pro4-M/MVP
- X99 Extreme4, X99 Taichi, X299 Steel Legend

**Gigabyte:**

- B75M-D3H, Z170-HD3, Z68MA-D2H-B3, GA-Z270P-D3
- B450 AORUS ELITE/M, B550M Pro-P, X470 AORUS GAMING 5 WiFi, AB350 Gaming, A320M-S2H

**Huananzhi / Machinist (AliExpress X99):**

- Huananzhi X99-QD4, X99-TF, X99-F8, X79 "Green"
- Machinist X99-MR9A PRO V2, Jingsha X79M-S/X99 D8

**Supermicro (server boards):**

- X9SRA, X9DRI-LN4F, X9DRD-7LN4F, X11DPH-T, X11DPU, X11SPH-nCTF, X10SRH-CLN4F, H11DSI

A few key notes:

- ReBarUEFI is a UEFI DXE driver to enable Resizable BAR on systems that don't officially support it.
- Motherboards that don't support at least 2GB BAR size are considered "not working" by the project.
- Many boards require **UEFIPatch** and/or a **DSDT patch** — especially Sandy/Ivy Bridge (Z68, Z77, H77) and Haswell (Z97, H97) boards.
- ASUS Z170 and X99 boards appear most frequently with the widest BAR size support (up to 16–32GB), making them arguably the most "recommended" by community results.

**References:**

- [ReBarUEFI GitHub Repository](https://github.com/xCuri0/ReBarUEFI)
- [List of Working Motherboards (Issue #11)](https://github.com/xCuri0/ReBarUEFI/issues/11)
