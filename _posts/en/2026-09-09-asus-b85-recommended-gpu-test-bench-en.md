---
audio: false
generated: true
image: false
lang: en
layout: post
title: "ASUS B85: Recommended GPU Test Bench"
translated: false
type: note
---

Good question — this is exactly the motherboard the GPU testing manual recommends. Let me evaluate the ASUS B85 specifically as a **graphics card test bench**, comparing it against both the manual's requirements and your X99 machine.

## ASUS B85 as a GPU Testing Platform

| Manual requirement | ASUS B85 (e.g., B85M-G / B85-PLUS) | Verdict |
| --- | --- | --- |
| Recommend ASUS B85 or above | ✅ This is literally the manual's first-choice board | ✅ Perfect match |
| Legacy/CSM boot (to pick from the multi-boot menu) | ✅ Haswell-era board, full Legacy + UEFI boot support | ✅ Works |
| Multi-GPU support (use iGPU to display, test the dGPU) | ✅ Any LGA1150 Haswell CPU (except some Pentium/Celeron) has **Intel HD integrated graphics** with D-Sub/DVI/HDMI outputs — this is the manual's key workflow: BIOS → Primary Display → CPU Graphics | ✅ Fully supports the "test a black-screen card" scenario |
| 8GB+ RAM | ✅ 4 DIMM slots, up to 32GB DDR3 (typically 2×8GB DDR3 1600 for ~cheap) | ✅ Easy to meet, even for testing 8GB-VRAM cards |
| 250GB+ SATA SSD for the test image | ✅ Native SATA III ports, plug a 250–500GB SSD in a USB enclosure or directly | ✅ Works |

## Why the manual prefers it (and why it beats your X99 machine)

1. **Has integrated graphics** — the single biggest advantage. When a test card fails to display, you switch to the iGPU output and still run MATS/MODS on the dGPU. Your Xeon E5-2673 v3 + X99 simply can't do this.
2. **Proven stable with the toolchain** — the manual's author verified ASUS H170/B85/B150 boards against MATS/MODS; this avoids flaky boot/USB issues common on other boards.
3. **Cheap and disposable** — B85 boards and i3/i5-4xxx CPUs go for very little secondhand, so you don't risk an expensive daily driver.
4. **Single-GPU focus is fine** — the B85 chipset doesn't do SLI/CrossFire, but the manual doesn't need that; it just needs *iGPU + one dGPU* (set Primary Display to "CPU Graphics"), which is not an SLI config and works fine.

## Two caveats

- **CPU choice matters**: pick an i3-4xxx/i5-4xxx (has iGPU). Some low-end Pentium/Celeron chips lack graphics, which would defeat the purpose.
- **Older N-card driver limits**: fine per the manual — the image covers GTX 6xx up to RTX 3090 regardless of platform age.
- **Your X99 machine still has a role**: it's fine as a *daily-use/multi-task rig*, and can test cards that at least display output — it just can't handle the "card won't POST" cases.

## Bottom line

If you're setting up a dedicated GPU-testing bench following this manual, **a used ASUS B85M-G/B85-PLUS + i5-4460 + 2×8GB DDR3 + 250GB SSD** is the textbook build — cheap, fully compatible, and it covers the iGPU-workflow that your Xeon/X99 setup fundamentally cannot do. The B85 is not "better" than X99 in general (X99 wins on CPU performance), but for **this specific testing purpose**, the B85 is the right tool.
