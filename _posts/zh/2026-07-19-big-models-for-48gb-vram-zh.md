---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 面向48GB显存的大模型
translated: true
type: note
---

问题：48GB显存（2×RTX 3090）能运行哪些大模型？

答案：

两张RTX 3090提供：

* **显存：** 24GB × 2 = **48GB**
* **内存带宽：** 每张卡约936 GB/s → 总计约1.9 TB/s（取决于并行方式）
* **FP16算力：** 每张约35.6 TFLOPS → 总计约71 TFLOPS
* **NVLink：** RTX 3090支持（与RTX 4070不同），可为支持的工作负载提升GPU间内存带宽

LLM推理的关键约束是：

```
模型内存 ≈ 参数量 × 每参数字节数 + KV缓存 + 运行时开销
```

典型大小：

| 模型 |  FP16 |  INT8 | 4-bit |
| ---- | ----: | ----: | ----: |
| 7B   |  14GB |   7GB |   4GB |
| 13B  |  26GB |  13GB |   7GB |
| 34B  |  68GB |  34GB |  17GB |
| 70B  | 140GB |  70GB |  35GB |
| 100B | 200GB | 100GB |  50GB |

所以48GB显存实际上是一个非常有趣的区间。

## 运行舒适的模型

### Qwen3 / Qwen2.5 32B

示例：

* Qwen3-32B
* Qwen2.5-Coder-32B

4-bit：

```
32B × 0.5 字节 ≈ 16GB
```

加上KV缓存：

```
约20-25GB
```

单张3090几乎可以运行，两张卡轻松运行。

良好用途：

* 编程代理
* 本地Copilot
* RAG
* LoRA微调

---

## 70B类模型

这正是48GB显存发挥作用的地方。

示例：

* Llama 3.1 70B
* Qwen2.5-72B
* DeepSeek-R1-Distill-70B

4-bit：

```
70B × 0.5 字节 = 35GB
```

运行时开销：

```
+5-10GB
```

总计：

```
40-45GB
```

因此：

```
2 × RTX3090 = 可行
```

典型设置：

```
GPU0: 24GB
GPU1: 24GB

llama.cpp:
--split-mode layer
```

或

```
vLLM tensor parallel = 2
```

你可以在本地运行70B量化模型。

---

## DeepSeek模型

一个有趣的案例。

### DeepSeek-V3

671B参数。

即使是4-bit：

```
671B × 0.5 字节
≈ 335GB
```

需要：

```
约8-10张RTX3090
```

不实用。

但：

### DeepSeek-R1-Distill-Qwen-32B

非常实用：

```
32B
4-bit
```

2×3090：

效果极佳。

---

## 训练 / 微调

48GB甚至更有趣。

### LoRA微调

可行：

* 7B全量微调
* 14B LoRA
* 32B LoRA
* 70B LoRA（需激进设置）

示例：

Qwen2.5-Coder-32B：

```
基础模型：
32B × 2 字节 = 64GB FP16

LoRA：
仅训练适配器

显存：
约35-45GB
```

2×3090可行。

---

## 与你的RTX 4070 12GB对比

你当前的显卡：

```
RTX4070
12GB显存
```

可运行：

* 7B FP16
* 14B Q4
* 32B Q4（勉强，需卸载）

2×3090改变了游戏规则：

```
12GB → 48GB
```

提升了4倍。

实际跨越：

```
7B模型
        ↓
32B模型
        ↓
70B量化模型
```

这是巨大的能力提升。

---

## NVLink说明

RTX 3090支持NVLink：

```
3090 GPU0
    |
 NVLink桥接器
    |
3090 GPU1
```

但：

* CUDA内核需要利用它
* PyTorch Distributed可使用NCCL
* llama.cpp可多GPU运行，无需NVLink

对于推理：

```
PCIe x16 + x16
```

通常已经足够。

对于训练：

NVLink更有帮助。

---

针对你的用例（训练小型GPT、代理、本地模型），**2×3090很可能是二手GPU市场的甜点**：

* 48GB显存
* CUDA生态
* 二手价格便宜
* 可运行Qwen3-32B / Qwen2.5-Coder-32B
* 可运行70B Q4推理
* 可进行正经LoRA训练

它基本上就是“穷人的A6000 48GB”配置。