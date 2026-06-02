---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disabling Hermes Agent Approval Prompts
translated: false
type: note
---

**Question:** In Hermes Agent, it often flags dangerous commands and asks for approval one by one — how can I allow any command without being prompted each time?

**Answer:**

Hermes Agent (by NousResearch) has a multi-layered security system for command approval. Here is a comprehensive breakdown of all the ways to reduce or bypass approval prompts, with appropriate warnings.

---

## Understanding the Approval System

Before executing any command, Hermes checks it against a curated list of dangerous patterns. If a match is found, the user must explicitly approve it. The approval system supports three modes, configured via `approvals.mode` in `~/.hermes/config.yaml`.

```yaml
approvals:
  mode: manual   # manual | smart | off
  timeout: 60    # seconds to wait before auto-deny
```

---

## Option 1: Disable All Approval Prompts (`approvals.mode: off`)

This is the most direct way. Setting `approvals.mode: off` disables all safety prompts.

```yaml
# ~/.hermes/config.yaml
approvals:
  mode: off
```

> ⚠️ **Warning:** This means Hermes will run ANY terminal command without asking you first (except the absolute blocklist — see below).

---

## Option 2: Use "Smart" Mode (LLM Risk Assessment)

Instead of `off`, you can set mode to `smart`:

Use an auxiliary LLM to assess risk. Safe commands will pass through automatically; only genuinely risky ones will prompt you.

```yaml
approvals:
  mode: smart
```

This is a middle ground — less interruption, but not fully blind.

---

## Option 3: Use Docker/Container Backend (Recommended for Safety)

For production gateway deployments, use `docker`, `modal`, `daytona`, or `vercel_sandbox` backend to isolate agent commands from your host system. This eliminates the need for dangerous command approval entirely.

```yaml
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"
  container_persistent: true
```

When running inside a container, dangerous command checks are skipped because the container already provides isolation. This is the **safest** way to allow all commands — the commands run freely inside the sandbox, not on your host machine.

---

## Option 4: Use `--yolo` Flag (CLI Only)

The `--yolo` flag is referenced in the codebase as a way to skip approval layers in the CLI. It works below the approval middleware but **above** the absolute blocklist.

```bash
hermes --yolo
```

> ⚠️ Commands on the `UNRECOVERABLE_BLOCKLIST` (like `rm -rf /`, fork bombs, direct block-device writes) are **always blocked** regardless of `--yolo` or `mode: off`.

---

## Option 5: Auto-Approve for Non-Interactive / Subagent Runs

When a subagent hits a dangerous-command approval prompt, `subagent_auto_approve: false` is the default — auto-deny. You can flip it to `true` to auto-approve "once" instead of blocking on stdin. Both choices emit a `logger.warning` audit line. Flip to `true` only for cron/batch pipelines.

```yaml
# ~/.hermes/config.yaml
subagent_auto_approve: true
```

---

## The Hard Limit: UNRECOVERABLE_BLOCKLIST

No matter what settings you use, some commands are so catastrophic — irreversible filesystem wipes, fork bombs, direct block-device writes — that Hermes refuses to run them regardless. The blocklist trips before the approval layer even sees the command, and there is no override flag. If a legitimate workflow needs one of these commands, run it outside the agent.

---

## Summary Table

| Method | Effect | Risk Level |
|---|---|---|
| `approvals.mode: off` | No prompts at all | High (host exposed) |
| `approvals.mode: smart` | LLM decides per-command | Medium |
| Docker backend | No prompts + isolation | Low (sandboxed) |
| `--yolo` flag | Skips approval layer | High |
| `subagent_auto_approve: true` | For batch/cron pipelines | Medium |

**Best Practice:** If you want zero interruptions, use `docker` backend + `approvals.mode: off` together — you get the convenience of no prompts while the container protects your host system.

---

**References:**

- [Hermes Agent Security Docs](https://hermes-agent.nousresearch.com/docs/user-guide/security)
- [Hermes Agent Configuration Docs](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- [GitHub: cli-config.yaml.example](https://github.com/NousResearch/hermes-agent/blob/main/cli-config.yaml.example)
- [GitHub: Permission Tiers Issue #527](https://github.com/NousResearch/hermes-agent/issues/527)
