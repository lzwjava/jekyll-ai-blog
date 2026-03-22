---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 诉讼揭露 Anthropic 内部战略
translated: true
type: note
---

Question: 关于 Bartz v. Anthropic 诉讼中泄露的关于 Anthropic 2025 年初 Product Vision 的邮件说了什么？

Answer:

在 **Bartz v. Anthropic** 案件中，并没有一份被广泛证实的“2025 年初泄露的 Product Vision 邮件”。人们通常指的是：

1. **法院解密的内部规划文件**（有时被误传为“邮件”）
2. **法官命令中的陈述**，描述了 Anthropic 的内部目标
3. 随后关于 **“Project Panama”** 和“扫描所有书籍”战略的报道

这些内容并不是单一的泄露邮件，而是在诉讼过程中披露的 **法律文件 + 内部文档**。

---

# “Bartz v. Anthropic” 实际披露的内容

诉讼声称 Anthropic 构建了一个包含**数百万本书的中央图书馆**来训练模型。法院文件将内部目标描述为创建 **“世界上所有书籍”** 的语料库。([Copyright Alliance][1])

披露的关键点：

### 1. 内部愿景：构建通用书籍语料库

法院文件称 Anthropic：

* 从**盗版网站下载了数百万本书籍**
* 通过**切割装订并数字化**的方式扫描购买的书籍
* 将它们存储在一个**永久性的中央图书馆**中
* 使用子集来训练 Claude 模型 ([Loeb & Loeb LLP][2])

法官将该计划总结为：

> 收集一个包含“世界上所有书籍”的中央图书馆并“永远”保留 ([Copyright Alliance][1])

这就是网上人们所指的 **“Product Vision 泄露”**。

---

### 2. “Project Panama”（后来解密的细节）

随后解密的文件描述了一项机密计划：

* 破坏性地扫描 **数百万本实体书**
* 拆除装订、扫描页面、丢弃原件
* 秘密构建训练语料库
* 内部说明：他们**不希望被公众知晓** ([Wikipedia][3])

这强化了人们对 Anthropic 早期产品策略的理解：

* 大规模数据获取先行
* 顶部构建 Safety-aligned 模型
* 专有数据集优势

---

### 3. 法律裁定澄清了架构

法院将 Anthropic 的 Workflow 分为：

1. 构建中心化的书籍图书馆
2. 从子集中训练 LLMs

训练本身被认为是 **Transformative** 的，但 **创建盗版图书馆则不是**。 ([PatentNext][4])

---

# 人们如何解读其 “Product Vision”

从这些文件中，观察者推断出 Anthropic 在 2025 年初的愿景：

* 构建 **最大的专有文本语料库**
* 相比 Web Scraping 更倾向于 **书籍**（质量更高）
* 创建 **永久性内部知识库**
* 使用同一个语料库训练未来的多个模型
* 在 **Data Quality + Safety** 上竞争，而非仅仅是 Scale

这与以下路径不同：

* OpenAI → Web-scale + RLHF 迭代
* Google → Search/Web + Multimodal
* Meta → Open-source scaling

Anthropic → **高质量策划的书籍语料库 + Alignment**

---

# 为什么这引起了争议

因为它暗示了：

* 大规模摄取受版权保护的书籍
* 使用了盗版图书馆（LibGen 等）
* 破坏性的扫描操作
* 对数据集创建过程的保密

这就是诉讼发生的原因，并最终导致了 **15 亿美元的妥协补偿（Settlement）**。 ([Legal Blogs][5])

---

# TL;DR (总结)

并不存在一份单一的“泄露邮件”。
“泄露”是指**法院解密的内部文件**，显示其：

* 目标：**扫描/收集所有书籍**
* 构建 **永久性训练图书馆**
* 从该语料库训练 Claude
* 保持数据集的专有性

这被公认为 Anthropic 的 **2025 年初 Product Vision**。

---

如果你需要，我还可以解释：

* 这与 OpenAI 策略的区别
* 为什么书籍是更好的训练数据
* 为什么 Anthropic 专注于“Library-first”设计

[1]: https://copyrightalliance.org/wp-content/uploads/2025/06/Bartz-v.-Anthropic-Order.pdf?utm_source=chatgpt.com "Bartz-v.-Anthropic-Order.pdf"
[2]: https://www.loeb.com/en/insights/publications/2025/07/bartz-v-anthropic-pbc?utm_source=chatgpt.com "Bartz v. Anthropic PBC"
[3]: https://en.wikipedia.org/wiki/Anthropic?utm_source=chatgpt.com "Anthropic"
[4]: https://www.patentnext.com/2025/07/u-s-district-courts-issue-first-decisions-on-ai-model-development-and-copyright-fair-use/?utm_source=chatgpt.com "First U.S Decision on AI Training & Copyright Fair Use"
[5]: https://legalblogs.wolterskluwer.com/copyright-blog/the-bartz-v-anthropic-settlement-understanding-americas-largest-copyright-settlement/?utm_source=chatgpt.com "The Bartz v. Anthropic Settlement"