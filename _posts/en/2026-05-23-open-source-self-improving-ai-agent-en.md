---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open-source Self-improving AI Agent
translated: false
type: note
---

Here's a rundown of what Hermes Agent is:

Hermes Agent is an open-source, self-improving AI agent built by Nous Research. Key points:

1. Self-improving loop — It learns from conversations: creates skills from experience, improves them during use, persists memory across sessions, and builds a user model over time. That's the core differentiator vs. a plain chatbot wrapper.

2. Model-agnostic — Works with OpenRouter (200+ models), OpenAI, Anthropic, Nous Portal, Xiaomi MiMo, HuggingFace, and custom endpoints. Switch with `hermes model`, no lock-in.

3. Multi-platform — One gateway process serves Telegram, Discord, Slack, WhatsApp, Signal, Email, and the CLI itself. You can talk to it from your phone via Telegram while it runs on a cloud VM.

4. Two interfaces:
   - CLI (`hermes`) — terminal UI with multiline editing, slash commands, autocomplete, streaming tool output
   - Gateway (`hermes gateway start`) — messaging platform bridge

5. 40+ built-in tools — terminal, file ops, web search, browser, image gen, TTS, cron scheduling, subagent delegation, etc. Tools are organized into toolsets you can enable/disable.

6. Skills system — Procedural memory stored as SKILL.md files. The agent creates skills after complex tasks, then reuses them. Compatible with agentskills.io open standard.

7. Runs anywhere — Terminal backends: local, Docker, SSH, Modal (serverless), Daytona, Singularity, Vercel Sandbox. Can run on a $5 VPS or a GPU cluster.

8. Research-ready — Batch trajectory generation and compression for training future tool-calling models.

9. Built-in cron — Schedule tasks in natural language, deliver results to any connected platform.

10. OpenClaw migration — If you used OpenClaw (a predecessor), `hermes claw migrate` imports settings, memories, skills, and API keys.

The project structure centers around `run_agent.py` (the AIAgent class with the core conversation loop) and `cli.py` (the interactive CLI). Tools auto-discover via `tools/registry.py`. The gateway lives in `gateway/` with per-platform adapters.

License: MIT. Built by Nous Research.
