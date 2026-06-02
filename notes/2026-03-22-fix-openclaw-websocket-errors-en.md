---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing OpenClaw WebSocket Connection Errors
translated: false
type: note
---

Question: How to fix the WebSocket connection error "ws://192.168.1.36:18789/" failed: WebSocket is closed before the connection is established in OpenClaw gateway?

Answer:

The error usually means the WebSocket handshake starts but the server immediately rejects and closes it (often with code 1008). This is **not** caused by using `ws://` (HTTP) instead of `wss://` (HTTPS) on a local LAN — plain HTTP + ws:// works fine in most cases.

The root cause is almost always one (or both) of these server-side checks failing:

1. **Origin not allowed** — the browser's `Origin` header doesn't match the allowed list
2. **Device identity required** — even for the Control UI, the gateway enforces device pairing/identity unless explicitly disabled

### Quick Fix Steps (LAN / HTTP setup)

1. **Check your current config**
   Run this command (adjust if your CLI path differs):

   ```
   openclaw config get gateway.controlUi
   ```

   Look for:
   - `allowedOrigins`: should include your exact browser URL, e.g. `["http://192.168.1.36:18789"]`
     (no trailing slash, exact protocol + IP + port)
   - `dangerouslyDisableDeviceAuth`: should be `true`

   If either is missing or wrong → that's the problem.

2. **Set the correct values**

   ```bash
   # Set the exact origin you're using in the browser
   openclaw config set gateway.controlUi.allowedOrigins '["http://192.168.1.36:18789"]'

   # Disable device identity check (needed for non-secure-context / non-loopback browser access)
   openclaw config set gateway.controlUi.dangerouslyDisableDeviceAuth true

   # Optional but often helpful for plain HTTP:
   openclaw config set gateway.controlUi.allowInsecureAuth true
   ```

   **Important notes about `allowedOrigins`:**
   - Must match **exactly** what appears in the browser address bar (protocol + host + port).
   - Do **not** use `["*"]` unless this is a throwaway test machine — it's a big security risk.
   - If you're accessing via `http://localhost:18789` or another hostname, add that too: `["http://192.168.1.36:18789", "http://localhost:18789"]`

3. **Restart the gateway** so changes take effect

   ```bash
   openclaw gateway restart
   ```

   Or if using systemd:

   ```bash
   systemctl --user restart openclaw-gateway.service
   ```

4. **Check gateway logs for the real rejection reason**

   ```bash
   journalctl --user -u openclaw-gateway.service -n 80 --no-pager
   ```

   Look for lines containing:
   - `origin not allowed`
   - `device-required`
   - `code=1008`
   - `reason=`

   That will tell you exactly which check failed.

### HTTPS / wss:// Alternative (more secure long-term)

- You can avoid `dangerouslyDisableDeviceAuth` completely if you use HTTPS, because browsers treat HTTPS pages as secure contexts → device identity can be handled via other mechanisms.
- But on LAN you need either:
  - Self-signed certificate (browser shows warning; you must manually trust it → tedious)
  - Or better: use a reverse proxy (Caddy / Nginx) + local DNS (e.g. `openclaw.lan`) + self-signed or mkcert certificate
- Most users stay on HTTP + the two config settings above for simple LAN access.

### Common Pitfalls

- Config keys are **case-sensitive** and nested correctly (`gateway.controlUi.…`)
- Changes don't apply until gateway restart
- If you recently updated OpenClaw, some versions had bugs where `dangerouslyDisableDeviceAuth` was ignored → check your version and consider downgrading/updating if needed
- Make sure you're opening the UI in a normal browser tab (not iframe / embedded)

After applying the config + restart, refresh the Control UI page — the WebSocket should connect.

References:

- [https://docs.openclaw.ai/gateway/security](https://docs.openclaw.ai/gateway/security)
- [https://github.com/openclaw/openclaw/issues/41043](https://github.com/openclaw/openclaw/issues/41043)
- [https://github.com/openclaw/openclaw/issues/44485](https://github.com/openclaw/openclaw/issues/44485)
- [https://docs.openclaw.ai/web/control-ui](https://docs.openclaw.ai/web/control-ui)
