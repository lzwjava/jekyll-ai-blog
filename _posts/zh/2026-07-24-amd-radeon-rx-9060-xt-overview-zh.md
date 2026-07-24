---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD Radeon RX 9060 XT 概述
translated: true
type: note
---

问题：**AMD RX 9060 XT GPU 简介**

答案：

![Image](https://images.openai.com/static-rsc-4/W1qBIWHtqA1o7nShFqzEuZqBtxur4EKeLKv3E9J-Trnx0ZB-TqyQZ8Be052ogpzLvwTg71kslnEh7nImnvcw0mALau5ZCkjIem4Igw2FVfHtXFdm2VJW75qIJQsP7Ao_PXdUQ1vrp8IaP3K8oeENubhSFjQBpPtoMwjQ7iZiUl9ydVD0nScmt0ixI_VelExS?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/IIesS4cfMjT2qephYKdnC44H6OzzN00vBbxrnyqlqr5UfKAlGoZHYwtwLCMYm4P7fI7-sJIDke-PNrnAVLOec7XPGjhh2ND_nihxj_zh0yAvmaAyu_8MfQFoJ3XK45Co-Mc0WunJe76geoO7_HpkvuR92sPkJA1Jxp6lYJp5Xd3Z0srtsoGQBx3vPr3pnfeu?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/xE2v9OvkNjNHKqjwSygEqCeVmRE0NiROk7aMedrG5JfMeb1j250J-Ma1TgEEQprNT5sN_q5RVN6JrMv04lPW3LFqMxGjH3xzoOQv5mqzeXCetDUP9fH8QycdZA-aJWnMZ30N52fuxIb5GvCZIheOZiUmWNzzd0bLKU-kc2xhz3IUedjUMU8RnyWn37HM6uCc?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ThD_LNLuwuSeIayvbjh7gbHihqXyj44D7n0zrxbhQgdduUJapOa9OFWcyp6WDCPXvQannqW54WtIcWlAyDQSgxFJPMCawRJCp88s9j7tny9M_evNx6VjPj9ep0s5g_rKYuWUJVOTvYz4apuni4XAQn4ZjEeMytXayjM4Zp4f_YXskQdDnaCA5svfc3mKJ8RT?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/6NqSHU5GccGZDfnlVDlH01pFsjMq9t5Gtx0aBMhaT-opQymkOtn8pocYJp1xBAuCaK4V0EHIC-yJSMoITdLXYwSwpvCJWgk2IYYuKdzPS2Fwv9OGl-D9kHq3WOJ_A3MB19cpGcySoKkspgGrm3OiBx8xCA4kE4ExqRNIWf0llPVMz5i3vecs0HsXIVEaKuZP?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/xZ_xQfAA8sXtF1GZs_cIhcg1rKfZc9OV_oZkrnmufjZiWnY0uvEUVpeMGIpyQxlQ7ad1MAm_4puCrM-9_2hIPZoKXTpV7hzI68wUqRbQCdgoCB_L3PLTT7qz9REDkEM2WA9jE1q8r0v5EWxTSQ0Gne7TgTo2sFHzKsmMpVeVj2SkFzHP0ba94oIxx0ycVH5k?purpose=fullsize)

**AMD Radeon RX 9060 XT** 是 AMD 基于 **RDNA 4 架构** 打造的主流/中端 GPU。它面向 **1440p 游戏**，主要竞争对手是 Nvidia 的 RTX 5060 Ti 级别 GPU。该显卡于 2025 年作为 Radeon RX 9000 系列的一部分发布。([AMD][1])

## 1. 主要规格

|                   | RX 9060 XT 16GB |
| ----------------- | --------------- |
| 架构              | RDNA 4          |
| GPU 核心          | Navi 44         |
| 计算单元          | 32              |
| 流处理器          | 2048            |
| 显存              | 16GB GDDR6      |
| 显存位宽          | 128-bit         |
| 显存带宽          | ~320 GB/s       |
| Infinity Cache    | 32MB            |
| 加速频率          | 最高 3.13 GHz   |
| FP32 算力         | 25.6 TFLOPS     |
| 板卡功耗          | ~160W           |
| PCIe              | PCIe 5.0 x16    |

([AMD][2])

此外还有一个 **8GB 版本**，但对于未来工作负载而言，16GB 型号更具吸引力，因为现代游戏和 AI 工作负载正日益触及显存限制。([AMD][3])

---

## 2. 架构：RDNA 4

RDNA 4 是 AMD 继 RDNA 3 之后的游戏 GPU 架构。

主要改进：

### 更优的光线追踪

AMD 将光线追踪吞吐量较上一代提升了一倍。([AMD][1])

### 新的 AI 加速器

每个计算单元都包含 AI 加速支持。

AMD 提供了：

* FP16 矩阵
* INT8
* INT4
* 结构化稀疏

RX 9060 XT 在低精度模式下可达到非常高的理论 AI TOPS 数值。([AMD][2])

但请注意：

> 理论 TOPS ≠ LLM 推理速度

对于 AI 而言，软件栈至关重要：

```
CUDA + cuBLAS + TensorRT
        |
        v

ROCm + HIP + rocBLAS
        |
        v

AMD GPU
```

Nvidia 仍然拥有巨大的生态系统优势。

---

## 3. 与你的 RTX 4070 对比

你的 RTX 4070：

|              | RTX 4070     | RX 9060 XT  |
| ------------ | ------------ | ----------- |
| 架构         | Ada Lovelace | RDNA 4      |
| 显存         | 12GB GDDR6X  | 16GB GDDR6  |
| FP32         | ~29 TFLOPS   | 25.6 TFLOPS |
| 显存带宽     | 504 GB/s     | 320 GB/s    |
| AI 生态系统  | CUDA         | ROCm/HIP    |
| 功耗         | 200W         | 160W        |

在游戏方面：

* RX 9060 XT 16GB 具有竞争力。
* 更大的显存是一个巨大优势。

在 AI 方面：

你的 RTX 4070 总体上仍然更好，因为：

```
PyTorch
 |
 CUDA
 |
 TensorRT
 |
 FlashAttention
 |
 vLLM
```

更加成熟。

AMD：

```
PyTorch
 |
 ROCm
 |
 HIP
 |
 MIOpen / rocBLAS
```

虽然改进很大，但兼容性差距依然存在。

---

## 4. AI 工作负载视角

对于本地 LLM：

### RX 9060 XT 16GB

可以运行：

* 7B 模型轻松应对
* 14B 量化模型
* 部分 20B+ 量化模型

示例：

```
Qwen3-14B Q4

权重：
14B * 0.5 字节 ≈ 7GB

+ KV 缓存
+ 运行时开销

16GB 显存足够舒适
```

但与 Nvidia 相比：

```
RTX 4070 12GB
       |
       CUDA 生态系统
       |
       更好的工具支持
```

胜出。

---

## 5. AMD 推出此显卡的原因

AMD 的策略：

```
Nvidia
 |
RTX 5090
RTX 5080
RTX 5070
RTX 5060
 |
CUDA 生态系统


AMD
 |
RX 9070 XT
RX 9070
RX 9060 XT
 |
性价比 + 开放生态系统
```

RX 9060 XT 并非试图击败 Nvidia 的 AI 生态系统。它的目标是：

* 游戏玩家
* 创作者
* 价格实惠的 GPU
* 开放计算用户

([AMD][1])

---

## 6. 针对你的 AI 实验室用例

考虑到你的实验：

* GPT-2 训练
* nanoGPT
* ROCm 探索
* 多 GPU 想法

我的排序是：

```
H100/H200
    |
MI300X
    |
RTX 4090
    |
RTX 3090 24GB
    |
RTX 4070 12GB
    |
RX 9060 XT 16GB
```

对于 AI 研究，显存是王道：

```
16GB AMD
<
24GB RTX 3090
```

因为许多 LLM 实验受限于显存容量。

RX 9060 XT 是一款非常优秀的 **消费级 GPU**，但并非 AI 研究级 GPU。

---

参考资料：

* AMD Radeon RX 9060 XT 官方规格 ([AMD][2])
* AMD Computex 2025 RX 9060 XT 发布公告 ([AMD][1])
* Tom's Hardware 发布概览 ([Tom's Hardware][4])

[1]: https://www.amd.com/en/newsroom/press-releases/2025-5-20-amd-introduces-new-radeon-graphics-cards-and-ryzen.html?utm_source=chatgpt.com "AMD Introduces New Radeon Graphics Cards and Ryzen Threadripper Processors at COMPUTEX 2025"
[2]: https://www.amd.com/en/products/graphics/desktops/radeon/9000-series/amd-radeon-rx-9060xt.html?utm_source=chatgpt.com "AMD Radeon™ RX 9060 XT (16GB)"
[3]: https://www.amd.com/en/products/graphics/desktops/radeon/9000-series/amd-radeon-rx-9060xt-8gb.html?utm_source=chatgpt.com "AMD Radeon™ RX 9060 XT (8GB)"
[4]: https://www.tomshardware.com/pc-components/gpus/amd-radeon-rx-9060-xt-launches-on-june-5-starting-at-usd299?utm_source=chatgpt.com "AMD Radeon RX 9060 XT launches on June 5, starting at $299"
