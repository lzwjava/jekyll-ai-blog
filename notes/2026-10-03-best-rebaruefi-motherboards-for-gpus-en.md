---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best ReBarUEFI Motherboards for GPUs
translated: false
type: note
---

Question: Which motherboards from ReBarUEFI are good choices for 4G Decoding + CSM configuration?

Answer:

For your use case (AI GPU lab, RTX 3090/4090/P100/M40 experiments, large VRAM BAR, multi-GPU), I would prioritize boards that:

1. Have **UEFI BIOS**
2. Expose **Above 4G Decoding**
3. Can disable **CSM**
4. Have enough PCIe resources
5. Have known ReBarUEFI success cases

ReBarUEFI requires (or strongly benefits from) **4G Decoding enabled and CSM disabled**. Without 4G Decoding, BAR size is limited. ([GitHub][1])

From the tested list, these are the ones I would consider:

| Motherboard                    | Platform         | ReBarUEFI result                 | My opinion                |
| ------------------------------ | ---------------- | -------------------------------- | ------------------------- |
| **ASUS Z170-A**                | Z170 / i7-6700   | RTX 3080/3090, 8-16GB BAR tested | ⭐⭐⭐⭐⭐ Best cheap choice   |
| **ASUS Z170-P**                | Z170 / 6th gen   | RTX 3090 32GB BAR tested         | ⭐⭐⭐⭐⭐ Very good           |
| **ASUS Z170-WS**               | Z170 workstation | Arc A770 16GB                    | ⭐⭐⭐⭐⭐ Best Z170           |
| **MSI Z170-A PRO**             | Z170             | RX 6650 XT                       | ⭐⭐⭐⭐ Good                 |
| **MSI Z170 KRAIT GAMING**      | Z170             | RX 6900 XT                       | ⭐⭐⭐⭐ Good                 |
| **ASUS Z270-A Prime**          | Z270             | RTX 3060 Ti                      | ⭐⭐⭐⭐⭐ Better BIOS         |
| **MSI Z270 GAMING M5**         | Z270             | RTX 3080 Ti                      | ⭐⭐⭐⭐ Good                 |
| **ASUS X99-A / X99-DELUXE II** | X99              | RTX 3090/A6000 16-24GB           | ⭐⭐⭐⭐⭐ Best multi-GPU      |
| **Huananzhi X99-QD4**          | X99              | RTX 3060 16GB                    | ⭐⭐⭐⭐ Cheap Chinese option |

([GitHub][2])

For your previous Z170 search, I would rank:

### 1. ASUS Z170-A

Probably the sweet spot.

Why:

* Cheap on Xianyu
* Intel 6th gen support
* DDR4
* M.2
* Good ASUS BIOS
* Known ReBarUEFI success
* Has Above 4G Decoding options

A typical setup:

```
ASUS Z170-A
+
i7-6700 / i7-6700K
+
32GB DDR4
+
RTX 3090 24GB
```

can potentially expose a large BAR after BIOS modification. ([GitHub][2])

### 2. ASUS Z170-P

Also excellent.

The ReBarUEFI list specifically has:

```
ASUS Z170-P
RTX 3090
32GB BAR
```

which is very relevant to your GPU experiments. ([GitHub][2])

The downside:

* fewer PCIe slots
* less workstation-like

### 3. X99 boards

For your AI GPU direction, X99 is actually more interesting.

Example:

```
X99
+
E5-2680 v4
+
64GB DDR4 ECC
+
Tesla / RTX cards
```

The ReBarUEFI list has X99 boards working with RTX 3090, RTX A6000, etc. ([GitHub][2])

Advantages:

* More PCIe lanes
* ECC memory
* cheap Xeons

Disadvantages:

* BIOS quality varies
* Chinese boards need more tweaking

Avoid:

### Old Z97 / Haswell unless cheap

Many Haswell systems lack 4G Decoding options, making large BAR harder. ([GitHub][3])

### ASRock Z170 K4/D3

Known issue:

* SATA controller problems when 4G Decoding enabled. ([GitHub][3])

For your current goal (repair + AI GPU lab), my buying order would be:

```
1. ASUS Z170-A        ~250-350 CNY
2. ASUS Z170-P        ~250-300 CNY
3. ASUS Z170-WS       if cheap
4. X99 + E5 v4        for multi GPU
5. MSI Z170/Z270      if very cheap
```

Also when checking Xianyu listings, search BIOS screenshots for:

```
Above 4G Decoding
CSM Support
Launch CSM
PCI Subsystem Settings
```

ASUS BIOS is usually easier than MSI for this kind of BIOS mod work.

I can also make you a **Xianyu motherboard shortlist specifically for RTX 3090/M40/P100 multi-GPU AI lab builds under 500 CNY**.

[1]: https://github.com/xCuri0/ReBarUEFI?utm_source=chatgpt.com "GitHub - xCuri0/ReBarUEFI: Resizable BAR for (almost) any UEFI system · GitHub"
[2]: https://github.com/xCuri0/ReBarUEFI/wiki?utm_source=chatgpt.com "Home · xCuri0/ReBarUEFI Wiki · GitHub"
[3]: https://github.com/xCuri0/ReBarUEFI/wiki/Common-issues-%28and-fixes%29?utm_source=chatgpt.com "Common issues (and fixes) · xCuri0/ReBarUEFI Wiki · GitHub"
