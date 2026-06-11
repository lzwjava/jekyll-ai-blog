---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Frontier Labs的秘密代码数据集
translated: true
type: note
---

**问题：** OpenAI、Google（Gemini）和 Anthropic 分别使用哪些代码数据集来训练它们的编码模型（如 Codex 等）？

**答案：**

坦率地说：前沿实验室大约在 2022 年左右就不再公开数据集构成。GPT-4、Gemini 和 Claude 的技术报告都只用一句含糊的话描述训练数据（"公开可用的数据、许可数据以及来自第三方的数据"）。因此，我们所知的信息分为三类：(1) 早期论文中披露的内容；(2) 从诉讼、交易和开源复现中推断出的内容；(3) 现代 post-training 方法的原理，这在很大程度上已经取代了原始的 GitHub 规模，成为区分模型能力的关键。

**实际披露的内容（历史记录）**

- **OpenAI Codex（2021 年论文，arXiv:2107.03374）：** 从 2020 年 5 月的 5400 万个公共 GitHub 仓库中抓取并去重后的 159 GB Python 文件，过滤条件包括：文件小于 1MB、移除自动生成的代码、平均行长度超过 100 的文件以及低字母数字比例的文件。在 GPT-3 基础上微调。后续的 Codex 变体添加了一个"监督微调"数据集，包含来自竞赛编程网站和具有 CI 的仓库中独立的、正确实现的函数（通过运行测试验证正确性——这是执行反馈训练的早期雏形）。
- **GPT-3 本身**已经通过 Common Crawl 和 WebText 偶然包含了代码；从 GPT-4 开始，没有任何信息披露。
- **Google：** PaLM（2022 年）披露了 5% 的代码（390 亿 token）来自 GitHub，涵盖 24 种语言。AlphaCode（DeepMind，2022 年）披露了 715 GB 的 GitHub 代码以及一个用于微调的精选 CodeContests 数据集。Gemini 报告仅提到"网络文档、书籍和代码"——没有具体量化。Google 还有一个内部单仓库（数十亿行代码），并在 DIDACT 论文（2023 年）中披露，他们使用内部 Google 开发者的活动数据（编辑历史、构建错误、代码审查评论）进行训练，而不仅仅是最终的代码快照。这是其他实验室没有的数据源。
- **Anthropic：** 从未发布过代码数据构成。公开声明：使用公开可用的互联网数据、许可的第三方数据以及由承包商/Claude 自身生成的数据，并尊重 robots.txt。Anthropic 默认不会使用 API 客户数据进行训练。Books 诉讼披露的内容揭示了大量关于文本获取的信息，但没有涉及代码细节。

**开源复现能告诉你什么（最佳代理）**

如果你想了解前沿代码预训练语料库的实际样子，请阅读那些*确实*披露信息的实验室的论文——它们的做法趋于一致：

- **The Stack v2 / StarCoder2（BigCode）：** 67.5 TB 原始数据 → 过滤后约 3TB，包含来自 Software Heritage 的 619 种语言，经过许可证过滤、使用 MinHash 近似去重、PII 脱敏和质量过滤。这大致是"所有宽松许可证 GitHub"的开源天花板。
- **DeepSeek-Coder（鉴于你对 DeepSeek v4 的兴趣，这与你最相关）：** 2T token，87% 源代码，10% 英文代码相关（GitHub Markdown、StackExchange），3% 中文。每个人现在都在复制的关键技巧是：**仓库级数据构建**——根据依赖关系拓扑排序仓库内的文件，使模型在使用之前看到导入，而不是打乱后的单个文件。此外还有 FIM（fill-in-the-middle），比例约为 50%。
- Qwen-Coder、Code Llama 的论文讲述了同样的故事：GitHub + StackOverflow/StackExchange + Jupyter notebooks + commit diffs + issues/PRs + 文档。

可以合理推断，OpenAI/Google/Anthropic 的预训练语料库是上述内容的超集：完整的 GitHub 克隆（包括非宽松许可证，这正是诉讼的焦点）、提交历史与差异（diff）、GitHub issue 和 PR 讨论、StackOverflow（OpenAI 在 2024 年与 Stack Overflow 签署了许可协议；Google 更早通过 OverflowAPI 签署）、包注册表和文档（PyPI、npm、readthedocs）以及 Common Crawl 中与代码相邻的页面。

**现代的区分因素：不再是预训练语料库**

对于 GPT-5.x-Codex、Gemini 3 和 Claude Opus/Sonnet 4.x 等模型，每个人的预训练数据基本上都是"所有公开代码"。能力差距现在来自于实验室*自己生成*的 post-training 数据：

1. **大规模合成代码数据**——由模型生成的问题、解决方案和解释，并通过执行进行过滤。开源的对应物是 Phi-1（"Textbooks Are All You Need"）和 Magicoder/OSS-Instruct 所展示的：从真实代码中提取种子片段 → LLM 生成指令/解决方案对 → 通过运行测试过滤。
2. **具有可验证奖励的强化学习（RLVR）**——生成解决方案，在沙箱中针对单元测试运行，根据通过/失败给予奖励。这是推理模型训练循环的核心（与 DeepSeek-R1 中使用 GRPO 披露的原理相同），这也是编码能力提升远快于其他领域的原因：代码为你提供了免费且完美的奖励信号。
3. **智能体轨迹数据**——SWE-bench 风格的数据：获取包含真实 issue 和合并 PR 的真实仓库，重建环境，并训练多步轨迹（读取文件 → 编辑 → 运行测试 → 修复）。OpenAI 的 Codex 模型被明确描述为通过 RL 在真实软件工程任务上训练；Anthropic 的 Claude Code 系列也是同样的思路。如果要查看代码中的构建流程，开源的复现是 SWE-Gym 和 SWE-smith。
4. **人类专家数据**——三个实验室都付费给承包商（Surge、Scale、Turing 等）来获取困难的编码问题、偏好排名和轨迹修正。

**给你的实用建议：** 由于你是在 nanoGPT/nanochat 规模上训练，可复现的流程是：在 The Stack v2（或 smollm-corpus 的 Stack 子集）的过滤切片上进行预训练，采用仓库级拼接 + FIM，然后在 OSS-Instruct 风格的合成数据上进行 SFT，最后使用如 verl 或 TRL 等工具，在单元测试奖励上进行 GRPO。这与前沿方案的形式相同，只是计算量少了三个数量级。DeepSeek-Coder 和 StarCoder2 的论文是信息密度最高的两篇——它们实际上是封闭实验室所做事情的泄露蓝图。

**参考文献：**

- [Evaluating Large Language Models Trained on Code (Codex paper)](https://arxiv.org/abs/2107.03374)
- [DeepSeek-Coder: When the Large Language Model Meets Programming](https://arxiv.org/abs/2401.14196)
- [StarCoder 2 and The Stack v2](https://arxiv.org/abs/2402.19173)
- [Competition-Level Code Generation with AlphaCode](https://arxiv.org/abs/2203.07814)
- [Magicoder: Source Code Is All You Need (OSS-Instruct)](https://arxiv.org/abs/2312.02120)
- [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770)
