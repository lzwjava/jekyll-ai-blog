---
audio: false
generated: true
image: false
lang: en
layout: post
title: Huanan X99 HD3 GPU ReBAR Check
translated: false
type: note
---

Question: Is the Huanan X99-HD3 V1.2 motherboard (with E5-2676 v3 CPU and DDR3 RAM) compatible with the NVIDIA M40 or P100 GPU? Does it support Resizable BAR?

---**Answer:**

Here's a breakdown covering both the GPU compatibility and the Resizable BAR question for this specific combo (Huanan X99-HD3 V1.2 + E5-2676 v3 + DDR3):

---

## ✅ M40 / P100 PCIe Compatibility

**Short answer: Both will physically seat in the PCIe x16 slot, but there are important caveats.**

**NVIDIA Tesla M40:**
The M40 uses a PCI Express 3.0 x16 interface and runs at 250W TDP. The critical issue: the M40 is configured to *require* an "Above 4G Decoding" BIOS option because it needs a very large PCIe memory address space. If your board doesn't expose this option, you'll get a "Device can't find enough free resources (Code 12)" error in Windows.

You need to go into BIOS, disable CSM, and enable "Above 4G Decoding" to get it working. The Huanan X99-HD3 is a Chinese X99 clone board; whether it has this BIOS option varies by firmware version — some do, some don't. You should confirm this in your BIOS before buying the M40.

Also note: the M40 uses a CPU 8-pin auxiliary power connector (not a standard PCIe 8-pin), so you'll need an adapter cable (NVIDIA P/N 030-0571-000: 2× PCIe 8-pin → 1× EPS 8-pin).

**NVIDIA Tesla P100 PCIe:**
The P100 PCIe is a dual-slot, ~10.5-inch card with a 250W TDP (down-clocked from the NVLink variant). It has the same "Above 4G Decoding" requirement as the M40. Additionally, the P100 is a passive-cooled data center card — it needs strong airflow (server-style case fans blowing directly over it) or it will thermal throttle severely. On a desktop board like the Huanan X99-HD3, this is a real concern.

Both cards work electrically on X99 + E5 v3, as the platform supports PCIe 3.0 x40 lanes. The E5-2600 v3 family supports up to 40 PCIe 3.0 lanes at 8.0 GT/s.

---

## ❌ Resizable BAR — Not Natively Supported

The Huanan X99-HD3 V1.2 does **not** natively support Resizable BAR. Here's why:

Resizable BAR (ReBAR) requires two things: the GPU must support it, and the motherboard BIOS must include the ReBar UEFI DXE driver and expose the option. Even if "Above 4G Decoding" is enabled and CSM is disabled on X99 clone boards like the JGINYUE X99I-SERVER, ReBAR still doesn't work because the BAR size is clamped somewhere in the BIOS/PciBus host bridge — it requires deeper BIOS modification.

There is a community workaround (ReBarUEFI by xCuri0): a DXE driver module that can be injected into the BIOS using UEFITool to enable Resizable BAR on unsupported systems, with the only prerequisite being that Above 4G Decoding is already enabled. Some users have successfully applied this to X99 boards, but it requires careful BIOS modification and results vary by board.

For the M40 and P100 specifically, ReBAR is also less relevant — these are compute/AI cards, not gaming GPUs, so the gaming-oriented BAR performance boost doesn't apply to them anyway.

---

## Summary Table

| Feature | M40 | P100 PCIe | X99-HD3 Support |
|---|---|---|---|
| PCIe Physical Fit | ✅ x16 slot | ✅ x16 slot | ✅ |
| Above 4G Decoding needed | ✅ Required | ✅ Required | ⚠️ Check BIOS |
| Power connector | EPS 8-pin (adapter needed) | EPS 8-pin (adapter needed) | ⚠️ Adapter needed |
| Passive cooling | ✅ (needs airflow!) | ✅ (needs airflow!) | ⚠️ Desktop case risk |
| Resizable BAR | N/A (compute card) | N/A (compute card) | ❌ Not native |

**Bottom line:** Check your specific Huanan X99-HD3 BIOS for the "Above 4G Decoding" option first — that's the gating factor. If it's there, both M40 and P100 can work, but plan for active airflow management and the proper power adapter cable.

---

**References:**
- [NVIDIA M40 Specs & Above 4G requirement](https://www.ebay.de/p/851104737)
- [ReBarUEFI project (xCuri0)](https://winraid.level1techs.com/t/release-resizable-bar-bios-efi-module/100235/1)
- [X99 + P40/P100 multi-GPU on consumer boards](https://winraid.level1techs.com/t/problem-ga-x99-ud3p-with-nvdia-tesla-p100-graphics/117195?page=2)
- [M40 power connector details](https://www.neweggbusiness.com/nvidia-tesla-m40/p/9B-1FT-0004-005S5)
