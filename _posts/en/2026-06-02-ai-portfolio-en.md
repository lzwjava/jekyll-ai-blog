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

### Xiaomi MIMO Subscription — 500 Million Tokens Used

Pro Monthly Plan with 38B main quota + 8.75B compensation quota (~4.6B free credit). 500M tokens consumed so far.

![Xiaomi MIMO Pro Plan — 500M tokens consumed, ~4.6B free credit remaining](/assets/images/ai-portfolio/xiaomi-mimo-usage.png)

### Summary

| Platform | Tokens | Period | Cost |
|----------|--------|--------|------|
| OpenRouter | 927M | Past year | $192 |
| SSSAICode (Claude) | 115M+ | April 2026 | $171.53 |
| Xiaomi MIMO | 500M | Current plan | Free 4.6B credit |
| **Total** | **~1.54B** | **Past year** | **—** |

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

### iclaw — Terminal AI Agent (REPL)

[iclaw](https://github.com/lzwjava/iclaw) is a terminal AI agent that codes, searches, and runs commands autonomously — works on personal machines and locked-down enterprise ones. A minimal openclaw implementation, built as a plain Python CLI with no browser extensions or IDE plugins, powered by GitHub Copilot.

```
lzwjava@lzw-mac iclaw % iclaw

  ██  █████  ██       █████  ██   ██
  ██ ██      ██      ██   ██ ██   ██
  ██ ██      ██      ███████ ██ █ ██
  ██ ██      ██      ██   ██ ██████
  ██  █████  ███████ ██   ██  ███ ██

Available commands:
  /provider_model      Select and authenticate with the model provider
  /model               Select specific model from your provider
  /search              Web search (usage: /search <query>)
  /provider_search     Select the web search provider
  /proxy               Set HTTP/HTTPS proxy (usage: /proxy [url|off])
  /ca_bundle           Set CA bundle for HTTPS (usage: /ca_bundle [path|off])
  /log                 Set log verbosity (usage: /log [verbose|info])
  /copy                Copy last Copilot response to clipboard
  /read                Print file contents to terminal (usage: /read <path>)
  /clear               Clear conversation history
  /compact             Compact conversation history using LLM
  /export              Export full conversation history to JSON file
  /status              Show current settings
  /help                Show available commands
  /exit                Quit the REPL.
```

**Key features:**
- **Multi-turn conversations** with GitHub Copilot or OpenRouter in your terminal.
- **Multiple Model Providers**: GitHub Copilot (OAuth device flow) and OpenRouter (API key).
- **Native Tool Calling**: The model autonomously invokes web search, executes shell commands, and edits files — no human in the loop.
- **Multiple Search Providers**: DuckDuckGo, Startpage, Bing, and Tavily.
- **Enterprise-friendly**: No IDE plugins or browser extensions required. Works behind corporate firewalls with proxy and CA bundle support.
- **Default model**: GPT-5.2.

![iclaw — Terminal AI agent REPL with native tool calling](/assets/images/ai-portfolio/iclaw.jpg)

![iclaw — Execution log showing autonomous coding and shell commands](/assets/images/ai-portfolio/iclaw-log.png)

### Other Projects

- **[zz](https://github.com/lzwjava/zz)** — Dataset processing and training utilities for ML projects. Used during GPT-2 124M training runs on RunPod H200, DigitalOcean H100, and home RTX 4070.
### jekyll-ai-blog — AI-Powered Blog Platform

[jekyll-ai-blog](https://github.com/lzwjava/jekyll-ai-blog) is the source for [lzwjava.github.io](https://lzwjava.github.io) — a Jekyll blog enhanced with AI-powered automation. 10,000+ English posts, 10,000+ Chinese posts, 9,700+ AI answer notes. ~70,000 page views in the past month (Cloudflare Analytics).

```
lzwjava@lzw-mac jekyll-ai-blog % ls README.md
README.md
```

**What makes it different from a standard Jekyll blog:**

- **AI-Powered Translation** — LLM-based translation pipeline expands every post to multiple languages automatically via GitHub Actions.
- **Google Cloud Text-to-Speech** — Audio versions of posts generated automatically for accessibility.
- **XeLaTeX PDF/EPUB Generation** — High-quality print-ready PDFs and ebook exports from Markdown source.
- **GitHub Actions CI/CD** — Automated building, testing, translation, and deployment workflows.
- **8,000+ AI Answer Notes** — Knowledge base built from daily LLM-assisted research, searchable on the blog.
- **MathJax, Night Mode, RSS, Bilingual Content** — Standard features enhanced with custom CSS and theme.

**Scale:**

| Metric | Count |
|--------|-------|
| English posts | 10,264 |
| Chinese posts | 10,259 |
| AI answer notes | 9,794 |
| Python scripts | 323 |
| ML scripts | 191 |
| Page views (past month) | ~70,000 |

![jekyll-ai-blog — AI-powered blog with 10K+ posts, translation, TTS, and PDF pipelines](/assets/images/ai-portfolio/blog.png)
- **[lzwjava.github.io](https://github.com/lzwjava/lzwjava.github.io)** — ~400 original posts, ~8,000 AI answer notes, ~70,000 page views in the past month.

---

* GitHub: https://github.com/lzwjava
* Blog: https://lzwjava.github.io
