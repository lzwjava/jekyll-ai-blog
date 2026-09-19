---
audio: false
generated: true
image: false
lang: en
layout: post
title: X99 Motherboards with ReBAR Support
translated: false
type: note
---

**Question:** What LGA2011-3 X99 motherboards natively support Resizable BAR and Above 4G Decoding?

**Answer:**

Here's a clear breakdown by category — from boards that support these features natively, to those that can get them via BIOS mod.

---

**Tier 1 — Native support (works out of the box)**

These are the best options if ReBAR and Above 4G Decoding matter to you:

**Huananzhi X99 BD4 (DDR4)**
The Huananzhi BD4 BIOS natively includes Above 4G Decoding and Resizable BAR support, along with smart fan control, RAM overclocking, Secure Boot, and TPM support. This board is the gold standard for ReBAR on the LGA2011-3 platform among budget Chinese boards. It uses DDR4 and is ATX form factor. This is the board most frequently recommended in the modding community as a drop-in solution.

**Huananzhi X99 F8D (Dual Socket, DDR4)**
For dual-socket Xeon builds, the F8D is the bigger sibling that inherits the same BIOS features. Less common but relevant if you're building a multi-CPU workstation.

---

**Tier 2 — Works via BIOS swap from Huananzhi BD4**

The modded Huananzhi BD4 BIOS has been confirmed working on the Jingsha X99-8D3 and X99-D8 boards, where Above 4G Decoding and ReBAR are enabled by default in the modded BIOS. ReBAR has also been confirmed working via this modded Huananzhi BD4 BIOS on JGINYUE X99 variants, tested personally with an Nvidia RTX 3070 and AMD RX 5700 XT and RX 6600 XT.

The key insight from the community is that the Huananzhi BD4 BIOS can be transplanted onto several compatible Chinese X99 boards by swapping the ME (Management Engine) region while keeping the BD4's BIOS region. This requires a CH341A hardware programmer.

---

**Tier 3 — BIOS mod required, confirmed working**

These branded boards have modded BIOSes available from the WinRaid community with ReBAR + Above 4G Decoding injected:

- **ASUS X99 Deluxe** — modded BIOS available, Above 4G offset at `0x173`
- **ASUS X99-A / X99-A USB 3.1** — modded BIOS available from WinRaid
- **ASUS X99-E WS / X99-E WS USB 3.1** — modded BIOS available
- **Gigabyte X99 UD4P / X99 Gaming 5 / X99 Designare EX** — modded BIOSes available

---

**Summary table**

| Board | DDR | ReBAR Native | Difficulty |
| --- | --- | --- | --- |
| Huananzhi X99 BD4 | DDR4 | ✅ Yes | None |
| Jingsha X99-D8 / 8D3 | DDR4 | via BIOS swap | Medium (needs CH341A) |
| ASUS X99 Deluxe/A | DDR4 | via BIOS mod | Medium |
| 精粤 X99M-D D3 / GD4 ARGB | DDR3/4 | ❌ No | Hard / uncertain |

**Bottom line:** If your goal is LGA2011-3 + full ReBAR + Above 4G Decoding with the least hassle, the **Huananzhi X99 BD4** is the clear community-recommended choice. It's also widely available on AliExpress and usually priced comparably to other Chinese X99 boards.

---

**References:**

- [Guide: Overclock BIOS mods for Chinese X99 MBs – WinRaid](https://winraid.level1techs.com/t/guide-overclock-bios-mods-for-chinese-x99-mbs/104683)
- [Request: Mod Jingsha X99-D8 with ReBAR – WinRaid](https://winraid.level1techs.com/t/request-mod-jingsha-x99-d8-with-rebar-4g-encoding/110083)
- [Request: Mod JGINYUE X99I-SERVER – WinRaid](https://winraid.level1techs.com/t/request-mod-jginyue-x99i-server-with-rebar-4g-decoding/114076)
- [Offer: ASUS X99-A Series BIOS Mods with ReBAR – WinRaid](https://winraid.level1techs.com/t/offer-asus-x99-a-series-bios-mods-with-rebar-support/116496)
