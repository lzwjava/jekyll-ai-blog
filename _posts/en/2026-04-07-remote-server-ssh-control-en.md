---
audio: false
generated: true
image: false
lang: en
layout: post
title: Remote Server Control via SSH
translated: false
type: note
---

Question: Is it a good practice to use Claude Code on a separate laptop to control a LAN server running OpenClaw (AI agent), since controlling it remotely via SSH avoids interruption issues that would occur if the agent tried to restart itself?

Answer:

Yes, this is an excellent architectural pattern and a well-established best practice in systems administration and AI agent deployment. Here's why it works so well:

## The Core Problem You're Avoiding

When an AI agent tries to **manage its own process**, you get a self-referential problem:

- Agent receives instruction: "restart the server"
- Agent begins executing restart command
- **Agent's own process dies mid-execution**
- No confirmation, no error handling, no recovery

This is analogous to why you don't perform surgery on yourself.

## Your Pattern: External Controller via SSH

```
[Your Laptop - Claude Code]
        |
        | SSH
        v
[LAN Server 192.168.1.36]
   ├── llama-server (Gemma model)
   ├── OpenClaw agent
   └── config files (openclaw.json, etc.)
```

Claude Code on your laptop becomes the **out-of-band controller** — it sits entirely outside the system it's managing.

## Why This Is The Right Approach

**1. No self-interruption risk**
Claude Code keeps running on your laptop regardless of what happens on the LAN server. It can restart `llama-server`, kill OpenClaw, edit configs, and verify the restart — all without losing its own execution context.

**2. Full observability**
Claude Code can tail logs, check process status, and confirm services came back up:
```bash
ssh lzw@192.168.1.36 "tail -f /home/lzw/llama-server.log"
```

**3. Atomic config changes + restart**
```bash
ssh lzw@192.168.1.36 "
  # Edit config
  sed -i 's/reasoning-format.*/reasoning-format none/' openclaw.json
  
  # Restart service
  kill \$(pgrep llama-server)
  nohup /home/lzw/projects/llama.cpp/build/bin/llama-server ... &
  
  # Verify
  sleep 3 && curl http://localhost:8081/health
"
```

**4. Separation of concerns**
- **Claude Code** = management plane (your laptop)
- **OpenClaw + llama-server** = data plane (LAN server)

This mirrors how production infrastructure works — your CI/CD pipeline (GitHub Actions, etc.) is never running *on* the server it's deploying to.

## Practical Tips for This Setup

- **Use `nohup` or `screen`/`tmux`** on the server so processes survive SSH session drops
- **SSH key auth** so Claude Code can connect without password prompts
- **Health check endpoints** — Claude Code can poll `http://192.168.1.36:8081/health` to confirm restarts succeeded
- **Idempotent scripts** — write restart scripts that work whether the process is running or not (`pkill -f llama-server || true`)

## Immediate Next Step

Yes, have Claude Code SSH in and restart with `--reasoning-format none`:

```bash
ssh lzw@192.168.1.36 "kill 109829; nohup /home/lzw/projects/llama.cpp/build/bin/llama-server \
  -m /home/lzw/projects/llama.cpp/models/gemma-4-26B-A4B-it-UD-IQ3_S.gguf \
  --port 8081 -c 32768 --reasoning-format none \
  >> /home/lzw/llama-server.log 2>&1 &"
```

Claude Code on your laptop will wait for the SSH command to complete and can immediately verify the fix — something OpenClaw could never safely do for itself.