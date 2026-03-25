---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基于标签的 AI 代理记忆检索
translated: true
type: note
---

问题：考虑到加载过多无关的 context 会降低 LLM 的响应质量，使用基于 tag 的检索系统（LLM + database search）来作为 AI agent memory 的方法是否正确？

回答：

## 你完全正确 —— 这被称为 RAG + Tag-Based Memory

---

### 你识别出的核心问题

| 问题 | 发生原因 |
|---|---|
| 加载了过多 context | LLM 失去焦点，出现 "lost in the middle" 问题 |
| 无关的 context | 显著降低响应质量 |
| Long context ≠ 良好的 memory | LLM 对所有 token 的处理权重基本一致，缺乏真正的“重要性加权” |
| 无跨 session memory | 默认情况下，每个 session 都是从空白开始的 |

**"lost in the middle"** 研究论文 (Liu et al., 2023) 证实了这一点 —— LLM 在处理位于长 context **中间位置的信息时表现最差**。大脑的运作方式则相反：它会主动抑制无关信息并提取相关信息。

---

### 你的 Tag-Based 解决方案 —— 正确的架构

```
User Prompt
    ↓
[LLM] 生成 tags + topics（例如："python, async, bug-fix, 2024-march"）
    ↓
[Vector DB / Tag Index] 通过 tags 搜索之前的 10k 个 sessions
    ↓
返回 Top-K 相关 sessions（例如：仅限前 5-10 个）
    ↓
[LLM] 仅使用这些检索到的相关 chunks 进行回答
```

这本质上是在 **RAG (Retrieval-Augmented Generation)** 之上叠加了 **tag-assisted retrieval**。

---

### 为什么 Tags 比纯 Vector Search 更有帮助

- **Vector search** 寻找语义相似的文本 —— 虽然不错，但可能会错过精确的话题匹配
- **Tags** 是显性的、分类化的，且索引和搜索速度极快
- **组合方案** = tags 缩小候选池 → vector search 进行重排序 (re-rank) → 只有最相关的 chunks 进入 context

这保证了 context **体积小、相关性强且质量高**。

---

### 现实系统的做法（你想法的生产环境落地）

| 系统 | 方法 |
|---|---|
| **MemGPT / OpenMemory** | 带有 retrieval 的层级化 memory，而非加载全部 context |
| **LangChain Memory** | Summary + store，按相关性 retrieve |
| **Mem0** | 每个 session 进行 Entity + tag 提取，结合 vector search |
| **Claude's memory feature** | 提取关键事实，存储为结构化笔记 |
| **OpenClaw / Claude Code** | 目前较受限 —— 主要是单次 session |

所有严肃的 memory 系统都遵循你的逻辑：**绝不加载所有内容，始终有选择性地进行 retrieve**。

---

### 你捕捉到的关键见解

> **大脑 = 联想式、并行的、主动抑制噪声**
> **LLM = 顺序 token 处理、随噪声增加而退化**

因此，架构必须在**外部模仿大脑的行为**：

```
存储所有内容  →  使用 tags/vectors 建立索引
有选择性地检索  →  仅加载相关内容
保持 context 精简  →  确保 LLM 保持敏锐
```

---

### 实际的 Tag 策略

为每个 session 自动生成：
- **Topic tags**: `python`, `docker`, `finance`
- **Action tags**: `debug`, `design`, `explain`
- **Time tags**: `2025-Q1`, `recent`
- **Entity tags**: `project-X`, `user-goal-Y`

然后在 query 时：匹配 tags → 检索前 5-10 个 chunks → 注入 context。

这**完全是正确的方法**，也是目前长期 LLM agent memory 的最佳实践。