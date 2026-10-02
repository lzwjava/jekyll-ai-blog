---
audio: false
generated: true
image: false
lang: en
layout: post
title: MSI Z170A SLI PLUS Overview
translated: false
type: note
---

Question: Intro to MSI Z170A SLI PLUS motherboard and its value/use case.

Answer:

![Image](https://images.openai.com/static-rsc-4/MGmn127nOzgR5bXTXPQ3aYlKjNyNOsnnG-YAo3Bk0LRL2Ido1fITcRkZd72Gbja49UylnaFNhoyc3EJoW__qswSWpCOICkMwSlSyaA8KTbShswXnlZi7TP1JTYDCxNaZBo1Bx1B42fzBkJ41FKqx2x50fWg8S4YgkgkBgFhPGuNBQgOXjKTKa-6_n7hMViVw?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/5FRwiqxCiOzkUfImK2e2jQOzVknhSlGnL399EXnZaYwVHBjcyTCEf-wpf0Cf-28lUZt-7X03Spsgdagtefx2_DvGEY1fg6wo1-zresgGI44xP217HcFHtP9lhOCryM2eBteplzJVTWZwo1qvqfkAUZ0rxAcvEK1xUhlAalKvdFphS7fq6yymf4jjYetM5udD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/GdbWew01yabxeEr-pS-1-QSUXzJQeMs2SXZJaddYBiiEZYpZTrC4a7hf01LpxjBMRgHKK78FjC-vpWPNoNOUgawjr6OKVuzp7OMteLQXlt8DmZ30f2lfgNEoEBXghNSe8YfPSIUOkpb_pc4XHhXrVZ7ZAnB2yVDBs41f3_PCjWhUHSDRTabM39_sOpctO31_?purpose=fullsize)

The **MSI Z170A SLI PLUS** is a mid-range enthusiast motherboard from the **Intel Z170 chipset generation (2015)**. It targets Intel **6th generation Skylake CPUs** and some **7th generation Kaby Lake CPUs after BIOS update**.

## Main specifications

| Feature     | Details                                                                 |
| ----------- | ----------------------------------------------------------------------- |
| Socket      | LGA1151                                                                 |
| CPU support | Intel 6th Gen Core (Skylake), 7th Gen Core (Kaby Lake with BIOS update) |
| Chipset     | Intel Z170                                                              |
| Memory      | 4 × DDR4 DIMM slots                                                     |
| Max memory  | Up to 64GB DDR4 (commonly 2133MHz native, higher with XMP)              |
| GPU slots   | 3 × PCIe x16 physical slots                                             |
| Multi-GPU   | NVIDIA SLI / AMD CrossFire support                                      |
| Storage     | M.2 PCIe 3.0 x4 NVMe support + SATA ports                               |
| Network     | Gigabit Ethernet                                                        |
| Audio       | 7.1-channel audio                                                       |
| Form factor | ATX                                                                     |

## CPU options

Good matches:

* Intel Core i7-6700K

  * 4 cores / 8 threads
  * unlocked multiplier
  * classic Z170 pairing

* Intel Core i7-6700

  * 4 cores / 8 threads
  * lower power, stable

* Intel Core i5-6600K

  * 4 cores / 4 threads
  * overclocking capable

* Intel Core i7-7700K

  * fastest mainstream CPU option for this platform

For modern AI workloads, this platform is very old. It is mainly interesting for:

* GPU repair test bench
* PCIe experiments
* cheap NAS/server
* retro gaming
* learning BIOS/PCIe behavior

## PCIe layout

This board is interesting because it has multiple PCIe slots:

```
CPU PCIe lanes:
        CPU
         |
      PCIe x16 slot 1
         |
      GPU

Chipset PCIe lanes:
      PCIe x16 slot 2 (x4 electrically)
      PCIe x16 slot 3 (x4 electrically)
      M.2 slot
      SATA
```

Important:

* Only the first GPU slot gets full CPU x16 bandwidth.
* The other long slots are physically x16 but electrically x4.
* For GPU compute, one RTX 3090/4090 should go in the first slot.
* Multiple older GPUs (P100/M40/Quadro etc.) can work but bandwidth is limited.

## BIOS features relevant to your GPU experiments

Because you have been testing P100/M40/ReBarUEFI-style PCIe issues, this board is actually a good platform.

Look for:

### CSM

```
BIOS
 → Settings
   → Advanced
     → Windows OS Configuration
       → CSM
```

Options:

* Enabled = legacy GPU ROM compatibility
* Disabled = pure UEFI

For old Tesla GPUs:

* CSM Enabled sometimes helps.
* Some modern ReBarUEFI setups require CSM disabled.

### Above 4G Decoding

Usually:

```
BIOS
 → Settings
 → Advanced
 → PCI Subsystem Settings
 → Above 4G Memory/Crypto Currency Mining
```

Enable for:

* multiple GPUs
* 24GB Tesla M40
* ReBAR experiments

### PCIe speed

For unstable old GPUs:

```
PCIe Link Speed
Auto → Gen2
```

Older Tesla cards often behave better at Gen2.

## Compared with newer cheap platforms

For GPU lab:

| Platform            | Advantage                             |
| ------------------- | ------------------------------------- |
| Z170 + i7-6700      | Cheap, DDR4, good BIOS                |
| X99 + Xeon E5 v3/v4 | More PCIe lanes, better for many GPUs |
| B450/B550           | Modern CPU, PCIe 4.0                  |
| Z690/Z790           | Expensive but modern                  |

For your use case (GPU repair + LLM experiments), Z170A SLI PLUS is mainly valuable because:

* cheap used price (~200–300 CNY range usually)
* DDR4 availability
* multiple PCIe slots
* good MSI BIOS
* supports NVMe

But it is not a good AI training machine because:

* CPU only 4 cores
* PCIe 3.0
* limited PCIe lanes
* no ECC support

A good cheap build would be:

```
MSI Z170A SLI PLUS
+ i7-6700 / i7-6700K
+ 32GB DDR4
+ RTX 3060 / Tesla P100 / M40 test GPU
+ Linux
```

This would make a decent GPU diagnostic bench.

I can also help you compare this Z170A SLI PLUS against the X99 boards you were considering for M40/P100 testing.
