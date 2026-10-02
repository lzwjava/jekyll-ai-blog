---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI Z170A SLI PLUS 概览
translated: true
type: note
---

问题：MSI Z170A SLI PLUS 主板介绍及其价值/用途。

回答：

![Image](https://images.openai.com/static-rsc-4/MGmn127nOzgR5bXTXPQ3aYlKjNyNOsnnG-YAo3Bk0LRL2Ido1fITcRkZd72Gbja49UylnaFNhoyc3EJoW__qswSWpCOICkMwSlSyaA8KTbShswXnlZi7TP1JTYDCxNaZBo1Bx1B42fzBkJ41FKqx2x50fWg8S4YgkgkBgFhPGuNBQgOXjKTKa-6_n7hMViVw?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/5FRwiqxCiOzkUfImK2e2jQOzVknhSlGnL399EXnZaYwVHBjcyTCEf-wpf0Cf-28lUZt-7X03Spsgdagtefx2_DvGEY1fg6wo1-zresgGI44xP217HcFHtP9lhOCryM2eBteplzJVTWZwo1qvqfkAUZ0rxAcvEK1xUhlAalKvdFphS7fq6yymf4jjYetM5udD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/GdbWew01yabxeEr-pS-1-QSUXzJQeMs2SXZJaddYBiiEZYpZTrC4a7hf01LpxjBMRgHKK78FjC-vpWPNoNOUgawjr6OKVuzp7OMteLQXlt8DmZ30f2lfgNEoEBXghNSe8YfPSIUOkpb_pc4XHhXrVZ7ZAnB2yVDBs41f3_PCjWhUHSDRTabM39_sOpctO31_?purpose=fullsize)

**MSI Z170A SLI PLUS** 是一款来自 **Intel Z170 芯片组世代（2015年）** 的中端发烧友主板。它面向 Intel **第六代 Skylake CPU**，以及（BIOS 更新后的）部分 **第七代 Kaby Lake CPU**。

## 主要规格

| 特性 | 详情 |
| --- | --- |
| Socket | LGA1151 |
| CPU 支持 | Intel 第六代酷睿（Skylake），第七代酷睿（Kaby Lake，需更新 BIOS） |
| 芯片组 | Intel Z170 |
| 内存 | 4 × DDR4 DIMM 插槽 |
| 最大内存 | 最高 64GB DDR4（原生通常 2133MHz，XMP 可更高） |
| GPU 插槽 | 3 × PCIe x16 物理插槽 |
| 多 GPU | 支持 NVIDIA SLI / AMD CrossFire |
| 存储 | M.2 PCIe 3.0 x4 NVMe 支持 + SATA 接口 |
| 网络 | 千兆以太网 |
| 音频 | 7.1 声道音频 |
| 板型 | ATX |

## CPU 选项

合适的搭配：

* Intel Core i7-6700K

  * 4 核 / 8 线程
  * 不锁倍频
  * 经典 Z170 搭配

* Intel Core i7-6700

  * 4 核 / 8 线程
  * 功耗较低，稳定

* Intel Core i5-6600K

  * 4 核 / 4 线程
  * 可超频

* Intel Core i7-7700K

  * 该平台最快的主流 CPU 选项

对于现代 AI 工作负载来说，这个平台非常老旧。它的主要用途在于：

* GPU 维修测试台
* PCIe 实验
* 便宜的 NAS/服务器
* 怀旧游戏
* 学习 BIOS/PCIe 行为

## PCIe 布局

这块主板很有趣，因为它有多个 PCIe 插槽：

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

重要：

* 只有第一个 GPU 插槽获得完整的 CPU x16 带宽。
* 其他长插槽物理上是 x16，但电气上只有 x4。
* 对于 GPU 计算，一块 RTX 3090/4090 应放在第一个插槽。
* 多块较旧的 GPU（P100/M40/Quadro 等）可以工作，但带宽有限。

## 与你的 GPU 实验相关的 BIOS 功能

因为你一直在测试 P100/M40/ReBarUEFI 风格的 PCIe 问题，这块主板实际上是一个不错的平台。

请查找：

### CSM

```
BIOS
 → Settings
   → Advanced
     → Windows OS Configuration
       → CSM
```

选项：

* 启用（Enabled）= 传统 GPU ROM 兼容
* 禁用（Disabled）= 纯 UEFI

对于旧款 Tesla GPU：

* 有时启用 CSM 会有帮助。
* 一些现代 ReBarUEFI 设置要求禁用 CSM。

### 高于 4G 地址解码

通常：

```
BIOS
 → Settings
 → Advanced
 → PCI Subsystem Settings
 → Above 4G Memory/Crypto Currency Mining
```

启用场景：

* 多块 GPU
* 24GB Tesla M40
* ReBAR 实验

### PCIe 速度

对于不稳定的旧 GPU：

```
PCIe Link Speed
Auto → Gen2
```

旧款 Tesla 显卡在 Gen2 下通常表现更好。

## 与更新的廉价平台相比

对于 GPU 实验室：

| 平台 | 优势 |
| --- | --- |
| Z170 + i7-6700 | 便宜，DDR4，BIOS 好 |
| X99 + Xeon E5 v3/v4 | 更多 PCIe 通道，更适合多块 GPU |
| B450/B550 | 现代 CPU，PCIe 4.0 |
| Z690/Z790 | 贵但现代 |

对于你的使用场景（GPU 维修 + LLM 实验），Z170A SLI PLUS 的价值主要在于：

* 便宜的二手价格（通常在 200–300 元人民币左右）
* DDR4 容易获得
* 多个 PCIe 插槽
* 良好的 MSI BIOS
* 支持 NVMe

但它不是一台好的 AI 训练机器，因为：

* CPU 只有 4 核
* PCIe 3.0
* PCIe 通道有限
* 不支持 ECC

一个不错的廉价配置是：

```
MSI Z170A SLI PLUS
+ i7-6700 / i7-6700K
+ 32GB DDR4
+ RTX 3060 / Tesla P100 / M40 test GPU
+ Linux
```

这将构成一个不错的 GPU 诊断工作台。

我还可以帮你将这款 Z170A SLI PLUS 与你正在考虑用于 M40/P100 测试的 X99 主板进行对比。
