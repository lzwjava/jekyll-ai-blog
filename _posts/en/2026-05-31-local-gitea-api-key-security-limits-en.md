---
audio: false
generated: true
image: false
lang: en
layout: post
title: Local Gitea API Key Security Limits
translated: false
type: note
---

**Question:** Is it safe to store API keys in a private repository on a self-hosted local Gitea server running on your local workstation?

**Answer:**

Significantly safer than GitHub, but still not the right tool for secrets. Here's the full picture:

## Why Local Gitea Is Better Than GitHub

| Risk | GitHub Private | Local Gitea |
| --- | --- | --- |
| GitHub staff access | ✅ exists | ❌ eliminated |
| GitHub breach | ✅ real risk | ❌ eliminated |
| Accidental public exposure | ✅ one click | ❌ much harder |
| Third-party Actions leakage | ✅ real | ❌ you control CI |
| Internet-exposed attack surface | ✅ always | ❌ LAN-only (if configured right) |

So if your Gitea is:

- LAN-only (not port-forwarded, not behind a public domain)
- Only you have access
- Running on your `192.168.1.36` workstation

...then practically speaking, the risk is very low. For a solo developer's personal tooling, this is arguably acceptable.

---

## But These Risks Remain

### 1. Git history is still permanent

Same problem as GitHub — if you ever `git log`, the key is there forever. Rotation becomes painful.

```bash
# Key deleted from file but still visible:
git log -p | grep "sk-ant-"
```

### 2. Gitea itself has vulnerabilities

Gitea has had CVEs. If your workstation is on a shared network (office, university, etc.), a network attacker could exploit Gitea.

### 3. Backup leakage

If you back up your workstation (Time Machine, rsync, cloud backup), your Gitea data — including all git history — goes with it. Now your keys are wherever your backups are.

### 4. Repo clones on multiple machines

You said you have a MacBook Air + workstation + AMD cloud. If you clone the repo to all three, the keys are on all three machines and in transit over SSH/HTTPS.

### 5. Discipline failure over time

Today it's just you. Tomorrow you add a collaborator, or accidentally expose Gitea to the internet for convenience. The key is already in history.

---

## The Real Problem: Git Is the Wrong Tool for Secrets

Git is designed to **never forget**. Secrets need **rotation, expiry, and revocation**. These are fundamentally incompatible goals.

---

## What I'd Actually Recommend for Your Setup

Given your 3-machine setup (MacBook + workstation + AMD cloud):

### Option 1: `pass` — the Unix password manager (best for solo dev)

```bash
# Install
brew install pass        # macOS
sudo apt install pass    # Ubuntu

# Init with your GPG key
pass init "your@email.com"

# Store keys
pass insert llm/anthropic
pass insert llm/openai
pass insert llm/openrouter

# Retrieve in scripts
export ANTHROPIC_API_KEY=$(pass llm/anthropic)
```

`pass` stores GPG-encrypted files in `~/.password-store/` — which IS a git repo, but the values are encrypted at rest. You can sync it via your Gitea and it's safe because the secrets are ciphertext in git.

```bash
# Sync across machines via your local Gitea
cd ~/.password-store
git remote add origin http://192.168.1.36:3000/lzw/pass-store.git
git push
```

Now keys are in Gitea but **encrypted**. Even if someone clones the repo, they need your GPG private key.

### Option 2: `direnv` + `.env` (per-project, simple)

```bash
brew install direnv      # macOS
sudo apt install direnv  # Ubuntu

# .envrc (git-ignored)
export ANTHROPIC_API_KEY="sk-ant-..."
```

```bash
# .gitignore
.envrc
.env
```

`direnv` auto-loads env vars when you `cd` into the project. No secret ever touches git.

### Option 3: Infisical self-hosted (if you want a proper secrets manager)

Since you already run Gitea locally, you can also self-host [Infisical](https://github.com/Infisical/infisical) — it's an open-source secrets manager with a CLI:

```bash
# Fetch secrets into your shell
infisical run -- python my_script.py
```

Overkill for solo use, but worth knowing if you expand to a team.

---

## My Recommendation for You Specifically

```
pass (GPG-encrypted) + synced via local Gitea
```

- Encrypted at rest → safe in git history
- Syncs across your 3 machines via your existing Gitea
- CLI-native, scriptable, no GUI
- Works perfectly with your Python/bash workflow:

```python
import subprocess
key = subprocess.check_output(["pass", "llm/anthropic"]).decode().strip()
```

Or just load at shell startup in `~/.zshrc`:

```bash
export ANTHROPIC_API_KEY=$(pass llm/anthropic)
export OPENAI_API_KEY=$(pass llm/openai)
export OPENROUTER_API_KEY=$(pass llm/openrouter)
```

---

## Summary

| Approach | Safe? | Syncs across machines | Notes |
| --- | --- | --- | --- |
| Local Gitea, plaintext | ⚠️ Low risk, but wrong tool | ✅ | History leakage, backup risk |
| Local Gitea + `pass` (GPG) | ✅ Good | ✅ | Best of both worlds |
| `.env` + `direnv`, no git | ✅ Good | Manual copy | Simple, no sync |
| Infisical self-hosted | ✅ Best | ✅ | Overkill for solo |
| `~/.zshrc` env vars | ✅ OK | Manual copy | Simplest, no sync |
