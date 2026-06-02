---
audio: false
generated: true
image: false
lang: en
layout: post
title: Upgrade Claude Code Quickly Now
translated: false
type: note
---

If you’re looking to **upgrade Claude Code**, the command-line coding agent from Anthropic, here’s how you can do it—and get the latest capabilities like learning modes and custom subagents working smoothly.

---

### How to Upgrade Claude Code

1. **Check your current version**
   Run:

   ```
   claude --version
   ```

   This lets you see which version you're currently running.

2. **Update via npm**
   The simplest upgrade method is:

   ```
   npm install -g @anthropic-ai/claude-code@latest
   ```

   This pulls down the latest release from npm.
   Users on Reddit report that this fixed bugs and improved responsiveness. One wrote:

   > “After updating to the latest version (1.0.18), it’s like night and day — feels way smarter and more responsive.”
   > ([Reddit][1], [Anthropic][2])

3. **Alternatively, use the native installer (Beta)**
   If you prefer a standalone binary (rather than npm), try:

   ```
   curl -fsSL https://claude.ai/install.sh | bash -s latest
   ```

   (On Windows, use the PowerShell version)
   ([Anthropic][3])

4. **Verify the update**
   After installation, restart your terminal and run `claude --version` again to confirm the new version is active.

5. **Troubleshooting installation issues**
   If you face problems, try uninstalling first:

   ```
   npm uninstall -g @anthropic-ai/claude-code
   npm install -g @anthropic-ai/claude-code
   ```

   Some users found this sequence resolved update glitches. ([Anthropic][4], [Reddit][1], [Anthropic][5], [The Verge][6])

---

### What’s New in Recent Updates?

#### Learning Modes

Anthropic recently added two new learning styles within Claude Code: **“Explanatory”** and **“Learning”**. These help you understand the reasoning behind generated code rather than just giving you solutions. To enable them:

1. Make sure you’ve updated Claude Code.
2. Run `/output-styles` in your Claude Code session.
3. Choose between **Default**, **Explanatory**, or **Learning** style.
   This feature launched on **August 14, 2025**. ([Tom's Guide][7])

#### Custom Subagents

Claude Code now supports **subagents**—specialized AI assistants tailored for specific tasks (e.g., bug fixing, refactoring, documentation). You can set different system prompts, tool permissions, and context windows for each.
To set one up:

1. Run `/agents`
2. Choose “Create New Agent” (either user-level or project-level)
3. Define its behavior, allowed tools, and save it
   Subagents help keep your workflow cleaner, more focused, and context-aware. ([Anthropic][8])

---

### Quick Recap (No Tables, Just Clear Steps)

* **To Upgrade**:

  ```
  npm install -g @anthropic-ai/claude-code@latest
  ```

  or use the native install with `curl | bash -s latest`.

* **Enable Learning Modes**:

  * Update
  * Inside Claude Code: run `/output-styles` and choose your mode.

* **Create Subagents**:

  * Inside Claude Code: run `/agents`
  * Customize tool access, system prompt, and behavior.

---

### Final Thoughts

Upgrading Claude Code is straightforward—use npm or native installer, check you’re on the latest version, then explore the new **learning modes** and **subagent** features. These additions shift Claude Code from being just a coding assistant toward something more like a teaching partner and agentic collaborator in your development workflow.

If you’d like help crafting your first subagent or using learning mode effectively, I’d be happy to walk you through it!

[1]: https://www.reddit.com/r/ClaudeAI/comments/1l8gbfo/dont_forget_to_update_your_claude_cli_it_makes_a/?utm_source=chatgpt.com "Don't forget to update your Claude CLI! It makes a huge ..."
[2]: https://www.anthropic.com/solutions/agents?utm_source=chatgpt.com "Claude Agents | Intelligent AI Solutions \ Anthropic"
[3]: https://docs.anthropic.com/en/docs/claude-code/quickstart?utm_source=chatgpt.com "Quickstart - Claude Code"
[4]: https://docs.anthropic.com/en/docs/claude-code/settings?utm_source=chatgpt.com "Claude Code settings"
[5]: https://docs.anthropic.com/en/docs/claude-code/overview?utm_source=chatgpt.com "Claude Code overview"
[6]: https://www.theverge.com/2024/11/25/24305774/anthropic-model-context-protocol-data-sources?utm_source=chatgpt.com "Anthropic launches tool to connect AI systems directly to datasets"
[7]: https://www.tomsguide.com/ai/claudes-new-learning-modes-take-on-chatgpts-study-mode-heres-what-they-do?utm_source=chatgpt.com "Claude's new 'learning modes' take on ChatGPT's Study Mode - here's what they do"
[8]: https://docs.anthropic.com/en/docs/claude-code/sub-agents?utm_source=chatgpt.com "Subagents"
