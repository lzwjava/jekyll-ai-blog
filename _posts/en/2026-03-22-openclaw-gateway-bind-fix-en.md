---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing OpenClaw Gateway Bind Validation Error
translated: false
type: note
---

**Question:** What does the error "Config validation failed: gateway.bind: gateway.bind host aliases (for example 0.0.0.0/localhost) are legacy; use bind modes (lan/loopback/custom/tailnet/auto) instead (auto-migrated on load)" mean, and how do I fix it?

**Answer:**

## What This Error Means

This error comes from **OpenClaw** (or a compatible gateway tool like ClawdBot), and it means your configuration file has an **outdated/legacy value** for the `gateway.bind` setting.

Older versions accepted raw IP addresses or hostname strings like:

- `"0.0.0.0"`
- `"localhost"`
- `"127.0.0.1"`
- A specific Tailscale IP address (e.g. `100.x.x.x`)

After a gateway upgrade (around version 2026.2.19), the config validator now rejects specific IP addresses set in `gateway.bind` — this breaking change was introduced alongside updates to how bind validation works.

The system now requires **named bind modes** instead of raw IPs or host aliases.

---

## The 5 Valid Bind Modes

| Mode | What It Does |
|---|---|
| `loopback` | Binds to `127.0.0.1` — local machine only (most secure, default) |
| `lan` | Listens on `0.0.0.0` (all interfaces) — allows local LAN access |
| `tailnet` | Binds to a Tailscale IP (`100.64.0.0/10` range) — for Tailscale network access |
| `custom` | Bind to a specific custom address you define |
| `auto` | Automatically selects the best available bind address; falls back when loopback is unavailable |

---

## What "auto-migrated on load" Means

The message says the config was **auto-migrated on load** — meaning the gateway attempted to automatically translate your old legacy value to the closest matching bind mode at runtime. However, it still **warns/fails validation** to alert you that your config file is outdated and should be manually updated.

---

## How to Fix It

Open your config file (typically `~/.openclaw/openclaw.json` or wherever `OPENCLAW_CONFIG_PATH` points) and change the `gateway.bind` field:

**Before (legacy — causes error):**

```json
{
  "gateway": {
    "bind": "0.0.0.0"
  }
}
```

**After (correct):**

```json
{
  "gateway": {
    "bind": "lan"
  }
}
```

### Choosing the Right Mode

- **Local-only access** (same machine): use `loopback`
- **Access from other devices on same network**: use `lan`
- **Access via Tailscale VPN**: use `tailnet` (requires Tailscale running)
- **Not sure**: use `auto`

---

## Important: Non-Loopback Modes Require Auth

Non-loopback bind modes (`lan`, `tailnet`, `custom`, or `auto` when loopback is unavailable) require authentication to be configured — specifically `gateway.auth.token` or the `OPENCLAW_GATEWAY_TOKEN` environment variable.

If you switch to `lan` or `tailnet` and haven't set up auth, you'll get a "refusing to bind without auth" error next.

---

## Quick Fix via CLI

You can also run the built-in migration/repair tool:

```bash
openclaw doctor --fix
```

or reinstall the gateway service cleanly:

```bash
openclaw gateway install --force
```

**References:**

- [OpenClaw Troubleshooting Docs](https://docs.claw.so/engine/gateway/troubleshooting/)
- [GitHub Issue #21504 — gateway.bind IP validation after upgrade](https://github.com/openclaw/openclaw/issues/21504)
- [OpenClaw Security Docs](https://docs.openclaw.ai/gateway/security)
- [Configuring OpenClaw Gateway Bind on Azure](https://lucaberton.com/blog/configuring-openclaw-gateway-bind-and-control-ui/)
