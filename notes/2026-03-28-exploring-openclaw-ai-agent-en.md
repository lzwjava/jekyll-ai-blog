---
audio: false
generated: true
image: false
lang: en
layout: post
title: Exploring OpenClaw Open Source AI Agent
translated: false
type: note
---

**Question:** What is OpenClaw (🦞), and how does this user's experience with it illustrate its key features — including setting up software, using it as a router, running multiple instances, upgrading Ubuntu, token usage, model preferences, configuration with Nextcloud Chat, and LAN/SSH control?

**Answer:**

## What is OpenClaw?

OpenClaw (formerly Clawdbot, then Moltbot) is a free and open-source autonomous AI agent that executes tasks via large language models (LLMs), using messaging platforms as its main user interface. It was developed by Austrian developer Peter Steinberger and first published in November 2025.

What makes OpenClaw distinct is its combination: MIT-licensed, open-source, local-first (memory and data stored as Markdown files on disk), and community-extensible through a portable skill format.

The "lobster" nickname (🦞) comes from its mascot, Molty the space lobster — hence users colloquially calling it "龙虾" (lobster in Chinese).

---

## Breaking Down This User's OpenClaw Experience

### 1. Building 7 Software Tools (Including a Local NAS Search Engine)

OpenClaw connects LLMs to real software. Via simple chat commands, it can read and write files, run shell commands, browse websites, send emails, and control APIs — actually carrying out steps rather than just explaining how. The user used it as an AI agent to assist in setting up and configuring multiple self-hosted applications (like a local network drive/NAS search engine), essentially using the AI to handle the tedious setup steps interactively.

### 2. Attempting to Use a Linux Host as a Router (Failed — Too Complex)

This is a common advanced use case. OpenClaw can run shell commands on a Linux machine, so the user tried to use it to configure routing/NAT/iptables. The user found it too complicated — which is honest; turning a general Linux box into a proper router involves many low-level networking configurations that even an AI agent struggles to reliably automate end-to-end.

### 3. Running Two OpenClaw Instances

OpenClaw supports isolated sessions per agent, workspace, or sender through its multi-agent routing system. The user deployed two separate OpenClaw "lobsters" — likely one per machine or one per use case — which is a supported and common setup.

### 4. Using OpenClaw to Upgrade Ubuntu 22 → 24

This is a practical power-user move. Since OpenClaw can execute shell commands on the host machine, the user instructed the AI to run the `do-release-upgrade` process and handle the interactive prompts along the way. The AI acts as an assistant guiding and executing the upgrade steps.

### 5. Token Usage: ~70M Claude tokens/week + ~50M via OpenRouter/week

The AI models can be cloud-hosted (Anthropic, OpenAI, Google) or local (via Ollama, LM Studio, or other OpenAI-compatible servers), depending on configuration. This user is a heavy user — running Claude as the primary backend through Anthropic directly, and also routing some traffic through OpenRouter (an API aggregator that provides access to many models). The volume (~120M tokens/week combined) indicates this is a heavily automated, always-on agentic setup.

### 6. Xiaomi V2 Model is Good

Xiaomi released AI models (MiMo series). The user tested it via OpenRouter and found it performs well. OpenClaw's model-agnostic design makes it easy to swap between providers and test different LLMs without reconfiguring the whole agent.

### 7. Configuring with Nextcloud Talk (Chat)

OpenClaw supports Nextcloud Talk as one of its messaging channel integrations. The user wired up OpenClaw to Nextcloud Talk (the self-hosted chat component of Nextcloud), using Claude as the underlying model. This means they can chat with the AI agent directly inside their self-hosted Nextcloud environment.

### 8. Memory and Plugins — Not Tried Yet

OpenClaw stores conversations and long-term memory as plain Markdown and YAML files under the workspace and `~/.openclaw`. The memory system and skill/plugin ecosystem are advanced features the user plans to explore next. Users can expand the tool's capabilities using over 100 preconfigured AgentSkills that allow the AI to execute shell commands, manage file systems, and perform web automation.

### 9. Controlling Other LAN Machines via SSH

This is one of OpenClaw's most powerful practical uses. OpenClaw is built for developers and power users who want a personal AI assistant they can message from anywhere without sacrificing control over their data or relying on a hosted service. As long as SSH is configured between hosts on the LAN, the user can send a chat message to OpenClaw and have it SSH into another machine and run commands there — turning OpenClaw into a natural-language remote administration tool across the whole local network.

---

## Summary Table

| Experience | OpenClaw Feature Used |
|---|---|
| 7 software setups | Shell commands + skill automation |
| Router attempt | Shell/networking commands (complex, failed) |
| Two instances | Multi-agent / multi-workspace support |
| Ubuntu upgrade | Shell command execution on host |
| 70M + 50M tokens/week | Multi-provider model backend support |
| Xiaomi V2 model | Model-agnostic, works via OpenRouter |
| Nextcloud Talk integration | Native Nextcloud Talk channel support |
| Memory/plugins | Not yet explored (planned) |
| SSH LAN control | Shell + SSH access to remote hosts |

**References:**

- [OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)
- [OpenClaw Official Site](https://openclaw.ai/)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Milvus Blog — OpenClaw Complete Guide](https://milvus.io/blog/openclaw-formerly-clawdbot-moltbot-explained-a-complete-guide-to-the-autonomous-ai-agent.md)
- [DigitalOcean — What is OpenClaw](https://www.digitalocean.com/resources/articles/what-is-openclaw)
- [KDnuggets — OpenClaw Explained](https://www.kdnuggets.com/openclaw-explained-the-free-ai-agent-tool-going-viral-already-in-2026)