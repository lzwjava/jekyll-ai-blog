---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing OpenClaw Gateway Crash and Warnings
translated: false
type: note
---

**Question:** How do I fix the `openclaw-gateway.service` that keeps crashing with the error `error: unknown option '--host'` and a Telegram group policy warning?

**Answer:**

Your log shows **two distinct problems** — one is the fatal crash (the `--host` option error), and the other is a Telegram warning. Fix them separately:

---

## Problem 1 (Fatal): `error: unknown option '--host'`

This is the root cause of the crash loop (restart counter at 131+). The gateway startup command is passing a `--host` flag that is **not a valid option** for the current version of OpenClaw. The error message itself hints: `(Did you mean --port?)`.

This typically happens when:

- Your config has a `gateway.host` key that the CLI is incorrectly translating to a `--host` flag, OR
- The systemd service unit was manually edited with `--host` in the `ExecStart` line, which is no longer valid in v2026.x

### Fix Steps

**Step 1 — Remove the invalid `gateway.host` config key:**

```bash
openclaw config set gateway.bind "localhost"
```

Or if you specifically want to set a port:

```bash
openclaw config set gateway.port 3001
```

Do **not** use `gateway.host` — the correct config keys are `gateway.host` for some older setups, but the current recommended fix is `openclaw config set gateway.bind "localhost"` and `openclaw config set gateway.port 3001`.

**Step 2 — Run the auto-fix doctor:**

```bash
openclaw doctor --fix
```

`openclaw doctor --fix` runs health checks and auto-fixes common issues including permissions, config, and missing directories.

**Step 3 — Check your systemd service unit** for any hardcoded `--host` flag:

```bash
systemctl --user cat openclaw-gateway.service
```

If you see `--host` in the `ExecStart=` line, edit it out:

```bash
systemctl --user edit openclaw-gateway.service
```

Remove the `--host` argument and save.

**Step 4 — Reinstall and restart the gateway:**

```bash
openclaw gateway install --force
openclaw gateway restart
```

Or via systemd:

```bash
systemctl --user restart openclaw-gateway
```

---

## Problem 2 (Warning): Telegram Group Messages Being Silently Dropped

The log warns:

> `channels.telegram.groupPolicy is "allowlist" but groupAllowFrom (and allowFrom) is empty — all group messages will be silently dropped.`

This won't crash the service, but it means your bot ignores all Telegram group messages. Fix it with **one of these two options**:

**Option A — Add allowed sender IDs to the allowlist:**

```bash
openclaw config set channels.telegram.groupAllowFrom '[-1001234567890]'
```

Replace the number with your actual Telegram group chat ID.

**Option B — Open group messages to everyone (less secure):**

```bash
openclaw config set channels.telegram.groupPolicy "open"
```

---

## Summary of Commands to Run

```bash
# 1. Fix the host config issue
openclaw config set gateway.bind "localhost"
openclaw config set gateway.port 3001

# 2. Auto-fix any other config problems
openclaw doctor --fix

# 3. Fix the Telegram group policy (choose one)
openclaw config set channels.telegram.groupPolicy "open"
# OR add specific group IDs to the allowlist

# 4. Reinstall and restart
openclaw gateway install --force
openclaw gateway restart

# 5. Verify it's stable
openclaw status
openclaw logs --follow
```

After restarting, the crash loop should stop and the restart counter should freeze.

**References:**

- [OpenClaw Official Troubleshooting](https://docs.openclaw.ai/gateway/troubleshooting)
- [ClawTank: Fix Common Errors](https://clawtank.dev/blog/openclaw-troubleshooting-common-errors)
- [LumaDock: OpenClaw Deep Troubleshooting](https://lumadock.com/tutorials/openclaw-troubleshooting-common-errors)
- [Zeabur: OpenClaw Troubleshooting](https://zeabur.com/blogs/openclaw-troubleshooting-on-zeabur)
