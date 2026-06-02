---
audio: false
generated: true
image: false
lang: en
layout: post
title: AGENTS.md in Open Source Assistants
translated: false
type: note
---

Question: What is equivalent to CLAUDE.md in OpenCode (or open-source assistants)?

Answer:
In the open-source and agentic IDE landscape of 2026, the equivalent to `CLAUDE.md` is **`AGENTS.md`**.

While Anthropic popularized the concept with `CLAUDE.md`, the open-source community and several "open" alternatives (like **OpenCode**, **Continue**, and **Aider**) have coalesced around `AGENTS.md` as the vendor-neutral standard for global and project-specific instructions.

### 1. The Standard: `AGENTS.md`

This file serves as the "source of truth" for any AI agent interacting with your codebase. Most open-source tools now support a hierarchical discovery process similar to how `.gitignore` works:

* **Global Rules:** Located at `~/.config/agents/AGENTS.md` (or similar home directory paths). These rules apply to every project you open.
* **Project Rules:** Located in the project root (`./AGENTS.md`). These override global rules for that specific repo.
* **Scoped Rules:** Some tools (like OpenCode) allow `AGENTS.md` files in subdirectories to provide context for specific modules (e.g., frontend vs. backend).

### 2. Tool-Specific Equivalents

If you are using specific open-source or popular alternatives to Claude Code, here is where they look for their "Global Rules":

| Tool | Primary Config File | Support for `AGENTS.md`? |
| :--- | :--- | :--- |
| **OpenCode** | `OPENCODE.md` or `.opencode/rules.md` | **Yes** (Native fallback) |
| **Continue** | `.continue/config.json` (System Prompt) | via custom context providers |
| **Aider** | `.aider.conf.yml` or `.aider.instructions.md` | **Yes** |
| **Cursor** | `.cursor/rules/*.mdc` | Partial (reads as reference) |
| **Cline / Roo Code** | `.clinerules` | **Yes** |

### 3. What to Include in Your "Global Rules"

Regardless of the filename, your equivalent file should follow the same Markdown structure to be effective:

* **Style & Conventions:** (e.g., "Always use Functional Components," "Prefer TypeScript over JS.")
* **Tech Stack:** Specific versions of libraries to avoid the AI guessing outdated APIs.
* **Forbidden Patterns:** (e.g., "Never use `any`," "Do not use Barrel exports.")
* **Workflow Hooks:** Build and test commands (e.g., `## Commands - Test: npm test`).

### 4. Why Use `AGENTS.md`?

Using the `AGENTS.md` standard in OpenCode allows you to remain **LLM-agnostic**. If you switch your backend from Claude to GPT-5 or a local Llama 4 model, the agent will still read the same ruleset without you having to rename files or update system prompts manually in a UI.

References:

* [How to Configure Every AI Coding Assistant: CLAUDE.md, AGENTS.md, Cursor Rules and More](https://www.deployhq.com/blog/ai-coding-config-files-guide)
* [Claude Code Overview - Customizing with CLAUDE.md](https://code.claude.com/docs/en/overview)
* [Cursor Alternatives in 2026 - Builder.io](https://www.builder.io/blog/cursor-alternatives-2026)
