---
audio: false
generated: true
image: false
lang: en
layout: post
title: GitHub Copilot CLI Guide 2026
translated: false
type: note
---

Question: How do I use GitHub Copilot CLI and when was it released?

Answer:

## GitHub Copilot CLI — Overview, Release Timeline & Usage Guide

---

### Release Timeline

GitHub Copilot CLI was first released as a **public preview on September 25, 2025**. It then reached **general availability (GA) on February 25, 2026**, becoming available to all Copilot subscribers. To mark the GA milestone, the version was bumped to **v1.0**.

> **Note:** The older `gh-copilot` CLI extension is a completely different, now-archived tool. That older extension was archived on October 30, 2025, and users were encouraged to migrate to the new Copilot CLI.

---

### What Is GitHub Copilot CLI?

GitHub Copilot CLI brings AI-powered coding assistance directly to your command line, enabling you to build, debug, and understand code through natural language conversations. It is powered by the same agentic harness as GitHub's Copilot coding agent and stays deeply integrated with your GitHub workflow.

---

### Prerequisites

You need an active Copilot subscription. Copilot CLI is included as a core feature of all GitHub Copilot plans: Free, Pro, Pro+, Business, and Enterprise. Each interaction draws on your plan's premium request allowance.

If you are on an organization or enterprise plan, your admin must have Copilot CLI enabled in the organization settings.

---

### Installation

There are multiple ways to install Copilot CLI. The most common methods are:

**Via npm (all platforms):**
```bash
npm install -g @github/copilot
```

**Via shell install script (macOS/Linux):**
```bash
curl -fsSL https://github.com/github/copilot-cli/releases/latest/download/install.sh | bash
```

Using `| sudo bash` installs to `/usr/local/bin`. You can set `PREFIX` to install to a custom directory, and set `VERSION` to install a specific version.

**Via Homebrew (macOS):**
```bash
brew install gh-copilot
```

**Via WinGet (Windows):**
```powershell
winget install GitHub.CopilotCLI
```

Copilot CLI is also included in the default GitHub Codespaces image and available as a Dev Container Feature.

---

### Authentication

After installation, authenticate using your GitHub credentials:
```bash
copilot auth login
```

The CLI automatically inherits your organization's Copilot policies and governance settings once authenticated.

---

### Basic Usage

Launch the CLI by simply running:
```bash
copilot
```

You can then type natural language prompts directly. Some example tasks you can ask:

- "Write a Python function to parse JSON from a file"
- "Debug this error in my code"
- "Create a branch and open a pull request for this change"
- "Explain what this function does"

---

### Key Features & Modes

**1. Default (Interactive) Mode**
The standard conversational mode where Copilot proposes each action before executing it. Every step requires your approval.

**2. Autopilot Mode**
Press `Shift+Tab` to cycle into autopilot mode, which encourages the agent to continue working until a task is completed autonomously — executing tools, running commands, and iterating without stopping for approval.

**3. Plan Mode**
Press `Shift+Tab` into plan mode first to outline the work, use `/model` to compare approaches, and then `Shift+Tab` into autopilot when you want Copilot to carry the task forward.

**4. Background Tasks (Fleet)**
Prefix any prompt with `&` to delegate work to the Copilot coding agent in the cloud, freeing your terminal for other tasks. Use `/resume` to switch between local and remote coding agent sessions.

---

### Useful Slash Commands

| Command | Description |
|---|---|
| `/model` | Switch or compare AI models |
| `/restart` | Restart CLI while preserving session |
| `/lsp show` | Show Language Server Protocol status |
| `/diff` | Review file changes |
| `/plugin install owner/repo` | Install a community plugin |
| `/experimental show` | Access preview features |
| `/changelog` | View latest CLI updates |
| `/fleet` | Coordinate parallel subagents |

---

### MCP (Model Context Protocol) Support

Copilot CLI ships with GitHub's MCP server built in and supports custom MCP servers for connecting to any tool or service. Plugins can bundle MCP servers, agents, skills, and hooks and be installed directly from GitHub repositories.

---

### Model Selection

You can choose from the latest models including Claude Opus 4.6, Claude Sonnet 4.6, GPT-5.3-Codex, and Gemini 3 Pro. GPT-5 mini and GPT-4.1 are included with your Copilot subscription at no additional premium request cost.

---

### Platform Support

Copilot CLI supports macOS, Linux, and Windows. It operates independently in your terminal and can modify files that any editor can then display, making it useful regardless of your editor choice.

---

References:

- [GitHub Copilot CLI — Official GitHub Page](https://github.com/features/copilot/cli)
- [GitHub Copilot CLI Repository](https://github.com/github/copilot-cli)
- [GitHub Copilot CLI — General Availability Announcement](https://github.blog/changelog/2026-02-25-github-copilot-cli-is-now-generally-available/)
- [GitHub Docs — Install Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli)
- [GitHub Docs — Copilot CLI Quickstart](https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-getting-started)