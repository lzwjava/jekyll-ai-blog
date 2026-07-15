---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI X870E 多GPU限制详解
translated: true
type: note
---

**问题：MSI X870E 主板 — 最多可安装多少张 RTX 4070 级别显卡？**

**回答：**

MSI X870E 是一款非常高端的 AM5 主板平台（适用于 Ryzen 7000/8000/9000 系列处理器）。它性能出色，但**并非像服务器主板那样的多 GPU AI 工作站主板**。（[MSI USA][1]）

典型的 MSI X870E 布局如下：

```
CPU (Ryzen 9000)
 |
 +-- PCIe 5.0 x16  ---> 显卡 #1 (RTX 4070)
 |
 +-- PCIe 5.0 x4/x8 ---> 显卡 #2 (具体取决于型号)
 |
 +-- PCIe 4.0 x4 ---> 显卡 #3 (可行，但速度较慢)
```

例如，MSI MPG X870E Carbon 具有：

* 一个 PCIe 5.0 x16 主插槽
* 一个 PCIe 5.0 副插槽（带宽共享）
* 一个 PCIe 4.0 x4 第三插槽（[MSI USA][1]）

因此，在物理上：

* **1 × RTX 4070** → 完美
* **2 × RTX 4070** → 可行
* **3 × RTX 4070** → 某些型号上可行，但不理想
* **4 × RTX 4070** → 几乎不可能（插槽空间 + PCIe 通道 + 供电限制）

（[MSI][2]）

针对 AI 工作负载：

### 1 张显卡

```
RTX 4070 12GB
PCIe 5.0 x16
```

非常出色。

### 2 张显卡

示例：

```
RTX 4070 12GB
RTX 4070 12GB

总计显存：
24GB
```

但无 NVLink，因此 PyTorch 分布式训练将使用 PCIe 进行通信。

### 3 张显卡

```
RTX 4070
RTX 4070
RTX 4070
=
36GB 显存
```

可行，但：

* 第三张卡仅为 PCIe x4
* 物理散热变得困难
* 主板通道成为瓶颈

### 更好的 AI 配置

对于 LLM 实验，我不会选择 X870E。我会选择：

```
二手工作站/服务器主板：

Threadripper Pro
EPYC
Xeon W
```

因为您能获得：

```
PCIe 通道：

CPU
 |
 +-- GPU x16
 +-- GPU x16
 +-- GPU x16
 +-- GPU x16
```

示例：

```
4 × RTX 3090 24GB

= 96GB 显存
```

这对本地 LLM 来说更具吸引力。

X870E 更适合：

```
Ryzen 9950X
+
RTX 5090 / RTX 4090
+
高速 NVMe
+
游戏 + AI 工作站
```

而非：

```
4 显卡训练机
```

针对您的用例（GPT 训练、ROCm 实验、本地 LLM），我的排序是：

```
EPYC / Threadripper Pro  >>>  X870E  >>>  普通 B650/B760
```

X870E 是一款优秀的发烧级主板，但 AM5 平台本身没有足够的 PCIe 通道来支撑一个正经的多 GPU 实验室。（[MSI][2]）

参考资料：

* MSI PCIe 通道共享说明（[MSI][2]）
* MSI MPG X870E Carbon 规格（[MSI USA][1]）
* MSI PRO X870E-P 规格（[MSI USA][3]）

[1]: https://us.msi.com/Motherboard/MPG-X870E-CARBON-WIFI/Specification?utm_source=chatgpt.com "MPG X870E CARBON WIFI | 游戏主板｜AI PC 最佳主板｜MSI"
[2]: https://www.msi.com/blog/pcie-lane-bifurcation-and-bandwidth-sharing-on-msi-x870e-x870-motherboards?utm_source=chatgpt.com "MSI X870E / X870 主板上的 PCIe 通道拆分与带宽共享"
[3]: https://us.msi.com/Motherboard/PRO-X870E-P-WIFI/Specification?utm_source=chatgpt.com "PRO X870E-P WIFI | PRO 系列主板｜AI PC 最佳主板｜MSI"
