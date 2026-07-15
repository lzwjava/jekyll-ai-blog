---
audio: false
generated: true
image: false
lang: en
layout: post
title: Threadripper Pro Motherboard Guide
translated: false
type: note
---

Question: What is a Threadripper Pro motherboard?

Answer:

AMD Ryzen Threadripper PRO platform is AMD's **workstation/server-class desktop platform**, positioned between normal Ryzen and EPYC.

A **Threadripper Pro motherboard** is a motherboard designed for CPUs like:

* Threadripper PRO 3000 WX series
* Threadripper PRO 5000 WX series
* Threadripper PRO 7000 WX series

Examples:

* ASUS Pro WS WRX80E-SAGE SE WIFI
* ASUS Pro WS WRX90E-SAGE SE
* Gigabyte WRX80 SU8-IPMI

![Image](https://images.openai.com/static-rsc-4/y1XJtejCAelzyjAMYQ4x7XJaf9NGt-l_YPEmoL0IY-HL2SfogWqKChOmZ1pkhRCaUw0g6fUm8rJkd3ZNzWcOV5DxuM4v3Dv5WsxIH9_MAoo-5idEdwh_qjKx4uzYt1l2qupWQbrYAUnNhVXkJI44MjO7fAcq5yQdilaV2CKehSzrdkfD-gbsRsJj5eUswzPo?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/vvVknn1dleu_xkBY8z34NjYaG6CpzNjeJSFH0VgiqmHAywQiqB1ixoDe-3-X-ni88pPe_AZmKlD0Wx6_x90WzEBTAmJLpqSR-k264qoRf5bt2LpBKDHJncB0VWt-vEyvAmIRlWjed2nodvMfPuvQi1STgCljU2YfsTnHCqsDjQDXnv1tyrNuKuny4ALrN4nu?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/kuxiKRdy2YfrZW0mETG49g7fGX6DTQVas8Acx9SFRykDTvP2SJg7R5oCMwmczJhkR83eNXjDDwn4EI8OqQHwXsIFfHMtueVH3A53xWtQhdgU25vCnya7hfpbNPho5rsc4ix5JbK3aEfWFEipuDxngrLFObfGa_wnDqN8ZQ7Euk935drD1Nd-QSwp8xqjG3z_?purpose=fullsize)

The key differences from normal Ryzen boards:

| Feature         | Ryzen AM5 board | Threadripper Pro board |
| --------------- | --------------- | ---------------------- |
| CPU socket      | AM5             | sWRX8 / sTR5           |
| CPU cores       | up to 16        | up to 96               |
| Memory          | DDR5 UDIMM      | DDR4/DDR5 RDIMM ECC    |
| Memory channels | 2               | 8                      |
| Max RAM         | ~192GB typical  | 1TB+                   |
| PCIe lanes      | ~28-32          | 128 PCIe lanes         |
| GPU support     | 1-3 GPUs        | 4-8 GPUs possible      |

Example:

A Threadripper PRO 7995WX:

* 96 Zen 4 cores
* 192 threads
* 8-channel DDR5 ECC RDIMM
* 128 PCIe 5.0 lanes

This is designed for:

* AI workstation
* 3D rendering
* CAD
* scientific computing
* multiple GPU setups

For AI specifically:

A Threadripper Pro machine can look like:

```
Threadripper PRO 7995WX
          |
          |
     WRX90 motherboard
          |
   +------+------+------+
   |      |      |      |
 RTX4090 RTX4090 RTX4090 RTX4090
```

Because you have many PCIe lanes, you can actually run multiple GPUs at full bandwidth.

Compared with your current type of build:

```
i9-13900KF
MSI B760
RTX 4070
```

you have:

* 8 PCIe lanes available after GPU/storage sharing
* dual-channel memory
* consumer platform

Threadripper Pro is a completely different class.

For LLM training/inference:

* 1× RTX 4090 → normal enthusiast
* 2-4× RTX 3090/4090 → Threadripper Pro starts making sense
* 4-8× GPUs → Threadripper Pro / EPYC territory

The downside:

* motherboard: often ¥5,000-10,000+
* CPU: ¥10,000-50,000+
* ECC RDIMM memory required
* huge power consumption

For a one-person AI lab (OPL), used Threadripper Pro 3955WX/3975WX + cheap RTX 3090s can actually be interesting because the PCIe lanes solve the multi-GPU bottleneck.
