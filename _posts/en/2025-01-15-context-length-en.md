---
audio: false
generated: false
image: false
lang: en
layout: post
title: Maximum Context Length of Large Language Models
translated: false
type: post
---

I recently encountered the context length limit of the DeepSeek API while generating a commit message, as detailed in [AI-Powered Git Commit Messages](./gitmessageai-en).

Specifically, when a commit involved numerous changed files, the API reported that the input exceeded its context length limit of 65,535 tokens (2^16 - 1).

According to their documentation: [https://api-docs.deepseek.com/quick_start/pricing](https://api-docs.deepseek.com/quick_start/pricing), the context length is 64k tokens, with a maximum output of 8k tokens.

Here's a comparison of context window sizes for several other models:

* **Claude 3 Family:** Launched in March 2024, these models offer context windows starting at 200,000 tokens.
* **GPT-4:** The standard version has a context window of 8,192 tokens, while the extended version (GPT-4-32k) supports 32,768 tokens.
* **Meta's LLaMA 2:** The base model supports 4,096 tokens, but fine-tuned versions can handle up to 16,384 tokens.
* **Mistral 7B:** Supports a context window of 8,000 tokens.
