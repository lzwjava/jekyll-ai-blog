---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI Z170A Gaming M5 CSM Configuration
translated: false
type: note
---

Question: How do I configure CSM on the **MSI Z170A Gaming M5**?

Answer: On this board, MSI exposes CSM through **Windows OS Configuration**, rather than necessarily showing a menu literally named “CSM.”

### To enable CSM

Enter BIOS with `Delete`:

```text
Settings
  → Advanced
    → Windows OS Configuration
      → Windows 10 WHQL Support
```

Set:

```text
Windows 10 WHQL Support = Disabled
```

MSI specifically documents this path for the **Z170A Gaming M5**. Disabling WHQL support makes the legacy/CSM configuration available. ([MSI USA][1])

Then check:

```text
Settings
  → Boot
    → Boot Mode Select
```

You should be able to select a legacy/UEFI-compatible mode rather than being locked to UEFI. ([MSI USA][2])

### For your M40 experiment

I'd actually test **both modes**, because the M40 is an older GPU:

**Test A — CSM enabled**

```text
Windows 10 WHQL Support = Disabled
Boot Mode               = Legacy + UEFI / CSM
Above 4G Decoding       = Enabled   ← if available
PCI_E1                  = M40
PCIe speed              = Gen2
```

Then test:

**Test B — pure UEFI**

```text
Windows 10 WHQL Support = Enabled / UEFI
CSM                     = Disabled
Above 4G Decoding       = Enabled
PCI_E1                  = M40
PCIe speed              = Gen2
```

One important correction to my previous answer: **on this generation of MSI BIOS, don't look for a standalone “CSM Support” switch first.** The relevant control is **Windows 10 WHQL Support / CSM-UEFI mode**. MSI's own documentation describes this as the CSM/UEFI setting. ([MSI USA][3])

Your **Z170A Gaming M5 BIOS version also matters**. MSI's current support page lists BIOS **7977v1I** for this board. ([au.msi.com][4])

[1]: https://us.msi.com/faq/2622?utm_source=chatgpt.com "MSI USA | MSI USA"
[2]: https://us.msi.com/faq/2803?utm_source=chatgpt.com "MSI USA | MSI USA"
[3]: https://us.msi.com/support/technical_details/DT_BIOS_Manual?utm_source=chatgpt.com "BIOS Manual"
[4]: https://au.msi.com/Motherboard/Z170A-GAMING-M5/support?utm_source=chatgpt.com "MSI Australia | MSI Australia"