---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building Claude Code Plugins Guide
translated: false
type: note
---

Question: How to make a plugin for Claude Code, and what APIs can we use to integrate with Claude Code?

Answer: 

**Claude Code** is Anthropic's agentic coding tool (terminal-based, with VS Code / JetBrains extensions) that lets Claude read/edit files, run commands, and handle development workflows.

Plugins extend it with custom **slash commands** (`/something`), **skills**, **agents**, **hooks**, and sometimes MCP (multi-step process) servers or LSP integrations.

### How to Create a Claude Code Plugin (2026 Current Approach)

Plugins are mostly **file-based** (Markdown + JSON) — no heavy compilation is needed in most cases.

#### Basic Steps to Create a Simple Plugin

1. **Create the directory structure**
   ```
   mkdir my-awesome-plugin
   cd my-awesome-plugin
   mkdir -p .claude-plugin
   ```

2. **Create the manifest file**  
   This is required — place it at `.claude-plugin/plugin.json`

   Minimal example:
   ```json
   {
     "name": "my-awesome-plugin",
     "version": "1.0.0",
     "description": "Adds /greet and a session summary skill",
     "author": "Your Name",
     "repository": "https://github.com/yourname/my-awesome-plugin"
   }
   ```

3. **Add functionality** (choose what you need)

   - **Slash commands** — put Markdown files in `commands/`
     Example: `commands/greet/COMMAND.md`
     ```markdown
     ---
     description: Prints a friendly greeting
     ---

     Greet the user warmly and ask how their coding is going today.
     ```

   - **Skills** — put in `skills/skill-name/SKILL.md`
     Skills are reusable prompt templates/behaviors.

   - **Hooks** (run on events like session-start) — in `hooks/`

   - More advanced: agents, MCP servers, LSP servers (see docs for those)

4. **Test locally**
   Start Claude Code with your plugin folder:
   ```
   claude --plugin-dir ./my-awesome-plugin
   ```
   Or add it as a local marketplace for easier testing.

5. **Share / distribute**
   - Push to GitHub
   - Others install via:
     ```
     /plugin marketplace add https://github.com/yourname/my-awesome-plugin
     /plugin install my-awesome-plugin
     ```
   - Or create a **marketplace** (a repo containing multiple plugins) with `marketplace.json`

Many people start with **standalone skills/commands** in `~/.claude/` and later convert them to plugins.

### What APIs Can You Use to Integrate with / Extend Claude Code?

Claude Code itself does **not** expose a traditional public REST API for plugins (most extensions are declarative Markdown + JSON).

However, several integration points exist:

- **Anthropic API (Messages / Tool Use API)**  
  Core way to build custom agents/tools that talk to Claude models.  
  You can build external tools/servers that Claude Code calls via **tool use**.

- **Code Execution Tool** (in API: `code_execution_20250825`)  
  Lets Claude run Python/Node/Bash in a sandbox — many plugins indirectly leverage model capabilities powered by this.

- **Computer Use Tool** (beta)  
  Allows Claude to control a desktop (screenshots, mouse, keyboard).  
  Useful for very advanced automation plugins.

- **MCP Servers** (Multi-step Custom Processes)  
  You can write lightweight HTTP servers that Claude Code calls during complex workflows.

- **Agent SDK** (for programmatic control)  
  Lets you load plugins programmatically and build custom Claude Code sessions from code.

- **External APIs via Tool Use**  
  You define tools in the normal Anthropic tool-use format → Claude decides when to call them → your code executes the API call (GitHub, weather, database, Slack, etc.).

For most plugin authors in 2026, you **don't need** to write API servers — you just write good Markdown prompts/commands/skills.  
If you want deep programmatic integration (calling external APIs, persistent state, etc.), combine **tool use + your own backend**.

**Official starting point**  
→ https://code.claude.com/docs/en/plugins

**Examples & inspiration**  
Search GitHub for "claude-code-plugin" or visit community marketplaces like buildwithclaude.com

References:  

- [Create plugins - Claude Code Docs](https://code.claude.com/docs/en/plugins)
- [How to Build Claude Code Plugins: A Step-by-Step Guide | DataCamp](https://www.datacamp.com/tutorial/how-to-build-claude-code-plugins)
- [How to Build Your Own Claude Code Plugin (Complete Guide) | Agnost AI Blog](https://agnost.ai/blog/claude-code-plugins-guide)
- [Code execution tool - Anthropic Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)
- [Computer use tool - Anthropic Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)