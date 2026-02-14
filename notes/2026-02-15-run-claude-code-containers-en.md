---
audio: false
generated: true
image: false
lang: en
layout: post
title: Run Claude Code in Containers
translated: false
type: note
---

Question: How to run Claude code (Claude Code interpreter/agent) in a container or cloud server?

Answer: 

**Claude Code** (Anthropic's terminal-based AI coding agent / code interpreter tool) is commonly run inside **Docker containers** for safety and isolation. This is the officially recommended approach in many cases because Claude Code can execute arbitrary code, install packages, run servers, etc.

Here are the main practical ways people run it in 2026 (local container or cloud / VPS):

### 1. Quickest & Recommended: Use Docker Sandbox (local or cloud VM)
Docker introduced built-in support for running coding agents like Claude Code in isolated sandboxes.

```bash
# Make sure you have recent Docker installed
docker sandbox run claude ~/my-project
```

- Mounts your current folder
- Runs Claude Code inside a secure, isolated environment
- Very low setup effort

You can also pass a prompt directly:
```bash
docker sandbox run claude -- "refactor this API client to use async/await"
```

Works on Mac, Windows, Linux.

### 2. Run inside VS Code Dev Container (very popular & secure)
Most developer-oriented way:

1. Install **Docker Desktop** + **VS Code** + **Dev Containers** extension
2. Use Anthropic's official template or community ones:
   - https://github.com/anthropics/claude-code (look for `.devcontainer` folder)
   - Many community forks / templates exist (search "claude code devcontainer")
3. Open folder → "Reopen in Container"
4. Claude Code runs inside the container with strong isolation
5. You can give `--dangerously-skip-permissions` for fully autonomous mode

This setup is frequently used for long-running agents.

### 3. Plain Docker container (DIY / cloud VPS friendly)

Minimal example Dockerfile:
```dockerfile
FROM ubuntu:24.04

RUN apt-get update && apt-get install -y curl git build-essential
RUN curl -fsSL https://claude.ai/install.sh | bash

# Optional: install common tools Claude Code likes
RUN apt-get install -y python3 python3-pip nodejs npm

WORKDIR /workspace

CMD ["claude"]
```

Build & run:
```bash
docker build -t claude-code .
docker run -it --rm \
  -v "$(pwd)":/workspace \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  claude-code
```

On a **cloud VPS** (RunPod, Hostinger, AWS EC2, DigitalOcean, etc.):
- SSH into the server
- Install Docker
- Use one of the above methods
- Many people use `tmux` + `claude` or expose via **ShellHub** / Tailscale for remote access from phone/laptop

### 4. Cloud-specific / managed sandbox options
- **Cloudflare Sandboxes** → run Claude Code via their sandbox SDK
- **E2B**, **Daytona**, **Vercel Sandbox**, **Fly Machines** — offer managed secure containers for AI agents
- **RunPod** — popular for GPU pods + Claude Code setups (good templates exist)
- **AWS ECS Fargate** / **Google Cloud Run** — containerize Claude Code and run serverless / always-on

### 5. If you want fully local models (no Anthropic API)
Some people replace the Anthropic backend with local models via **Docker Model Runner** or Ollama + Anthropic-compatible endpoint:
```bash
ANTHROPIC_BASE_URL=http://localhost:12434 claude --model your-local-model ...
```

But most people still use real Claude models (Sonnet 3.7 / Opus 4 / etc.) via API key.

**Security note**: Always run Claude Code in a container — never directly on your main machine with dangerous flags, especially if giving it long-running / autonomous tasks.

Choose method depending on your goal:
- Quick & local → `docker sandbox run claude`
- Development workflow → VS Code Dev Container
- 24/7 cloud agent → VPS + Docker or managed sandbox (E2B, Cloudflare, RunPod)

References:  

- [Docker Sandboxes for Claude Code](https://docs.docker.com/ai/sandboxes/claude-code)
- [Claude Code official docs – Dev Containers](https://code.claude.com/docs/en/devcontainer)
- [Run Claude Code in DevContainer guide](https://codewithandrea.com/articles/run-ai-agents-inside-devcontainer)
- [Cloudflare Sandbox – Claude Code example](https://developers.cloudflare.com/sandbox/tutorials/claude-code)
- [RunPod Claude Code setup guide](https://www.runpod.io/blog/your-first-claude-code-project-within-runpod-a-complete-setup-guide)