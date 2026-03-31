---
audio: false
generated: true
image: false
lang: en
layout: post
title: Claude Code Source Leak Details
translated: false
type: note
---

Question: How to see that Claude Code source leaked?

Answer: The source code for Anthropic's **Claude Code** (the official CLI tool) was reportedly leaked on **March 31, 2026**. The leak originated from an exposed `.map` (source map) file in the `@anthropic-ai/claude-code` package on the npm registry.

While the original repository you linked (`instructkr/claude-code`) is described as a **Python feature port** and workspace inspired by the leak, the actual leak details and evidence can be found by looking for the following indicators:

### 1. The Source of the Leak (npm)
The leak was discovered by security researcher **Chaofan Shou (@Fried_rice)**. He identified a `cli.js.map` file (approximately 60MB) in the official npm package. This source map contained references to the original, unobfuscated TypeScript source code, which was then mirrored across various GitHub repositories.

### 2. Evidence within the Leaked Code
The leaked codebase (estimated at ~512,000 lines of code) contains several "unhinged" and unreleased features that confirm its authenticity as internal Anthropic code:
* **"Buddy" System:** A hidden Tamagotchi-style pet system inside the terminal that hatches an ASCII companion (like a duck, capybara, or dragon) based on your user ID.
* **Undercover Mode:** A feature that automatically hides AI traces (like `Co-Authored-By` lines) when Anthropic employees contribute to public repositories.
* **Internal Codenames:** The code refers to the project as **"Tengu"** and mentions future model versions like **"Fennec"** (Opus 4.7) and **"Sonnet 4.8"**.
* **"Dream" System:** A background process that triggers every 24 hours to "consolidate" and tidy up session memories.

### 3. Repository Structure
The leaked `src/` directory typically includes:
* `src/tools/`: Implementation of tools like `BashTool`, `FileEditTool`, and `YOLO classifier` (an automated permission system).
* `src/commands/`: Slash commands like `/commit`, `/review`, and `/compact`.
* `src/bridge/`: A communication layer for IDE extensions (VS Code/JetBrains).



References:
* [Claude Code — Leaked Source (2026-03-31) - GitHub](https://github.com/nirholas/claude-code)
* [Anthropic's Claude Code source leaked via npm - PiunikaWeb](https://piunikaweb.com/2026/03/31/anthropic-claude-code-source-leaked-npm-registry/)
* [I dug through Claude Code's leaked source - Reddit](https://www.reddit.com/r/ClaudeAI/comments/1s8lkkm/i_dug_through_claude_codes_leaked_source_and/)