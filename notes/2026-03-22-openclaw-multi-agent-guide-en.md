---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quick OpenClaw Multi Agent Installation Guide
translated: false
type: note
---

Question: If I already have an OpenClaw AI agent installed, what is the fastest way to install another one? Can I skip providing API keys during the initial installation and configure them later, then copy the `openclaw.json` to the target machine?

Answer:

## Fastest Way to Install Another OpenClaw Agent

There are two distinct scenarios here — **adding a second agent on the same machine** and **replicating to a new machine** — and OpenClaw handles both well.

---

### Scenario 1: Add Another Agent on the Same Machine

This is the most straightforward path. OpenClaw has a dedicated command for it:

```bash
openclaw agents add <name> \
  --workspace ~/.openclaw/workspace-<name> \
  --model anthropic/claude-sonnet-4-6 \
  --non-interactive \
  --json
```

Using `openclaw agents add <name>` creates a separate agent with its own workspace, sessions, and auth profiles. Each agent gets its own `agents.list[].name`, `agents.list[].workspace`, and `agents.list[].agentDir`. Default workspaces follow `~/.openclaw/workspace-<agentId>`.

---

### Scenario 2: Replicate to a New Machine (Copy `openclaw.json`)

**Yes — copying `openclaw.json` is a valid and fast approach**, but there are important nuances:

**Step 1: Install OpenClaw on the target machine**

Install with:

```bash
npm install -g openclaw@latest
```

Then run `openclaw onboard --install-daemon` for the guided setup.

**Step 2: Can you skip API keys during initial install?**

You can use `--non-interactive` mode to automate `openclaw onboard`. For example, using `--secret-input-mode ref` stores env-backed references in auth profiles instead of plaintext values — meaning the key is pulled from an environment variable at runtime, not embedded in the config file.

This means **yes**, you can run onboarding without embedding an API key in the JSON, by using `--secret-input-mode ref` and setting the key as an environment variable later.

**Step 3: Copy `openclaw.json`**

Config lives at `~/.openclaw/openclaw.json`. It is only readable by your user account (assuming default permissions). Treat it like any other secrets file — do not commit it to version control.

Simply copy your existing `~/.openclaw/openclaw.json` to the same path on the target machine. This brings over all your agent definitions, channel configurations, model settings, and auth profiles.

---

### Recommended Fastest Workflow (New Machine)

```bash
# 1. On new machine: install OpenClaw
npm install -g openclaw@latest

# 2. Run a minimal non-interactive onboard (no key yet, using ref mode)
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --secret-input-mode ref \
  --install-daemon

# 3. Copy your tuned openclaw.json from the existing machine
scp user@old-machine:~/.openclaw/openclaw.json ~/.openclaw/openclaw.json

# 4. Set the API key as an environment variable (or configure it in the dashboard)
export ANTHROPIC_API_KEY="sk-ant-..."

# 5. Restart the gateway
openclaw daemon restart
```

---

### Key Points to Know

| Topic | Detail |
|---|---|
| Config location | `~/.openclaw/openclaw.json` |
| Skip keys at install? | Yes — use `--secret-input-mode ref` to defer key to env var |
| Copy config to new machine? | Yes — this is the fastest replication method |
| Add agent on same machine | Use `openclaw agents add <name>` |
| Secrets in config file? | Avoid — store keys as env refs or in keychain |

For more secure credential management, you can use OpenClaw's auth profiles instead of environment variables. This is automatically configured when you use the `openclaw onboard` command — which stores the key in your system keychain rather than in the config file.

References:

- [OpenClaw Official Docs](https://docs.openclaw.ai)
- [OpenClaw CLI Automation Guide](https://docs.openclaw.ai/start/wizard-cli-automation)
- [OpenRouter + OpenClaw Integration](https://openrouter.ai/docs/guides/guides/openclaw-integration)
- [OpenClaw Setup Guide - Verdent](https://www.verdent.ai/guides/openclaw-setup-guide-from-zero-to-ai-assistant)
