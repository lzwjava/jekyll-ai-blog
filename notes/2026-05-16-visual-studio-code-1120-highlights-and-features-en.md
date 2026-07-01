---
audio: false
generated: true
image: false
lang: en
layout: post
title: Visual Studio Code 1.120 Highlights and Features
translated: false
type: note
---

Question: What are the new features and highlights of Visual Studio Code version 1.120?

Answer:

## Visual Studio Code 1.120 — Release Overview

**Released:** May 13, 2026

VS Code 1.120 brings the Agents window to Stable, improves BYOK model visibility and control, and adds Markdown quality-of-life improvements and agent safety features.

---

## 🤖 Agents

### Agents Window Now in Stable (Preview)

The new Agents window is a companion to the editor you already know — purpose-built for agent-driven development, with a dedicated space to explore, iterate on, and review tasks across multiple projects, and seamlessly switch between them. It lets you pick your agent harness, run agents on remote machines, and configure the environment the way you want it — color themes, keybindings, and extensions included.

Key improvements in this release for the Agents window:

- **Preferences persist across sessions** — your last choices in dropdowns like agent harness and isolation mode are retained.
- **Discard changes easily** — edits can be discarded directly from the Changes panel.
- **Sync upstream changes** — a sync button on the Files panel lets you pull in upstream changes from the base branch before the agent starts.
- **Navigate between recent sessions** — arrow buttons in the top-left of the title bar let you jump between recent sessions.
- **Per-window settings overrides** — you can override specific VS Code settings just for the Agents window.

You can open the Agents window via the **"Open in Agents"** button in the VS Code title bar.

### Copilot CLI Plugins Auto-Discovery

Agent plugins installed with the GitHub Copilot CLI are picked up automatically by VS Code, so a single `copilot plugin install` covers both surfaces. Previously, you had to install the same plugin separately in VS Code or add its path to the `chat.plugins.paths` setting.

---

## 🧠 Language Models (BYOK Improvements)

### Accurate Token Usage for BYOK Models

The context window control in the Chat view now shows accurate token usage and percent-full for BYOK (Bring Your Own Key) models. Previously, when chatting with a model brought via your own API key (Anthropic, OpenAI, or other), the control always displayed 0% and a zero-token count because token accounting was only working for built-in models.

### Configure Thinking Effort for BYOK Reasoning Models

You can now configure the thinking effort for BYOK reasoning models directly from the model picker in the Chat view. The selected effort is forwarded to the model on every request, letting you trade off latency and cost against answer quality. This applies to OpenAI-compatible endpoints (OpenAI, xAI/Grok, OpenRouter, and custom Azure OpenAI deployments). Anthropic models already supported this; the control is now consistent across providers.

### Model Picker Organized by Provider

The model picker in the Chat view now groups models by their provider, making it easier to find the model you want when you have access to models from multiple sources. Recently used models also display the provider name in grey text alongside the model name, so you can quickly distinguish between similarly named models from different providers. You can also quickly access models by typing `/models` in the chat input.

---

## 💬 Chat Enhancements

### Terminal Tool Output Compression (Preview)

Long terminal output from commands like `git diff`, `ls -l`, and `npm install` can consume a large share of the model's context window. When you enable the `chat.tools.compressOutput.enabled` setting, VS Code post-processes the output of these commands before sending it to the model. Large unchanged hunks in diffs are collapsed, lockfile and snapshot diffs are dropped, `ls -l` is reduced to entry names, and `npm install` progress bars, deprecation warnings, and audit summaries are stripped.

### Risk Assessment for Terminal Commands (Experimental)

To help you decide quickly whether a command is worth a closer look, terminal command confirmations now include a risk badge with an AI-generated explanation of what the command does. Each badge shows one of three levels: **Safe** (green) — reads files or prints output without changes; **Caution** (orange) — modifies the workspace, installs packages, or sends data over the network; **Review carefully** (red) — performs an action that may be difficult or impossible to undo, such as force-pushing to a remote or deleting files outside the workspace.

---

## 📝 Markdown Improvements

This release adds a Markdown diff preview, allowing developers to review Markdown content as rendered output instead of raw syntax when viewing diffs.

---

## 📊 Summary Table

| Area | Feature | Status |
| --- | --- | --- |
| Agents | Agents Window | Stable Preview |
| Agents | Copilot CLI Plugin Auto-Discovery | GA |
| Language Models | BYOK Token Usage Display | GA |
| Language Models | Thinking Effort for BYOK | GA |
| Language Models | Model Picker by Provider | GA |
| Chat | Terminal Output Compression | Preview |
| Chat | Terminal Command Risk Assessment | Experimental |
| Editor | Markdown Diff Preview | GA |

References:

- [Visual Studio Code 1.120 Release Notes](https://code.visualstudio.com/updates/v1_120)
- [VS Code Release Archive](https://code.visualstudio.com/updates/archive)
