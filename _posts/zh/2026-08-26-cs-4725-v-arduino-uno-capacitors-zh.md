---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CS 4725 V Arduino Uno 电容器
translated: true
type: note
---

**问题：** Arduino Uno 板上标有“CS 4725 V”的元件是什么？

**答案：**

“CS 4725 V”（有时读作“CS47 25V”）是 Arduino Uno 板上两个**铝电解电容器**上印有的标记，在官方原理图中分别标注为 **PC1** 和 **PC2**。

这些标记的含义如下：

| 标记 | 含义 |
|---|---|
| **CS** | 元件系列/制造商代码（松下“CS”系列） |
| **47** | 电容值：**47 µF** |
| **25V** | 额定电压：**25 伏** |

根据 Arduino Uno 板的拓扑结构，PC1 和 PC2 被列为 **额定值为 47µF、20%、25V 的 SMD 铝电解电容器**，零件编号为 `EEE-1EA470WP`。

**在板上的作用：** 这些电容器位于 Arduino Uno 的电源部分。它们作为**大容量去耦/滤波电容器**，平滑电源输出的电压纹波，确保为板上的元件提供稳定的电力供应。

**参考资料：**
- [Arduino Uno Board Parts – VideotronicMaker](https://videotronicmaker.com/arduino-uno-board-parts/)
- [Arduino Uno Rev3 – 官方商店页面](https://store-usa.arduino.cc/products/arduino-uno-rev3)
- [Arduino UNO 元件概述 – Arduino 文档](https://docs.arduino.cc/tutorials/uno-rev3/intro-to-board)