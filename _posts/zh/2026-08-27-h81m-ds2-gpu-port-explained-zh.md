---
audio: false
generated: true
image: false
lang: zh
layout: post
title: H81M-DS2显卡接口详解
translated: true
type: note
---

**问题：** Gigabyte H81M-DS2 是否有 dedicated GPU port（比如 Nvidia card slot），或者为什么没有？

**答案：**

Gigabyte H81M-DS2 **确实有一个 PCIe slot**，你可以安装 discrete GPU（如 Nvidia 或 AMD 的 card）——但它**没有**在 motherboard 上集成 dedicated GPU chip（integrated Nvidia graphics）。原因如下：

**1. 它是 motherboard，不是 GPU**
Motherboard 不会焊接 Nvidia/AMD GPU chips。这些 GPU chips 是作为单独的 **discrete graphics cards** 出售的，你将这些 cards 插入 motherboard 上的 PCIe slot。

**2. 它通过 PCIe 支持 discrete GPU**
GA-H81M-DS2 使用 Intel H81 Express Chipset，并包含一个 PCIe x16 slot，这是安装 dedicated Nvidia 或 AMD graphics card 的标准 slot。

**3. Integrated graphics 来自 CPU，而不是 motherboard**
该 board 支持 LGA1150 封装中的 4th Gen Intel Core i7/i5/i3、Pentium 和 Celeron processors。许多这些 CPUs（例如 Core i3 或 i5）在 CPU die 内部集成了 Intel HD Graphics。这就是为什么后面板包含 D-SUB (VGA) port——它用于使用 CPU 的 integrated graphics，而不是 dedicated GPU。

**4. Budget/entry-level board——没有 onboard Nvidia**
H81M-DS2 是一款 budget microATX board。Onboard Nvidia 或 AMD graphics 在 desktop motherboards 上极其罕见——它们主要出现在一些 laptops 上。Desktop boards 要么依赖 CPU-integrated graphics，要么依赖单独的 discrete GPU card。

**简而言之：** 要使用 Nvidia GPU，只需将 Nvidia graphics card 插入 H81M-DS2 上的 PCIe x16 slot。Motherboard 本身永远不会包含 Nvidia chip——这不是 desktop PC 设计的方式。

---

**参考资料：**

- [GA-H81M-DS2 (rev. 4.1) 概览 – GIGABYTE](https://www.gigabyte.com/us/Motherboard/GA-H81M-DS2-rev-41)
- [GA-H81M-DS2 (Rev. 3.0) 规格 – GIGABYTE](https://www.gigabyte.com/Motherboard/GA-H81M-DS2-rev-30/sp)
