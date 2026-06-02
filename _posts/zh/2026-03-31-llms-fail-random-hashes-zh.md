---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么大语言模型无法处理随机哈希
translated: true
type: note
---

**问题：** 为什么 LLM 不擅长处理像 Git commit hashes 这样的随机字符串？具体来说，如果我给它 10–20 条 Git commit log 条目，并要求它生成 `git cherry-pick` 命令，然后运行这些命令，Git 会报告 fatal error，因为这些 commit hashes 在仓库中实际上并不存在。

**回答：**

这是一个非常著名且基础的 LLM 局限性。造成这种情况的原因有多个层面。

---

## 1. 根本原因：Tokenization —— LLM 处理的是块，而不是字符

最深层的原因是 **Tokenization**。LLM 无法拼写单词或执行简单的字符串处理任务（如反转字符串），其根源就在于 Tokenization。Token 是 Large Language Models 的基本单位 —— 所有内容都以 Token 为单位进行处理，而 Tokenization 将字符串转换为 Token 序列。许多看起来像是神经网络的问题，实际上都可以追溯到 Tokenization。

一个 Git commit hash 看起来像这样：`a3f9c2d1b8e047...`

Tokenization 通常将字符串拆分为词级或子词级的 Token，而不是单个字符。这意味着 LLM 缺乏字符级的理解。因此，当 LLM “看到”一个 commit hash 时，它不会像人类仔细复制那样逐字符处理。相反，它将 hash 的任意 **chunks** 处理为组合 Token，从而失去了精确重现它所需的精确位置感知。

研究表明了两个关键问题：(1) Tokenization 未能将字符串拆分为单个字符，导致缺乏字符级理解；(2) Token embeddings 缺乏诸如 Token 长度之类的字符级信息，进一步凸显了 LLM 对字符串有限的字符级理解。

---

## 2. LLM 是概率型模式生成器，而非复印机

即使你将 commit hashes 直接粘贴到 Prompt 中，LLM 也不会将其视为不可更改的字面量。它在每一步都在生成 **统计上最有可能的下一个 Token**。

对于词汇表中的任何字符串，LLM 可能会在任何位置停止。由于不知道必须从哪里开始或在哪里停止，生成任何内容的概率都不是零 —— 这就是为什么 LLM 会生成看起来像是随机内容的原因。

因此，当模型输出看起来像 `a3f9c2d1b8e047` 的内容时，它实际上生成的可能是 `a3f9c2d1b8e048` 或其他类似但错误的变体，因为这些字符位置被编码为块（chunks），而不是原子。

---

## 3. 对于稀有/唯一值，幻觉是数学上的必然

OpenAI 的研究表明，幻觉（Hallucinations）不仅是由于糟糕的训练数据或草率的 Fine-tuning 造成的，而是使用 Cross-entropy 进行 Pretraining 方式的数学结果。Generative models 可以简化为一个二元的“这是否有效”分类器，这意味着非零错误率是不可避免的 —— 特别是在稀有或孤立的事实上。

Git commit hash 是终极的孤立事实 —— 这是一个 40 字符的 SHA-1 字符串，不会出现在任何训练数据中，没有语义含义，且携带零统计信号。模型以前从未见过 *你的* 仓库的 hashes。拥有私有代码库的公司尤其容易受到影响，因为在公共数据上训练的流行 LLM 没见过它们的代码。正如一位研究人员所说：“产生幻觉的机会要大得多，因为模型不知道关于其代码库的事实。”

---

## 4. 模型感到必须完成任务的迫切感

Generative AI 工具的目标是完成分派给它们的任务 —— 为 Prompt 提供完整的响应。模型有时为了实现这一目标而编造内容。

当你要求 LLM 为 20 个 commits 生成 `git cherry-pick` 命令时，它不会说“我无法确定这些 hashes”。它会自信地填入看起来像有效 hash 的内容。训练目标和常见的排行榜奖励自信的猜测而非校准后的不确定性，因此模型学会了“虚张声势”。

---

## 5. 为什么 Cherry-Pick Hashes 特别容易失败

当你运行生成的 cherry-pick 命令时：

- LLM 输出的 hash 在 **视觉上接近** 你的真实 hash，但有 1–4 个字符有细微错误
- Git 执行精确的 SHA-1 查找 —— 对任何偏差零容忍
- Git 报告 `fatal: bad object` 或 `fatal: reference is not a tree`

这是 LLM 的最坏情况：一项需要在 **唯一的、未见的、语义不透明的字符串** 上保持 **精确字符级忠实度** 的任务。

---

## 在实践中如何修复

不要让 LLM 凭记忆或上下文重现 commit hashes，而应使用适当的工具：

**方案 1 — 直接使用 Git 获取列表，然后进行 cherry-pick：**

```bash
# 从 git log 获取 hashes 并自行构建 cherry-pick 命令
git log --oneline origin/feature-branch | head -20 | awk '{print $1}' | xargs git cherry-pick
```

**方案 2 — 如果使用 LLM，给它 hashes 并只要求它提供命令结构：**
自行提供 hashes，仅要求 LLM 将其包装在 `git cherry-pick` 语法中 —— 不要相信它能从散文描述中重现精确的 hashes。

**方案 3 — 使用带有范围的 `git cherry-pick`：**

```bash
git cherry-pick <oldest-hash>^..<newest-hash>
```

**方案 4 — 始终验证 LLM 生成的 hashes：**

```bash
git cat-file -t <hash>   # 如果真实存在，应返回 "commit"
```

---

## 总结表

| 属性 | 自然语言 | Git Commit Hash |
| :--- | :--- | :--- |
| 出现在训练数据中 | 大规模 | 从不（私有仓库） |
| 具有语义含义 | 是 | 否 |
| Tokenization 清晰度 | 是 | 否 —— 被任意分块 |
| 容忍微小错误 | 是 | 零容忍 |
| LLM 可靠性 | 好 | 非常差 |

底线：永远不要相信 LLM 会重现精确的不透明标识符，如 commit hashes、UUIDs、API keys 或任何高熵随机字符串。始终为它提供确切的值，并让它将其作为传递项（pass-through）使用 —— 而不是重新生成。

**参考资料：**

- [StringLLM: Understanding the String Processing Capability of LLMs (ICLR 2025)](https://arxiv.org/html/2410.01208)
- [LLMs Will Always Hallucinate — arxiv](https://arxiv.org/html/2409.05746v1)
- [Why LLMs Hallucinate — Lakera](https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models)
- [LLM Tokenization Explained — fast.ai](https://www.fast.ai/posts/2025-10-16-karpathy-tokenizers)
- [Nonsense and Malicious Packages: LLM Hallucinations in Code — ACM](https://cacm.acm.org/news/nonsense-and-malicious-packages-llm-hallucinations-in-code-generation/)
