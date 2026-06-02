---
audio: false
generated: true
image: false
lang: en
layout: post
title: Yolo Mode in Hermes
translated: false
type: note
---

Here's the full breakdown of what was changed and how yolo mode works in Hermes.

---

## What changed

In `/home/xiaoxin/.hermes/config.yaml`, at line 406-407:

```yaml
approvals:
  mode: false   # ← was not set (defaults to 'manual')
```

This is under the `approvals` section (lines 406-412), which also includes `timeout`, `cron_mode`, `mcp_reload_confirm`, and `destructive_slash_confirm`.

---

## What this does

Hermes has a **command approval system** that intercepts potentially destructive shell commands (`rm -rf`, `git reset --hard`, `chmod -R 777`, etc.) and asks you to confirm before running them. There are three modes:

| Mode | Behavior |
|------|----------|
| `manual` | Always prompt before flagged commands (default) |
| `smart` | Use a small LLM to auto-approve low-risk commands, prompt on high-risk ones |
| `off` / `false` | Skip all approval prompts — this is **yolo mode** |

Setting `mode: false` (= `off`) means Hermes will **never ask for confirmation** before running any shell command it thinks is dangerous. It just executes them directly.

---

## Scope of "yolo mode"

Yolo mode only affects **dangerous-command approval prompts**. It does NOT change:

- **Secret redaction** (`security.redact_secrets`) — that's independent
- **Tirith security policies** (`security.tirith_enabled`) — security rules still apply
- **Tool access** — all your tools still work exactly as before
- **Any other config** — it's a narrowly scoped toggle

---

## How to use it

| Method | Scope |
|--------|-------|
| `hermes config set approvals.mode off` | **Persistent** — you just did this |
| `hermes --yolo` | Per-invocation flag (one session) |
| `export HERMES_YOLO_MODE=1` | Per-shell environment variable |
| `/yolo` (slash command in-session) | Toggle on/off for the current session |

---

## When it takes effect

Config changes like this are read at session startup. For **future sessions** (next time you run `hermes`), yolo will be on automatically. To apply it to your current session immediately, type `/yolo` (it toggles the approval bypass inline).

To revert later:

```bash
hermes config set approvals.mode manual    # back to default prompts
hermes config set approvals.mode smart     # AI-assisted approval
```
