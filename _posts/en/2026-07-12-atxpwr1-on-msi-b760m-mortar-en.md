---
audio: false
generated: true
image: false
lang: en
layout: post
title: ATX_PWR1 on MSI B760M Mortar
translated: false
type: note
---

**Question: What is ATX_PWR1 on MSI MAG B760M Mortar WiFi motherboard?**

**Answer:**

`ATX_PWR1` is the **main 24-pin motherboard power connector** from your PSU (power supply). It provides power to the motherboard itself. ([MSI][1])

Physical appearance:

```
PSU 24-pin ATX cable
        |
        v

+----------------+
| ATX_PWR1       |
| [24 pins]      |
+----------------+

Motherboard
```

Your PSU will have a cable usually labeled:

```
ATX 24P
MB
MAIN
```

Plug that into `ATX_PWR1`.

It supplies:

* +3.3V → chipset, memory logic, PCIe devices
* +5V → USB, controllers, storage
* +12V → motherboard power rails
* standby power (5VSB) → allows motherboard wake features

The MSI MAG B760M Mortar WiFi has:

* `ATX_PWR1` = 24-pin motherboard power
* `CPU_PWR1` + `CPU_PWR2` = 8-pin CPU EPS power connectors ([MSI Download][2])

The layout is roughly:

```
Top of motherboard

[ CPU socket ]

[ CPU_PWR1 ][ CPU_PWR2 ]
      8-pin     8-pin


Middle:

[ PCIe GPU slot ]


Right edge:

[ ATX_PWR1 ]
[ 24-pin ]
```

For your build:

* RTX 4070 / MI50 GPU → powered separately from PSU
* CPU → CPU_PWR1 (and CPU_PWR2 if high power CPU)
* Motherboard → ATX_PWR1

For normal CPUs like i5-12400 / i5-13600 / i7 at stock:

* connect **ATX_PWR1**
* connect **CPU_PWR1**
* CPU_PWR2 is usually optional unless heavy load/high-end CPU. MSI designed this board with dual 8-pin CPU connectors for higher power CPUs. ([MSI][3])

So basically:

```
PSU
 |
 +-- 24 pin ATX  ----------> ATX_PWR1
 |
 +-- 8 pin EPS CPU --------> CPU_PWR1
 |
 +-- another 8 pin EPS ----> CPU_PWR2 (optional)
 |
 +-- PCIe power -----------> GPU
```

For your MI50 AI workstation build, the important thing is: **make sure your PSU has enough PCIe/EPS connectors and wattage. The ATX_PWR1 itself is standard and every ATX PSU has it.**

[1]: https://www.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/Specification?utm_source=chatgpt.com "MAG B760M MORTAR WIFI"
[2]: https://download-2.msi.com/archive/mnu_exe/mb/B760MMORTAR_WIFI_MAXWIFI.pdf?utm_source=chatgpt.com "MAG B760M MORTAR MAX WIFI"
[3]: https://us.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/Overview?utm_source=chatgpt.com "MAG B760M MORTAR WIFI"
