---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华为昇腾950PR概览
translated: true
type: note
---

## 问题：Ascend 950PR 9579 简介

我推测您指的是 **华为 Ascend 950PR**（昇腾 950PR）。"9579" 可能是笔误或内部编号。Ascend 950PR 是华为的新一代 AI 加速器，主要面向 **LLM 推理预填充** 和 **推荐系统工作负载**。（[华为][1]）

![Image](https://images.openai.com/static-rsc-4/7IxRtIPq_rWrZesWOWPhZiU5N7xg9u1XkXTabRCwpJMFZzctsMUaRMJObkaijvmPxlTHk_UPPwkzLHkGm2FJPjzavprBHOMCCM9MYJdYyc92P7pGZwbioJb2KTyKY3khATvjmCCBx3WkKZKNzRKGMPuYK_3xmVeAOdOxIigzml0ja6Ssq1oKeqCE8lOEEoi2?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/lLCXeST-jpDRBNRm8Owmoj8iecEpEdYP_DVS815KV14afMUU-B4AfRVux7PzIhpMTgBlAwL45ecR-iShK22qySLhDfF4eZsKV2A_cZX7QefCfPgFhuWVX-Iki79_QeKJil2978hBTvnRnR2zgGcypbk5EswofHqtNBdcOJST4epk9vMINfJEkKy0sPeuHM41?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/PiNDAPc67VuEh_qkeUkxKnzfMU7t6Y3-zgrlpp95Ib1G8MgE5Mo10DsgKznNU4d_rEHJ5JwodJ_AYxzjgfEWgfKvNRrQ0KnNGj0nj6lt2JUK63aKCjipdEQM19Nxle_iLXDqKVsQEh1We7XgI2XI3m9yzuzW24W4U4V9Rt16TjIcn5RUYyrCntmdN2R3F6Go?purpose=fullsize)

## 1. 在华为昇腾路线图中的定位

华为昇腾路线图：

```
Ascend 310  (边缘AI)
      |
Ascend 910 / 910B / 910C  (训练 + 推理)
      |
Ascend 950 系列  (2026年)
      |
      +-- Ascend 950PR  -> 预填充 + 推荐系统
      |
      +-- Ascend 950DT  -> 解码 + 训练
      |
Ascend 960 (2027年)
      |
Ascend 970 (2028年)
```

950PR 和 950DT 共享相同的 Ascend 950 芯片，但针对不同工作负载封装了不同的内存系统。（[华为][1]）

---

# 2. 为何拆分 PR 和 DT？

华为瞄准了新的 LLM 服务架构：

```
用户提示词
     |
     v
+------------+
|  预填充     |  <- 计算密集型
+------------+
     |
     v
+------------+
|  解码       |  <- 内存带宽密集型
+------------+
     |
     v
Token 输出
```

示例：

```
输入：
"请解释 Transformer 架构..."

预填充：
处理全部 1000 个输入 token
       |
       v
创建 KV 缓存

解码：
生成：
"Transformer..."
"架构..."
"是..."
```

不同阶段的瓶颈：

| 阶段    | 瓶颈                       |
| ------- | -------------------------- |
| 预填充  | 张量计算                   |
| 解码    | 内存带宽 + KV 缓存          |
| 训练    | 两者兼有                   |

因此：

```
950PR
   |
   +-- 预填充
   +-- 推荐系统
   +-- 高吞吐推理

950DT
   |
   +-- 解码
   +-- 训练
```

（[华为][1]）

---

# 3. 主要规格

根据华为官方信息：

## 计算能力

低精度 AI 格式：

```
FP8
MXFP8
MXFP4
HiF8
```

峰值性能：

```
FP8：
约 1 PFLOPS

MXFP4：
约 2 PFLOPS
```

（[华为][2]）

对比：

```
                    FP8 AI 计算能力

NVIDIA H100       约 1 PFLOPS
NVIDIA H200       约 1 PFLOPS+
Ascend 950PR      约 1 PFLOPS
```

（具体对比高度依赖于工作负载和软件栈。）

---

# 4. 内存系统

950PR 采用：

```
Ascend 950 芯片
        |
        |
     HiBL 1.0
        |
        |
      HBM
```

华为针对预填充场景设计了成本更低的 HBM。

据称的目标参数：

```
内存：
约 128GB 级别

带宽：
约 1.4-1.6 TB/s
```

（[Investing.com][3]）

为何带宽低于 950DT？

因为预填充主要是：

```
大型矩阵乘法

Q、K、V 投影：

X @ Wq
X @ Wk
X @ Wv
```

主要受计算限制。

解码则是：

```
单个 token 生成

小型 GEMM
+
KV 缓存查找

内存带宽占主导
```

---

# 5. 互联

大型 AI 集群需要加速器之间的通信。

950 系列：

```
互联：
2 TB/s
```

华为采用自有互联技术，而非 NVIDIA NVLink。（[华为][1]）

对比：

```
NVIDIA H100 NVLink：
约 900 GB/s

H200：
约 900 GB/s

B200：
多 TB/s 级别
```

---

# 6. 软件栈

硬件只是 AI 加速的一半。

NVIDIA：

```
CUDA
 |
cuBLAS
 |
TensorRT
 |
PyTorch
```

华为：

```
CANN
 |
Ascend 算子
 |
MindSpore / PyTorch Ascend
 |
LLM 框架
```

（[华为][2]）

最大的挑战不在于 FLOPS。

而在于：

```
CUDA 生态系统
        vs
CANN 生态系统
```

例如：

一个 CUDA 内核：

```python
torch.matmul(q, k.transpose(-1,-2))
```

在 NVIDIA 上：

```
PyTorch
 |
CUDA 内核
 |
Tensor Core
```

在昇腾上：

```
PyTorch
 |
torch_npu
 |
CANN
 |
Ascend Cube Engine
```

软件成熟度至关重要。

---

# 7. 预期应用场景

## LLM 服务

示例：

```
Qwen
DeepSeek
Llama
```

部署：

```
用户请求
       |
       |
负载均衡器
       |
       |
Ascend 950PR 集群
       |
       |
预填充
       |
       |
950DT 集群
       |
       |
解码
```

---

## 推荐系统

企业如：

* 电商
* 短视频
* 广告

需要：

```
嵌入层
+
排序模型
+
大规模推理
```

950PR 面向此场景。

---

# 8. 与 NVIDIA 对比如何？

简化对比：

|          | Ascend 950PR                | NVIDIA H100/H200      |
| -------- | --------------------------- | --------------------- |
| 厂商     | 华为                        | NVIDIA                |
| 目标     | 推理                        | 训练 + 推理           |
| 优势     | 性价比推理                  | 生态系统              |
| 软件     | CANN                        | CUDA                  |
| 内存     | HiBL HBM                    | HBM3/HBM3e            |
| 集群     | SuperPod                    | NVLink/NVSwitch       |

---

# 9. 战略意义

Ascend 950PR 的意义并不在于直接击败 NVIDIA RTX/H100。

而在于：

```
中国 AI 基础设施自主可控

CPU：
鲲鹏

加速器：
昇腾

框架：
MindSpore

云：
华为云
```

华为正在构建一个全栈替代型 AI 生态系统。（[华为][2]）

---

## 对于 LLM 工程师的视角

有趣的部分并非芯片本身。

重要的问题在于：

```
昇腾能否高效运行：

DeepSeek-V3
Qwen3
Llama 4
混合专家模型（MoE）

```

胜出的平台很可能是：

```
硬件
+
编译器
+
分布式运行时
+
模型优化
```

而不仅仅是 TOPS/FLOPS。

参考文献：

* 华为昇腾路线图及规格（[华为][1]）
* 华为官方 Ascend 950 架构概述（[华为][2]）
* 路透社关于华为 AI 芯片路线图的报道（[reuters.com][4]）

[1]: https://www.huawei.com/en/news/2025/9/hc-xu-keynote-speech?utm_source=chatgpt.com "Groundbreaking SuperPoD Interconnect: Leading a New Paradigm for AI Infrastructure - Huawei"
[2]: https://www.huawei.com/cn/news/2025/9/hc-xu-keynote-speech?utm_source=chatgpt.com "以开创的超节点互联技术，引领AI基础设施新范式"
[3]: https://www.investing.com/news/stock-market-news/factboxkey-products-in-huaweis-ai-chips-and-computing-power-roadmap-4244325?utm_source=chatgpt.com "Factbox-Key products in Huawei’s AI chips and computing power roadmap By Reuters"
[4]: https://www.reuters.com/world/china/key-products-huaweis-ai-chips-computing-power-roadmap-2025-09-18/?utm_source=chatgpt.com "Key products in Huawei's AI chips and computing power roadmap"