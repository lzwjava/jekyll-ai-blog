---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5.2
title: Codex CLI with OpenRouter Guide
translated: false
type: note
---

Question: How to use the OpenRouter API in the Codex CLI

Answer:

Below is a **practical, step-by-step guide** to using the **OpenRouter API** with the **Codex CLI**. I’ll explain both the **conceptual model** and the **exact commands**, so you can actually run it without guessing.

---

## 1. What’s going on conceptually

* **Codex CLI** is a command-line interface that talks to an LLM via an **OpenAI-compatible API**.
* **OpenRouter** provides an **OpenAI-compatible endpoint** that proxies many models (Claude, GPT-4, DeepSeek, Qwen, etc.).
* Therefore, you **do not need special Codex support** for OpenRouter.
* You just point Codex to:

  * a **custom API base URL**
  * your **OpenRouter API key**
  * a **model name that OpenRouter supports**

---

## 2. Get an OpenRouter API key

1. Go to OpenRouter and sign in.
2. Create an API key.
3. Copy it — you’ll use it as `OPENAI_API_KEY`.

> OpenRouter keys look like:
> `sk-or-v1-xxxxxxxxxxxxxxxx`

---

## 3. Install Codex CLI (if not installed)

```bash
npm install -g @openai/codex
```

Verify:

```bash
codex --version
```

---

## 4. Configure environment variables (most important step)

Codex CLI reads **OpenAI-style environment variables**.

### Bash / Zsh / Linux / macOS

```bash
export OPENAI_API_KEY="sk-or-v1-xxxxxxxxxxxxxxxx"
export OPENAI_BASE_URL="https://openrouter.ai/api/v1"
```

### Optional but recommended (OpenRouter headers)

OpenRouter asks for attribution headers. Codex won’t set them automatically, but you can:

```bash
export OPENROUTER_SITE_URL="https://your-site-or-github"
export OPENROUTER_APP_NAME="codex-cli"
```

> These are optional but help avoid rate limits.

---

## 5. Choose a model supported by OpenRouter

Examples:

* `anthropic/claude-3.5-sonnet`
* `openai/gpt-4o`
* `deepseek/deepseek-coder`
* `qwen/qwen-2.5-coder-32b`

You can see the full list on OpenRouter’s model page.

---

## 6. Run Codex with OpenRouter

### Basic example

```bash
codex \
  --model anthropic/claude-3.5-sonnet \
  "Explain how a TCP three-way handshake works"
```

### Code generation example

```bash
codex \
  --model deepseek/deepseek-coder \
  "Write a Python script that parses a log file and counts HTTP status codes"
```

### Interactive mode

```bash
codex --model openai/gpt-4o
```

Then just type prompts interactively.

---

## 7. Using Codex for repo-aware coding (common use case)

Inside a Git repo:

```bash
codex \
  --model qwen/qwen-2.5-coder-32b \
  "Refactor this project to use dependency injection"
```

Codex will:

* Read files
* Propose diffs
* Ask before applying changes (depending on flags)

---

## 8. Common problems & fixes

### ❌ `401 Unauthorized`

* Your `OPENAI_API_KEY` is wrong
* Key not exported in the current shell

Check:

```bash
echo $OPENAI_API_KEY
```

---

### ❌ `404 model not found`

* Model name must **exactly** match OpenRouter’s model ID

Example mistake:

```text
claude-3.5-sonnet   ❌
anthropic/claude-3.5-sonnet ✅
```

---

### ❌ Codex still talks to OpenAI

* `OPENAI_BASE_URL` not set or set incorrectly

Correct value:

```text
https://openrouter.ai/api/v1
```

---

## 9. Recommended model choices (practical)

| Use case               | Model                         |
| ---------------------- | ----------------------------- |
| Large refactors        | `anthropic/claude-3.5-sonnet` |
| Competitive coding     | `deepseek/deepseek-coder`     |
| Balanced daily use     | `openai/gpt-4o`               |
| Big codebase reasoning | `qwen/qwen-2.5-coder-32b`     |

---

## 10. Mental model to remember

> **Codex CLI = OpenAI client**
> **OpenRouter = OpenAI-compatible proxy**

Once you understand this, everything “just works.”

If you want, I can also:

* Show a **`.env` setup**
* Compare **Codex CLI vs Aider vs Continue**
* Optimize **model + cost** for long coding sessions

Just say the word. 🚀