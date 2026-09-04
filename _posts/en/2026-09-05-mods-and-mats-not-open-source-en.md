---
audio: false
generated: true
image: false
lang: en
layout: post
title: MODS and MATS Not Open Source
translated: false
type: note
---

Short answer: **No, MODS/MATS are not open source.** They are **proprietary, internal NVIDIA engineering tools** that were never publicly released.

## What MODS/MATS actually are

- **MODS** = NVIDIA's internal **diagnostic and validation framework**. It ships with its own low-level driver that talks to the GPU almost directly (bypassing the normal display driver stack — that's why `-skip_rm_state_init` exists).
- Test logic is written in **JavaScript-like scripts** (`gputest.js`) that the MODS engine interprets — NVIDIA engineers use it for chip bring-up, validation, and failure analysis on new GPUs before drivers even exist.
- **MATS** = the **memory test module** built on top of MODS. It writes/reads patterns across all VRAM channels and subpartitions and reports errors per location (that's the FBI0A0 / A0 / low-byte–high-byte stuff in your manual).

## How the repair community got them

- They were **never sold or published** by NVIDIA. Versions (367.x, 400.x, 455.x — matching the folder names in your manual, e.g. `400.250`, `455.127`) **leaked out** of NVIDIA and its factory/partner validation environments over the years.
- They spread mainly through **repair-community forums** (Chinese repair forums, badcaps, videocard repair groups), usually bundled like your manual's package — a Linux/DOS image with pre-matched MODS builds per GPU generation.
- Each MODS build is tied to a **specific driver branch** because the register layouts/init sequences differ per generation — that's why the manual has you pick `400.250` for a GTX660, `455.127` for RTX 30-series, etc.

## Practical implications

- **No source code, no official support** — NVIDIA does not acknowledge or support these tools publicly. You can't get documentation, updates, or fixes.
- **Legal grey area** — distributing/using leaked internal tools isn't sanctioned by NVIDIA; the manual-style packages you find are community-assembled.
- **Newer cards lag** — support for each new GPU generation depends on a leaked build matching that generation appearing in the community (e.g. RTX 40-series support is spotty/incomplete compared to ≤3090, which your manual lists as the limit).
- The **open-source alternatives** are much weaker for this purpose: `memtestG80`/`memtest_vulkan` (VRAM stress, but no per-chip fault localization like MATS), `gpu-burn` (stress test), or AMD's `amdgpu` + UMRs for AMD cards.

So in short: it's leaked internal silicon-validation software from NVIDIA, not open source — which is also why it's so much more powerful (register-level access, per-chip VRAM mapping) than anything the open-source world has for GPU repair.
