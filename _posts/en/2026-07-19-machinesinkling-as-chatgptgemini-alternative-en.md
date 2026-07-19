---
audio: false
generated: true
image: false
lang: en
layout: post
title: machines/inkling as ChatGPT/Gemini Alternative
translated: false
type: note
---

Question: Is Inkling's image understanding a good alternative because ChatGPT/Gemini image analysis doesn't work well for Chinese users?

Answer:

Yes, your test result is a good sign. The interesting part is not just "it can see the image"; many models can now do that. The important thing is **availability + API accessibility**.

Your flow:

```
image
  ↓
OpenRouter
  ↓
thinkingmachines/inkling
  ↓
vision reasoning
  ↓
"solid blue rectangular field..."
```

means you have a usable multimodal pipeline without depending on a consumer app region restriction. Inkling is a native multimodal model accepting image, text, and audio inputs. ([Thinking Machines Lab][1])

For Chinese users, the situation is roughly:

| Model                    | Image analysis access | China usability                                                                      |
| ------------------------ | --------------------- | ------------------------------------------------------------------------------------ |
| ChatGPT vision           | Excellent             | Often difficult because ChatGPT service availability/payment/access can be a blocker |
| Gemini vision            | Excellent             | Google services have similar access issues                                           |
| OpenRouter vision models | Usually easier        | API-based, depends on provider                                                       |
| Inkling                  | New but interesting   | Developer-friendly via OpenRouter                                                    |

([OpenAI Help Center][2])

The key difference:

**ChatGPT/Gemini are product-first.**

```
User
 ↓
ChatGPT app
 ↓
policy / account / region / billing
 ↓
model
```

**OpenRouter is infrastructure-first.**

```
Your CLI / app
 ↓
OpenRouter API
 ↓
model routing
 ↓
vision model
```

For developers in China, the second architecture is often much more practical.

Inkling is also technically interesting because it is not just a text LLM with a separate vision plugin. Its model card describes a multimodal architecture where image/audio/text representations are processed in a shared model space. ([Thinking Machines Lab][1])

A simple test matrix would be:

```bash
# same image
models=(
  "thinkingmachines/inkling"
  "google/gemini-2.5-pro"
  "openai/gpt-5"
  "qwen/qwen3-vl"
)

for m in "${models[@]}"; do
    ww vision-model test \
       --model "$m" \
       --image test.png
done
```

Compare:

1. OCR accuracy
2. chart understanding
3. UI screenshot understanding
4. Chinese text recognition
5. hallucination rate

For your use case (AI CLI tools, agents, coding assistants), vision availability matters more than benchmark score. A slightly weaker model that your agent can always call beats a stronger model you cannot reliably access.

Inkling is especially interesting because it is open-weight and aimed at developers/agents, not only chat. ([Reuters][3])

So your conclusion is reasonable:

> "Gemini/ChatGPT image analysis recently hard to use for Chinese users, but OpenRouter + Inkling gives a practical alternative."

I would add: Qwen VL family is also worth testing because Chinese OCR/UI understanding is usually a strong area. The winning stack for Chinese developers may become:

```
English reasoning:
  GPT / Claude / Gemini / Inkling

Chinese vision:
  Qwen-VL

Cheap routing:
  OpenRouter
```

References:

* OpenRouter multimodal docs ([OpenRouter][4])
* Inkling model card ([Thinking Machines Lab][1])
* Thinking Machines Inkling announcement ([Thinking Machines Lab][5])
* ChatGPT image input FAQ ([OpenAI Help Center][2])

[1]: https://thinkingmachines.ai/model-card/inkling/?utm_source=chatgpt.com "Inkling Model Card - Thinking Machines Lab"
[2]: https://help.openai.com/zh-hans-cn/articles/8400551-chatgpt-%E5%9B%BE%E7%89%87%E8%BE%93%E5%85%A5%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98?utm_source=chatgpt.com "ChatGPT 图像输入常见问题 | OpenAI Help Center"
[3]: https://www.reuters.com/business/ai-startup-thinking-machines-launches-an-open-weight-ai-model-2026-07-15/?utm_source=chatgpt.com "AI startup Thinking Machines launches an open-weight AI model"
[4]: https://openrouter.ai/docs/guides/overview/multimodal/overview?utm_source=chatgpt.com "OpenRouter Multimodal | Complete Documentation | OpenRouter | Documentation"
[5]: https://thinkingmachines.ai/news/introducing-inkling/?utm_source=chatgpt.com "Inkling: Our Open-Weights Model - Thinking Machines Lab"
