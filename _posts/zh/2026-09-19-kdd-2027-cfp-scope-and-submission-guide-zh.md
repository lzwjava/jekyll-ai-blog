---
audio: false
generated: true
image: false
lang: zh
layout: post
title: KDD 2027 征文范围与投稿指南
translated: true
type: note
---

问题：**KDD 2027 研究轨道 CFP 实际上要求什么，你应该注意什么？**

答案：

我阅读了官方 CFP。重点是 **KDD 研究比经典的“数据挖掘”要广泛得多。** 2027 年 CFP 明确包含现代 LLM/推理工作、可扩展 AI 系统、RL、生成和基础模型。（[KDD 2027][1]）

### 1. 范围与你的工作非常相关

CFP 明确列出了：

*   **In-context learning**
*   **Prompt engineering**
*   **Continual learning**
*   **Few-shot adaptation**
*   **Reinforcement learning**
*   **Generation and reasoning**
*   **LLMs**
*   **Multimodal foundation/frontier models**
*   **Emergent reasoning**
*   **Neural-symbolic integration**
*   **Hypothesis generation**
*   **Scalable AI systems / infrastructure**
*   Distributed computing
*   Scheduling/orchestration
*   ML systems

因此，诸如 **reasoning models、RL with verifiable rewards、Lean/code-based verification、inference systems、agent systems、training infrastructure** 等内容，如果有真正的研究贡献，完全可以纳入研究轨道。（[KDD 2027][1]）

关键短语是：

> **“innovative research”**

一篇论文不能仅仅是 *“我用 GPT-5 构建了一个 agent，并且它有效。”* 你需要一个能够推动知识进步的技术想法。

---

### 2. 最大的限制：8 页主论文

提交格式为：

```text
PDF
├── 8 页主论文       <-- 审稿人将据此评判
├── 参考文献
└── 附录              <-- 页数不限
```

前 **8 页必须自成一体**。附录可以包含证明、实现细节、伪代码、可重复性材料等。（[KDD 2027][1]）

这实际上是一种有用的思考 KDD 论文的方式：

```text
问题
   ↓
观察
   ↓
新想法
   ↓
方法
   ↓
实验
   ↓
证据
   ↓
为什么这改变了我们的理解
```

你没有 30 页来慢慢解释项目。

---

### 3. 他们关心的是研究贡献，而不仅仅是工程

他们的决策因素包括：

```text
technical merit
originality
potential impact
quality of execution
quality of presentation
related work
reproducibility
ethics
```

（[KDD 2027][1]）

例如，比较：

**弱研究框架**

> 我们用 RL 训练了一个 7B 推理模型，获得了 5% 的性能提升。

对比：

**研究框架**

> 我们发现可验证推理任务中的 reward sparsity 会导致一种特定的失败模式。我们引入了 X，它以可衡量的方式改变了探索轨迹的分布。在 N 个推理环境中，X 将样本效率提高了 Y%，并且我们提供了一个分析来解释原因。

第二种有一个实际的 **科学主张**。

---

### 4. 你的 RL + Lean 想法非常自然地契合范围

你之前的想法：

```text
LLM
 ↓
生成推理 / 证明 / 代码
 ↓
Lean / 编译器 / 执行
 ↓
可验证奖励
 ↓
RL
 ↓
更好的推理策略
```

几乎就在 CFP 列出的主题中：

```text
reinforcement learning
generation
reasoning
LLMs
neural-symbolic integration
```

（[KDD 2027][1]）

但有趣的论文不是：

> “我们使用 Lean 作为奖励函数。”

这已经是一个显而易见的方向。

研究问题需要更深入，例如：

```text
为什么基于验证器的 RL 有效？

什么样的验证器能产生最好的学习信号？

验证器奖励可以有多稀疏？

部分证明验证能否提供更好的 credit assignment？

失败的证明能否转化为有用的密集奖励？

验证器反馈如何改变模型的探索分布？

我们能否预测哪些生成的轨迹值得进行 RL 训练？

当验证器具有不同的粒度级别时会发生什么？
```

那些是 **研究问题**。

---

### 5. 还有一个 System 角度

鉴于你对 LLM 基础设施的兴趣，另一个可能的 KDD 方向是：

```text
推理模型
      ↓
轨迹生成
      ↓
验证器
      ↓
奖励提取
      ↓
RL 训练
```

并优化实际系统：

