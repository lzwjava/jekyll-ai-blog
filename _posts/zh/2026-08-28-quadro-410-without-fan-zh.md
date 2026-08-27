---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Quadro 410 无风扇
translated: true
type: note
---

问题：如果你从 NVIDIA Quadro 410 上拆下风扇并插上使用，会发生什么？

答案：

![Image](https://images.openai.com/static-rsc-4/DEoK1G2XdBPcnMVi6tx4dEGAhG00nIcy-IDyI2wKDIDH153xHeotRZifeAOr6j1PBfI4kh2j2_vWa7zVWG15-WvhHg_9y2hTdMpkBa7StCuKryB-tZxECwWLPPz21KsY1ZfXmljmzTYwA-amx1AEDGCVCa9Vs0g9UuF6sEVQw3jWIhIgJcnfh0VwF41T6tWC?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Ld0rnL0J79Ja8XVG0CucwlltB7m0d9jeNQMLBL8XZ7GQ80oq2USCrGrjOLu0AP4NP6b14l2fvfPlaLicH3qSii5gGy8nTT9uUU3SnPaSH2pKybedv7NAYVXhnrN42cHLjnAYUKomYGs6NnToA2kZY9DSRuCO38Ug0UAWsC4XqRQohTX7vViFPsbEZbfdkKux?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/otr-F_xmxkEsggWnpUUt2XMPEdJhmmdBa9PP5hILJH9V5RiJmXaQ26r9bWtRzhFnkkBG-kMtfGgXX0AHVA8INXPb29vlMtzoxWJYVxXt4JVXoB-vPDhK5_hwb-oblPKzB0tVk-l5-yIaIhurSHv8UXggKme1XGvLvtcFQzaC_R2I17Gs0eZ6u6S9GEvMcDM_?purpose=fullsize)

Quadro 410 是一款功耗非常低的工作站 GPU。它使用 **NVIDIA GK107 Kepler 芯片**，TDP 约为 **38W**。散热器主要是一个小型散热片加一个小风扇，因为与现代 GPU 相比，该芯片温度不算高。

如果你拆下风扇但保留散热片：

* **空闲 / 桌面使用：** 可能正常工作。
* **轻负载：** 可能可以工作一段时间。
* **高 GPU 负载：** 温度会迅速上升，可能会降频或崩溃。

GPU 本身具有热保护机制：

1. 温度升高。
2. 驱动程序降低时钟频率（热降频）。
3. 如果温度过高（约 90–100°C 范围），GPU 会关闭以保护自身。

具体行为取决于气流情况：

### 情况 1：拆下风扇，散热片仍保留，开放环境

也许没问题。

示例：

```
GPU chip
  |
thermal paste
  |
metal heatsink
  |
room air
```

38W 的芯片有时能撑住，因为散热片可以被动散掉部分热量。

### 情况 2：拆下风扇，没有散热片

坏主意。

```
GPU chip
  |
  |
air only
```

微小的硅芯片裸片几乎没有表面积。它很快就会达到危险温度。

### 情况 3：拆下风扇但加装更大的散热片

实际上是个不错的实验。

大型 CPU 散热片或主板 VRM 散热片可以轻松为 Quadro 410 降温：

```
Quadro 410 PCB
       |
thermal pad/paste
       |
large aluminum heatsink
       |
case airflow
```

因为 38W 的功耗很小。现代笔记本电脑 CPU 的功耗往往更高。

对于学习硬件知识来说，Quadro 410 是一款很适合的“安全”实验 GPU，因为：

* 便宜
* 功耗低
* PCB 简单
* 不太可能瞬间烧毁自己
* 可以观察热行为

你可以用以下命令测量：

```bash
watch -n 1 nvidia-smi
```

并观察：

```
temperature
power draw
GPU clock
```

一个有趣的实验：

1. 运行 `glmark2` 或 CUDA 工作负载。
2. 拔掉风扇电源连接器。
3. 观察温度攀升。
4. 观察降频现象。

这基本上与调试故障 GPU 显卡时使用的原理相同：许多“死亡”GPU 实际上是散热、VRAM、供电或焊点问题，而不是 GPU 核心本身的问题。
