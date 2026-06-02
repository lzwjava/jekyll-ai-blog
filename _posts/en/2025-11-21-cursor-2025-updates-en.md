---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Cursor 2025 Features and Updates
translated: false
type: note
---

### Overview of Cursor's Recent Features

Cursor, the AI-powered code editor built on VS Code, has seen rapid evolution in 2025, with a major focus on agentic workflows, multi-model support, and seamless integrations. The biggest update is **Cursor 2.0** (released October 29, 2025), which introduces Composer—a proprietary coding model—and a redesigned interface for managing multiple AI agents in parallel. This shifts the editor from traditional coding to orchestrating AI-driven tasks, like building features autonomously or debugging across codebases. Below, I'll break down the key new functions, grouped by release and category, based on official announcements and user reports up to November 21, 2025.

### Major Releases and Core New Functions

#### Cursor 2.0 (October 29, 2025) – Agent-Centric Overhaul

This version reimagines Cursor as an "agent fleet manager," emphasizing delegation over manual coding. Key additions:

- **Composer Model**: Cursor's first in-house coding model, optimized for speed and large codebases. It uses semantic search for context-aware edits, enabling natural language code generation/modification. It's 21% more selective in suggestions but has a 28% higher acceptance rate than prior models.
- **Multi-Agent Interface**: Run up to 8 agents simultaneously on the same task (e.g., one for planning, another for testing). Includes an "inbox" sidebar for monitoring progress, reviewing diffs like pull requests, and spawning agents with different models (e.g., Claude Sonnet 4.5 vs. GPT-5.1).
- **Integrated Browser Controls**: Agents can now control an embedded Chrome instance—taking screenshots, debugging UI issues, or testing end-to-end. This is generally available (GA) post-beta, with enterprise support for secure usage.
- **Plan Mode (Enhanced)**: Agents auto-generate editable plans for tasks, with tools for codebase research and long-running executions. Press Shift + Tab to start; it includes clarifying questions for better outputs.
- **Voice Mode**: Dictate prompts via speech-to-text; custom submit keywords trigger agent runs. Supports MCP elicitation for structured user inputs (e.g., JSON schemas for preferences).
- **Automatic Code Review**: Built-in diff reviews for every AI-generated change, catching bugs before merge.
- **Cloud Agents**: Run agents remotely (faster startup, improved reliability) without tying up your local machine. Manage fleets in-editor, ideal for offline work.

#### 1.7 Update (September 29, 2025) – Workflow Boosters

- **Slash Commands**: Quick actions like `/summarize` for on-demand context compression (frees up token limits without new chats).
- **Custom Hooks**: Automate agent behaviors, e.g., pre/post-task scripts for linting or testing.
- **Team-Wide Rules**: Share codebase rules (e.g., Bugbot for automated reviews) across teams via `.cursorrules` files.
- **Menubar Support and Deeplinks**: Easier navigation and external integrations.

#### Earlier 2025 Highlights (May–August)

- **Background Agents (0.50, May 15)**: Parallel task execution (e.g., one agent refactors while another tests). Preview on macOS/Linux.
- **Improved Tab Model (Multiple Updates)**: Cross-file edits, 1M+ token context windows, and online RL training for smarter, faster autocompletions (e.g., React hooks, SQL queries).
- **@folders and Inline Edits**: Reference entire directories in prompts; refreshed CMD+K for full-file changes with precise search/replace.
- **YOLO Mode (Agent Enhancements)**: Autonomous terminal commands, lint fixing, and self-debugging until resolution.

### Model Integrations

Cursor now supports cutting-edge models for varied tasks:

- **OpenAI (November 13, 2025)**: GPT-5.1 (planning/debugging), GPT-5.1 Codex (ambitious coding), GPT-5.1 Codex Mini (efficient edits).
- **Anthropic**: Sonnet 4 (May 22, 2025) and Sonnet-3.7 (February 24, 2025) for superior codebase understanding.
- **Google**: Gemini 2.5 Pro (June 10, 2025) for fast growth in integrations.
- **Others**: o3/o4-mini (April 17, 2025) for enhanced coding.

| Category | Key New Function | Benefit | Release |
|----------|------------------|---------|---------|
| **Agents** | Multi-Agent Parallelism | Delegate tasks to 2–8 agents; compare outputs | 2.0 (Oct) |
| **Models** | Composer + GPT-5.1 Suite | Faster, context-aware generation | 2.0/Nov |
| **UI/Workflow** | Plan Mode + Integrated Browser | Auto-planning + end-to-end testing | 2.0/Sep |
| **Edits** | Cross-File Tab + Inline Refresh | Smarter refactors; full-file precision | May–Oct |
| **Collaboration** | Team Rules + Cloud Agents | Shared guidelines; remote execution | Sep/Oct |

### Pricing and Accessibility Updates

- **Simplified Tiers (June 16, 2025)**: Pro ($20/mo compute baseline, unlimited tool calls); new Ultra ($200/mo, 20x usage) for power users.
- **Max Mode**: Token-based access to full model capabilities (e.g., long contexts) across all top models.

These features make Cursor ideal for agent-driven development, reducing manual work by up to 39% in PR merges (per a University of Chicago study). For the full changelog, check [Cursor's official site](https://cursor.com/changelog). If you're on VS Code, the migration is seamless—download and experiment with 2.0's agent view for a quick win.
