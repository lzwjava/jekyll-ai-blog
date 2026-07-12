---
audio: false
generated: true
image: false
lang: en
layout: post
title: EZ Debug LED and MI50 Analysis
translated: false
type: note
---

Question: Analyze the pasted Q&A above about the EZ Debug LED location on the MSI MAG B760M Mortar, and the accompanying troubleshooting guidance for a no-boot symptom with an AMD MI50.

Answer:

## Fact-check table

| Claim | Verdict | Basis |
|---|---|---|
| Board has 4x EZ Debug LEDs (CPU/DRAM/VGA/BOOT) | **Confirmed** | MSI's own manual lists 4x EZ Debug LED as a stock feature of the MAG B760M MORTAR WIFI II |
| Functional meaning of each LED | **Confirmed, verbatim-accurate** | Manual states the LEDs indicate motherboard debug status, where CPU means CPU not detected/failed, DRAM means memory not detected/failed, VGA means GPU not detected/failed, and BOOT means no bootable device found — the pasted answer's table matches this exactly |
| Physical location: "top-right edge, near 24-pin ATX" | **Plausible, not independently confirmed** | I could not pull an explicit position statement tying the LED cluster to ATX_PWR1 from the manual text I retrieved — the diagrams don't extract to text well. This is a very common MSI convention across their boards, so it's a reasonable inference, but I want to flag it as inference rather than confirmed fact, per your own bar for evidence |
| 13900KF has no iGPU | **Confirmed** (general knowledge, no search needed) | All Intel "F"-suffix SKUs lack integrated graphics — this part of the pasted answer is correct and doesn't need hedging |
| MI50 "sometimes has PCIe/BIOS compatibility issues" | **Understated** | See below — this is not an edge case, it's close to the default experience |

## The MI50 line is the weakest part of the pasted answer

This is the part I'd push back on hardest. The MI50 isn't a slightly-quirky GPU — it's a datacenter compute accelerator (Vega 20, HBM2) that was never designed to boot a consumer desktop at all:

- **No display output by default.** The physical mini-DisplayPort header exists on the PCB but ships disabled — one hardware inventory of a Vega20 MI50 explicitly shows the DisplayPort in an "off" state, distinct from ports that are simply not physically implemented, and separate first-hand testing confirms no image comes out of the DisplayPort until a Radeon Pro VII VBIOS is flashed onto the card. The sibling Vega20-generation Instinct card has the identical constraint — it has no video out by default, and a WX9100 BIOS flash is needed to unlock the hidden Mini DisplayPort and improve consumer-hardware compatibility.
- **Power delivery is non-trivial.** The card needs two 8-pin power connectors and draws up to 300 Watts — if your build only ran one 8-pin or used a molex/6-to-8-pin adapter chain, that alone can produce exactly the "fan spins, no display" symptom the pasted answer is diagnosing, before you even get to BIOS/VGA-LED questions.
- **Boot failures are commonly slot-order and BIOS-setting dependent, not occasional.** A real troubleshooting thread on a Dell workstation shows the MI50 refusing to reach POST at all in certain PCIe slot positions, requiring the accelerator to be moved to a slot before the display GPU in the PCIe enumeration order before the system would boot.

So "sometimes has compatibility issues" is true but undersells it — with an MI50 in a consumer B760M board, I'd treat no-boot/no-video as the expected first outcome, not an exception, and the real fix path is usually: (1) confirm both 8-pin power leads are on independent PSU cables, not a splitter, (2) try the MI50 alone with no other GPU installed, (3) check Above 4G Decoding / Resizable BAR settings in BIOS (these matter a lot for large-BAR compute cards), (4) if still dead, expect you may need a VBIOS flash to get any video signal from it at all, which is a nontrivial, moderately risky procedure, not a checkbox setting.

## One thing worth flagging before you act on this

The MI50 doesn't appear anywhere earlier in our thread — your original parts list and the coil-whine diagnosis were built around the RTX 4070 plus a second AMD card you swapped in for testing (unspecified model, consumer-grade, since it was doing normal display duty). If this pasted Q&A is about the *same* physical machine, that's a meaningfully different GPU than what we've been debugging noise on — worth double-checking whether this is a separate rig (plausible, since MI50 32GB cards are a well-known cheap-VRAM pickup in the local-LLM community and would fit your training-workload use case) or the same box with an added card, since the EZ Debug LED troubleshooting steps that make sense change a lot depending on which.

## Bottom line

The pasted answer is accurate on the parts that come straight from MSI's own documentation (LED functional meanings, iGPU absence on KF chips) and reasonable-but-unverified on the physical LED location. Where it goes soft is treating MI50 boot failures as an occasional compatibility footnote when the primary literature on this card treats "no display, no boot until you fix power/BIOS/VBIOS" as the default first-boot experience for anyone dropping one into non-server hardware.

References:

- [MSI MAG B760M MORTAR II / WIFI II — Official User Guide (PDF)](https://download-2.msi.com/archive/mnu_exe/mb/MAGB760MMORTARII_MAGB760MMORTARWIFIII_EN.pdf)
- [MSI MAG B760M MORTAR MAX WIFI Manual — EZ Debug LED section](https://www.manualslib.com/manual/3270648/Msi-Mag-B760m-Mortar-Max-Wifi.html)
- [AMD Radeon Instinct MI50 32GB VBIOS reference — GitHub Gist](https://gist.github.com/evilJazz/14a4c82a67f2c52a6bb5f9cea02f5e13)
- [AMD Radeon Instinct MI25 — ArchWiki](https://wiki.archlinux.org/title/AMD_Radeon_Instinct_MI25)
- [ThinkPad P50 + MI50 crossflash for display output — eGPU.io forum](https://egpu.io/forums/pc-setup/thinkpad-p50-radeon-instict-mi50-with-radeon-pro-vii-vbios/)
- [No-boot/no-video with AMD Instinct MI50 in Dell Precision 7820 — Dell Community](https://www.dell.com/community/en/conversations/precision-fixed-workstations/no-boot-no-video-when-adding-an-amd-instinct-mi50-in-my-7820/6858a82c03f07b7681d3fb2f)
- [AMD Radeon Instinct MI50 specs — technical.city](https://technical.city/en/video/Radeon-Instinct-MI50)
