---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tiny OpenClaw on Raspberry Pi
translated: false
type: note
---

**Question:** How do I build a very small/tiny OpenClaw setup using a Raspberry Pi?

**Answer:**

## Overview: What is OpenClaw?

OpenClaw is a project that gives an LLM agent control over a computer. The agent can install software, write and run programs, integrate with external services, and much more. Think of it as an AI assistant that doesn't just talk — it actually *does things*.

For a tiny/minimal setup, you have two main paths: **PicoClaw** (the smallest option) and **standard OpenClaw on a minimal Pi**.

---

## Option 1: PicoClaw — The Truly Tiny Version (Recommended for Small Hardware)

PicoClaw is an ultra-lightweight personal AI assistant inspired by nanobot, rewritten in Go. It runs on $10 hardware with less than 10MB RAM — that's 99% less memory than OpenClaw and 98% cheaper than a Mac mini.

Compared to OpenClaw (TypeScript) and NanoBot (Python), PicoClaw reduces memory usage by 99% (from 100MB+ to 10MB) and startup time from 30 seconds to under 1 second. It also supports RISC-V architecture.

### Hardware Requirements

PicoClaw has extremely low hardware requirements — recommended 64MB+ memory (minimum 10MB). It supports x86_64, ARM64, and RISC-V architectures, running on Raspberry Pi, embedded devices, Mac, Linux, and Windows.

This means it works on a **Raspberry Pi Zero 2 W**, Pi 3, Pi 4, or Pi 5.

### Installation Steps for PicoClaw

```bash
# 1. Clone the repo
git clone https://github.com/sipeed/picoclaw.git
cd picoclaw

# 2. Install dependencies
make deps

# 3. Build for your Pi model:
# Pi Zero 2 W (32-bit OS):
make build-linux-arm

# Pi Zero 2 W (64-bit OS) or Pi 3/4/5:
make build-linux-arm64

# Or build all Pi Zero variants at once:
make build-pi-zero

# 4. Install system-wide
make install
```

### Configure PicoClaw

Create a config file at `~/.picoclaw/config.json`:

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.picoclaw/workspace",
      "model_name": "claude-sonnet",
      "max_tokens": 8192,
      "temperature": 0.7,
      "max_tool_iterations": 20
    }
  },
  "model_list": [
    {
      "model_name": "claude-sonnet",
      "model": "anthropic/claude-sonnet-4-6",
      "api_key": "your-anthropic-api-key"
    }
  ],
  "tools": {
    "web": {
      "duckduckgo": {
        "enabled": true,
        "max_results": 5
      }
    }
  }
}
```

### Start the Gateway (connect to Telegram, Discord, etc.)

Simply run `picoclaw gateway` to start the gateway service, configure the respective bot tokens, and use your AI assistant on platforms like Telegram, Discord, QQ, and DingTalk.

```bash
picoclaw gateway
```

---

## Option 2: Standard OpenClaw on a Minimal Pi (Pi 4 or Pi 5)

If you want the full OpenClaw experience on slightly larger hardware:

### Minimum Specs

Minimum specs: 1GB RAM, 1 core, 500MB disk. Recommended: 2GB+ RAM, 64-bit OS, 16GB+ SD card (or USB SSD). Use Raspberry Pi OS Lite (64-bit) — no desktop needed for a headless server.

### Install OpenClaw

On the newly installed and updated Raspberry Pi OS, simply run this command to complete the installation and initial setup:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### Prep the OS First

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essentials
sudo apt install -y git curl build-essential

# Set timezone
sudo timedatectl set-timezone America/Chicago  # change to yours

# Install Node.js (required by OpenClaw)
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
```

### Add Swap (critical for low-RAM Pis)

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

---

## Option 3: Tiny Handheld Pi Zero Build (Physical Device)

One maker built a handheld personal assistant that fits in a pocket using a Raspberry Pi Zero 2 W, a Whisplay HAT (with 1.69-inch LCD display, speaker, microphone, and buttons), and a PiSugar battery module. Since the Pi Zero 2 W can't run OpenClaw directly, the handheld records user requests, transcribes them, then sends the text to an OpenClaw instance running in a cloud environment.

This is the "true pocket-sized" approach — the Pi Zero acts as a thin client talking to OpenClaw in the cloud.

---

## About the "Pi Lib" / Python Question

OpenClaw is fundamentally a Node.js-based agent, not a Python library. However, PicoClaw is written in Go and provides a binary you can run anywhere. If you want to call OpenClaw from Python scripts, you interact with it via its HTTP gateway API or its CLI. There is a community Python project called `pizero-openclaw` that uses Python modules like `main.py`, `display.py`, and `openclaw_client.py` to create a voice-controlled Pi Zero assistant that streams responses to an LCD screen.

---

## Quick Comparison Table

| Feature | PicoClaw | OpenClaw (standard) |
|---|---|---|
| RAM usage | ~10MB | ~100MB+ |
| Startup time | <1 second | ~30 seconds |
| Language | Go | TypeScript/Node.js |
| Runs on Pi Zero | ✅ Yes | ❌ Too slow |
| Minimum Pi | Pi Zero 2 W | Pi 4 (4GB+) |
| API needed | Yes (OpenAI/Anthropic/etc.) | Yes |

---

## Security Warning

Running an LLM-based AI agent with shell access is dangerous. There is a risk of prompt injection or adversarial input getting sent to the bot via the enabled communications channels or other text it finds online. The bot could run malicious software, or expose API tokens and other private information that it has access to if proper safeguards are not implemented and maintained.

Always run OpenClaw on a **dedicated Pi**, not your main machine.

**References:**

- [PicoClaw GitHub (sipeed/picoclaw)](https://github.com/sipeed/picoclaw)
- [PicoClaw official site](https://picoclaw.net/)
- [OpenClaw Raspberry Pi docs](https://docs.openclaw.ai/platforms/raspberry-pi)
- [Adafruit Guide: OpenClaw on Raspberry Pi](https://learn.adafruit.com/openclaw-on-raspberry-pi/installing-openclaw)
- [Raspberry Pi official blog: Turn your Pi into an AI agent with OpenClaw](https://www.raspberrypi.com/news/turn-your-raspberry-pi-into-an-ai-agent-with-openclaw/)
- [Hackster.io: DIY handheld OpenClaw assistant](https://www.hackster.io/news/the-diy-openclaw-assistant-you-ll-actually-want-to-carry-97888b183ac1)
- [pizero-openclaw Python project (GitHub)](https://github.com/sebastianvkl/pizero-openclaw)
