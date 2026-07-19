---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Z790-P多GPU PCIe限制
translated: true
type: note
---

问题：**MSI PRO Z790-P 的 PCIe 布局对于多 GPU / AI 工作负载表现如何？**

答案：

MSI PRO Z790-P 采用**消费级桌面 PCIe 布局**，而非工作站/服务器多 GPU 布局。它适合**一块高性能 GPU + 扩展卡**，但不适合**2× RTX 3090 / AI 训练机**。

插槽：

```
CPU PCIe 通道：
PCI_E1：
    PCIe 5.0 x16
    ↑ 直接连接到 Intel CPU

Z790 芯片组通道：
PCI_E3：
    PCIe 4.0 x4

PCI_E4：
    PCIe 3.0 x1

PCI_E2：
    PCIe 3.0 x1
```

物理布局：

```
CPU
 |
 |  PCIe 5.0 x16
 |
[ GPU 插槽 ]  <- 此处放 RTX 4070 / 3090

（空白区域）

[ PCIe x4 插槽 ] <- 第二个 GPU 可能，但只有 x4

[ PCIe x1 ]

[ PCIe x1 ]
```

## 对于 RTX 3090 + RTX 3090

示例：

### GPU1

RTX 3090：

```
PCIe 4.0 x16
```

实际运行：

```
PCIe 4.0 x16
```

很好。

### GPU2

RTX 3090：

```
PCI_E3：
PCIe 4.0 x4
```

带宽：

```
PCIe 4.0：
1 条通道 ≈ 每个方向 2 GB/s

x4：
≈ 8 GB/s
```

与 x16 对比：

```
x16：
≈ 32 GB/s
```

因此第二块 GPU 仅有 25% 的带宽。

对于推理：

```
GPU1 -> 模型层
GPU2 -> 模型层
```

PCIe x4 通常是可以的。

对于训练：

```
GPU1 梯度
       |
       | PCIe
       |
GPU2 梯度
```

x4 会变得非常吃力。

---

## 更大的问题：Intel 桌面 CPU 通道

你的 i9-13900KF：

```
CPU PCIe 通道：
16 条 GPU 通道
4 条 NVMe 通道
```

只有：

```
GPU：
x16
```

没有：

```
x16/x16
```

支持。

主板无法凭空创造通道。

Z790 主板不会神奇地提供更多 GPU 带宽。

---

## 对比更好的主板

针对你的 AI 使用场景（3090、4070、ROCm 实验），可考虑：

### MSI MPG Z790 Carbon WiFi

更好：

```
GPU1：
PCIe 5.0 x16

GPU2：
PCIe 5.0 x8
```

因为它利用了 CPU 分叉。

两块 GPU 都能获得 CPU 通道：

```
x8 + x8
```

好得多。

---

### ASUS ProArt Z790 Creator WiFi

更像工作站：

```
PCIe 5.0 x16
PCIe 5.0 x8
Thunderbolt
10Gb 以太网
```

适合创作者 / AI。

---

### 真正的多 GPU 平台

如果你的目标变成：

```
2× RTX 3090
4× RTX 3090
```

那么消费级 Intel 就是错误的平台。

需要：

* AMD Threadripper
* Intel Xeon W
* EPYC

示例：

Threadripper：

```
CPU PCIe 通道：
64-128 条通道
```

然后：

```
GPU1 x16
GPU2 x16
GPU3 x16
GPU4 x16
```

---

## 针对你当前的情况

你拥有：

* i9-13900KF
* RTX 4070
* 对 AI 训练感兴趣
* 考虑二手 RTX 3090

我对选项的排序：

### 选项 A —— 最省钱

保留 PRO Z790-P：

```
RTX 4070：
PCIe x16

RTX 3090：
PCIe x4
```

适合：

* LLM 推理
* QLoRA
* vLLM 实验
* 运行 40B+ 模型

不适合：

* 分布式训练

---

### 选项 B —— 更换主板

购买支持 x8/x8 的 Z790：

```
RTX 3090
+
RTX 3090

两者均为 x8
```

更干净利落。

---

### 选项 C —— 工作站

以后：

```
Threadripper + 4 GPU
```

当你真正需要多 GPU 训练时使用。

---

对于你的使用场景（训练 GPT-2 类模型，尝试 24GB VRAM），**PRO Z790-P 是可以接受的。第二块 RTX 3090 运行在 PCIe 4.0 x4 下会降低训练吞吐量，但不会阻止你运行更大的模型。** 对于推理而言，VRAM 比 PCIe 带宽重要得多。