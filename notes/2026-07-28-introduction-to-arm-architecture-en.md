---
audio: false
generated: true
image: false
lang: en
layout: post
title: Introduction to ARM Architecture
translated: false
type: note
---

Question: **Introduction to ARM chips**

Answer:

![Image](https://images.openai.com/static-rsc-4/SsDBzUcrpB-r-tFFDXAjSofX7BYcHIqwMHb496t9G4bQxx00UhYsrCpAdAnoHV40DBChb7VeCvMiFQ49d2BGSTvHJkJgyGCQBbvGu66S3MAxrAgGVyDg5c7S0J0oUuE15HNpxQIAaTD25iIf5jpIhAzCD2moVsRtgwJ6zYECqaed8Zi3ThNpdDL5NpsK6k66?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/eUKAa7NyIAPibP0WotiKojWabawtrEhaZ6KF_xVsBAkgImw42CiZ9MjgQcwRPgXfxCmoyGXovCR3KU7XVmkWiJQHCzrxmVlKPcS2ms3p9IT7hb6VeDyJ1WEfyCKLC146FcM6EV3A7sGK8BbRSasjwCP0ryqAzFhVPiHotglhtb71uhfEVNZ4TsYmKhxeYOYY?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ofWM5OaOxUvn1tfzR3Ht3UtH46-m4Y3H9jCmS94KA6an-e2Cx9F5wnKu4Hi0SWrcP5C-txaH0D8_nEUiHsWPKVKU49-d3osN2DhtLGZ_XkZT1PpJbAGeHQUb0LsZICNtM8wTDv9F6MhEoYjJSL4ZRd253aOrbF_giQ6xOfz-gu6Zkr03aV77vSdMtWxqZhR6?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/3oUSUdPt-YRF9p8jEfgS6xHv342SJQUVrZnhyANH8FNKaYccicNzWJ7Wn7Ca6cThwIqnovJnVNP5Ha-A7QsY6P6ZtjnmNcSgPN025rBrcomi32yEv3s5yVvFh9j0x4lqtq_5aH_E7Yx15wmK0OP9sp9s5bulqHQ4cZGeSLDFN5QSBAqdIs23S4TnQ56r20A0?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/2fVoP5kepDzEnzWW0oR5xRbZbjERDXtYAzbhBK9O3IWsTgVGVTSLGpzmRYQUGF-LH5OIlKUBvy-jKB_LGPxuUZ0Pe7NuXX06RH-HpmQnHHxao-zguhUMokNfccQnVqI16L5Z5sxenRtMEsjV6c-1JAMC2fgKwGh9EhHVk-A6ZWvlepsgPC4JwXMYkYtrF1BP?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/qSbq-ki83Uhh5l3KA2ZuWRws-51n3GY4D4bz8pd_DKFTbQgNzKCnwgr281rz3GjUQL3QHCrFVMFln25QQn18pZd8MGkOovQht17rIBIYRS0t7Y-CVTVBnU-um7BRKWkl6KnLFU7CDrFXkohHgdFVSfWOcD1SebmsXJrxYFBJg9kDHDcW5m5zSfa5JVc2M6M2?purpose=fullsize)

ARM is a **CPU instruction set architecture (ISA)** originally created by Arm Holdings. Unlike Intel x86 CPUs (used in most PCs), ARM CPUs are designed around **low power consumption and high efficiency**.

The key idea:

> ARM licenses the CPU design/architecture. Companies build their own chips around it.

Examples:

* Apple designs M-series chips (M1/M2/M3/M4) based on ARM architecture.
* Qualcomm designs Snapdragon chips.
* MediaTek designs smartphone SoCs.
* Huawei uses ARM-based designs in Kirin chips.

---

## 1. ARM vs x86

Traditional PC:

```
Intel Core / AMD Ryzen
        |
        v
      x86 ISA
        |
        v
    CPU cores
```

ARM:

```
ARM ISA license
        |
        +----------------+
        |                |
      Apple           Qualcomm
        |                |
     M4 chip       Snapdragon X
```

ARM is not a chip itself. It is like a "language" the CPU understands.

Example:

x86 instruction:

```
ADD RAX, RBX
```

ARM instruction:

```
ADD X0, X1, X2
```

Different machine languages.

---

## 2. Why ARM became popular

### Power efficiency

ARM follows a simpler instruction design:

**RISC**
(Reduced Instruction Set Computer)

Characteristics:

* fewer instruction types
* simpler CPU decoding
* lower transistor cost
* better energy efficiency

Typical comparison:

| CPU           | Device        | Power    |
| ------------- | ------------- | -------- |
| Intel Core i9 | Desktop       | 100-250W |
| Apple M4      | Laptop/tablet | ~10-30W  |
| Snapdragon    | Phone         | ~3-8W    |

---

## 3. ARM SoC design

Modern ARM chips are usually **SoCs (System on Chip)**:

```
+--------------------------------+
| ARM SoC                        |
|                                |
|  CPU cores                     |
|   - Cortex-X big cores         |
|   - Cortex-A efficiency cores  |
|                                |
|  GPU                           |
|                                |
|  NPU / AI accelerator          |
|                                |
|  ISP camera processor          |
|                                |
|  Memory controller             |
|                                |
|  Modem (sometimes)             |
+--------------------------------+
```

A phone chip is basically a whole computer.

---

## 4. Apple Silicon example

Apple M4:

```
             M4 SoC

+--------------------------+
| CPU                      |
|  4 efficiency cores      |
|  6 performance cores     |
+--------------------------+
| GPU                      |
+--------------------------+
| Neural Engine             |
| (AI acceleration)         |
+--------------------------+
| Unified Memory            |
+--------------------------+
```

The important innovation:

### Unified Memory

Traditional PC:

```
CPU RAM <----> PCIe ----> GPU VRAM
```

Apple:

```
        Unified Memory
             |
     +-------+-------+
     |               |
    CPU             GPU
```

Less copying, better efficiency.

---

## 5. ARM in AI computing

ARM is becoming important because AI workloads need efficiency.

Examples:

### Edge AI

```
Camera
 |
ARM chip
 |
Neural Engine
 |
AI inference
```

No cloud needed.

Applications:

* autonomous vehicles
* robots
* drones
* smart cameras
* phones

---

## 6. ARM server market

ARM is also entering servers.

Examples:

* Amazon Web Services Graviton processors
* Ampere Altra CPUs

Server advantages:

```
same electricity budget:

x86:
100 cores

ARM:
150+ cores
```

Cloud providers like ARM because electricity is a major cost.

---

## 7. ARM vs RISC-V

Another important architecture:

```
ARM
 |
 |-- proprietary ISA
 |-- license required

RISC-V
 |
 |-- open ISA
 |-- anyone can implement
```

RISC-V is becoming popular in China and research because companies can avoid ARM licensing.

---

## 8. For developers

ARM affects software because binaries differ.

Example:

x86:

```
app-x86_64
```

ARM:

```
app-aarch64
```

Linux:

```bash
uname -m

# Intel PC
x86_64

# ARM machine
aarch64
```

Docker:

```bash
docker build \
  --platform linux/arm64 .
```

Modern tools support multi-architecture images:

```
myapp:latest

        |
        +-- linux/amd64
        |
        +-- linux/arm64
```

---

## 9. Future trend

The computing landscape is moving:

```
2000-2020

Intel x86
   |
   +-- PC
   +-- Server


2020-2030

ARM
   |
   +-- Mobile
   +-- Laptop
   +-- Server
   +-- AI Edge


2030+

ARM + RISC-V + custom AI accelerators
```

For AI engineers, ARM matters because the future is not only GPU clusters. A lot of inference will run on **efficient ARM + NPU devices**.

References:

* [Arm Architecture](https://www.arm.com/architecture?utm_source=chatgpt.com)
* [Apple M4 chip overview](https://www.apple.com/newsroom/2024/05/apple-introduces-m4-chip/?utm_source=chatgpt.com)
* [AWS Graviton Processors](https://aws.amazon.com/ec2/graviton/?utm_source=chatgpt.com)
* [RISC-V International](https://riscv.org/?utm_source=chatgpt.com)
