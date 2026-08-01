---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD硬件系列差异
translated: true
type: note
---

问题：AMD Instinct、Radeon 和 Ryzen 设备系列简介——它们有什么区别？

答案：

AMD 拥有多个硬件系列，因为它们针对不同的工作负载：

```
AMD
├── Ryzen      → 消费级 CPU（PC/笔记本）
├── EPYC       → 服务器 CPU
├── Radeon     → 消费级 GPU（游戏/工作站）
└── Instinct   → AI/HPC 加速 GPU（数据中心）
```

## 1. AMD Instinct — AI / HPC GPU

AMD Instinct 是 AMD 对标 NVIDIA Tesla/A100/H100/B200 的产品。

目标：

* LLM 训练
* AI 推理服务器
* 科学计算
* 超级计算机

示例：

| GPU    | 显存              | 内存类型 | 目标                 |
| ------ | ----------------- | -------- | -------------------- |
| MI50   | 16GB HBM2         | HBM      | 较旧 HPC             |
| MI100  | 32GB HBM2         | HBM      | HPC                  |
| MI200  | 64GB/128GB HBM2e  | HBM      | AI/HPC               |
| MI250X | 128GB HBM2e       | HBM      | 超级计算机           |
| MI300A | 128GB HBM3        | HBM      | HPC + AI             |
| MI300X | 192GB HBM3        | HBM      | LLM 训练/推理        |
| MI325X | 256GB HBM3E       | HBM3E    | 较新 AI              |

示例：

```
MI300X

192GB HBM3
|
├── 大模型权重
├── 大 KV 缓存
└── 高带宽推理
```

与消费级 GPU 相比的主要优势：

* 海量显存
* 极高的内存带宽
* 针对矩阵运算优化

MI300X：

```
显存：       192GB
带宽：       ~5.3 TB/s
FP16/BF16：  巨大吞吐量
```

一张 MI300X 可容纳许多需要多张 RTX 4090/5090 的模型。

---

## 2. Radeon — 消费级 GPU

AMD Radeon 与 NVIDIA GeForce 竞争。

目标：

* 游戏
* 桌面图形
* 视频编辑
* 部分 AI 工作负载

示例：

```
RX 7600
RX 7700 XT
RX 7800 XT
RX 7900 XTX
RX 9060 XT
```

架构：

```
RDNA
 |
 ├── RDNA 1
 ├── RDNA 2
 ├── RDNA 3
 └── RDNA 4
```

示例 RX 7900 XTX：

```
24GB GDDR6
384-bit 内存总线
RDNA 3
```

适用于：

* 游戏
* Stable Diffusion
* llama.cpp
* ROCm 实验（支持的模型）

不太适合：

* 大规模 LLM 训练
* 生产推理

因为：

* 显存较小
* 可靠性功能较弱
* 软件生态较弱

---

## 3. Ryzen — CPU

AMD Ryzen 不是 GPU。

示例：

```
Ryzen 9 7950X
Ryzen 7 7800X3D
Ryzen AI 300
```

用途：

* 台式机
* 笔记本
* 边缘 AI

架构：

```
Zen
 |
 ├── Zen 1
 ├── Zen 2
 ├── Zen 3
 ├── Zen 4
 └── Zen 5
```

典型的 AI 工作站：

```
Ryzen CPU
    |
    +-- RTX 4090
    |
    +-- 128GB RAM
```

CPU 准备数据，GPU 执行张量计算。

---

## 4. EPYC — 服务器 CPU

AMD EPYC 是 Ryzen 的企业级兄弟。

用于：

* 云服务器
* AI 集群
* 超级计算机

示例：

```
EPYC 9654

96 核
192 线程
12 通道 DDR5 内存
```

AI 服务器：

```
          EPYC CPU
             |
   ---------------------
   |        |          |
 MI300X   MI300X   MI300X
```

---

# NVIDIA 与 AMD 对照

| NVIDIA              | AMD 对应产品       |
| ------------------- | ------------------ |
| GeForce RTX         | Radeon RX          |
| RTX Professional    | Radeon Pro         |
| Tesla / A100 / H100 | Instinct MI 系列   |
| Xeon                | EPYC               |
| CUDA                | ROCm               |

---

# 对于 LLM 开发者

重要对比：

```
消费级 AI：

RTX 4070
RTX 4090
RX 7900 XTX

        ↓

实验/微调
```

```
生产级 AI：

A100
H100
B200
MI300X
MI325X

        ↓

训练数十亿/万亿参数模型
```

你的 RTX 4070：

```
12GB 显存
CUDA
优秀的生态
```

适用于：

* nanoGPT
* nano-vLLM
* LoRA
* QLoRA 7B/8B 模型

MI300X：

```
192GB 显存
HBM3
ROCm
```

适用于：

* DeepSeek 规模推理
* Qwen 大模型
* 分布式训练

---

主要的架构差异：

**Radeon = 图形优先 GPU**

```
像素 → 着色器 → 游戏
```

**Instinct = 张量优先加速器**

```
矩阵乘法 → AI 模型
```

对于 AI 基础设施，Instinct 是 AMD 最重要的系列。它是 AMD 直接与 NVIDIA 的 AI 数据中心垄断地位竞争所使用的硬件。
