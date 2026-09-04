---
audio: false
generated: true
image: false
lang: en
layout: post
title: Barebones GPU Diagnostic Boot
translated: false
type: note
---

Yes, your understanding is basically correct, but let me clarify a few details from the manual:

## 1. No normal login needed — it's a purpose-built test environment

This is not a regular Debian/Ubuntu desktop install. The image (restored to a 250G+ disk with 5–6 MBR partitions, or used as a USB version 「优盘版」) gives you a **boot menu with 7 options**:

| Menu | System | Purpose |
| ------ | -------- | --------- |
| 1 | **DOS** | Old NVIDIA cards (GTX6xx/5xx/2xx/GTxxx/8400GS and below) |
| 2 | Linux | NVIDIA up to RTX 3090 |
| 3 | Linux | NVIDIA up to 2080Ti |
| 4 | Linux | AMD RX4xx/5xx/Vega and below |
| 5 | Linux | AMD RX5700/6800/6900 etc. |
| 6 | Linux | AMD Radeon VII |
| 7 | Windows | FurMark / 3DMark / GPU-Z (mostly useless, often BSODs) |

You just press **F8 → Legacy mode**, pick a menu item, and it drops you straight into a terminal-like environment with MODS/MATS pre-installed. No desktop, no user login — the whole system exists only to run these test tools. (Menu 2/3 can also boot via UEFI for laptops that can't do Legacy.)

## 2. Why it works when Ubuntu can't detect the card

Correct — this is the key point. MODS/MATS are NVIDIA's **internal engineering tools** that talk to the GPU **directly at the hardware/register level**, bypassing the normal driver stack:

- A normal Ubuntu uses the official driver → if the card is badly broken or half-initialized, the driver fails → card "not detected."
- MODS with `-skip_rm_state_init` **skips the normal driver/resource-manager initialization**, so it can still initialize and talk to a GPU that the regular driver rejects.
- MATS then reads VRAM test results **per memory channel/subpartition** (e.g. FBI0A0), so you know *which* VRAM chip is faulty — e.g. "A0 low-byte has 31760 errors" → B-side first chip.

## 3. But there are limits — it's not magic

The manual is explicit about this:

- **If the GPU can't initialize at all** (dead core, bad power delivery), you won't even get the PASS screen after `./mods gputest.js -skip_rm_state_init -notest` — then MATS **cannot test it**. It tells you the card has a hardware fault, but not which chip.
- You need RAM ≥ VRAM size (8G+ recommended), and a motherboard supporting Multi-GPU (iGPU for display) to test a card that gives no display.
- MATS diagnoses **VRAM faults precisely**; for core vs VRAM ambiguity you run the second check (`./mods gputest.js -oqa -test 118 -matsinfo`).

**So in short:** yes — it's a barebones bootable test environment (no normal OS login), and yes — MODS/MATS work at a much lower level than a normal Linux driver, which is exactly why they can detect and localize VRAM faults on cards that regular Ubuntu/Windows can't even initialize. Just remember the GPU still needs basic power + a minimally alive core for the tools to run.
