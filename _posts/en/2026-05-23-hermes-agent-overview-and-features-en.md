---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Agent Overview and Features
translated: false
type: note
---

Here's the rundown on the Hermes Agent README:

**What is Hermes Agent?**
Hermes is Nous Research's open-source AI agent framework. The headline feature is its self-improving learning loop — it creates skills from experience, improves them over time, maintains persistent memory across sessions, and searches past conversations. It's not just a chat wrapper; it's an autonomous agent that can schedule tasks, delegate to subagents, and talk to you across multiple platforms.

**Key capabilities:**

1. **Multi-platform gateway** — One process serves CLI, Telegram, Discord, Slack, WhatsApp, Signal, and Email simultaneously. Talk to it from anywhere.

2. **Closed learning loop** — Skills are auto-created after complex tasks, self-improve during use, and persist across sessions. FTS5-backed session search lets it recall past conversations.

3. **Cron scheduling** — Natural-language scheduled tasks that run unattended and deliver to any connected platform.

4. **Subagent delegation** — Can spawn parallel isolated agents for concurrent work, or run Python scripts via RPC to collapse multi-step tool pipelines.

5. **7 terminal backends** — Local, Docker, SSH, Singularity, Modal, Daytona, Vercel Sandbox. Serverless options (Modal, Daytona) hibernate when idle.

6. **Model-agnostic** — Nous Portal, OpenRouter (200+ models), NovitaAI, NVIDIA NIM, Xiaomi MiMo, z.ai/GLM, Kimi/Moonshot, MiniMax, Hugging Face, OpenAI, or any custom endpoint. Switch with `hermes model`.

**Install:** One-liner `curl | bash` on Linux/macOS/WSL2. PowerShell one-liner for Windows (early beta).

**Migration:** Has a `hermes claw migrate` command to import everything from OpenClaw (memories, skills, API keys, persona).

**Docs:** Full docs at hermes-agent.nousresearch.com/docs — covers quickstart, CLI usage, config, messaging gateway, security, tools, skills, memory, MCP, cron, and architecture.

**License:** MIT.

Want me to dig into any specific section in more detail?
