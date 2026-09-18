---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Edge0-35B-A3B-preview 设备端MoE
translated: true
type: note
---

**问题：** <https://huggingface.co/Edge0/Edge0-35B-A3B-preview> 的模型是什么？

**答案：**

**Edge0-35B-A3B-preview** 是一个稀疏混合专家（MoE）语言模型，专为**边缘/设备端推理**而设计——其最突出的特点是能在 **3 GiB 活跃内存** 以下运行 35B 参数模型。

以下是对其亮点的详细解析：

**架构与基础**
它基于 **Qwen3.6-35B-A3B** 作为基础模型构建，具有 40 层、256 个专家（每个 token 激活 4 个），隐藏大小为 2048。

**关键创新**
该模型使用三种技术，在可用速度下实现低内存占用：

1. **SSD 专家卸载** —— 专家权重按需从存储中流式传输，因此 RAM 仅保存当前激活的权重，而不是整个模型。
2. **预路由器（Prerouter）** —— 一个经过训练的头会提前一步预测专家路由，使专家加载与前向传播重叠而非停滞，从而实现高达 +59% 的解码吞吐量提升。
3. **Recover-LoRA** —— int4 基础模型被冻结，通过从 FP16 教师模型蒸馏来训练 LoRA 适配器，在 4 比特下恢复了大部分量化损失。

**性能（在 Mac mini M4 Pro 上）**
解码速度为 14.9–17.7 tok/s，预填充吞吐量为 113–140 tok/s，峰值活跃内存仅为 **2.9 GiB**。

**质量**
与 fp16 基础模型相比，int4 + 适配器流水线平均仅损失 **3.9 分**，在 AIME 2026 上得分为 86.6，在 HumanEval 上为 90.9，在 GPQA-Diamond 上为 79.8。

**局限性**
这是一个预览版本——智能体能力（工具使用、多步规划）目前较弱，且 MLX 后端目前仅支持 **Apple Silicon**。

**参考链接：**

- [Edge0/Edge0-35B-A3B-preview — Hugging Face](https://huggingface.co/Edge0/Edge0-35B-A3B-preview)
- [arXiv 论文：2609.18063 — The Other Half of the Memory Wall](https://arxiv.org/abs/2609.18063)
- [Edge0-AI GitHub 仓库](https://github.com/Edge0-AI/edge0)
