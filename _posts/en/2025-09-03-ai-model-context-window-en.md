---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Model Context Window Capacities
translated: false
type: note
---

Here are the **current maximum token capacities (context window sizes)** for the models you've listed, based on recent documentation and announcements:

---

### Anthropic Models

* **Claude Opus 4 / Opus 4.1**
  Offers a context window of **200,000 tokens**, ideal for sustained reasoning and complex workflows ([Anthropic][1], [Amazon Web Services, Inc.][2]).

* **Claude Sonnet 4**
  Also supports **200,000 tokens** of context natively ([Prompthub][3]).
  Additionally, a **beta upgrade** now enables a **massive 1 million tokens** of context for enterprise/API users ([Anthropic][4]).

---

### Mistral AI Models

* **Mistral Medium 3.1**
  Has a context window of **128,000 tokens** ([OpenRouter][5]).

* **Mistral Large 2**
  Also supports a **128,000 token** context length ([Wikipedia][6]).

* **Mistral Medium (earlier versions)**
  Previously, the standard was **32,000 tokens** for context ([Clarifai][7], [Mistral AI][8]).

* **Mistral Small 3.1**
  Upgraded its context window **from 32K to 128K tokens** in this newer version ([Wikipedia][6]).

---

### Additional Notes

* A Wikipedia overview confirms that **Claude 3 Opus** had a **200K token** context window, with expansions to **1 million tokens** in certain cases ([Wikipedia][9]).

* **Mistral's sliding window attention mechanism** theoretically supports up to **4096 × 32 = 131,072 tokens**, which closely aligns with the 128K figures reported ([Hugging Face][10]).

---

### Summary (Concise Format)

* **Claude Opus 4 / 4.1**: 200,000 tokens
* **Claude Sonnet 4**: 200,000 tokens (standard), up to **1 million tokens** (beta/enterprise)
* **Mistral Medium 3.1**: 128,000 tokens
* **Mistral Large 2**: 128,000 tokens
* **Mistral Small 3.1**: 128,000 tokens (upgraded from 32K)

---

Let me know if you’d like more details on other models or architecture-specific capabilities!

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
