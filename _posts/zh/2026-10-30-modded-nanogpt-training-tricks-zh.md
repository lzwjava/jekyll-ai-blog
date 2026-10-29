---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Modded-nanoGPT 训练技巧
translated: true
type: note
---

**问题：** modded-nanoGPT 使用哪些技巧来训练模型？

**回答：**

Keller Jordan 的 [Modded-nanoGPT](https://github.com/KellerJordan/modded-nanogpt) 是一个竞争性的“速度跑”基准——在 8×H100 上尽可能快地训练一个 124M GPT 风格模型，使 FineWeb 验证损失达到 ≤3.28。从最初耗时 45 分钟的 llm.c 基线开始，现在它在 40 秒内、使用不到 3.3 亿个 token 即可达到相同目标。这些技巧分为几类：

---

### 🏗️ 架构

核心架构改动包括：

- **旋转位置编码（RoPE）** 取代学习式位置嵌入
- **QK-Norm**（在点积之前对查询和键进行归一化）
- **ReLU²** 激活（对 ReLU 输出取平方）取代 GELU
- **解绑输出头与嵌入** — LM 输出头和 token 嵌入矩阵是独立的权重（在后续纪录中部分阶段重新绑定）
- **U-net 跳跃连接** — 从嵌入层到每个块的残差捷径，以及从第 3 块到第 6 块的直接跳跃
- **值嵌入** — 额外的学习嵌入混合到注意力值向量中（受 Zhou 等人 2024 启发）
- **长短滑动窗口注意力**（受 Gemma 2 启发），带有窗口大小预热调度和用于 RoPE 缩放的 YaRN
- **Smear 模块** — 通过将 token 嵌入向前涂抹一个位置来实现 1-token“回看”
- **稀疏注意力门控** — 对注意力进行稀疏门控
- **成对头注意力** — Q 和 K 矩阵按头成对正交化，而不是跨所有头正交化
- **部分键偏移**
- **哈希二元组 + 三元组嵌入表**（8460 万行跨 GPU 分片，使用符号技巧）
- **MUDD 跳跃连接** 到残差流和注意力值
- **可学习 XSA**
- **轻量动态可组合 MHA**
- **深度缩减和混合宽度注意力**（大多数层使用 64 维 QK，两层使用半宽 V）

---

### ⚙️ 优化器

最核心的优化器是 **Muon**（Newton-Schulz 动量正交化），应用于所有线性层。它的工作原理是取梯度，应用 Nesterov 动量，然后通过五次 Newton-Schulz 迭代对结果进行正交化——近似地将更新 `G` 替换为 `U @ V.T`，其中 `U, S, V = G.svd()`。对于这种训练场景，它比 Adam 内存占用更低、样本效率约提高 1.5 倍、墙钟开销低于 2%。

后续纪录在此基础上叠加：

- **NorMuon** — Muon 的归一化变体
- **Polar Express** — 替代 Newton-Schulz 正交化步骤
- **谨慎权重衰减**（带有与学习率绑定的调度）
- **ANVIL 优化器** — 双轨（快 + 慢）动量变体，带有重新推导的正交化映射和在慢轨上门控的谨慎衰减
- **尾部权重平均（EMA）** 带有提高的学习率下限
- **批量大小调度** 和 **最大序列长度调度**

---

### 🔢 精度 / 数值

- **FP8** 用于 LM 输出头、MLP 前向和反向传播以及 QKV 投影
- **非对称 logit 重新缩放** 和 **logit 软上限**（从 30 → 15 → 非对称逐步降低）
- **BFloat16 激活** 和交叉熵计算
- **零初始化投影**（muP 风格的输出投影零初始化）

---

### 📐 训练调度技巧

- 将训练批次起始与 **EoS token** 对齐，并设置 **最大文档长度**
- 对嵌入和 LM 输出头进行 **2 步梯度累积** 后再更新
- 最后 3 个注意力层使用 **单激活输入**
- **多 token 预测（MTP）** 辅助损失
- **前缀 token 预测** 辅助损失
- 在训练进行到 2/3 时 **解绑 embed/lm_head**
- 大部分训练阶段对共享候选集使用 **采样 softmax**
- **稀疏行式嵌入更新** — 仅交换和更新被触及的行

---

### 🚀 系统 / 内核技巧

- **FlexAttention**（将上下文从 1024 扩展到 64K），随后升级到 **Flash Attention 3**
- **计算与梯度通信重叠**（异步梯度全归约 → 归约散射）
- **融合 Triton 内核** 用于 ReLU²、软上限交叉熵、QK-norm + RoPE + KeyOffset
- **CUDA 图捕获** 整个训练步骤，包括优化器和 FP8 权重刷新
- **异步数据批次获取**

---

世界纪录已从 45 分钟一路降至 8×H100 上的 40 秒以内，每一次提升都记录在仓库的世界纪录表中。这是一个活着的基准，上述几乎每一个技巧都通过真实的耗时改进得到了验证。

**参考资料：**

- [KellerJordan/modded-nanogpt（GitHub）](https://github.com/KellerJordan/modded-nanogpt)
- [Muon 优化器说明](https://kellerjordan.github.io/posts/muon/)
- [世界纪录历史（wiki）](https://github.com/KellerJordan/modded-nanogpt/wiki)
