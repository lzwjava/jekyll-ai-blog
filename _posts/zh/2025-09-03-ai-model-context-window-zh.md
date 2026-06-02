---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI模型上下文窗口容量
translated: true
type: note
---

以下是您列出的模型**当前最大标记容量（上下文窗口大小）**，基于最新的文档和公告：

---

### Anthropic 模型

* **Claude Opus 4 / Opus 4.1**
  提供 **200,000 个标记**的上下文窗口，非常适合持续推理和复杂工作流程（[Anthropic][1], [Amazon Web Services, Inc.][2]）。

* **Claude Sonnet 4**
  同样原生支持 **200,000 个标记**的上下文（[Prompthub][3]）。
  此外，**测试版升级**现在为企业/API 用户提供了 **高达 100 万个标记** 的上下文容量（[Anthropic][4]）。

---

### Mistral AI 模型

* **Mistral Medium 3.1**
  拥有 **128,000 个标记**的上下文窗口（[OpenRouter][5]）。

* **Mistral Large 2**
  同样支持 **128,000 个标记**的上下文长度（[Wikipedia][6]）。

* **Mistral Medium (早期版本)**
  此前，标准的上下文容量为 **32,000 个标记**（[Clarifai][7], [Mistral AI][8]）。

* **Mistral Small 3.1**
  在此新版本中，其上下文窗口**从 32K 升级到了 128K 标记**（[Wikipedia][6]）。

---

### 补充说明

* 一份维基百科概述证实，**Claude 3 Opus** 拥有 **200K 标记**的上下文窗口，在某些情况下可扩展至 **100 万个标记**（[Wikipedia][9]）。

* **Mistral 的滑动窗口注意力机制**理论上支持高达 **4096 × 32 = 131,072 个标记**，这与报告的 128K 数据非常接近（[Hugging Face][10]）。

---

### 总结（简洁格式）

* **Claude Opus 4 / 4.1**: 200,000 个标记
* **Claude Sonnet 4**: 200,000 个标记（标准），**高达 100 万个标记**（测试版/企业版）
* **Mistral Medium 3.1**: 128,000 个标记
* **Mistral Large 2**: 128,000 个标记
* **Mistral Small 3.1**: 128,000 个标记（从 32K 升级而来）

---

如果您需要关于其他模型或架构特定功能的更多详细信息，请告诉我！

* [The Verge](https://www.theverge.com/ai-artificial-intelligence/757998/anthropic-just-made-its-latest-move-in-the-ai-coding-wars?utm_source=chatgpt.com)
* [Tom's Guide](https://www.tomsguide.com/ai/anthropic-looks-to-beat-gpt-5-and-grok-4-with-this-one-major-upgrade?utm_source=chatgpt.com)

[1]: https://www.anthropic.com/claude/opus?utm_source=chatgpt.com "Claude Opus 4.1"
[2]: https://aws.amazon.com/bedrock/anthropic/?utm_source=chatgpt.com "Anthropic's Claude in Amazon Bedrock"
[3]: https://www.prompthub.us/blog/the-complete-guide-to-claude-opus-4-and-claude-sonnet-4?utm_source=chatgpt.com "The Complete Guide to Claude Opus 4 and Claude Sonnet 4"
[4]: https://www.anthropic.com/news/1m-context?utm_source=chatgpt.com "Claude Sonnet 4 now supports 1M tokens of context"
[5]: https://openrouter.ai/mistralai/mistral-medium-3.1?utm_source=chatgpt.com "Mistral Medium 3.1 - API, Providers, Stats"
[6]: https://en.wikipedia.org/wiki/Mistral_AI?utm_source=chatgpt.com "Mistral AI"
[7]: https://clarifai.com/mistralai/completion/models/mistral-medium?utm_source=chatgpt.com "mistral-medium model | Clarifai - The World's AI"
[8]: https://mistral.ai/news/mistral-large?utm_source=chatgpt.com "Au Large"
[9]: https://en.wikipedia.org/wiki/Claude_%28language_model%29?utm_source=chatgpt.com "Claude (language model)"
[10]: https://huggingface.co/docs/transformers/en/model_doc/mistral?utm_source=chatgpt.com "Mistral"
