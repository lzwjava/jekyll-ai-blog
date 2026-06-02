---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Agent Architecture Overview
translated: false
type: note
---

Based on exploring the codebase, here's the architecture of Hermes Agent:

HERMES AGENT ARCHITECTURE
=========================

1. CORE ENTRY POINTS
--------------------
- run_agent.py (AIAgent class) - Core conversation loop, ~12k LOC
- cli.py (HermesCLI class) - Interactive CLI orchestrator, ~11k LOC
- model_tools.py - Tool orchestration, discovery, and dispatch

2. MAIN COMPONENTS
------------------

AIAgent (run_agent.py)
  - Main agent loop: user message → LLM call → tool calls → repeat
  - Handles: model providers, message history, budget tracking, interrupts
  - Supports multiple API modes: chat_completions, codex_responses, etc.
  - Max 90 tool-calling iterations by default

Tool System (tools/ + model_tools.py)
  - tools/registry.py - Central registry, auto-discovers tools/*.py
  - Each tool file calls registry.register() at import time
  - Tools organized by "toolset" (web, terminal, file, etc.)
  - Handler must return JSON string

CLI (cli.py)
  - Rich for banners/panels, prompt_toolkit for input
  - Skin engine for theming (default, ares, mono, slate)
  - Slash command registry in hermes_cli/commands.py
  - Commands: /help, /model, /skin, /note, etc.

Gateway (gateway/)
  - Messaging platforms: telegram, discord, slack, whatsapp, signal, matrix, etc.
  - Platform adapters in gateway/platforms/
  - Session management via SQLite (hermes_state.py)
  - Run with: hermes gateway

3. PLUGIN SYSTEM (plugins/)
---------------------------
- PluginManager discovers from ~/.hermes/plugins/, ./.hermes/plugins/, pip
- Plugins can register:
  - Tools (ctx.register_tool)
  - Commands (ctx.register_command)
  - Hooks (pre/post tool/LLM calls)
  - Model providers
  - Memory providers
  - Image/video gen providers

4. CONFIG & STATE
-----------------
- ~/.hermes/config.yaml - Settings
- ~/.hermes/.env - API keys only
- ~/.hermes/skills/ - Custom skills
- ~/.hermes/plugins/ - Custom plugins
- ~/.hermes/skins/ - Custom themes
- Logs: ~/.hermes/logs/ (agent.log, errors.log)

5. DEPENDENCY FLOW
------------------
tools/registry.py (no deps)
       ↑
tools/*.py (import registry at module level)
       ↑
model_tools.py (imports registry + triggers discovery)
       ↑
run_agent.py, cli.py, batch_runner.py

6. SKILLS SYSTEM
----------------
- Built-in skills in skills/ directory
- Optional skills in optional-skills/
- Custom skills in ~/.hermes/skills/
- Loaded as user message (not system prompt) for prompt caching
- Each skill is a SKILL.md with YAML frontmatter

7. ADDITIONAL COMPONENTS
------------------------
- ui-tui/ - Ink (React) terminal UI
- tui_gateway/ - Python JSON-RPC backend for TUI
- acp_adapter/ - ACP server (VS Code/Zed/JetBrains)
- cron/ - Job scheduler
- batch_runner.py - Parallel batch processing
- website/ - Docusaurus docs

The architecture follows a clean plugin-based design where:
- Core agent loop is simple: LLM → tools → repeat
- Tools are auto-discovered and registered
- Platforms are pluggable via gateway adapters
- Everything extensible via plugins
