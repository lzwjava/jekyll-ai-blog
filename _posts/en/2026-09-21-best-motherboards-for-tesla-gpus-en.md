---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best Motherboards for Tesla GPUs
translated: false
type: note
---

Question: What motherboards are recommended to pair with an NVIDIA Tesla M40 or P100 GPU?

Answer:

Here are well-regarded boards that are known to work with M40/P100 class cards, grouped by use case. Since you're already holding an E5-2676 v3 (LGA 2011-3), all options below keep that socket so your CPU carries over.

---

## 🏆 Top Picks (LGA 2011-3, Compatible with E5-2676 v3)

**1. ASUS X99-E WS / X99-E WS USB3.1** — Best overall pick

Community testing has confirmed this board boots with up to 6 Tesla P40s under Above 4G Decoding without issue. There is also a community-modded BIOS available that unlocks Resizable BAR support, increases MMIO High space from 256 GiB to 1 TiB, and updates all microcodes — making it one of the most capable X99 boards for compute GPU work. It has 7 PCIe 3.0 x16 slots with a PLX switch for full x16 bandwidth on four cards simultaneously.

- Socket: LGA 2011-3 | DDR4 | E-ATX
- Above 4G Decoding: ✅ Yes (BIOS → Boot → Above 4G Decoding)
- ReBAR: ✅ Via community BIOS mod
- Secondary display GPU needed: Yes (M40/P100 are headless)

**2. Supermicro X10SRA / X10SRA-F** — Best for workstation use

The X10SRA-F supports the Intel Xeon E5-2600 v3 and v4 families via the C612 chipset, with four PCIe 3.0 x16 slots (running at 16/16/NA/8 or 16/8/8/8) and dual-port Intel GbE LAN. Supermicro's server-grade BIOS reliably exposes Above 4G Decoding and handles large-BAR cards with fewer quirks than consumer boards. Good balance of PCIe slots and desktop usability (audio, USB 3.0).

- Socket: LGA 2011-3 | DDR4 ECC | ATX
- Above 4G Decoding: ✅ Yes (reliable server BIOS)
- ReBAR: ⚠️ Not officially supported

**3. Supermicro X10SRL-F** — Best for server/headless compute

The X10SRL-F is an ATX-sized board supporting E5-2600 v3 and v4 with the C612 chipset, offering 7 PCIe slots total (including two PCIe 3.0 x8 in x16 physical slots), 10 SATA 6Gbps ports, and dual Intel i210 GbE LAN. It's a proper server board — solid, no-frills, and has an onboard VGA for headless management. Great if you're running Linux for inference/training.

- Socket: LGA 2011-3 | DDR4 ECC RDIMM (up to 1TB) | ATX
- Above 4G Decoding: ✅ Yes
- ReBAR: ⚠️ Not officially, but BIOS mod possible

---

## Quick Comparison

| Board | Form | PCIe x16 Slots | Above 4G | ReBAR Mod | DDR | Price (used) |
|---|---|---|---|---|---|---|
| ASUS X99-E WS | E-ATX | 7 (PLX) | ✅ | ✅ | DDR4 | ~$80–150 |
| Supermicro X10SRA-F | ATX | 4 | ✅ | ⚠️ | DDR4 ECC | ~$60–120 |
| Supermicro X10SRL-F | ATX | 7 | ✅ | ⚠️ | DDR4 ECC RDIMM | ~$50–100 |

---

## ⚠️ Important Notes

- **Your current DDR3 RAM won't carry over** — all these boards use DDR4. If you want to keep the DDR3, you'd need to stay on a Chinese X99 clone board (Huanan, Machinist, JGINYUE), but none of them reliably expose Above 4G Decoding without BIOS hacking.
- For the **M40/P100**, you still need a cheap display GPU (GT 710, Quadro 600, etc.) for video output, since these cards are headless compute-only.
- **Power**: All three boards use a standard ATX 24-pin + 8-pin EPS connector. The M40/P100 need the additional CPU 8-pin power adapter.

The **ASUS X99-E WS** is the community favorite specifically for Tesla-class GPU work, given the confirmed multi-GPU support and available BIOS mod.

---

**References:**
- [ASUS X99-E WS BIOS Mod with ReBar + Multi-Tesla confirmed](https://winraid.level1techs.com/t/offer-asus-x99-e-ws-usb3-1-bios-mods-incl-rebar-support/116427)
- [Supermicro X10SRL-F specs](https://www.supermicro.com/zh_cn/products/motherboard/X10SRL-F)
- [Supermicro X10SRA-F specs](https://www.supermicro.com/ja/products/motherboard/X10SRA-F)
