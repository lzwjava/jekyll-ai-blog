---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过 SSH 代理命令部署 OpenClaw
translated: true
type: note
---

问题：使用现有的 OpenClaw AI agent 自动在另一台机器上安装并设置另一个 OpenClaw 实例，且仅通过 SSH 连接，最好的方法是什么？

回答：

## 使用 OpenClaw Agent 通过 SSH 自我部署到另一台机器

你的想法非常优雅 —— 既然 OpenClaw 已经具备了 terminal/shell 访问能力，你只需**指令现有的 agent 通过 SSH 执行远程安装**。这正是它所擅长的任务类型。

---

### Prerequisites

在要求你的 agent 进行远程安装之前，请确保：

- 从 Machine A 到 Machine B 的 SSH 连接正常（建议使用 key-based auth，无需密码提示）
- Machine B 具备互联网访问权限（以便从 npm 拉取资源）
- 目标机器需要 Node.js >= 22（OpenClaw installer 可以处理此步骤）
- 目标机器最低配置：2 cores, 2 GB RAM, 2 GB storage

---

### 如何指令你现有的 OpenClaw Agent

只需与你的 agent 进行自然对话。Prompt 示例：

```
SSH into user@192.168.1.50 and install OpenClaw there.
Create a dedicated user called openclaw, install Node 24 via nvm,
then run the OpenClaw installer. Don't do the onboarding wizard yet.
I'll copy my config over after.
```

你的 agent 随后会执行如下命令：

```bash
# Step 1: Agent 通过 SSH 登录目标机器
ssh user@192.168.1.50

# Step 2: 创建专用用户（安全最佳实践）
adduser openclaw --gecos "" && usermod -aG sudo openclaw

# Step 3: 通过 nvm 安装 Node
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc && nvm install 24

# Step 4: 全局安装 OpenClaw
npm install -g openclaw@latest
```

建议使用专用的非 root 用户 —— 避免以 root 身份运行所有程序以获得更好的安全性。

---

### 安装后：复制你的 Config（最快路径）

一旦 OpenClaw 在目标机器上安装完成，让你的 agent 复制配置文件：

```bash
# Agent 在 Machine A 上运行此命令将 config 复制到 Machine B
scp ~/.openclaw/openclaw.json user@192.168.1.50:~/.openclaw/openclaw.json
```

若要完整迁移包含 memory 和 sessions 的设置，请复制 `$OPENCLAW_STATE_DIR`（默认：`~/.openclaw`）和 workspace 目录，然后运行 `openclaw doctor` 并重启 gateway 服务。这样可以保留 config、auth profiles、channel credentials、sessions 以及 memory。

---

### 然后让 Agent 启动 Daemon

```bash
# Agent 重新通过 SSH 登录并运行：
ssh openclaw@192.168.1.50 "openclaw onboard --non-interactive --install-daemon --skip-skills"
```

或者如果你只想启动 gateway 而不进行完整的 onboarding：

```bash
ssh openclaw@192.168.1.50 "openclaw gateway start"
```

---

### 完整流程总结

```
[Machine A - Existing Agent]
        |
        | SSH + shell commands
        ↓
[Machine B - Target]
  1. Create openclaw user
  2. Install nvm + Node 24
  3. npm install -g openclaw@latest
  4. scp ~/.openclaw/openclaw.json from Machine A
  5. openclaw daemon start (or onboard --non-interactive)
  6. openclaw doctor  ← 验证一切正常
```

---

### 关键点

| 项目 | 详情 |
|---|---|
| Agent 能力 | OpenClaw 原生支持通过 SSH 运行 shell 命令 |
| 安装时需要 Key 吗? | 不需要 —— 在基础安装后使用现有配置复制 `openclaw.json` 即可 |
| Config 位置 | `~/.openclaw/openclaw.json` |
| 完整克隆 (包括 memory) | 复制整个 `~/.openclaw/` + workspace，然后运行 `openclaw doctor` |
| 安全提示 | 严禁在没有 authentication 和 TLS 的情况下将 18789 端口暴露在公网 —— 远程访问请使用 SSH tunnels |

这确实是最优雅的实现方式 —— 你的 agent 处理无聊的远程 shell 工作，而你最终会得到一个配置完美的克隆环境。

References:

- [OpenClaw FAQ - Migration Guide](https://docs.openclaw.ai/help/faq)
- [Self-Hosting OpenClaw on VPS - Hivelocity](https://www.hivelocity.net/kb/self-hosting-openclaw-guide/)
- [Deploy OpenClaw on Ubuntu 24.04 - DEV Community](https://dev.to/sst21/how-to-deploy-openclaw-ai-agent-on-ubuntu-2404-e87)
- [OpenClaw Security-First Self-Hosting Guide](https://www.dsebastien.net/how-to-self-host-openclaw-securely-on-a-vps-a-security-first-guide/)
