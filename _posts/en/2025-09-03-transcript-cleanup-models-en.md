---
audio: false
generated: true
image: false
lang: en
layout: post
title: Best Models for Transcript Cleanup Guide
translated: false
type: note
---

Great use case. For **long-form transcript cleanup with strict formatting and “no extra chatter”**, here’s what works best right now on OpenRouter, by scenario.

**Fast + cheap workhorse (EN/zh, long files): DeepSeek-V3.1**
Strong at instruction-following, handles 128k context, and you can toggle “reasoning” off for speed or on when the text is messy. Good bilingual performance for filler-word removal and consistent speaker tags. ([DeepSeek API Docs][1], [OpenRouter][2])

**Chinese-heavy interviews & colloquialisms: Kimi K2 Instruct**
Moonshot’s K2 (MoE) is particularly fluent with Chinese slang and style; great for zh-first transcripts while keeping technical nouns intact. ([OpenRouter][3])

**Highest compliance on editing instructions: Claude Sonnet (3.7/4)**
Anthropic’s Sonnet line is excellent at “output only the refined text, no meta,” and tends to be conservative about meaning changes—ideal for your step-list constraints. Use Sonnet 4 if available; 3.7 also performs well. ([OpenRouter][4])

**Ultra-long sessions or one-shot whole-project passes: GPT-5**
When you want to push very large contexts and keep hallucinations low, GPT-5 is the safest bet among frontier models on OpenRouter (listed with a very large context; strong reasoning and editing). Use for marathon transcripts or final “polish” passes. ([OpenRouter][5])

**Also strong, but watch cost profiles: Gemini 2.5 Pro**
Very capable at reasoning and long-context editing. It’s solid for refinement, but mind pricing/quotas depending on your provider route. ([OpenRouter][6])

---

### A practical routing recipe (no tables)

* **≤128k tokens, EN/zh mix, speed matters:** DeepSeek-V3.1 (non-thinking). Flip to thinking only when paragraphs are chaotic. ([DeepSeek API Docs][1])
* **Primarily Chinese transcripts:** Kimi K2 Instruct. ([OpenRouter][3])
* **Strict “editor” behavior (no commentary), legal/finance tone:** Claude Sonnet. ([OpenRouter][4])
* **Gigantic files or final single-pass polish:** GPT-5. ([OpenRouter][5])

---

### Quick code tweaks to make this robust

* **Make model selectable**: add `--model` CLI flag; default to `deepseek-v3.1`.
* **Auto-route by size/language**: detect token count and zh ratio; pick K2 for zh-heavy, GPT-5 for huge inputs, Claude for “strict edit” mode.
* **Reasoning toggle** (DeepSeek): add a param to set `reasoning.enabled` in your OpenRouter call for hard passages. ([DeepSeek API Docs][1])
* **Fix small bugs**: that stray `print(".1f")`; and widen speaker-label regex to allow `A：` (full-width colon) and no-space variants.
* **Guardrails**: if length delta >10%, auto-retry with a “don’t delete content” reminder; if no `A:`/`B:` found, auto-retry with a “label speakers” nudge.

If you want, I can rewrite your script to add the `--model` flag and smart routing logic right now.

[1]: https://api-docs.deepseek.com/quick_start/pricing?utm_source=chatgpt.com "Models & Pricing"
[2]: https://openrouter.ai/deepseek/deepseek-chat-v3.1?utm_source=chatgpt.com "DeepSeek V3.1 - API, Providers, Stats"
[3]: https://openrouter.ai/moonshotai/kimi-k2?utm_source=chatgpt.com "Kimi K2 - API, Providers, Stats"
[4]: https://openrouter.ai/anthropic/claude-3.7-sonnet?utm_source=chatgpt.com "Claude 3.7 Sonnet - API, Providers, Stats"
[5]: https://openrouter.ai/openai/gpt-5?utm_source=chatgpt.com "GPT-5 - API, Providers, Stats"
[6]: https://openrouter.ai/google/gemini-2.5-pro?utm_source=chatgpt.com "Gemini 2.5 Pro - API, Providers, Stats"
