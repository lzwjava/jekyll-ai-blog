---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 测试时缩放与RL推理
translated: true
type: note
---

**问题：** 解释向 test-time compute scaling + RL refinement 的范式转变，以及像 o3、DeepSeek-R1 和 Gemini 2.0 Flash Thinking 这样的模型如何利用 RL 来教授推理。

---

**答案：**

## 旧范式 vs. 新范式

### 旧范式 — “训练更大，推理更快”

```
Training (expensive) → Fixed model weights → Single-pass answer (cheap)
```

- 扩大参数、数据和训练计算量
- 推理时：一次前向传播 → 一个答案
- RL 仅用于**alignment（对齐）**（RLHF）：让模型变得礼貌、安全、有用

### 新范式 — “训练如何思考，在推理时投入计算”

```
Training (RL teaches reasoning) → Model that can THINK → Extended reasoning at inference → Better answer
```

- RL 用于教模型**如何推理**，而不仅仅是如何表现
- 推理时：模型在回答之前会花费可变的计算量来“思考”
- 更多的思考时间 → 在困难问题上得到更好的答案

---

## 1. 什么是 Test-Time Compute Scaling？

核心洞察：

> **你并不总是需要更大的模型——你需要一个思考时间更长的模型。**

与其让模型变得更大（training-time scaling），你允许模型在生成最终答案之前**生成长长的内部 reasoning trace**。

```
[User Question]
      ↓
  [Think... think... think... verify... backtrack... try again...]
      ↓
  [Final Answer]
```

这样做之所以强大，是因为：
- 困难问题（数学、代码、逻辑）**需要探索**，而不仅仅是模式匹配
- 错误可以在**思考过程中被发现并纠正**
- 模型可以**生成并验证多条解题路径**

---

## 2. RL 如何教授推理（机制）

传统的 RLHF 基于**人类偏好**训练：

> “人类更喜欢哪个答案？” → 奖励信号 → 更新模型

用于推理的 RL 基于**带有可验证奖励的结果正确性**训练：

```
Model generates a chain-of-thought reasoning trace
        ↓
Final answer is checked against ground truth
        ↓
Reward = +1 if correct, -1 if wrong (or partial for partial credit)
        ↓
RL updates the model to produce reasoning traces that lead to correct answers
```

这被称为 **RLVR（RL with Verifiable Rewards，带可验证奖励的强化学习）**——它之所以有效，是因为数学/代码有**客观、可检查的答案**，不需要人工标注者。

### Key Components:

| 组件 | 作用 |
|-----------|------|
| **Process Reward Model (PRM)** | 对推理中的每一步打分，而不仅仅是最终答案 |
| **Outcome Reward Model (ORM)** | 仅对最终答案打分（更简单但噪声更大） |
| **推理时的 MCTS / Beam Search** | 探索多条推理路径，选择最佳路径 |
| **Self-consistency / Majority voting** | 采样 N 个解决方案，选择最常见的答案 |

---

## 3. 每个模型如何实现这一点

### 🔵 OpenAI o1 / o3

- 训练模型生成**隐藏的 chain-of-thought**（o1 中不向用户展示，o3 中部分展示）
- 在训练期间使用带**搜索**的 RL 来寻找能导向正确答案的 reasoning trace
- 推理时：模型“思考”可变的时长（几秒到几分钟）
- **o3** 将这一点大幅扩展——在 ARC-AGI 基准上，更多计算时间 = 显著更好的分数
- reasoning trace 就像是模型的**草稿纸（scratchpad）**——它可以写下公式、检查步骤、放弃错误的路径

```
o3 performance on ARC-AGI:
Low compute  → ~75%
High compute → ~87%
         ↑
   Same model, more thinking time
```

### 🟠 DeepSeek-R1

- 使用 **GRPO（Group Relative Policy Optimization）**——一种更高效的 PPO 变体
- 关键创新：训练时**没有预先构建 reward model**——只使用可验证的数学/代码答案
- 模型**自发形成了**以下行为：
  - 自我反思（Self-reflection）（“等等，让我重新考虑一下……”）
  - 回溯（Backtracking）（“那个方法错了，换个思路……”）
  - 验证（Verification）（“让我检查一下：3 × 7 = 21 ✓”）
- 这些“啊哈时刻”行为**源于 RL**，而不是来自监督训练
- 开源，以一小部分成本即可与 o1 竞争

### 🟢 Gemini 2.0 Flash Thinking

- 谷歌基于 RL 训练的扩展 chain-of-thought 实现
- 向用户展示 reasoning trace（透明思考）
- 针对**速度**优化（Flash = 比 Pro/Ultra 更快），同时仍能深度推理
- 使用 RL 来学习何时多思考、何时少思考（adaptive compute）

---

## 4. 为什么这是一次范式转变

### 以前：Scaling Law 是关于训练的

```
More parameters + More data + More training FLOPs = Better model
```

（Chinchilla scaling laws，GPT-3 → GPT-4）

### 现在：Scaling 有两个维度

```
Axis 1: Training compute (bigger model, more data)
Axis 2: Inference compute (more thinking time per question)
```

这意义重大，因为：
- **推理计算量是灵活的**——你可以把更多计算花在困难问题上，花在简单问题上的更少
- **RL 解锁了新的能力上限**——一个推理能力强的小模型可以击败一个不擅长推理的大模型
- **它改变了经济性**：与其训练一个大 10 倍的模型，不如在困难问题上让同一个模型运行 10 倍的时间

---

## 5. 可视化总结

```
TRAINING TIME:
┌──────────────────────────────────────────────────┐
│  RL generates thousands of reasoning traces      │
│  Verifiable reward (correct/wrong) guides model  │
│  Model learns: good reasoning → correct answers  │
└──────────────────────────────────────────────────┘
                        ↓
                  Model Weights
                        ↓
INFERENCE TIME:
┌─────────────────────────────────────────────────────────────────┐
│ Question → [Explore path A... dead end]                         │
│           → [Explore path B... looks promising...]              │
│           → [Verify step 3... error found, fix it...]           │
│           → [Path B leads to solution ✓]                        │
│           → Final Answer                                         │
└─────────────────────────────────────────────────────────────────┘
   ^                                                    ^
   More time here                            Better answer here
```

---

## 6. 这对未来的意义

- **RL 对前沿模型不再是可选项**——它是构建推理能力的方式
- **数学和代码**是切入点（可验证奖励），但该技术正在扩展到**科学、医学、法律**
- 现在的竞争核心是：谁能训练出最好的 *reasoner*（推理者），而不仅仅是谁的模型最大
- 具有强大 RL 推理能力的小模型（DeepSeek-R1 7B）可以与大得多的非推理模型竞争

---

**参考文献：**

- [DeepSeek-R1 Paper: Incentivizing Reasoning via RL](https://arxiv.org/abs/2501.12948)
- [OpenAI o3 and Test-Time Compute Scaling (OpenAI Blog)](https://openai.com/index/openai-o3-mini/)
- [Scaling LLM Test-Time Compute Verbosely (Google DeepMind, 2024)](https://arxiv.org/abs/2408.03314)
- [Let's Verify Step by Step — Process Reward Models (Lightman et al.)](https://arxiv.org/abs/2305.20050)
- [GRPO: Group Relative Policy Optimization (DeepSeek)](https://arxiv.org/abs/2402.03300)