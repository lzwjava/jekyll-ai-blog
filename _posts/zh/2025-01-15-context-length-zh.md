---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 大型语言模型的最大上下文长度
translated: true
type: post
---

最近，我使用了DeepSeek API来生成提交信息，正如[AI驱动的Git提交信息](./gitmessageai-en)一文所述。

当一次提交涉及大量更改文件时，DeepSeek API报告输入超出了其65,535个令牌（2^16 - 1）的上下文长度限制。

以下是其他一些模型的上下文窗口大小：

* **Claude 3系列：** 2024年3月推出，这些模型的上下文窗口从200,000个令牌起。
* **GPT-4：** 标准版本支持8,192个令牌，而扩展版本（GPT-4-32k）支持32,768个令牌。
* **Meta的LLaMA 2：** 标准版本支持4,096个令牌，但经过微调的版本可以处理多达16,384个令牌。
* **Mistral 7B：** 支持多达8,000个令牌。
