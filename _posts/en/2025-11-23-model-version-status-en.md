---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5.1
title: AI Model Version Status Check
translated: false
type: note
---

Good question. I looked into each of those models in your `MODEL_MAPPING` and checked whether they’re currently (as of late 2025) the latest in their respective series. Here’s what I found — and where there may be newer versions.

---

### Analysis of Your Models

| **Model Key**        | **Mapped Model**               | **Is It the Latest?** | **Notes**                                                                                                                                                                                                                                                  |
| -------------------- | ------------------------------ | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **claude-opus**      | `anthropic/claude-opus-4`      | **Not quite**         | Anthropic released **Claude Opus 4.1** on Aug 5, 2025. ([Anthropic][1]) So `claude-opus-4` is slightly outdated.                                                                                                                                           |
| **claude-sonnet**    | `anthropic/claude-4.5-sonnet`  | **Yes / No**          | According to the Claude wiki page, Anthropic announced **Sonnet 4.5** on Sep 29, 2025, which is more capable than Sonnet 4. ([Wikipedia][2]) If by “claude-sonnet” you meant Sonnet 4, then it's not the latest; but if you used “4.5”, you're up-to-date. |
| **gemini-flash**     | `google/gemini-2.5-flash`      | **Probably not**      | Google’s Gemini 2.5 Flash is GA. ([blog.google][3]) But there is now a **Gemini 3.0 Pro** model as of November 2025. ([Wikipedia][4]) Depending on the variant, 2.5 may not be “latest”.                                                                   |
| **gemini-pro**       | `google/gemini-3-pro-preview`  | **Yes-ish**           | Gemini 3.0 Pro was just rolled out. ([Reddit][5]) Given it's labeled “preview,” it may be the cutting-edge but might not yet be fully stable.                                                                                                              |
| **kimi-k2**          | `moonshotai/kimi-k2`           | **Likely yes**        | I found a paper for **Kimi K2** (32B MoE). ([arXiv][6]) I did *not* find a stable Kimi-K3 or K2.1 publicly announced, so K2 is probably the current version.                                                                                               |
| **deepseek-v3.2**    | `deepseek/deepseek-v3.2-exp`   | **Unclear**           | I didn’t find reliable public evidence that DeepSeek has a newer stable version beyond v3.2 (or at least not one that’s clearly documented). Without a changelog or version registry, it’s hard to confirm.                                                |
| **mistral-medium**   | `mistralai/mistral-medium-3.1` | **Yes**               | Mistral’s own model list shows **Mistral Medium 3.1** as the latest medium model. ([Mistral AI][7])                                                                                                                                                        |
| **qwen-coder**       | `qwen/qwen3-coder`             | **Unclear**           | I didn’t see a clearly newer “Qwen 4-coder” or “Qwen 3.1-coder” in public documentation. Without more info, it’s ambiguous whether 3-coder is still the latest.                                                                                            |
| **gpt**              | `openai/gpt-5.1`               | **Yes**               | According to sources, **GPT-5.1** was released in November 2025. ([Wikipedia][8])                                                                                                                                                                          |
| **grok-code**        | `x-ai/grok-code-fast-1`        | **Unclear**           | I found no public release notes confirming a newer “grok-code” model beyond version **1**. Without an official roadmap or model card, this may still be current.                                                                                           |
| **grok-fast**        | `x-ai/grok-4.1-fast`           | **Unclear**           | Similar to grok-code: no clear public documentation of a “grok-4.2-fast” or equivalent, so 4.1-fast might still be their latest.                                                                                                                           |
| **glm**              | `z-ai/glm-4.6`                 | **Unclear**           | I couldn’t find an official “GLM 4.7” or later from Z-AI. Public information on recent GLM versions is limited, so hard to say.                                                                                                                            |
| **minimax**          | `minimax/minimax-m2`           | **Unclear**           | I didn’t find strong public version history for Minimax. It’s possible M2 is the current or a stable version, but I can’t confirm a newer one.                                                                                                             |
| **kimi-k2-thinking** | `moonshotai/kimi-k2-thinking`  | **Likely yes**        | There’s no public mention of a “Kimi-K2- thinking 2.0” or similar; K2-thinking appears to be a thinking-mode variant of the K2 model.                                                                                                                      |

---

### **Summary & Recommendations**

* **Not up-to-date**: Your mapping for **claude-opus** probably should point to `claude-opus-4.1` instead of `claude-opus-4`.
* **Gemini**: Depending on your use-case, you might consider switching from Gemini 2.5 Flash to a 3.0 model, especially since 3.0 Pro is out.
* **Some models are unclear**: For Qwen, Grok, DeepSeek, GLM, and Minimax, the public versioning is either limited or not clearly documented, so you may want to revisit their official repos or documentation.
* **Kimi K2**: Looks stable and current.

---

If you like, I can check **all** of the model keys in your mapping (or even more) and produce a *fully up-to-date mapping* with the latest versions as of now — do you want me to do that?

[1]: https://www.anthropic.com/news/claude-opus-4-1?utm_source=chatgpt.com "Claude Opus 4.1 \ Anthropic"
[2]: https://en.wikipedia.org/wiki/Claude_%28language_model%29?utm_source=chatgpt.com "Claude (language model)"
[3]: https://blog.google/products/gemini/gemini-2-5-model-family-expands/?utm_source=chatgpt.com "Gemini 2.5 model family expands"
[4]: https://en.wikipedia.org/wiki/Gemini_%28language_model%29?utm_source=chatgpt.com "Gemini (language model)"
[5]: https://www.reddit.com//r/GeminiAI/comments/1p0h2f3/gemini_3_fast_thinking_is_now_live_on_the_gemini/?utm_source=chatgpt.com "Gemini 3 (Fast &Thinking) is now live on the Gemini app"
[6]: https://arxiv.org/abs/2507.20534?utm_source=chatgpt.com "Kimi K2: Open Agentic Intelligence"
[7]: https://docs.mistral.ai/getting-started/models?utm_source=chatgpt.com "Mistral Docs"
[8]: https://en.wikipedia.org/wiki/GPT-5.1?utm_source=chatgpt.com "GPT-5.1"
