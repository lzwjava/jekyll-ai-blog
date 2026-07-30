---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微星双RTX 3060主板
translated: true
type: note
---

**问题：哪款 MSI 主板可以装下两张 RTX 3060 显卡？**

**答案：**

对于 **2 张 NVIDIA RTX 3060** 显卡，你需要：

1.  **两个物理 PCIe x16 长度的插槽**
2.  足够的间距，因为大多数 RTX 3060 显卡是 **2 槽厚**
3.  CPU/平台提供足够的 PCIe 通道（对于普通 ML 工作负载，x8/x8 即可）

可用的 MSI 主板：

### 1. MSI MAG B760M Mortar WiFi（你当前的主板）

MSI MAG B760M Mortar WiFi 具有：

*   PCIe x16 主插槽 → GPU 1
*   PCIe x16 物理插槽（电气 x4）→ GPU 2

它可以物理容纳两张 RTX 3060 显卡，但：

```
RTX 3060（插槽 1）
████████
████████
（空白/间隔）
RTX 3060（插槽 2）
████████
```

第二张 GPU 以 PCIe 4.0 x4 运行。对于 LLM 训练/微调，这并不理想，因为 GPU 间带宽有限，但可以工作。

---

### 2. MSI PRO Z790-A WiFi / MAG Z790 Tomahawk WiFi（更好的消费级选择）

示例：

MSI MAG Z790 Tomahawk WiFi

布局：

```
CPU PCIe x16
    |
 RTX 3060 #1  PCIe 4.0/5.0 x16

芯片组 PCIe x16 插槽
    |
 RTX 3060 #2  PCIe x4
```

间距比许多 mATX 主板更好。

---

### 3. MSI Creator / 工作站主板（多 GPU 最佳选择）

如果你的目标是 AI 训练：

MSI Creator X299 / TRX40 / WRX80 平台好得多。

示例：

```
GPU1 x16
GPU2 x16
GPU3 x16
GPU4 x16
```

因为工作站 CPU 提供了大量 PCIe 通道。

---

## 对于 RTX 3060 + LLM 工作很重要

两张 RTX 3060 显卡：

*   VRAM **不会自动合并**
*   2 × 12GB ≠ 24GB VRAM

示例：

```
GPU0:
12GB VRAM

GPU1:
12GB VRAM
```

模型仍然看到：

```
GPU0 内存 = 12GB
GPU1 内存 = 12GB
```

除非使用分布式训练：

*   PyTorch DDP
*   FSDP
*   DeepSpeed ZeRO
*   tensor parallel 推理

对于你的用例（nanoGPT、Qwen 微调、vLLM 实验），第二张 GPU 主要用于：

*   更大的批量大小
*   DDP 训练
*   运行两个模型
*   推理服务

---

鉴于你当前的硬件（RTX 4070 12GB + 对 LLM 基础设施的兴趣），我 **不建议仅仅为了 VRAM 再购买一张 RTX 3060 和一块主板**。更好的升级路径：

```
当前：
RTX 4070 12GB

更好：
RTX 3090 24GB 二手
+
RTX 4070 12GB
```

你就能获得一个真正的 24GB 单 GPU 工作空间，用于：

*   QLoRA
*   更大的 LLM 推理
*   CUDA 开发
*   vLLM 实验

在你的 B760 主板上使用 3090 + 4070 实际上是一个非常实用的 AI 家庭实验室。

**参考资料：**

*   NVIDIA GeForce RTX 3060 规格：[https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3060/](https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3060/)
*   PyTorch 分布式数据并行：[https://pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html](https://pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html)