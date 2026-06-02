---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 2025年AI模型上下文窗口对比
translated: true
type: note
---

以下是对您所列模型上下文窗口大小的清晰说明（不含表格）：

---

### 领先的上下文窗口

**Gemini-2.5-Pro**
谷歌的Gemini 2.5 Pro提供**100万token**的上下文窗口，并计划很快扩展至**200万token**（[Google AI for Developers][1], [blog.google][2]）。这是当前所列模型中最大的上下文窗口。

---

### Claude模型（Anthropic家族）

* **Claude-3 Opus**（及同系列如Sonnet）最初提供**20万token**，部分用户可使用超过100万token的能力（[Reddit][3], [Wikipedia][4]）。
* 在付费计划中，上下文窗口保持**20万+ token**（约500页）（[Anthropic Help Center][5]）。
* 企业版**Sonnet 4**最高支持**50万token**（[Anthropic Help Center][6]）。
* 通过Claude Code API，**Claude 4 Sonnet**可能支持**100万token**（[ClaudeLog][7]）。

因此最大上下文窗口为：
* 标准Claude Opus 4：约20万token
* Sonnet 4（企业版）：最高50万token
* 通过API的Claude 4 Sonnet（Claude Code）：最高100万token

---

### GPT-5（OpenAI）

* OpenAI官方声明GPT-5的上下文窗口为**25.6万token**（[WIRED][8], [Amazon Web Services, Inc.][9], [Anthropic Help Center][10]）。
* 有消息称免费版ChatGPT界面支持25.6万token，而API版本可能更高——但GPT-5未确认支持100万token（[Cinco Días][11]）。
* 社区报告提及上限推测，但文档显示稳定在25.6万（[OpenAI Community][12], [Encord][13]）。

---

### 其他模型

* **Gemini-Flash**可能与其他Gemini模型具有相同的大上下文窗口（100万+），但"Flash"的具体细节尚未确认。
* **其他所列模型**——如"kimi-k2"、"deepseek-v3/x"、"mistral-medium"、"qwen-coder"和"gpt-oss"——在现有资料中未明确记录上下文窗口大小。它们可能提供更标准范围（如<20万），但未经明确确认。

---

### 核心结论

* **最大上下文窗口：Gemini 2.5 Pro**（100万token，将扩展至200万）
* **紧随其后：Claude 4 Sonnet（API版本）**（约100万token）
* **其次：GPT-5**（约25.6万token）
* **随后：** 标准**Claude模型**（约20万token），**Sonnet 4企业版**提升至50万token

---

如需任何特定模型的更深入细节，请随时告知——保证无需长表格即可提供帮助！

[1]: https://ai.google.dev/gemini-api/docs/long-context?utm_source=chatgpt.com "长上下文 | Gemini API | Google AI for Developers"
[2]: https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/?utm_source=chatgpt.com "Gemini 2.5：我们最智能的AI模型 - The Keyword"
[3]: https://www.reddit.com/r/singularity/comments/1b6e0id/claude_3_context_window_is_a_big_deal/?utm_source=chatgpt.com "Claude 3上下文窗口意义重大 : r/singularity - Reddit"
[4]: https://en.wikipedia.org/wiki/Claude_%28language_model%29?utm_source=chatgpt.com "Claude（语言模型）"
[5]: https://support.anthropic.com/en/articles/7996856-what-is-the-maximum-prompt-length?utm_source=chatgpt.com "提示词最大长度是多少？| Anthropic帮助中心"
[6]: https://support.anthropic.com/en/articles/11647753-understanding-usage-and-length-limits?utm_source=chatgpt.com "了解使用量和长度限制 | Anthropic帮助中心"
[7]: https://www.claudelog.com/faqs/what-is-context-window-in-claude-code/?utm_source=chatgpt.com "Claude Code中的上下文窗口是什么"
[8]: https://www.wired.com/story/openais-gpt-5-is-here/?utm_source=chatgpt.com "OpenAI终于发布GPT-5。以下是全部重点..."
[9]: https://aws.amazon.com/bedrock/anthropic/?utm_source=chatgpt.com "Anthropic的Claude in Amazon Bedrock - AWS"
[10]: https://support.anthropic.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans?utm_source=chatgpt.com "付费Claude计划的上下文窗口有多大？"
[11]: https://cincodias.elpais.com/smartlife/lifestyle/2025-08-11/gpt-5-openai-grandes-novedades.html?utm_source=chatgpt.com "OpenAI的GPT-5：2025年主宰AI的重大革新"
[12]: https://community.openai.com/t/huge-gpt-5-documentation-gap-flaw-causing-bugs-input-tokens-exceed-the-configured-limit-of-272-000-tokens/1344734?utm_source=chatgpt.com "GPT-5文档重大缺陷导致输入token超限"
[13]: https://encord.com/blog/gpt-5-a-technical-breakdown/?utm_source=chatgpt.com "GPT-5：技术深度解析"
