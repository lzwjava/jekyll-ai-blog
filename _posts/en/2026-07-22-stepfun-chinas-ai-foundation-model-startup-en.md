---
audio: false
generated: true
image: false
lang: en
layout: post
title: "StepFun: China's AI Foundation Model Startup"
translated: false
type: note
---

Question: Introduction to **StepFun** ([https://www.stepfun.com/](https://www.stepfun.com/))

Answer:

## Overview

StepFun (Chinese name: 上海阶跃星辰智能科技有限公司) is one of China's leading foundation model startups, often grouped with companies such as Moonshot AI, MiniMax, and Zhipu AI as the new generation of Chinese frontier AI labs. It was founded in **April 2023** and is headquartered in **Shanghai**. ([Wikipedia][1])

The company is building:

* Large Language Models (LLMs)
* Multimodal models (vision + language)
* Speech models (ASR/TTS)
* Image generation/editing models
* Agent-oriented models
* API platform for developers

Their positioning today is similar to what OpenAI or Anthropic provides, but focused on both the Chinese market and increasingly international developers.

---

## Founders

The company was founded by former Microsoft executives:

* Jiang Daxin (CEO)
* Zhu Yibo
* Jiao Binxing

Jiang Daxin previously served as a Microsoft Vice President and has a strong systems/software engineering background. ([Wikipedia][1])

---

## Funding

StepFun has attracted major Chinese investors, including:

* Tencent
* Qiming Venture Partners
* Shanghai state-backed investment funds

According to recent reporting, the company has raised multiple large funding rounds and has been preparing for a Hong Kong IPO with valuations reported around **US$10–12 billion**. ([Wikipedia][1])

---

## Model Family

StepFun develops several model families.

### Step 3.x

Their flagship LLM series.

Recent releases include:

* Step 3
* Step 3.5 Flash
* Step 3.7 Flash

These models emphasize:

* coding
* agents
* tool use
* long context
* multimodal reasoning

Their official platform describes Step 3.7 Flash as optimized for production agents with reliable tool orchestration, browser/terminal interaction, MCP compatibility, and multimodal understanding. ([StepFun][2])

---

### Step-Audio

One of the stronger open speech models from China.

Capabilities include:

* speech recognition
* speech synthesis
* voice cloning
* emotion control
* multilingual speech

They also published the research paper and open-sourced parts of the system. ([arXiv][3])

---

### Step Image

Image generation and editing models intended to compete with systems like FLUX, GPT Image, and Midjourney for developer workflows. ([StepFun][2])

---

### Agent Models

A major strategic direction.

Recent products include:

* Step DeepResearch
* Step Plan
* agent-oriented Flash models

The company is investing heavily in:

* browser agents
* coding agents
* tool calling
* planning
* long-horizon reasoning

rather than only chatbot-style interaction. ([StepFun][4])

---

## Research

Compared with many startups that mainly ship APIs, StepFun publishes a significant amount of research.

Examples include:

* Step-3 system/model co-design
* Step-Audio
* Step-Prover
* Step-Formalizer

Topics include:

* efficient inference
* theorem proving
* speech models
* RL
* multimodal learning
* reasoning
* agent systems

([arXiv][5])

---

## Open Source

They have begun open-sourcing several projects, including:

* Step-Audio
* StepDeepResearch
* model checkpoints for some releases

Recent Step 3.7 Flash releases are available in formats including BF16, FP8, and GGUF for local inference. ([Reddit][6])

---

## Developer Platform

Their API platform provides:

* Chat Completion APIs
* Vision APIs
* Image APIs
* Speech APIs
* Embeddings
* Agent-oriented models
* Subscription plans ("Step Plan")

The platform is targeting developers building with tools such as Cursor, Claude Code, OpenClaw, and other agent frameworks. ([StepFun][2])

---

## Why StepFun Matters

From an engineering perspective, StepFun is interesting because it is focusing on several frontier areas simultaneously:

* Production-grade agent models
* Multimodal reasoning
* Efficient MoE architectures
* Model–system co-design for faster inference
* Open-source speech technology
* Long-context coding models

If you're interested in LLM infrastructure, inference optimization, or agent engineering, StepFun is one of the Chinese labs worth following alongside DeepSeek and Moonshot.

References:

* [StepFun official website](https://www.stepfun.com/?utm_source=chatgpt.com)
* [StepFun Open Platform](https://platform.stepfun.ai/?utm_source=chatgpt.com)
* [Developer Documentation](https://platform.stepfun.ai/docs/en/step-plan/overview?utm_source=chatgpt.com)

[1]: https://en.wikipedia.org/wiki/StepFun?utm_source=chatgpt.com "StepFun"
[2]: https://platform.stepfun.ai/?utm_source=chatgpt.com "StepFun Open Platform"
[3]: https://arxiv.org/abs/2502.11946?utm_source=chatgpt.com "Step-Audio: Unified Understanding and Generation in Intelligent Speech Interaction"
[4]: https://platform.stepfun.ai/docs/en/step-plan/overview?utm_source=chatgpt.com "Step Plan overview - StepFun Documentation"
[5]: https://arxiv.org/abs/2507.19427?utm_source=chatgpt.com "Step-3 is Large yet Affordable: Model-system Co-design for Cost-effective Decoding"
[6]: https://www.reddit.com/r/LocalLLM/comments/1trlnrp/stepfun_releases_step_37_flash_a_198b_moe/?utm_source=chatgpt.com "StepFun Releases Step 3.7 Flash: A 198B MoE Vision-Language Model for Coding Agents and Search Workflows"
