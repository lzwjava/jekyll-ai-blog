---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA NVLink 桥接器概述
translated: true
type: note
---

**问题：NVIDIA NVLink Bridge（2插槽/3插槽/2路/4路）有什么用途，特别是针对RTX 3090、A6000、A100、H100？**

**答案：**

![Image](https://images.openai.com/static-rsc-4/IkHwikN9QA4muNyeTGZrzJ2dtez6C-OduZHsv_Yr56HiozSZbiiu297DlmCPLjuu7pzpbR0gFc8bx9JTNFh9O0VjaAD5_3vyqrEY3Y_TEYCO8HQgLTONyqayb8Y2zTrZG1X0eCvlinHucc6R9rQV9nnVU4hKxrkSQd2tJosxevBnWwPem2RHLktVpH6GEiup?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/rITK3DB6-D0rJdi8YvDstzZh2btIAjyBOSk86SipOhzR_RjDsJx_AuQJIyNlG6VmL2dipNH-KI6m44C8qzd8uOPXY4yoGUM05eABkgDwZIi-CzZw5EZDZwqAO-1B985hjTSjbgL0jatX5TkA5beg6bB_ApQOKW8rNo-Bzxi-Xj2j7AaFRWWVZEo_09o_Rfcb?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/omuFtOu67coKGFWnEXiFQMfOIpOc8fRkKvMFGKz40ZP24sxroAjkcC9xsKB0m7hvSk4z0n5kcA05Ux_jIFYqGWs_D_Y3x0J-tC7teTCMq3aZrC2Y_f4JjvQo44dT7X6uB0uXQXFHBRp21Uz3MEi_Y26IbwlzW1GD4jRTsMVFcGJvrPYdpTOrqVZ3A47oDu11?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/5rJoh8iKcemXwIGYkQGmwU04-loq0RHULyB6837s6tNdaLtUl8QwqphwitcoiGK6znlzXs0TyZrg7vy4WF2sdjXvHOuGPJayOId7RU-iVp8fm6SVjtGsRN0yc-qyUKwgebW01MCybkgntd0lzzkYrl3ARFkfHGceNdcmGmbRHdo7COsO34RR46W7wN_PMvYs?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/H2JQAIeEFmVT5xnqHG2jnJ0ovR0brkjyez9SDnIxf61cdYQrtWXWaqUTvETB1mRZ4PIEpBK3YAMPgI1X1UTGUbdMhlbbritdUjoYo7SK16snVXdwbJglHMnmARAc-K52EOFNwTx0WKp_SYaL394udr4P3hsDqUkgxMLQPMFWhxYNy3IjPDxmUay8OsB8tMYX?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/4hfUeODPBHNxAZAdLAzn31wyLY0GpyKTEk-mFi1o8k4SdIAwIOgE4Mnr_n_7mYK27xVmj3s9OHlxVeL9ZMUGRd6KKhFhnsBirPjzu-jxDi4uz47k_e6bhpi5PTgb2zib8TXuY51D-u0GCaTA0j0DcTKrM9ffdNTE_oUHhSM3VcEiZPNutlvKqICXv9litv8A?purpose=fullsize)

**NVLink Bridge 是一个物理连接器，用于将两块 NVIDIA GPU 通过高速 GPU 到 GPU 互联连接起来。** 它不是一个能将 GPU 自动合并成一块巨型 GPU 的适配器。多 GPU 通信必须得到软件（如 CUDA、PyTorch、NCCL 等）的支持。([NVIDIA][1])

可以将其想象为：

```
没有 NVLink：

GPU 0 ---- PCIe ---- CPU ---- PCIe ---- GPU 1

使用 NVLink：

GPU 0 ===== NVLink ===== GPU 1
```

第二种路径具有更高的 GPU 到 GPU 带宽和更低的延迟。

---

## 1. "2插槽 / 3插槽" 是什么意思？

它描述了**主板上两个 GPU 之间的物理距离**。

示例：

### 2插槽桥接器

```
GPU
[====]

(空间)

GPU
[====]
```

两个 GPU 之间间隔 2 个 PCIe 插槽。

### 3插槽桥接器

```
GPU
[====]

(空间)

(空)

GPU
[====]
```

两个 GPU 相隔更远。

桥接器只是一个刚性连接器。你需要选择正确的间距。

---

## 2. "2路 / 4路" 是什么意思？

### 2路 NVLink

大多数消费级/工作站显卡：

```
GPU0 <==== NVLink Bridge ====> GPU1
```

示例：

* RTX 3090
* RTX A6000
* RTX 6000 Ada

这些显卡支持**配对两块 GPU**。([NVIDIA][1])

---

### 4路 NVLink

这主要是服务器/HPC领域的范畴：

```
GPU0 ===== GPU1
 ||         ||
GPU2 ===== GPU3
```

通常需要：

* SXM 模块
* NVSwitch
* HGX/DGX 系统

示例：

* A100 SXM
* H100 SXM

普通的带有 PCIe RTX 显卡的桌面主板无法构建 4 路 NVLink 网络。([NVIDIA Developer][2])

---

## 3. RTX 3090 NVLink Bridge

RTX 3090 很特别，因为它是最后一代支持 NVLink 的 GeForce 显卡。

两块 RTX 3090：

```
RTX3090 24GB
      |
   NVLink
      |
RTX3090 24GB
```

内存：

```
总计 48GB VRAM
```

但**并非像一块 48GB 的单 GPU**。

例如：

适用场景：

* 分布式训练
* 某些 CUDA 工作负载
* 模型并行

非自动生效：

```python
model.to("cuda")
```

**不会**使其变成 48GB。

PyTorch 仍然看到：

```
cuda:0 -> 24GB
cuda:1 -> 24GB
```

你需要：

* DDP
* FSDP
* DeepSpeed
* 张量并行框架

---

## 4. RTX 3090 + A6000 桥接器兼容性

有趣的一点：

RTX A6000 NVLink 桥接器经常被用于 RTX 3090，因为 Ampere 架构的 NVLink 使用的是同一代技术。社区测试证实，A6000 的 2插槽/3插槽桥接器可以与 RTX 3090 配合使用。([Reddit][3])

示例：

```
RTX3090
   |
A6000 3插槽 NVLink Bridge
   |
RTX3090
```

这在 AI 工作站构建中很常见。

---

## 5. A100 / H100 是不同的

### A100 PCIe

类似的概念：

```
A100 PCIe
    |
 NVLink
    |
A100 PCIe
```

存在双卡配置。

### A100 SXM / H100 SXM

这些是数据中心加速器：

```
        NVSwitch
       /   |   \
H100  H100 H100 H100
```

它们拥有更强大的互联能力。

H100 使用第四代 NVLink：

* H100：总计 900 GB/s NVLink 带宽
* A100：总计 600 GB/s NVLink 带宽 ([NVIDIA Developer][2])

---

## 6. 对于你的 AI 工作站使用场景

考虑到你对本地 LLM 训练/推理的兴趣：

### 双 RTX 3090

适用场景：

```
2 x RTX3090
=
48GB VRAM
+
NVLink
```

用于：

* 30B~70B 量化模型
* LoRA 训练
* 分布式推理

但是：

NVLink 并**不能**神奇地让你获得：

```
单 GPU 48GB
```

许多现代的 LLM 框架无论如何都能有效地利用 PCIe/NCCL。

---

### 购买优先级

对于 AI：

```
VRAM
  >
GPU 算力
  >
显存带宽
  >
NVLink
```

通常：

2 x RTX3090 没有 NVLink

仍然可以胜过

1 x RTX3090 有 NVLink

因为你获得了：

* 48GB 物理 VRAM
* 更多 CUDA 核心
* 更高吞吐量

NVLink 是锦上添花。

---

## 简单总结

| 产品       | NVLink? | 典型配置             |
| ---------- | ------- | -------------------- |
| RTX 3060   | ❌       | 无                   |
| RTX 4070   | ❌       | 无                   |
| RTX 3090   | ✅       | 2 GPU 桥接器         |
| RTX A6000  | ✅       | 2 GPU 桥接器         |
| A100 PCIe  | ✅       | 2 GPU                |
| A100 SXM   | ✅✅      | NVSwitch 系统        |
| H100 SXM   | ✅✅      | NVSwitch 系统        |

对于家庭 AI 实验室，最有趣的是：

```
2 × RTX3090 24GB
+
A6000 2插槽/3插槽 NVLink bridge
```

但这需要在你拥有足够的 PCIe 通道、电源供应能力和散热能力之后考虑。([Reddit][4])

参考资料：

* ([NVIDIA][1])
* ([NVIDIA Developer][2])
* ([NVIDIA][5])
* ([Reddit][4])

[1]: https://www.nvidia.com/en-us/products/workstations/nvlink-bridges/?utm_source=chatgpt.com "NVLink 高速 GPU 互联 | NVIDIA Quadro"
[2]: https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/?utm_source=chatgpt.com "NVIDIA Hopper 架构深入解析 | NVIDIA 技术博客"
[3]: https://www.reddit.com/r/nvidia/comments/kqvbus?utm_source=chatgpt.com "是否存在（非）官方的 GEFORCE RTX NVLINK BRIDGE 2插槽版本？"
[4]: https://www.reddit.com/r/nvidia/comments/kdro5w?utm_source=chatgpt.com "3090 2插槽和3插槽桥接器已经/即将上市！"
[5]: https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/quadro-product-literature/proviz-print-nvidia-rtx-a6000-datasheet-us-nvidia-1454980-r9-web%20%281%29.pdf?utm_source=chatgpt.com "NVIDIA RTX A6000 数据手册"
