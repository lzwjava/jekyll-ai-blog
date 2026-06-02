---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install OpenClaw on Ubuntu 22.04 Guide
translated: false
type: note
---

Question: How do I install OpenClaw on Linux kernel 6.8.0-90-generic (Ubuntu 22.04 x86_64)?

Answer:

Your system (`6.8.0-90-generic #91~22.04.1-Ubuntu SMP`) is running **Ubuntu 22.04 LTS (Jammy Jellyfish)** on x86_64 — this is fully supported by OpenClaw.

---

## Prerequisites

Minimum system requirements:

- 2 vCPU
- 2 GB RAM (important: 0.5–1 GB RAM will crash; swap does not fix this)
- 20 GB SSD
- Ubuntu 22.04 or 24.04
- root or sudo access
- internet access

---

## Step 1 — Update System & Install Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git ca-certificates curl build-essential
```

---

## Step 2 — Install Node.js 22 (Required)

OpenClaw requires Node.js 22+. Install it via the NodeSource repository:

```bash
# Add NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -

# Install Node.js
sudo apt install -y nodejs

# Verify
node --version   # Should show v22.x.x
npm --version
```

**Alternative: use nvm (recommended to avoid permission issues)**

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 24
nvm use 24
```

---

## Step 3 — Configure npm Global Path (if not using nvm)

To avoid permission issues with global npm packages:

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

---

## Step 4 — Install OpenClaw

**Option A — Official Installer Script (recommended):**

The installer script is the recommended way to install OpenClaw. It handles Node detection, installation, and onboarding in one step.

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Option B — Git method (for full workspace/gateway support):**

The Git method ensures you get the full source tree, including all workspace packages:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method git --no-prompt --no-onboard
```

**Option C — npm global install:**

```bash
npm install -g openclaw@latest
```

---

## Step 5 — Verify Installation

```bash
openclaw --version
```

If the command is not found, add npm global bin to PATH:

```bash
echo 'export PATH=$(npm prefix -g)/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

---

## Step 6 — Run Onboarding (Mandatory)

You must run onboarding once. Follow the prompts carefully. This is not optional:

```bash
openclaw onboard
```

---

## Step 7 — Install & Start the Gateway

```bash
openclaw gateway install
openclaw gateway start
```

---

## Step 8 — Access the Dashboard

SSH tunneling is the only correct way to access the dashboard on a VPS or remote server:

```bash
# From your local machine:
ssh -N -L 18789:127.0.0.1:18789 your_user@YOUR_SERVER_IP
```

Then open in your browser: `http://localhost:18789/`

If a token is required:

```bash
openclaw dashboard --no-open
# Copy the tokenized URL and open it in your browser
```

---

## Step 9 — Set Up as a systemd Service (Optional but Recommended)

Set up systemd so OpenClaw restarts automatically after crashes or reboots:

```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw
sudo systemctl start openclaw

# Check status
sudo systemctl status openclaw

# View real-time logs
sudo journalctl -u openclaw -f
```

---

## Common Troubleshooting

| Problem | Fix |
|---|---|
| `openclaw: command not found` | Add `$(npm prefix -g)/bin` to `$PATH` in `~/.bashrc` |
| Dashboard won't open | Use SSH tunnel, not direct IP access |
| Crashes on startup | Check RAM — minimum 2 GB required |
| Systemd using wrong Node version | Reinstall using Git method |

References:

- [OpenClaw Official Install Docs](https://docs.openclaw.ai/install)
- [Complete Guide from Scratch (archy.net)](https://www.archy.net/installing-openclaw-a-complete-guide-from-scratch/)
- [Step-by-Step OpenClaw Setup on Ubuntu LTS (ddevops.com)](https://blogs.ddevops.com/step-by-step-openclaw-setup-on-ubuntu-lts/)
- [OpenClaw Linux Install Guide 2026 (vpn07.com)](https://vpn07.com/en/blog/2026-openclaw-install-linux-ubuntu-debian-server-tutorial.html)
- [How to Install OpenClaw for Beginners (boostedhost.com)](https://boostedhost.com/blog/en/how-to-install-openclaw-get-started-guide/)
