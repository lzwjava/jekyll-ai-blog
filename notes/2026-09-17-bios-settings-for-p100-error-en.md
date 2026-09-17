---
audio: false
generated: true
image: false
lang: en
layout: post
title: BIOS Settings for P100 Error
translated: false
type: note
---

Question: **I can't find CSM on the ASUS A68HM-E. Does that matter for the P100 PCI resource error?**

Answer: **No — stop looking for CSM for now.** I checked the A68HM-E documentation, and this is an old FM2+ BIOS. ASUS's current support page only exposes the 2014-era A68HM series manual for this board. ([ASUS Global][1])

More importantly, **CSM is not the setting I want you to chase for this problem**.

### What I want you to check instead

Go into BIOS and look under:

```text
Advanced
  ├─ North Bridge
  ├─ PCI Configuration
  ├─ PCI Express Configuration
  └─ Chipset Configuration
```

Search for anything named:

```text
Above 4G Decode
Above 4G Decoding
64-bit PCI
Memory Remap
MMIO
PCI MMIO
```

The important option is:

```text
Above 4G Decoding = Enabled
```

When supported, this allows 64-bit PCI devices to be mapped above the 4-GB address space. ASUS describes this function explicitly as decoding 64-bit PCI devices above the 4G address space. ([ASUS Download Center][2])

### If A68HM-E has NO "Above 4G Decoding"

Then that's a much more significant finding.

The P100 is asking the firmware for a **very large PCI BAR/MMIO region**, and an old FM2+ BIOS may simply be unable to allocate it. In that case:

```text
Gen1 ❌
Gen2 ❌
Gen3 ❌
Latency 32 ❌
Latency 64 ❌
Latency 128 ❌
```

aren't likely to fix the resource allocation failure.

### Do this now

Enter BIOS and **take a photo of the entire `Advanced` tab**.

Also take photos of:

```text
Advanced → North Bridge
Advanced → PCI*
Advanced → Chipset*
Boot
```

Don't change anything else yet.

I'll look at the actual A68HM-E BIOS options and tell you whether there's a way to make the P100's BAR allocation work, or whether we're hitting a **motherboard firmware limitation**.

[ASUS A68HM-E support/manual page](https://www.asus.com/us/supportonly/a68hm-e/helpdesk_manual/?utm_source=chatgpt.com) 

[1]: https://www.asus.com/us/supportonly/a68hm-e/helpdesk_manual/?utm_source=chatgpt.com "A68HM-E - Support"
[2]: https://dlcdnet.asus.com/pub/ASUS/mb/LGA1151/MAXIMUS_VIII_HERO/E10343_MAXIMUS_VIII_HERO_UM_WEB.pdf?utm_source=chatgpt.com "Above 4G Decoding [Disabled]"
