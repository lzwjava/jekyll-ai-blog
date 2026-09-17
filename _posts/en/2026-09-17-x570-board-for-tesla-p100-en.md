---
audio: false
generated: true
image: false
lang: en
layout: post
title: X570 Board for Tesla P100
translated: false
type: note
---

Question: **Which motherboard should I buy for a Tesla P100 PCIe?**

Answer: **I’d move away from the A68HM-E and buy an X570 board.** The important requirement is not PCIe Gen4 itself; it is **proper 64-bit PCI resource allocation / Above 4G Decoding**. NVIDIA lists the P100 PCIe as a Gen3 x16, 250 W card, and its compute-mode BAR1 is **16 GB**, which explains the resource exhaustion on the old board. ([NVIDIA][1])

### My pick: ASUS TUF Gaming X570-PLUS

### [ASUS TUF GAMING X570-Plus](https://www.newegg.com/asus-tuf-gaming-x570-plus-atx-amd-motherboard-amd-x570-am4/p/N82E16813119198?item=9SIC70UKZU0650&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$197.38*

I'd choose this if you're happy moving to **AM4**.

Why:

* X570 + modern AM4 firmware
* Full-length PCIe x16 slot for the P100
* Much newer PCIe resource allocation than the A68 platform
* ASUS still provides BIOS updates for this board; the support page currently lists BIOS 5044 from February 2026. ([ASUS Global][2])
* ASUS provides the X570 BIOS manual/support documentation. ([ASUS Global][3])
* Good availability on the used market

For the P100, I'd configure:

```text
BIOS
├── Above 4G Decoding = Enabled
├── CSM                = Disabled
├── Re-Size BAR        = Disabled initially
└── PCIe x16           = Auto / Gen3
```

**Don't enable Re-Size BAR initially.** First get the P100 working with plain Above 4G decoding.

NVIDIA itself recommends Above 4G Decoding for devices/features requiring large PCIe resources. ([NVIDIA Networking][4])

### Cheaper option

### [ASRock X570 PRO4](https://www.newegg.com/asrock-x570-pro4-atx-amd-motherboard-amd-x570-am4/p/N82E16813157886?item=9SIC6E1M4H8976&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$147.14*

The **ASRock X570 Pro4** is another reasonable target if you find it substantially cheaper used.

ASRock's own BIOS documentation explicitly shows:

```text
BIOS
  → Advanced
    → Chipset Configuration
      → Above 4G Decoding = Enabled
```

so this is exactly the firmware capability we're looking for. ([ASRock][5])

### I would NOT buy another old A68/FM2+ board

Your current topology is basically:

```text
A68HM-E
   │
   └── old AMD platform
          │
          └── PCIe
                │
                └── P100
                     └── BAR1 = 16 GB
```

The P100 is asking the firmware for a huge MMIO aperture:

```text
BAR0    16 MB
BAR1    16 GB    ← the big one
BAR3    32 MB
```

in compute mode. ([NVIDIA][1])

That's why I'd spend the money on the motherboard rather than trying to hack around the A68 BIOS.

### One more important point

The P100 is **250 W and passively cooled**. A desktop motherboard can electrically run it, but your case needs strong airflow directly through the P100 heatsink. NVIDIA specifies the PCIe P100 as a passive, full-height/dual-slot card requiring system airflow. ([NVIDIA][6])

So my target build would be:

```text
ASUS TUF X570-PLUS
        │
        ├── Ryzen 5 3600 / 5600
        ├── 32–64 GB DDR4
        ├── Tesla P100 12/16 GB
        ├── NVMe
        └── 650–750 W PSU
```

**If you tell me your budget ($50 / $100 / $150 / $200) and whether you want to keep your current AMD CPU/RAM, I can narrow it down to a specific motherboard + CPU combination.**

References:

* [NVIDIA Tesla P100 PCIe specifications](https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com)
* [ASUS TUF Gaming X570-PLUS support/BIOS](https://www.asus.com/us/supportonly/tuf%20gaming%20x570-plus/helpdesk_bios/?utm_source=chatgpt.com)
* [ASRock Above 4G Decoding documentation](https://www.asrock.com/support/faq.asp?k=bios&utm_source=chatgpt.com)

[1]: https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com "Specifications"
[2]: https://www.asus.com/us/supportonly/tuf%20gaming%20x570-plus/helpdesk_bios/?utm_source=chatgpt.com "TUF GAMING X570-PLUS - Support"
[3]: https://www.asus.com/us/supportonly/tuf%20gaming%20x570-plus/helpdesk_manual/?utm_source=chatgpt.com "TUF GAMING X570-PLUS - Support"
[4]: https://networking-docs.nvidia.com/doca/archive/2-5-5/features-overview-and-configuration?utm_source=chatgpt.com "Features Overview and Configuration | DOCA"
[5]: https://www.asrock.com/support/faq.asp?k=bios&utm_source=chatgpt.com "ASRock > FAQ"
[6]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-p100/pdf/nvidia-tesla-p100-PCIe-datasheet.pdf?utm_source=chatgpt.com "Data Sheet: Tesla P100"
