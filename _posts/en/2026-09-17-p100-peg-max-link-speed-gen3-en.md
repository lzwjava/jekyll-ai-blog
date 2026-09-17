---
audio: false
generated: true
image: false
lang: en
layout: post
title: P100 PEG Max Link Speed Gen3
translated: false
type: note
---

Question: For an NVIDIA Tesla P100 on an ASUS A68HM-E, what should I set for **PEG Max Link Speed** and **PCI Latency Timer**?

Answer:

For your **Tesla P100 PCIe + ASUS A68HM-E**, I would use:

| BIOS option            | Setting                                                          |
| ---------------------- | ---------------------------------------------------------------- |
| **PEG Max Link Speed** | **Gen3**                                                         |
| **PCI Latency Timer**  | **64 PCI Bus Clocks**                                            |
| PCIe Link Width        | **Auto / x16**                                                   |
| Above 4G Decoding      | **Enabled** if available                                         |
| CSM                    | Prefer **Disabled** if your OS/GPU boot setup supports pure UEFI |

The important one is **PEG Max Link Speed = Gen3**. The P100 PCIe is a **PCIe 3.0 ×16** GPU, so Gen3 is its native interface. NVIDIA specifies PCIe Gen3 ×16 and up to 32 GB/s bidirectional PCIe bandwidth. ([NVIDIA][1])

### PCI Latency Timer

Set **64**.

But this setting is much less important on a modern PCIe GPU than the link-generation setting. The PCI Latency Timer is primarily a legacy PCI bus arbitration parameter; it does **not** mean "GPU latency = 64 cycles." You shouldn't expect 32 vs 64 to produce a meaningful CUDA performance difference.

If your BIOS gives:

```text
PCI Latency Timer
    32 PCI Bus Clocks
    64 PCI Bus Clocks
    96 PCI Bus Clocks
    128 PCI Bus Clocks
```

I'd simply use:

```text
64 PCI Bus Clocks
```

### One important issue with the A68HM-E

The ASUS A68HM-E is an old AMD A68H/FM2+ platform, and ASUS provides its manual/support documentation from that generation. ([ASUS Global][2])

So if your P100 is currently showing something like:

```text
PCIe x16  @ x8 1.1
```

or

```text
PCIe x16  @ x16 2.0
```

**don't immediately blame PCI Latency Timer.** We should first determine what the motherboard/CPU is actually negotiating.

After booting Linux, run:

```bash
lspci -vv -s $(lspci | awk '/NVIDIA/{print $1; exit}')
```

and:

```bash
nvidia-smi -q | grep -i -A5 "PCI"
```

For the P100, the ideal result is approximately:

```text
LnkCap: Speed 8GT/s, Width x16
LnkSta: Speed 8GT/s, Width x16
```

`8 GT/s` corresponds to **PCIe Gen3**.

So my BIOS starting point is simply:

```text
PEG Max Link Speed  -> Gen3
PCI Latency Timer   -> 64
```

[ASUS A68HM-E support/manuals](https://www.asus.com/us/supportonly/a68hm-e/helpdesk_manual/?utm_source=chatgpt.com)
[NVIDIA Tesla P100 PCIe specifications](https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com) 

If you paste your **full BIOS Advanced → PCI/PCIe settings screen** (a photo is fine), I can map each setting specifically for the P100.

[1]: https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com "SPECIFICATIONS"
[2]: https://www.asus.com/us/supportonly/a68hm-e/helpdesk_manual/?utm_source=chatgpt.com "A68HM-E - Support"
