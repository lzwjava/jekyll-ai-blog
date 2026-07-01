---
audio: false
generated: true
image: false
lang: en
layout: post
title: Deploying OpenClaw via SSH Agent Commands
translated: false
type: note
---

Question: What is the best way to use an existing OpenClaw AI agent to automatically install and set up another OpenClaw instance on a different machine, using only an SSH connection?

Answer:

## Using OpenClaw Agent to Self-Deploy to Another Machine via SSH

Your idea is genuinely elegant — since OpenClaw already has terminal/shell access capabilities, you can simply **instruct your existing agent to do the remote installation over SSH**. This is exactly the kind of task it's built for.

---

### Prerequisites

Before telling your agent to go install itself remotely, make sure:

- SSH connection from Machine A → Machine B is working (key-based auth preferred, no password prompt)
- Machine B has internet access (to pull from npm)
- Node.js >= 22 is required on the target machine (though the OpenClaw installer can handle this)
- Minimum specs on the target: 2 cores, 2 GB RAM, 2 GB storage

---

### What to Tell Your Existing OpenClaw Agent

Just chat with your agent naturally. Example prompt:

```
SSH into user@192.168.1.50 and install OpenClaw there.
Create a dedicated user called openclaw, install Node 24 via nvm,
then run the OpenClaw installer. Don't do the onboarding wizard yet.
I'll copy my config over after.
```

Your agent will then execute commands like:

```bash
# Step 1: Agent SSHes into target machine
ssh user@192.168.1.50

# Step 2: Create dedicated user (security best practice)
adduser openclaw --gecos "" && usermod -aG sudo openclaw

# Step 3: Install Node via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc && nvm install 24

# Step 4: Install OpenClaw globally
npm install -g openclaw@latest
```

A dedicated non-root user is recommended — avoid running everything as root for better security.

---

### After Installation: Copy Your Config (Fastest Path)

Once OpenClaw is installed on the target, have your agent copy your config over:

```bash
# Agent runs this on Machine A to copy config to Machine B
scp ~/.openclaw/openclaw.json user@192.168.1.50:~/.openclaw/openclaw.json
```

To fully migrate a setup including memory and sessions, copy `$OPENCLAW_STATE_DIR` (default: `~/.openclaw`) and the workspace directory, then run `openclaw doctor` and restart the gateway service. This preserves config, auth profiles, channel credentials, sessions, and memory.

---

### Then Have the Agent Start the Daemon

```bash
# Agent SSHes back in and runs:
ssh openclaw@192.168.1.50 "openclaw onboard --non-interactive --install-daemon --skip-skills"
```

Or if you just want the gateway started without full onboarding:

```bash
ssh openclaw@192.168.1.50 "openclaw gateway start"
```

---

### Full Flow Summary

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
  6. openclaw doctor  ← validates everything
```

---

### Key Points

| Item | Detail |
| --- | --- |
| Agent capability | OpenClaw can run shell commands over SSH natively |
| Keys needed at install? | No — copy `openclaw.json` with existing config after bare install |
| Config location | `~/.openclaw/openclaw.json` |
| Full clone (including memory) | Copy entire `~/.openclaw/` + workspace, then run `openclaw doctor` |
| Security note | Never expose port 18789 to the public internet without authentication and TLS — use SSH tunnels for remote access |

This is genuinely the most elegant way to do it — your agent handles the boring remote shell work and you end up with a clean clone of your setup.

References:

- [OpenClaw FAQ - Migration Guide](https://docs.openclaw.ai/help/faq)
- [Self-Hosting OpenClaw on VPS - Hivelocity](https://www.hivelocity.net/kb/self-hosting-openclaw-guide/)
- [Deploy OpenClaw on Ubuntu 24.04 - DEV Community](https://dev.to/sst21/how-to-deploy-openclaw-ai-agent-on-ubuntu-2404-e87)
- [OpenClaw Security-First Self-Hosting Guide](https://www.dsebastien.net/how-to-self-host-openclaw-securely-on-a-vps-a-security-first-guide/)
