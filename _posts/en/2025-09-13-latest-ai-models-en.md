---
audio: false
date: 2025-09-13
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Latest AI Models and Their Applications
translated: false
type: note
---

Here’s a summary of what we *do* know (as of mid-September 2025) about GPT-5, Gemini 2.5 Pro, GPT-5 mini, and how they are being used, including in Copilot / premium models:

---

## GPT-5 (OpenAI)

* **Released**: August 7, 2025. ([OpenAI][1])
* **What it is**: A unified LLM with improved reasoning, lower hallucination, better performance in coding, math, writing, health, visual perception, etc. It includes a version “GPT-5 pro” for more demanding tasks. ([OpenAI][1])
* **Reasoning / thinking**: GPT-5 has an internal mechanism (“fast” vs “deeper reasoning”) and users can select “GPT-5 thinking” or give prompts like “think hard about this” to ask for more in-depth reasoning. ([OpenAI][1])
* **Access tiers / limitations**:

  * All ChatGPT users have access (free + paid). ([OpenAI][1])
  * Free users have more limited usage, and after certain usage they might be transitioned to a lighter version (“GPT-5 mini”). ([OpenAI][1])
  * Paid (Plus, Pro, Team, Enterprise, EDU) get higher usage limits; Pro users get “GPT-5 pro”. ([OpenAI][1])

---

## Gemini 2.5 Pro (Google)

* **Release / availability**:

  * Gemini 2.5 Pro (experimental) was first announced March 25, 2025. ([blog.google][2])
  * The stable (“general availability”) Gemini 2.5 Pro was released June 17, 2025. ([Google Cloud][3])
* **Capabilities**: It is Google’s most advanced model in the Gemini 2.5 family. It has things like a large context window (1 million tokens), strong reasoning, coding, multilingual support, etc. ([blog.google][2])

---

## GPT-5 mini

* **What / when**: GPT-5 mini is a lighter/faster version of GPT-5 that has become available in GitHub Copilot (public preview) in mid-August 2025. ([The GitHub Blog][4])
* **Where and how**: It’s available in GitHub Copilot Chat (on github.com), in VS Code, on GitHub Mobile (iOS/Android). It will also appear in the model picker for users. ([The GitHub Blog][4])
* **Premium requests / cost**: It does *not* consume “premium requests” in GitHub Copilot paid plans. That is, using GPT-5 mini doesn’t use up the “premium request” quota. ([The GitHub Blog][4])

---

## How these are used in **Copilot / Premium / Microsoft / GitHub**

* **GitHub Copilot**:

  * All Copilot plans (including Free) now have access to GPT-5 mini. ([The GitHub Blog][4])
  * GPT-5 (full version) is available only on paid Copilot plans. ([The GitHub Blog][5])
  * Model picker lets users choose between GPT-5, GPT-5 mini, etc., depending on their plan and organization settings. ([The GitHub Blog][4])

* **Microsoft Copilot / Copilot Studio / 365 Copilot**:

  * Microsoft supports using GPT-5 in its Copilot products. For example, makers using Copilot Studio can select GPT-5, and there is auto-routing between different GPT-5 variants (chat vs reasoning) etc. ([Microsoft Developer][6])
  * Premium features generally require paid subscriptions. GPT-5 usage, or higher-capacity models, or those with more reasoning are often restricted to paying users or enterprise tiers. ([OpenAI][1])

---

If you want, I can also dig into **performance comparisons** (GPT-5 vs Gemini 2.5 Pro etc.), or **future/rumored features**. Do you want that?

[1]: https://openai.com/index/introducing-gpt-5/?utm_source=chatgpt.com "Introducing GPT-5"
[2]: https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/?utm_source=chatgpt.com "Gemini 2.5: Our most intelligent AI model"
[3]: https://cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions?utm_source=chatgpt.com "Model versions and lifecycle | Generative AI on Vertex AI"
[4]: https://github.blog/changelog/2025-08-13-gpt-5-mini-now-available-in-github-copilot-in-public-preview/?utm_source=chatgpt.com "GPT-5 mini now available in GitHub Copilot in public preview"
[5]: https://github.blog/changelog/2025-09-09-openai-gpt-5-and-gpt-5-mini-are-now-generally-available-in-github-copilot/?utm_source=chatgpt.com "OpenAI GPT-5 and GPT-5 mini are now generally available ..."
[6]: https://developer.microsoft.com/blog/gpt-5-for-microsoft-developers?utm_source=chatgpt.com "GPT-5 for Microsoft Developers"
