---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 盘古 v1 v2 v3 的训练次数
translated: true
type: note
---

Question:
根据 “True-Story-of-Pangu” 仓库的描述，训练 Pangu v1、v2 或 v3 通常需要多少时间？

Answer:

简短回答：**该仓库并未给出 v1 / v2 / v3 明确的训练时间（例如 “3 周” 或 “2 个月”）。**
它仅提供了**相对描述**，例如 “数千亿 tokens”、“非常长的训练时间”、“多次重启的从零训练” 等。因此，你必须从上下文推断大致规模。

以下是文档隐含的内容：

---

# 1. Pangu v1 (早期 13B → 38B → 71B → 135B)

根据爆料文本：

* 早期模型在 Ascend 910A 上训练
* compute 资源有限
* tokenizer 效率低下导致浪费了 compute
* 135B 需要在 **≥1T tokens 上进行 continued training**
* 经历了多次失败和重启

这暗示了：

* **训练方式：** 增量训练 / continued training
* **token 数量：** 约 1T tokens (明确提到)
* **时间：** 可能为 **数周至数月** (取决于集群大小)

文中明确提到 135B vocabulary 替换成功是在：

> “在至少 1T 数据上进行了持续训练”
> ([Reddit][1])

因此，v1 的生成过程是**漫长的迭代训练**，而非一次性运行。

---

# 2. Pangu v2 (据称是 “套壳” 版本)

该仓库声称：

* 参数继承自旧的 135B
* 在 **数千亿 tokens** 上进行 continued training
* 性能提升迅速

引用摘要：

> “仅通过在几千亿个 tokens 上进行训练，他们就提升了指标……”
> ([Reddit][1])

含义：

* **并非全量训练**
* **属于 continued training / fine-tuning**
* 时间可能为 **数天至两周** (取决于 compute 资源)

因此，v2 的速度 **比 v1 快得多**。

---

# 3. Pangu v3 (首次真正的从零训练)

其描述如下：

* 从零开始训练 (from scratch)
* 多次稳定性回滚 (rollbacks)
* 无 loss spike
* 进行了大量实验
* “巨大的投入”

引用摘要：

> “为了确保稳定训练……每当 gradient 出现异常时就进行回滚和重启……整个训练过程中没有出现一次 loss spike。”
> ([Reddit][1])

这暗示了：

* 完整的 pretraining
* 多次重启
* 非常长的训练周期

因此，v3 ≈ **月量级的训练时间**。

---

# 典型时间线 (推断)

基于 token 数量 + 典型硬件：

| version | training type                | tokens        | estimated time |
| ------- | ---------------------------- | ------------- | -------------- |
| v1      | from scratch + retries       | ~1T           | 数周至数月     |
| v2      | continued training           | 数千亿        | 数天至数周     |
| v3      | full scratch stable training | ~1T+          | 数月           |

---

# 为什么没有确切时间？

因为训练时间取决于：

* Ascend 910 / 910B 显卡的数量
* 并行策略 (parallelism)
* batch size
* tokenization 效率
* 重启次数

该仓库有意在描述**工程上的挣扎**，而非具体的 metric。

---

# 核心洞察

该仓库传达的重要信息是：

* v1 → 漫长但低效
* v2 → 快速，因为是 continued training
* v3 → 缓慢，但是“真正的”全量训练

因此，**速度差异巨大**：

v2 << v1 ≈ v3

这实际上是该爆料者想要表达的主要观点。

---

如果你想将其与以下内容对比：

* DeepSeek v3 训练时间
* GPT 训练时间
* nanoGPT 规模

我也可以提供相关的估算。

[1]: https://www.reddit.com/r/LocalLLaMA/comments/1lsz4hk?utm_source=chatgpt.com "Huawei's Pangu AI Rocked by Unverified Claims of Fraud from Alleged Team Member"