```text
GPU 利用率
↓
轨迹吞吐量
↓
验证吞吐量
↓
KV-cache 复用
↓
分布式 rollout
↓
RL 训练效率
```

CFP 明确欢迎 **大规模 AI 的系统与基础设施**，包括分布式计算、编排与调度。（[KDD 2027][1]）

因此，一篇论文可能涉及类似以下内容：

> **Efficient Verifier-Guided Reinforcement Learning for Large-Scale Reasoning Models**

其中新颖性实际上在于训练/rollout/验证器架构。

---

### 6. 重要：KDD 不想要综述

CFP 明确表示，其目的仅仅是全面总结现有主题的综述论文 **超出范围**。（[KDD 2027][1]）

因此：

```text
❌ "A Survey of RL for Reasoning Models"

❌ "A Comprehensive Review of Lean + LLM"

❌ "The State of AI Agents in 2027"
```

不会仅仅因为它们有趣而适合研究轨道。

但是：

```text
✅ 新算法
✅ 新训练方法
✅ 新的经验发现
✅ 新模型/系统架构
✅ 新的理论见解
```

可以。

---

### 7. 双盲评审非常严格

你的提交不能透露：

```text
作者姓名
所属机构
身份信息
致谢
明显的自我识别
```

他们特别推荐：

```latex
\documentclass[sigconf,anonymous,review]{acmart}
```

（[KDD 2027][1]）

有趣的是，**允许并推荐**使用匿名化的 GitHub 仓库，尽管这不是强制的。（[KDD 2027][1]）

---

### 8. 对你来说很重要的一件事：OpenReview 个人资料

每位作者都需要一个足够完整的 OpenReview 个人资料。

CFP 指出缺失所需的个人资料信息本身就可能导致 **直接拒稿**。

所需信息包括：

```text
当前/过去所属机构（5 年内）
个人主页
DBLP
ORCID
导师
近期出版物
```

视情况而定。（[KDD 2027][1]）

没有机构邮箱的新 OpenReview 账户也可能需要 **最多两周** 进行审核。（[KDD 2027][1]）

所以如果你真的瞄准 KDD，这件事需要尽早设置，而不是在提交前一周。

---

### 9. 当前时间线

对于 **KDD 2027 第一轮**：

| 事件         | 日期                         |
| ------------ | ---------------------------- |
| 摘要         | **2026 年 7 月 19 日**       |
| 论文         | **2026 年 7 月 26 日**       |
| 反驳         | **2026 年 9 月 29 日 – 10 月 13 日** |
| 通知         | **2026 年 11 月 14 日**      |
| 会议         | **2027 年 8 月 1–5 日，圣何塞** |

所有提交截止时间均为 **Anywhere on Earth (AoE)**。（[KDD 2027][1]）

考虑到今天的日期，**第一轮的论文截止日期已经过了**。CFP 表示 KDD 每年有两个提交轮次，因此对于新论文来说，相关机会是后续轮次，而不是现在尝试提交到第一轮。（[KDD 2027][1]）

### 10. 最重要的区别

我会将整个 CFP 简化为：

```text
             KDD 研究
                  │
        ┌─────────┴─────────┐
        │                   │
    工程              研究
        │                   │
"我们构建了 X"     "我们发现了 X"
        │                   │
基准测试             假设
实现              机制
系统               算法
                   证据
                   分析
```

对于 **你**，我会按照以下思路思考：

```text
想法
 ↓
最小实现
 ↓
运行实验
 ↓
发现一些令人惊讶的东西
 ↓
制定假设
 ↓
设计对照实验
 ↓
将发现转化为算法
 ↓
撰写 KDD 论文
```

而不是：

```text
选择 KDD 主题
 ↓
构建一些东西
 ↓
写论文
```

第一种工作流程更符合这个 CFP 的要求。

**官方 CFP：** [KDD 2027 Research Track — Call for Papers](https://kdd2027.kdd.org/research-track-call-for-papers/?utm_source=chatgpt.com)

参考文献：

* [KDD 2027 Research Track CFP](https://kdd2027.kdd.org/research-track-call-for-papers/?utm_source=chatgpt.com)
* [KDD 2027 official site](https://kdd2027.kdd.org/?utm_source=chatgpt.com)

[1]: https://kdd2027.kdd.org/research-track-call-for-papers/ "Research Track: Call for Papers – KDD 2027"