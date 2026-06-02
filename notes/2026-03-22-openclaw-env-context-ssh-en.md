---
audio: false
generated: true
image: false
lang: en
layout: post
title: Defining OpenClaw Environment Context via SSH
translated: false
type: note
---

**Question:** When working with OpenClaw (AI agent) accessed via SSH tunnel (`ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36`), how should I clearly communicate to OpenClaw which machine it is actually running on, so it doesn't get confused — especially since services like Gitea are also deployed on the remote machine but I'm accessing them from my laptop?

---

**Answer:**

This is an important context-awareness problem with OpenClaw. Because the Gateway binds only to `localhost` by default, and you access it remotely via SSH tunnels, OpenClaw has no inherent way to know *which machine* it is physically executing on unless you tell it explicitly. If you don't, it may mistakenly assume it's running on your laptop (the machine you're typing from), when in reality it's deployed on your second computer (`192.168.1.36`).

---

## The Core Problem

Your setup:

| Layer | Reality |
|---|---|
| **Your laptop** | You type here, browser opens `localhost:18789` via SSH tunnel |
| **Remote machine** (`192.168.1.36`) | OpenClaw Gateway actually runs here, along with Gitea, etc. |

OpenClaw's context engine and memory system work by reading files, running shell commands, and accessing services — all on the machine it is **physically running on**. It reads actual files from the filesystem, executes shell commands, and connects to localhost services. If it thinks it's on your laptop, it may try to reach the wrong filesystem or the wrong `localhost`.

---

## How to Tell OpenClaw Clearly Which Machine It's On

### 1. Set It in the System Prompt / Agent Identity (Most Important)

When you configure the agent (via onboarding or the `openclaw.json` / agent config), explicitly state the deployment context in the agent's persona or system instructions:

```
You are running on the machine "lzw-server" at 192.168.1.36.
This is NOT a laptop. It is a dedicated second computer (Linux server).
The user accesses you remotely via an SSH tunnel: ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36
When the user says "localhost" in a URL, they may mean localhost on THEIR laptop,
not this server. Always clarify if a service like Gitea (running on THIS machine at
192.168.1.36) is intended before acting on any localhost reference.
Services on THIS machine include: Gitea, OpenClaw itself.
The user's laptop is a separate machine and has its own filesystem.
```

### 2. Use a `HEARTBEAT.md` or `SYSTEM_CONTEXT.md` File on the Remote Machine

Every 30 minutes, the agent wakes up, reads a `HEARTBEAT.md` file for instructions, and decides whether it needs to do anything. You can embed machine identity there:

```markdown
# System Context
- **Host machine**: lzw-server (192.168.1.36)
- **OS**: Linux (Ubuntu)
- **Access method**: User connects via SSH tunnel on port 18789
- **Important**: localhost here = 192.168.1.36, NOT the user's laptop
- **Services on this machine**: Gitea (port 3000), OpenClaw (port 18789)
- **Do NOT confuse**: user's laptop filesystem ≠ this server's filesystem
```

### 3. Tell It Directly in the First Message of Every Session

Develop a habit of starting sessions with a context-setting message:

```
Context: You are running on my second computer (192.168.1.36, Linux).
I'm on my laptop accessing you via SSH tunnel.
When I say "Gitea", it's running on YOU (192.168.1.36:3000), not my laptop.
When I say "my laptop", I mean a separate machine — you cannot access it directly.
```

### 4. Use Clear Naming in All Instructions

Avoid ambiguous terms. Always use:

| ❌ Ambiguous | ✅ Clear |
|---|---|
| "localhost" | "localhost on the server (192.168.1.36)" or "localhost on my laptop" |
| "my machine" | "the server" or "my laptop" |
| "this computer" | "lzw-server" or "192.168.1.36" |
| "Gitea" | "Gitea on the server at 192.168.1.36:3000" |

---

## Why This Matters — The Gitea Example

If you tell OpenClaw "go check Gitea", it will try to connect to Gitea. But:

- Gitea is running on `192.168.1.36:3000` — the **same machine** as OpenClaw
- From OpenClaw's perspective, that's `http://localhost:3000` ✅
- But if OpenClaw thinks it's on your laptop, it may either fail or make wrong assumptions

By explicitly telling it that **both OpenClaw and Gitea live on `192.168.1.36`**, it will correctly use `localhost:3000` to reach Gitea — which is correct since they're co-located.

---

## Summary Checklist

- [ ] Add machine identity to the agent's **system prompt / persona config**
- [ ] Put context in **`HEARTBEAT.md`** on the remote server
- [ ] Start sessions with a **context-setting message**
- [ ] Always refer to machines by **explicit names** (server IP or hostname, not "localhost" ambiguously)
- [ ] Never assume OpenClaw infers its own deployment location automatically

---

**References:**

- [OpenClaw Architecture Explained](https://ppaolo.substack.com/p/openclaw-system-architecture-overview)
- [What Is OpenClaw — MindStudio](https://www.mindstudio.ai/blog/what-is-openclaw-ai-agent)
- [OpenClaw Security Docs](https://docs.openclaw.ai/gateway/security)
- [OpenClaw Deployment Guide — FreeCodeCamp](https://www.freecodecamp.org/news/how-to-deploy-your-own-24x7-ai-agent-using-openclaw/)
