---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD MI50 PCIe 4.0 支持
translated: true
type: note
---

问题：AMD Instinct MI50 是否兼容 PCIe 4.0 或 PCIe 3.0？

答案：AMD Instinct MI50 原生支持 **PCIe 4.0 x16**。该显卡发布时，AMD 将其与 MI60 一同作为全球首批支持 PCIe Gen 4 的 GPU 系列进行推广。

由于 PCIe 技术具有向后兼容性，该显卡也能在 **PCIe 3.0** 插槽中完美运行，不过带宽速度将限制在 PCIe 3.0 水平。

参考来源：

* [AMD Radeon Instinct MI50 规格 | TechPowerUp GPU 数据库](https://www.techpowerup.com/gpu-specs/radeon-instinct-mi50.c3335)
* [加速器规格 | AMD](https://www.amd.com/en/products/specifications/accelerators.html)