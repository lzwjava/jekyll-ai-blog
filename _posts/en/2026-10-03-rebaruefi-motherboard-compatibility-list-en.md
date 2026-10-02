---
audio: false
generated: true
image: false
lang: en
layout: post
title: ReBarUEFI Motherboard Compatibility List
translated: false
type: note
---

Question: Where in `xCuri0/ReBarUEFI` can I find which motherboards have 4G Decoding / CSM / related BIOS cases?

Answer:

The main page you want is the **Wiki → List of tested motherboards**:

[xCuri0/ReBarUEFI Wiki - List of tested motherboards](https://github.com/xCuri0/ReBarUEFI/wiki?utm_source=chatgpt.com)

Inside that table, look at:

* **Motherboard**
* **UEFIPatch req (Y/N)**
* **Notes**
* GPU tested
* BAR size achieved

Examples:

```
Motherboard                  UEFIPatch   Notes
---------------------------------------------------------
ASUS Z170-A                  Y           ...
Huananzhi X99-QD4            N           ...
MSI B150M PRO-VDH            N           ...
ASUS Z170-P                  Y           RTX3090 32GB BAR
```

The table itself does **not always directly say "has 4G Decoding option"**, because many boards hide it. The related page is:

[xCuri0/ReBarUEFI - Enabling hidden 4G decoding](https://github.com/xCuri0/ReBarUEFI/wiki/Enabling-hidden-4G-decoding?utm_source=chatgpt.com)

That page explains how to find hidden BIOS variables:

Search BIOS with UEFITool:

```
4G Decod
Above 4G
MMIO
64-Bit Resource Allocation
```

If found, you can enable it with `setup_var`. ([GitHub][1])

For CSM:

Usually the rule is:

```
4G Decoding = Enabled
CSM = Disabled
UEFI boot only
```

ReBarUEFI README explicitly says after installing the modified firmware:

```
make sure that 4G decoding is enabled and CSM is off
```

([GitHub][2])

For your cases:

### Z170 / B150 / X99

Good candidates:

* ASUS Z170-A
* ASUS Z170-P
* MSI Z170A series
* Huananzhi X99-QD4
* Huananzhi X99-TF
* ASUS X99 series

They already have successful reports. ([GitHub][3])

### When buying used motherboard

Check these pages:

1. Google:

```
<motherboard model> "Above 4G Decoding"
```

2. Search BIOS manual:

```
<model> manual pdf "Above 4G"
<model> manual pdf "CSM"
<model> manual pdf "PCI Subsystem Settings"
```

3. Search ReBarUEFI issue list:

```
site:github.com/xCuri0/ReBarUEFI <motherboard model>
```

For your P100 / M40 / RTX 3090 experiments, the important BIOS items are:

```
Advanced
 └─ PCI Subsystem Settings
      ├─ Above 4G Decoding
      ├─ Re-Size BAR Support
      ├─ MMIO High Base
      ├─ MMIO High Size

Boot
 └─ CSM
      └─ Disabled
```

For older platforms (X79/X99/Z77/Z97), **MMIO space is often more important than the visible 4G option**, especially with 24GB+ VRAM GPUs. ReBarUEFI notes that HEDT/server boards may need `MMIOH Size` / `MMIO High Granularity Size` adjustment for large VRAM GPUs. ([GitHub][4])

References:

* [xCuri0/ReBarUEFI GitHub](https://github.com/xCuri0/ReBarUEFI?utm_source=chatgpt.com)
* [ReBarUEFI Wiki - Common issues](https://github.com/xCuri0/ReBarUEFI/wiki/Common-issues-%28and-fixes%29?utm_source=chatgpt.com)

[1]: https://github.com/xCuri0/ReBarUEFI/wiki/Enabling-hidden-4G-decoding?utm_source=chatgpt.com "Enabling hidden 4G decoding · xCuri0/ReBarUEFI Wiki · GitHub"
[2]: https://github.com/xCuri0/ReBarUEFI/blob/master/README.md?plain=1&utm_source=chatgpt.com "ReBarUEFI/README.md at master · xCuri0/ReBarUEFI · GitHub"
[3]: https://github.com/xCuri0/ReBarUEFI/wiki?utm_source=chatgpt.com "Home · xCuri0/ReBarUEFI Wiki · GitHub"
[4]: https://github.com/xCuri0/ReBarUEFI/wiki/Common-issues-%28and-fixes%29?utm_source=chatgpt.com "Common issues (and fixes) · xCuri0/ReBarUEFI Wiki · GitHub"
