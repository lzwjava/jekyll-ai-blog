---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 拉德福德复古语言模型时代
translated: true
type: note
---

**问题：** 前 OpenAI 研究员 Alec Radford 近年来在做什么？

**回答：**

快速回顾一下他为何重要：Radford 是 GPT-1、GPT-2、CLIP 和 Whisper 的第一作者，也是 DALL-E 的核心贡献者——他是一位技术型独立贡献者，从未以管理层的身份领导过团队，却不断推动领域向前发展，他名字位列第一的论文定义了当今的人工智能时代。以下是他近期的动态时间线：

**2024 年 12 月 —— 离开 OpenAI。** 他告诉同事，他将离开并独立开展研究，并表示计划与 OpenAI 及其他人工智能开发者合作。没有成立新实验室，也没有创办初创公司——只是独立研究，这非常符合他一贯的风格。

**2025 年 3 月至 4 月 —— Thinking Machines Lab 顾问。** 他加入 Mira Murati 的 Thinking Machines Lab 担任顾问，同行的还有 OpenAI 前首席研究官 Bob McGrew。仅担任顾问角色，并非全职。

**2026 年 4 月 28 日 —— 发布 Talkie，一个“复古语言模型”。** 鉴于你对 nanoGPT/模型训练的兴趣，这可能是最有趣的一条。Radford 与 Nick Levine 和 David Duvenaud 合作，在 2600 亿个 token 的英文文本上训练了一个 130 亿参数模型，所有文本的日期均早于 1931 年 1 月 1 日——包括历史书籍、报纸、科学期刊、专利和判例法。没有网络爬虫数据，没有维基百科，也没有现代代码。关键技术细节：

* 在 Apache 2.0 许可下发布两个检查点：talkie-1930-13b-base 和一个经过指令微调（从 1931 年之前的参考著作中提取的指令-响应对）的 -it 变体。
* 选择 1930 年作为截止点，是因为 2026 年 1 月 1 日美国出版的 1930 年作品进入公共领域——因此整个语料库不存在版权问题。
* 这是一个非营利的团队合作，得到了 Anthropic 的计算支持。
* 研究动机非常严肃：这是一个研究泛化与记忆化的干净测试平台。基准测试污染——测试问题泄露到训练数据中——是人工智能领域最棘手的问题之一，而一个物理上不可能看到 1930 年后文本的模型正好规避了这个问题。它也打破了所有现代 LLM 共享的网页数据血统，使研究人员能够研究哪些行为是语言建模的普遍特性，哪些是训练于当代网络数据所带来的假象。
* 团队称这是迄今为止最大的复古语言模型，并计划继续大幅扩展规模。
* 他们提到的一个相关的开放问题是：正如 Demis Hassabis 所暗示的，一个仅用 1911 年前文本训练的模型能否独立推导出广义相对论？更大的复古模型可能揭示这些规模化的趋势。

如果你想亲自尝试：模型权重在 Hugging Face 上（Apache 2.0 许可，基础模型约 53 GB，可以舒适地放入你的 MI300X，量化后的 -it 版本可以在 4070 上运行），推理库在 GitHub 上，在线聊天地址是 talkie-lm.com。鉴于你正在从头训练 GPT-2 规模的模型，Talkie 的数据集工程方面（OCR 流水线、时间泄漏过滤——日期错误的文档或带有时代错位编辑引言的历史文本可能会损害历史保真度）可能是最值得深入研究的部分。

**参考资料：**

* [Simon Willison — 介绍 talkie](https://simonwillison.net/2026/Apr/28/talkie/)
* [The Decoder — 对 1930 年后一无所知的 LLM](https://the-decoder.com/here-is-what-an-llm-that-knows-nothing-after-1930-thinks-our-world-looks-like-in-2026/)
* [MarkTechPost — Talkie-1930 技术概述](https://www.marktechpost.com/2026/04/27/meet-talkie-1930-a-13b-open-weight-llm-trained-on-pre-1931-english-text-for-historical-reasoning-and-generalization-research/)
* [维基百科 — Alec Radford](https://en.wikipedia.org/wiki/Alec_Radford)
