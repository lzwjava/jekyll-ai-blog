---
audio: false
generated: false
image: false
lang: en
layout: post
title: "My AI Portfolio — Evidence of Daily AI Work"
translated: false
---

I don't just talk about AI — I use it every day, at scale. This post is a visual portfolio of my AI effort: the tools I've built, the tokens I've consumed, and the certifications I've earned.

---

## 🛠️ ww — Cross-Platform CLI Toolkit

[ww](https://github.com/lzwjava/ww) is my flagship CLI toolkit — 255+ commits, 10+ command groups, cross-platform (macOS + Linux). It covers git workflows with AI commit messages, note management, image/PDF processing, web search, GitHub Copilot chat, system utilities, and LLM-powered helpers.

```
lzwjava@lzw-mac ww % uv run ww --help
Usage: ww <group> [command] [options]

Action:
  ww action [workflow.yml]  Trigger a GitHub Actions workflow

AMD Dev Cloud:
  ww amd-dev-cloud snapshots    List snapshots
  ww amd-dev-cloud start-train  Create GPU droplet for training
  ww amd-dev-cloud end-train    Snapshot and destroy a GPU droplet

Copilot:
  ww copilot auth           Authenticate via GitHub OAuth
  ww copilot chat           Chat with a Copilot model

Git:
  ww git gpa            Git pull --all for all repos
  ww git squash <n>     Squash last n commits
  ww git amend-push     Amend last commit and force push

LLM:
  ww llm compare <prompt>   Compare multiple LLM responses
  ww llm query <question>   Query local RAG documents

Note:
  ww note              Clipboard to note (fast capture)
  ww note process      Drain the note queue
  ww note watch        Auto-process daemon

Screenshot:
  ww screenshot              Capture and create a note
  ww screenshot interact-note  Interactive screenshot note

255+ commits. 10+ command groups. Cross-platform (macOS + Linux).
```

![ww — Cross-platform CLI toolkit on GitHub](/assets/images/ai-portfolio/ww1.png)

![ww — Command groups and features](/assets/images/ai-portfolio/ww2.png)

---

## 📊 LLM API Usage — The Numbers

### OpenRouter — Past Year

927M tokens consumed, $192 spend, 142K API requests across multiple models.

![OpenRouter Activity Dashboard — 927M tokens, $192 spend, 142K requests over 1 year](/assets/images/ai-portfolio/openrouter-activity.png)

![OpenRouter Model Spend Breakdown — Claude 4 Sonnet $44.40, Claude 3.5 Sonnet $9.67, Grok 3, Mistral, Kimi](/assets/images/ai-portfolio/openrouter-spend.png)

![OpenRouter Token Usage by Model — MiniMax 240M, Gemini 203M, DeepSeek 110M](/assets/images/ai-portfolio/openrouter-models.png)

### Claude API via SSSAICode — April 2026

$171.53 in one month. 2,555 requests. 115M+ tokens. 90.9% cache hit rate.

![SSSAICode Claude Usage — Opus 4.6, Opus 4.7, Sonnet 4.6, Haiku 4.5](/assets/images/ai-portfolio/sssaicode-usage.png)

### Xiaomi MIMO Subscription — 3.88 Billion Tokens Used

Pro Monthly Plan with 38B main quota + 8.75B compensation quota. 3.88B tokens consumed (44% of compensation quota).

![Xiaomi MIMO Pro Plan — 3.88B tokens consumed out of 8.75B compensation quota](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

### Summary

| Platform | Tokens | Period | Cost |
|----------|--------|--------|------|
| OpenRouter | 927M | Past year | $192 |
| SSSAICode (Claude) | 115M+ | April 2026 | $171.53 |
| Xiaomi MIMO | 3.88B | Current plan | Pro subscription |
| **Total** | **~1.5B+** | **Past year** | **—** |

---

## 🎓 Certificates

### Machine Learning Specialization — DeepLearning.AI & Stanford University

Completed Nov 2023. Three courses: Supervised Machine Learning, Advanced Learning Algorithms, Unsupervised Learning, Recommenders, Reinforcement Learning.

![Coursera Machine Learning Specialization Certificate — Zhiwei Li, Nov 2023](/assets/images/ai-portfolio/coursera-ml-1.png)

### Deep Learning Specialization — DeepLearning.AI

Completed Dec 2023. Five courses: Neural Networks, Hyperparameter Tuning, Structuring ML Projects, CNNs, Sequence Models.

![Coursera Deep Learning Specialization Certificate — Zhiwei Li, Dec 2023](/assets/images/ai-portfolio/coursera-dl-1.png)

---

## 🤖 Other AI Projects

- **[iclaw](https://github.com/lzwjava/iclaw)** — Terminal AI agent (REPL) that codes, searches, and runs shell commands autonomously. Supports GitHub Copilot (OAuth) and OpenRouter.
- **[zz](https://github.com/lzwjava/zz)** — Dataset processing and training utilities for ML projects. Used during GPT-2 124M training runs on RunPod H200, DigitalOcean H100, and home RTX 4070.
- **[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog)** — AI-powered blog platform with automated multi-language translation, Google Cloud TTS audio generation, and GitHub Actions workflows.
- **[lzwjava.github.io](https://github.com/lzwjava/lzwjava.github.io)** — ~400 original posts, ~8,000 AI answer notes, ~70,000 page views in the past month.

---

* GitHub: https://github.com/lzwjava
* Blog: https://lzwjava.github.io
