---
audio: false
generated: true
image: false
lang: en
layout: post
title: Never Store API Keys in GitHub Repositories
translated: false
type: note
---

**Question:** Is a private GitHub repository safe to store API keys or tokens for OpenAI, Anthropic, OpenRouter, and other LLM providers?

**Answer:**

**No. Do not store API keys in any GitHub repo, private or public.**

Here's why "private" is not a security boundary:

## Why Private Repos Are Not Safe

1. **Accidental visibility changes** — One wrong click converts private → public. GitHub has a history of UI confusion causing this.
2. **Collaborator access** — Anyone you add to the repo gets the keys. That's a flat access model — no granularity.
3. **GitHub itself** — GitHub scans repos (including private ones) and has had breaches. GitHub staff can access private repos per their ToS.
4. **Forks and clones** — Collaborators can fork or clone, and now your key lives on their machine.
5. **Git history is forever** — Even if you delete a key from the file, it remains in `git log`. Requires `git filter-branch` or BFG to purge.
6. **CI/CD exposure** — GitHub Actions logs, third-party Actions, or misconfigured workflows can leak secrets from private repos.
7. **Token leakage** — If your GitHub personal access token (PAT) is ever compromised, the attacker sees all your private repos and all the keys inside.

---

## The Right Way: Secrets Management

### Local dev (your MacBook / workstation)

```bash
# ~/.zshrc or ~/.bashrc — NOT in any repo
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENROUTER_API_KEY="sk-or-..."
```

Load in code:

```python
import os
key = os.environ["ANTHROPIC_API_KEY"]
```

### Per-project: `.env` files

```bash
# .env  ← git-ignored
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

```bash
# .gitignore
.env
.env.*
*.env
```

Load with `python-dotenv`:

```python
from dotenv import load_dotenv
load_dotenv()
```

**Always add `.env` to `.gitignore` before the first commit.**

### Audit your `.gitignore` before every new repo

```bash
# Verify .env is ignored before git add
git check-ignore -v .env
```

### Production / CI

| Context | Tool |
|---|---|
| GitHub Actions | [Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) via `Settings → Secrets` |
| Any cloud | AWS Secrets Manager, GCP Secret Manager, Azure Key Vault |
| Self-hosted | HashiCorp Vault |
| Team secrets | 1Password Secrets Automation, Doppler |

---

## If You Already Committed a Key

Assume it's compromised. Keys in git history are effectively public.

1. **Revoke the key immediately** — go to OpenAI/Anthropic/OpenRouter dashboard and delete it
2. **Generate a new key**
3. **Purge history** if needed (BFG Reaper or `git filter-repo`)

```bash
# Install BFG
brew install bfg

# Purge a specific string from all history
bfg --replace-text secrets.txt my-repo.git
```

---

## Summary

| Storage method | Safe? |
|---|---|
| Private GitHub repo | ❌ No |
| Public GitHub repo | ❌ Absolutely not |
| `~/.bashrc` / `~/.zshrc` (local) | ✅ OK for local dev |
| `.env` (git-ignored) | ✅ OK for local dev |
| GitHub Actions Encrypted Secrets | ✅ OK for CI |
| Cloud secrets manager | ✅ Best for prod |

Given your setup — two machines plus AMD cloud — the practical recommendation is: env vars in `~/.zshrc` on each machine, `.env` files with a solid `.gitignore` template for per-project keys, and GitHub Encrypted Secrets for any CI/CD pipelines.