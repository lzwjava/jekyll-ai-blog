---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing OpenClaw Gateway Password Missing Error
translated: false
type: note
---

**Question:** How do I fix the "unauthorized: gateway password missing (enter the password in Control UI settings)" error in OpenClaw (AI agent)?

**Answer:**

This error means the OpenClaw Gateway is configured to use **password-based authentication**, but no password has been entered in the Control UI browser interface. Here is a full explanation and the steps to fix it.

---

## What Is Causing This Error?

The error `disconnected (1008): unauthorized: gateway password missing (enter the password in Control UI settings)` means that `gateway.auth.mode` is set to `password`, but no credentials were sent by the browser to the gateway.

The `unauthorized` error means the endpoint is reachable, but the wrong (or missing) auth was provided.

---

## Fix Option 1: Enter the Password in the Control UI (Quickest Fix)

If the UI prompts for auth, paste the token (or password) from your `gateway.auth` config into Control UI settings. The UI stores it in `localStorage` after you connect.

Steps:

1. Open the Control UI in **Chrome** (not Safari — see note below): `http://127.0.0.1:18789/`
2. You should see a **Settings** panel or a connection prompt.
3. Enter the password you set in `gateway.auth.password` in the password field.
4. Click **Connect**.

> ⚠️ **Safari Note:** The Control UI in Safari fails to render the password input dialog and loops reconnection attempts. Use Chrome instead — Chrome works correctly with the same configuration.

---

## Fix Option 2: Set a Password via CLI

If you haven't set a password yet, do it from the terminal:

```bash
openclaw config set gateway.auth.mode password
openclaw config set gateway.auth.password "YourSecurePasswordHere"
openclaw gateway restart
```

After running those commands and restarting, you will be prompted for the password in the UI.

---

## Fix Option 3: Switch to Token Auth Instead

If you'd prefer token-based auth (simpler for browser access), switch the mode:

```bash
openclaw config set gateway.auth.mode token
openclaw config set gateway.auth.token "$(openssl rand -hex 32)"
openclaw gateway restart
```

Then access the dashboard URL with the token appended:

```
http://127.0.0.1:18789/?token=YOUR_TOKEN_HERE
```

The token source is `gateway.auth.token` (or the environment variable `OPENCLAW_GATEWAY_TOKEN`); the UI stores a copy in `localStorage` after you connect.

---

## Fix Option 4: Avoid Auth Entirely (Localhost Only)

If you only access OpenClaw locally and don't want any auth, bind to loopback and remove the auth block:

```json
{
  "gateway": {
    "mode": "local",
    "bind": "loopback",
    "port": 18789
  }
}
```

> ⚠️ Only do this if you are **not** exposing the gateway to any network. Non-loopback binds (lan, tailnet, custom) need auth configured.

---

## Common Mistake: Wrong Config Key (Breaking Change in v2026.3.7)

As of OpenClaw 2026.3.7, if both `gateway.auth.token` and `gateway.auth.password` are configured but `gateway.auth.mode` is unset, the Gateway will refuse to start. You must explicitly declare which one is active.

Correct config examples:

**Token mode:**

```json
{ "gateway": { "auth": { "mode": "token", "token": "${OPENCLAW_GATEWAY_TOKEN}" } } }
```

**Password mode:**

```json
{ "gateway": { "auth": { "mode": "password", "password": "${OPENCLAW_GATEWAY_PASSWORD}" } } }
```

---

## Diagnostic Commands

Run these to debug auth issues:

```bash
openclaw config get gateway.auth.mode
openclaw config get gateway.auth.token
openclaw gateway status
openclaw doctor
```

---

**References:**

- [OpenClaw Dashboard Auth Docs](https://openclaw-ai.com/en/docs/web/dashboard)
- [OpenClaw Troubleshooting Guide](https://docs.openclaw.ai/gateway/troubleshooting)
- [Fix OpenClaw 1008 Unauthorized — ucartz.com](https://www.ucartz.com/blog/fix-openclaw-disconnected-from-gateway-1008-unauthorized/)
- [OpenClaw 2026.3.7 Breaking Change — clawcloud.sh](https://www.clawcloud.sh/guides/openclaw-3-7-gateway-auth-mode)
- [GitHub Issue: Safari password prompt bug #4458](https://github.com/openclaw/openclaw/issues/4458)
