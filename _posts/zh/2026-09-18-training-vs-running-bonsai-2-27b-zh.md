---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 培育盆景与制作盆景 2 27B
translated: true
type: note
---

**问题：** 训练像 Ternary Bonsai 2 27B 这样的模型需要什么设备或多少 FLOPS？

**回答：**

这里有一个重要区别：**Bonsai 2 27B 并非从头训练——它是在 Qwen3.8-27B 基础上进行后训练量化得到的**，因此原始预训练算力属于阿里巴巴 Qwen 团队。这里涉及两个独立的算力问题。

---

## 1. 基座模型预训练（Qwen3.8-27B）——由阿里巴巴完成

Qwen3.8-27B 的发布并未包含模型专属的技术报告、训练 token 数量、数据集清单或训练算力数据，因此确切数字未公开。不过，我们可以使用标准公式进行估算。

**预训练 FLOPs 的 Kaplan/Chinchilla 公式：**
> `FLOPs ≈ 6 × N × D`
> 其中 N = 参数量，D = 训练 token 数

一个 27B 模型在约 10–15 万亿 token（遵循 LLaMA 3 风格的典型现代“过训练”规模）上训练，结果大致如下：

| Token 预算 | 估算 FLOPs |
|---|---|
| 540B token（Chinchilla 最优，20×N） | ~8.7 × 10²³ FLOPs |
| 5T token（中度过训练） | ~8.1 × 10²⁴ FLOPs |
| 15T token（LLaMA 3 规模） | ~2.4 × 10²⁵ FLOPs |

**实现此规模的合理硬件：**

在 512 张 H100 GPU 上以 BF16 训练 LLaMA 70B，每 1 万亿 token 大约需要 109 天。一个 27B 模型每个 token 的算力大约是 70B 的 ~40%，因此在 512 张 H100 上运行 5T token 的任务大约需要 **~90–120 天**。实际上，前沿实验室会使用 **512–2048 张 H100/H200 GPU** 组成的集群，将实际运行时间控制在数周而非数月。

对于一个严肃的 27B 预训练任务，实际可行的最小集群配置：

- **最低可行：** 64–128 张 H100 80GB（实际运行时间数月）
- **实际可行：** 256–512 张 H100 80GB（约 4–8 周）
- **快速：** 1024+ 张 H100/H200（约 1–2 周）

---

## 2. Prism ML 的工作：三元量化（后训练）

Prism ML 的贡献是在现有 Qwen3.8-27B 权重基础上进行**量化感知训练 / PTQ（后训练量化）**——将 FP16 权重转换为包含 Hadamard 旋转的 {−1, 0, +1} 三元值。这比预训练的计算量小得多：

- 不需要在数万亿 token 上从头训练
- 在更小的数据集上运行校准/微调过程
- Hadamard 旋转离线计算后并入存储的权重

这个阶段的粗略估算：**数十到数百 H100 GPU 小时**，而预训练则需要数百万 GPU 小时。Prism ML 尚未公布该阶段的确切数据。

---

## 总结表

| 阶段 | 执行方 | 硬件 | 估算 FLOPs | 实际运行时间 |
|---|---|---|---|---|
| 预训练 Qwen3.8-27B | 阿里巴巴 | ~256–2048 张 H100 | ~10²⁴–10²⁵ | 数周–数月 |
| 三元量化（Bonsai） | Prism ML | 数十–数百张 H100 | ~10²¹–10²² | 数天 |
| **运行推理** | **你** | **单张 M5 Pro / RTX 4090** | **不适用** | **~47 tok/s** |

核心结论：**运行** Bonsai 2 27B 对于拥有现代笔记本电脑或单张消费级 GPU 的任何人来说都是可行的。**复现基座模型的预训练**则是一项耗资数百万美元、需要数百张 GPU 的工程。

---

**参考来源：**
- [Bonsai 2 27B 模型卡 — Hugging Face](https://huggingface.co/prism-ml/Ternary-Bonsai-2-27B-gguf)
- [从头训练一个 70B LLM 的成本（2026）— Spheron](https://www.spheron.network/blog/cost-to-train-70b-parameter-llm-from-scratch-2026/)
- [NVIDIA NeMo LLaMA 3.1 训练基准](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/dgxc-benchmarking/resources/nemo-llama31-dgxc-benchmarking-g)
- [Chinchilla Scaling Laws — Hoffmann et al.](https://arxiv.org/abs/2203.15556)