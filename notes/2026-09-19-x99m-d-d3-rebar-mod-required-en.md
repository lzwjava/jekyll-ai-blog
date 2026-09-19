---
audio: false
generated: true
image: false
lang: en
layout: post
title: "X99M-D D3 ReBAR: Mod Required"
translated: false
type: note
---

**Question:** Does the 精粤 X99M-D D3 V1.2 motherboard support Resizable BAR and Above 4G Decoding?

**Answer:**

No specific documentation exists for this exact model, but here's the complete picture based on what's known about this class of board.

---

**The short answer: Not natively, but partially achievable via BIOS mod.**

---

**What this board is**

The 精粤 (Jingyu) X99M-D D3 V1.2 is a budget Chinese micro-ATX board built on the Intel X99/C612 chipset (LGA2011-3), targeting Xeon E5 v3/v4 use. The "D3" in the name means DDR3 memory. Boards in this category share a common BIOS foundation (AMI Aptio-based) with other Chinese X99 boards like JGINYUE, Huananzhi, and Machinist. None of them include native ReBAR or Above 4G Decoding options in their stock BIOS menus.

---

**What's achievable:**

| Feature | Native support | Workaround possible? |
| --- | --- | --- |
| Above 4G Decoding | ❌ No visible option | ⚠️ Maybe — hidden BIOS variable |
| Resizable BAR | ❌ No | ⚠️ Partial via BIOS mod |

**Path 1 — Above 4G Decoding (hidden variable method)**

Many Chinese X99 boards have the Above 4G Decoding option present in the BIOS firmware but hidden from the UI. You can use `setup_var` in a GRUB EFI shell to directly write to the BIOS variable offset — for example, `setup_var 0x93 0x1` — after first identifying the correct offset by extracting your board's IFR (Internal Form Representation). The offset differs per board version, so you'd need to dump your own BIOS and inspect it with AMIBCP or UEFITool to find the right one.

**Path 2 — Resizable BAR via ReBarDxe injection**

The ReBarUEFI project provides a DXE driver that can be injected into the BIOS using UEFITool to enable Resizable BAR on supported systems, with the requirement that 4G Decoding be enabled first.

If your board does not have Above 4G Decoding enabled, the maximum ReBAR size you can set is 1 GB — setting it higher will prevent the system from booting. Still, even 1 GB ReBAR provides some GPU performance improvement over the default 256 MB window.

**Path 3 — CSM conflict risk**

A known issue on similar Chinese X99-M D4/D3 boards is that only CSM/Legacy mode works for display output, meaning UEFI-only mode shows no display — making it impossible to disable CSM, which is a prerequisite for enabling ReBAR. Your V1.2 board may or may not have this issue depending on your GPU's UEFI GOP support.

---

**Practical recommendation**

Before attempting any BIOS mod:

1. Check if your GPU has a UEFI GOP ROM (required for disabling CSM)
2. Get a **CH341A programmer** as a recovery backup in case of a failed flash
3. Dump your current BIOS and open it in **AMIBCP** to check whether the Above 4G Decoding string exists
4. If it exists, use the hidden variable method; if it doesn't, you're limited to ≤1 GB ReBAR only

---

**References:**

- [榨干矿卡：老主板修改BIOS开启ReBAR – Bilibili](https://www.bilibili.com/opus/743982326937026580)
- [JGINYUE X99-M D4 BIOS & ReBAR discussion – WinRaid](https://winraid.level1techs.com/t/guide-overclock-bios-mods-for-chinese-x99-mbs/104683/68)
- [xCuri0/ReBarUEFI – GitHub](https://github.com/xCuri0/ReBarUEFI)
- [ReBarUEFI Release Thread – WinRaid Level1Techs](https://winraid.level1techs.com/t/release-resizable-bar-bios-efi-module/100235)
