---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 技嘉MZ01-CE1人工智能搭建指南
translated: true
type: note
---

**问题：** 这块技嘉 MZ01-CE1 主板用于 AI GPU 工作负载表现如何？

**回答：**

技嘉 **MZ01-CE1** 是一款**服务器/工作站主板**，并非普通消费级主板。以2800元的价格来看，它其实是一个非常有趣的AI构建平台。

![Image](https://images.openai.com/static-rsc-4/KkHGmOyr3gvD6nYYg6gOkUlqc4I_SOg6ZXfX5FUKuETK_dLx00yN5XircZBlVh9yzfbeSTUDk6o0_Dh9PQddqK7l1StdTqsmvwuDJp3bmt73q8WLVcBpCYzReAiKWYOHkPbrakKQev-cqtLOun2EW2RJN59ucKBdYB91eri_s3R-dXzfhTvALhthyJ3UFxNO?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/pRm-m-_dyzEmrGw94fAcITZMtGFRa_8TUJ_91PWiv-H_pNapr_NbfzHrThE1ModOBxNmXMw7q4xp6PNRfSVOQC9gTQlD1JPg_RY3qe5F6pMBZtx-GPrPEcb1j4eq8Y14gVUIdN-apMSm0Jhvb5fb-Vnuk6yxmsfBJWN4VyKtV06O_s3PtIpcHajD0BvOS5zA?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/4wHvEU8F4m2ZwW_tgqHF_YsaSDZrFKvBd6Ss0ph7zp-cQpJZcNwmIcvKgsLM-a8nFncKGlHlta8SQSFQcAA-zsmrRJhnIRbAs8ftVDWCDzZ1rEFFXOvIO1Yjh6UIhbugc1WUuJFJQxKUtuNTwew1U4psepnBrFXsic9qtnAKI_xGy4vgVgamEX_jprYaDJWM?purpose=fullsize)

### 核心规格

| 项目        | 详情                              |
| ----------- | --------------------------------- |
| CPU 插槽    | AMD SP3                           |
| CPU 支持    | EPYC 7002 Rome / EPYC 7003 Milan |
| CPU 核心数  | 最高64核 (如 EPYC 7763)           |
| 内存        | 8通道 DDR4 ECC RDIMM              |
| PCIe        | PCIe 4.0                          |
| GPU 支持    | 4 × PCIe x16 插槽                 |
| 外形规格    | 服务器/工作站                     |
| 价格        | 全新2800元                        |

关键点在于：

**EPYC + PCIe 4.0 + ECC 内存 + 4块GPU** 正是小型AI服务器所采用的架构。

---

## 与您的 i9-13900KF + B760M 配置对比

您当前的配置：

```
i9-13900KF
DDR5
RTX 4070
消费级主板
```

优点：

* 单线程性能非常快
* 游戏
* 开发

不足：

* PCIe 通道数有限
* 无 ECC 内存
* 两块 GPU 已显困难
* 内存带宽受限

MZ01-CE1：

```
EPYC Milan
      |
128条 PCIe 4.0 通道
      |
GPU1 x16
GPU2 x16
GPU3 x16
GPU4 x16

8通道 ECC 内存
```

更适用于：

* 多GPU推理
* 分布式训练
* LLM 服务
* CUDA 工作负载

---

## 搭配什么 GPU 比较合理？

### 4 × RTX 3090

非常有趣：

```
4 × RTX3090
= 96GB 显存
```

可以运行：

* 量化版 Llama 70B
* 量化版 Qwen 72B
* DeepSeek 模型
* 大型嵌入系统

用于训练：

* LoRA 微调
* 小型模型预训练
* 多模态实验

---

### 4 × RTX 4090

性能极强：

```
4 × RTX4090
= 96GB 显存
```

性能接近老款 A100 系统。

但：

* 功耗约1800W
* 散热问题严峻
* 消费级显卡体积较大

---

### 4 × RTX 4070

您当前的 GPU：

```
4 × RTX4070
= 48GB 显存
```

适用于：

* Qwen 14B/32B
* 编码代理
* vLLM 服务
* 多用户并发

---

## EPYC CPU 选择

二手市场：

### EPYC 7302

16核/32线程

价格便宜。

### EPYC 7402

24核/48线程

不错。

### EPYC 7543

32核/64线程

性能出色。

### EPYC 7763

64核/128线程

性能怪兽。

对于AI推理而言，CPU的重要性低于GPU，因此不必过度消费。

---

## 隐藏成本

主板本身便宜，但整个生态系统并不便宜。

您需要：

### ECC RDIMM 内存

示例：

```
256GB DDR4 ECC RDIMM
8 × 32GB
```

二手价格约1500-2500元。

### EPYC CPU

示例：

```
EPYC 7543
二手约2000-3000元
```

### 电源 (PSU)

4块GPU：

```
RTX3090 ×4
≈ 1400W GPU功耗

需要：
1600W-2000W 电源
```

### 机箱

服务器主板通常需要：

* E-ATX 机箱
* 良好的风道
* 较大的GPU间距

---

## AI Token 速度预期

示例：4× RTX3090：

在 Llama/Qwen 推理场景下：

```
Qwen2.5-72B INT4

单块 RTX3090：
约10-15 tok/s

4块 RTX3090：
约35-50 tok/s
```

并非线性提升，因为GPU之间通过PCIe通信，而非NVLink。

针对 LoRA 训练：

```
7B 模型：
非常轻松

32B：
可行

70B：
有难度，但可通过技巧实现
```

---

## 与您之前问到的技嘉 G292-Z20 对比

G292-Z20：

```
2U 服务器
8块GPU
双路CPU
2200W 冗余电源
```

是一台真正的数据中心机器。

MZ01-CE1：

```
塔式/工作站
4块GPU
单路 EPYC
```

更适合家庭实验室。

对于AI创业者/研究实验室：

我实际上更倾向于 MZ01-CE1。

为什么？

* 更静音
* 电费更低
* 维护更方便
* GPU容量足够

---

我对您使用场景的排序：

1. 🥇 **MZ01-CE1 + EPYC + 4× RTX3090**

   * 最佳 DIY AI 工作站

2. 🥈 二手服务器 + 8块GPU

   * 容量更大，麻烦更多

3. 🥉 消费级 B760 + 多块GPU

   * 受限于 PCIe 瓶颈

以2800元的价格，主板本身是一笔划算的交易——**前提是卖家确实提供3年质保，且不是工程样品**。真正花钱的大头在于为其配备 CPU/内存/GPU。
