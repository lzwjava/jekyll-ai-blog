---
audio: false
generated: true
image: false
lang: en
layout: post
title: Creating Portable Server Environments with Docker
translated: false
type: note
---

**Question:** How can I maintain a single, portable server environment image (with Emacs and other tools installed) that can be easily migrated across cloud platforms like Alibaba Cloud, AWS Lightsail, Vultr, Google Cloud, and DMIT without having to set up everything from scratch each time?

---

**Answer:**

This is a very common pain point. The good news: there are several clean strategies, and the **Docker-based approach** is the most portable and practical for your use case. Here's the full picture:

---

## Strategy Overview: Your Options

### Option 1 — Custom Docker Image (Recommended)

This is the most platform-agnostic solution. Docker containers package applications and dependencies into portable units that can run practically anywhere, so your Emacs, dotfiles, shell config, etc., all live inside the image.

**How it works:**

1. Write a `Dockerfile` that installs everything you need:

```dockerfile
FROM ubuntu:24.04

# Install your tools
RUN apt-get update && apt-get install -y \
    emacs \
    git \
    zsh \
    tmux \
    curl \
    wget \
    ripgrep \
    && rm -rf /var/lib/apt/lists/*

# Copy your dotfiles into the image
COPY dotfiles/.emacs.d /root/.emacs.d
COPY dotfiles/.zshrc /root/.zshrc
COPY dotfiles/.tmux.conf /root/.tmux.conf

CMD ["/bin/zsh"]
```

2. Build and push the image to a registry (Docker Hub or GitHub Container Registry — both are free for public images):

```bash
docker build -t yourusername/myenv:latest .
docker push yourusername/myenv:latest
```

3. On any new server (regardless of cloud provider), spin it up instantly:

```bash
docker pull yourusername/myenv:latest
docker run -it --name myenv \
  -v /home/data:/data \   # mount persistent data outside container
  yourusername/myenv:latest
```

**Key principle:** Keep your **data/config in a mounted volume**, not baked into the image. This way the image stays clean and portable, and your work persists across container restarts.

---

### Option 2 — Dockerfile + dotfiles Git Repo (Hybrid, Very Clean)

Instead of baking dotfiles into the image at build time, keep your dotfiles in a **private GitHub repo** and pull them at container startup. This means you only need to rebuild the image when software versions change — dotfile tweaks just need a `git pull`.

```dockerfile
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y emacs git zsh tmux ...
# At runtime, clone dotfiles
CMD git clone https://github.com/you/dotfiles ~/.dotfiles && ~/.dotfiles/install.sh && zsh
```

---

### Option 3 — Nix or Homebrew + Shell Bootstrap Script (No Docker)

If you don't want Docker at all, a **shell bootstrap script** can reinstall everything in ~5 minutes on any fresh Linux server:

```bash
#!/bin/bash
# bootstrap.sh — run on any fresh Ubuntu/Debian server
apt-get update && apt-get install -y emacs git zsh tmux
git clone https://github.com/you/dotfiles ~/.dotfiles
cd ~/.dotfiles && ./install.sh
chsh -s $(which zsh)
```

This approach is simpler but slower than pulling a pre-built Docker image.

---

### Option 4 — Self-Hosted Image Registry (Advanced)

You can self-host your own private container registry using the Distribution project (the engine behind Docker Registry), which gives you full control over your images without relying on Docker Hub. This is overkill for personal use but useful if you want to avoid Docker Hub's rate limits.

---

## Recommended Setup for Your Case

Given you've used Alibaba Cloud, AWS Lightsail, Vultr, GCP, and DMIT — here's a practical, minimal setup:

| Component | Tool |
|---|---|
| Image registry | Docker Hub (free) or GitHub Container Registry |
| Dotfiles management | Chezmoi or a Git bare repo |
| Image base | `ubuntu:24.04` or `debian:bookworm-slim` |
| Data persistence | Docker named volume or host bind mount |
| Rebuild trigger | Makefile or simple shell script |

**Workflow once set up:**

1. Provision new server → install Docker (one command)
2. `docker pull yourusername/myenv:latest`
3. `docker run -it -v ~/data:/data yourusername/myenv:latest`
4. You're immediately in your familiar environment

**Installing Docker on any new server:**

```bash
curl -fsSL https://get.docker.com | sh
```

---

## What to Keep Outside the Docker Image

- **Your actual work files / projects** → bind mount a host directory
- **SSH keys** → pass via environment or mount, never bake into image
- **Secrets / API keys** → use `.env` files or Docker secrets

---

## Tips Specific to Your Situation

- Since you use **DMIT for CN2**, Docker works perfectly there — it's just plain Linux
- For **Emacs specifically**, consider keeping your `~/.emacs.d` as a separate Git repo (e.g., Doom Emacs or Spacemacs config) — this makes it easy to update independently of your base image
- Tag your images with dates: `myenv:2026-03` so you can roll back if something breaks
- Rebuild the image every few months to get security updates in the base OS layer

---

**References:**

- [Self-Hosting Docker vs Cloud-Based Docker](https://runcloud.io/blog/self-hosting-docker-vs-cloud-based-docker)
- [Self-Hosted Docker Registry (Distribution project)](https://dev.to/mechcloud_academy/the-ultimate-docker-hub-alternative-building-a-secure-self-hosted-registry-with-distribution-302k)
- [Tools That Make Self-Hosting Easier](https://blog.openreplay.com/tools-platforms-self-hosting-easier/)
