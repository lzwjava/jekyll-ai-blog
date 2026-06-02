---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw 多智能体快速安装指南
translated: true
type: note
---

Question: If I already have an OpenClaw AI agent installed, what is the fastest way to install another one? Can I skip providing API keys during the initial installation and configure them later, then copy the `openclaw.json` to the target machine?

Answer:

## Fastest Way to Install Another OpenClaw Agent

There are two distinct scenarios here — **adding a second agent on the same machine** and **replicating to a new machine** — and OpenClaw handles both well.

---

### Scenario 1: Add Another Agent on the Same Machine

这是最直接的路径。OpenClaw 专门为此提供了一个命令：

```bash
openclaw agents add <name> \
  --workspace ~/.openclaw/workspace-<name> \
  --model anthropic/claude-sonnet-4-6 \
  --non-interactive \
  --json
```

使用 `openclaw agents add <name>` 会创建一个独立的 agent，拥有自己的 workspace、sessions 和 auth profiles。每个 agent 都会获得自己的 `agents.list[].name`、`agents.list[].workspace` 和 `agents.list[].agentDir`。默认的 workspaces 遵循 `~/.openclaw/workspace-<agentId>`。

---

### Scenario 2: Replicate to a New Machine (Copy `openclaw.json`)

**是的 — 复制 `openclaw.json` 是一个有效且快速的方法**，但有一些重要的细节需要注意：

**Step 1: 在目标机器上安装 OpenClaw**

使用以下命令安装：
```bash
npm install -g openclaw@latest
```
然后运行 `openclaw onboard --install-daemon` 进行引导式设置。

**Step 2: 初始安装期间能否跳过 API keys？**

你可以使用 `--non-interactive` 模式来自动化 `openclaw onboard`。例如，使用 `--secret-input-mode ref` 会在 auth profiles 中存储 environment-backed 引用，而不是明文值 —— 这意味着 key 在运行时从 environment variable 中提取，而不是嵌入在配置文件中。

这意味着 **是的**，你可以通过使用 `--secret-input-mode ref` 并在稍后设置 environment variable，在不将 API key 嵌入 JSON 的情况下运行 onboarding。

**Step 3: 复制 `openclaw.json`**

配置文件位于 `~/.openclaw/openclaw.json`。它只能由你的用户账户读取（假设是默认权限）。请像对待任何其他 secrets 文件一样对待它 —— 不要将其提交到版本控制系统。

只需将现有的 `~/.openclaw/openclaw.json` 复制到目标机器上的相同路径即可。这会同步你所有的 agent 定义、channel 配置、model 设置和 auth profiles。

---

### Recommended Fastest Workflow (New Machine)

```bash
# 1. 在新机器上：安装 OpenClaw
npm install -g openclaw@latest

# 2. 运行最小化的非交互式 onboard（暂不输入 key，使用 ref 模式）
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --secret-input-mode ref \
  --install-daemon

# 3. 从现有机器复制调整好的 openclaw.json
scp user@old-machine:~/.openclaw/openclaw.json ~/.openclaw/openclaw.json

# 4. 将 API key 设置为 environment variable（或在 dashboard 中配置）
export ANTHROPIC_API_KEY="sk-ant-..."

# 5. 重启 daemon
openclaw daemon restart
```

---

### Key Points to Know

| Topic | Detail |
|---|---|
| Config location | `~/.openclaw/openclaw.json` |
| Skip keys at install? | 是的 — 使用 `--secret-input-mode ref` 将 key 延迟到 env var 设置 |
| Copy config to new machine? | 是的 — 这是最快的复制方法 |
| Add agent on same machine | 使用 `openclaw agents add <name>` |
| Secrets in config file? | 避免使用 — 将 keys 存储为 env refs 或在 keychain 中 |

为了更安全的 credential 管理，你可以使用 OpenClaw 的 auth profiles 而不是 environment variables。当你使用 `openclaw onboard` 命令时，这会自动配置 —— 它会将 key 存储在你的系统 keychain 中，而不是配置文件中。

References:

- [OpenClaw Official Docs](https://docs.openclaw.ai)
- [OpenClaw CLI Automation Guide](https://docs.openclaw.ai/start/wizard-cli-automation)
- [OpenRouter + OpenClaw Integration](https://openrouter.ai/docs/guides/guides/openclaw-integration)
- [OpenClaw Setup Guide - Verdent](https://www.verdent.ai/guides/openclaw-setup-guide-from-zero-to-ai-assistant)
