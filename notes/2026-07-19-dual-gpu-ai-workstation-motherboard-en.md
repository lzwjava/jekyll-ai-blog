---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dual GPU AI Workstation Motherboard
translated: false
type: note
---

Question: You have an i9-13900KF + RTX 4070 + DDR5 64GB build and want to add a second RTX 3060. Which motherboard should you choose?

Answer:

Your main requirement changes the motherboard choice:

**You are not just building a gaming PC anymore. You are building a small AI workstation.**

The important thing is **PCIe slot layout**, not CPU compatibility.

Your i9-13900KF has:

* 16 PCIe 5.0 lanes from CPU

  * usually used by first GPU: PCIe x16
* Z790 chipset provides extra PCIe lanes

  * second GPU usually comes from chipset: PCIe x4

For AI workloads (PyTorch, CUDA), a second RTX 3060 running at **PCIe 4.0 x4** is usually OK. The GPU is mostly limited by VRAM and compute, not PCIe bandwidth.

A typical layout:

```
CPU
 |
 +-- RTX 4070
 |      PCIe 5.0 x16
 |
Z790 chipset
 |
 +-- RTX 3060
        PCIe 4.0 x4
```

The second card is not for SLI/NVLink. It is for:

* extra VRAM
* running another model
* separate CUDA process
* distributed training experiments

---

## My recommendation: ATX Z790 board

Do NOT buy mATX.

Your case is "Mini" but if you want dual GPU, you need physical space and airflow.

Good choices:

### 1. MSI MAG Z790 Tomahawk WiFi DDR5 (my first choice)

### [MSI MAG Z790 TOMAHAWK WIFI DDR5 ATX Motherboard](https://www.newegg.com/msi-mag-z790-tomahawk-wifi-atx-motherboard-intel-z790-lga-1700/p/N82E16813144567?item=N82E16813144567&negg_topt=22&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$209.99*

Why:

* i9-13900KF power delivery is handled easily
* 4 DIMM DDR5 slots
* two usable PCIe GPU slots
* good VRM cooling
* many M.2 slots
* good BIOS

Expansion:

```
PCIe 5.0 x16  -> RTX 4070

PCIe 4.0 x4   -> RTX 3060

PCIe 4.0 x4 M.2
PCIe 4.0 x4 M.2
...
```

MSI lists the board as Z790/LGA1700 supporting 12th/13th/14th gen Intel CPUs with strong VRM design. ([MSI-US Official Store][1])

---

### 2. ASUS TUF Gaming Z790-PLUS WIFI

### [ASUS TUF GAMING Z790-PLUS WIFI](https://www.bestbuy.com/product/asus-tuf-gaming-z790-plus-wifi-socket-lga-1700-intel-z790-atx-ddr5-wi-fi-6e-motherboard-black/JJGGL6ZF32/sku/11121666?fs=tic1l0&utm_medium=feed&utm_source=chatgpt.com)

*$268.40*

Also very good.

Expansion:

```
PCIe 5.0 x16

PCIe 4.0 x16 slot
   (electrically x4)

PCIe 4.0 x4
```

ASUS specifies:

* 1× PCIe 5.0 x16
* 1× PCIe 4.0 x16 (max x4)
* 1× PCIe 4.0 x4

which is exactly the configuration needed for two GPUs. ([ASUS Global][2])

---

## Your PSU problem

Your current:

```
Corsair CX650F RGB 750W
```

is borderline.

Power:

```
i9-13900KF
~250W peak

RTX 4070
~200W

RTX 3060
~170W

Motherboard + disks + fans
~80W
```

Peak:

```
250 + 200 + 170 + 80
≈700W
```

750W works, but not much headroom.

For AI workloads where GPU runs 100% for hours:

I would upgrade to:

```
850W Gold
```

Examples:

* Corsair RM850x
* Seasonic Focus GX-850
* MSI MPG A850G

---

## Your case is also a concern

Your RTX 4070 Gaming X Trio is huge.

Then adding RTX 3060:

```
slot 1:
RTX 4070
████████

slot 2:
RTX 3060
████
```

Problems:

* second GPU may block airflow
* temperatures increase
* motherboard spacing matters

A better case:

* ATX mid tower
* 7 PCIe slots
* front mesh airflow

Examples:

* Lian Li Lancool series
* Fractal Design Meshify
* Corsair 4000D Airflow

---

## One more AI-specific point

For your use case:

RTX 4070 + RTX 3060:

```
RTX 4070
12GB VRAM

RTX 3060
12GB VRAM

Total:
24GB VRAM
```

But:

**you cannot combine them like one 24GB GPU automatically.**

Example:

Qwen model:

```
12GB model
```

works.

But:

```
20GB model
```

does not simply use:

```
4070 12GB + 3060 12GB
```

unless using model parallelism.

Tools:

* PyTorch Distributed
* DeepSpeed ZeRO
* Accelerate

can split models, but bandwidth between GPUs is slow compared with NVLink.

---

My final build recommendation:

```
CPU:
i9-13900KF

Motherboard:
MSI MAG Z790 Tomahawk WiFi DDR5

GPU:
RTX 4070 12GB
+
RTX 3060 12GB

RAM:
64GB DDR5 6000

PSU:
850W Gold

Case:
ATX airflow case
```

This is actually a very reasonable "poor man's AI workstation". It gives you:

* 20 CPU cores / 32 threads
* 64GB RAM
* 24GB total NVIDIA VRAM
* CUDA compatibility
* ability to experiment with multi-GPU training

References:

* ASUS TUF GAMING Z790-PLUS WIFI specifications ([ASUS Global][2])
* MSI MAG Z790 TOMAHAWK WIFI specifications ([MSI-US Official Store][1])

[1]: https://us-store.msi.com/Intel-Z790/MAG-Z790-TOMAHAWK-WIFI?limit=12&utm_source=chatgpt.com "MSI MAG Z790 TOMAHAWK WIFI DDR5 ATX Gaming Motherboard - MSI-US Official Store"
[2]: https://www.asus.com/motherboards-components/motherboards/tuf-gaming/tuf-gaming-z790-plus-wifi/?utm_source=chatgpt.com "TUF GAMING Z790-PLUS WIFI｜Motherboards｜ASUS Global"
