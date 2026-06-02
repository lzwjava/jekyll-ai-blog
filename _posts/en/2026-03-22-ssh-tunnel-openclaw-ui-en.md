---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH Tunneling for OpenClaw UI Access
translated: false
type: note
---

Question: If using SSH port forwarding with the command `ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36`, will the copy button work in the OpenClaw Control UI?

Answer:

Yes, using this SSH tunnel setup should allow the full Control UI (including the copy button and other clipboard features) to work properly in your browser.

### Why this setup fixes the original WebSocket issue and enables copy functionality

- **Origin becomes localhost (secure context)**
  When you run `ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36` on your local machine and keep the tunnel open, then open your browser to `http://localhost:18789` (or `http://127.0.0.1:18789`), the browser sees the page as coming from **http://localhost:18789**.
  OpenClaw gateway treats `localhost` (127.0.0.1) as a **loopback / secure context**, even over plain HTTP. This bypasses several strict security checks that apply to non-loopback / remote IPs (like your original `http://192.168.1.36:18789` access).

- **Key security checks that get relaxed automatically**
  - **Origin allowlist (`allowedOrigins`)**: localhost is implicitly allowed (no need to set `allowedOrigins` explicitly for loopback access).
  - **Device identity / pairing requirement**: Browsers treat localhost as a secure context → OpenClaw does **not** require `dangerouslyDisableDeviceAuth: true` anymore. The "device-required" rejection (code 1008) usually disappears.
  - **Insecure auth fallback**: Often not needed, but if you still see issues you can set `gateway.controlUi.allowInsecureAuth: true` as a backup.

- **Copy button / clipboard access specifically**
  The copy button in the Control UI uses the modern Clipboard API (`navigator.clipboard.writeText()`).
  This API requires a **secure context** (HTTPS or localhost/127.0.0.1).
  Accessing via `http://192.168.1.36:18789` (non-secure, non-loopback) blocks clipboard permission → copy button fails or shows "unavailable. No GUI detected."
  Accessing via the SSH tunnel (`http://localhost:18789`) provides a secure context → clipboard works normally, no extra browser prompts or errors.

### How to use it correctly

1. On your local computer, open a terminal and run:
   ```bash
   ssh -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36
   ```
   - Keep this terminal open (the tunnel dies if you close it).
   - You may need to enter the password or use key-based auth.

2. In your browser (on the same local computer), go to:
   `http://localhost:18789`
   (or `http://127.0.0.1:18789` — same thing)

3. Log in with your gateway token if prompted (usually shown during onboarding or in `~/.openclaw/openclaw.json` on the server).

4. The Control UI should load fully, WebSocket connects without closure, and copy buttons (e.g. for tokens, commands, logs) function normally.

### Optional: Make it more convenient

- Add to your `~/.ssh/config` for easier reconnect:
  ```
  Host openclaw-tunnel
      HostName 192.168.1.36
      User lzw
      LocalForward 18789 127.0.0.1:18789
  ```
  Then just run: `ssh -N openclaw-tunnel`

- For persistent tunnel (auto-reconnect), use `autossh` if installed:
  `autossh -M 0 -N -L 18789:127.0.0.1:18789 lzw@192.168.1.36`

- If you still get "origin not allowed" (rare with localhost):
  Run on the server (192.168.1.36):
  ```bash
  openclaw config set gateway.controlUi.allowedOrigins '["http://localhost:18789", "http://127.0.0.1:18789"]'
  openclaw gateway restart
  ```

This SSH tunnel method is the officially recommended way in OpenClaw docs for secure LAN/remote access without exposing the port publicly or setting up HTTPS.

References:

- [https://docs.openclaw.ai/gateway/security](https://docs.openclaw.ai/gateway/security)
- [https://docs.openclaw.ai/gateway/remote](https://docs.openclaw.ai/gateway/remote)
- [https://github.com/openclaw/openclaw/issues/1679](https://github.com/openclaw/openclaw/issues/1679)
- [https://intercom.help/lumadock/en/articles/13548567-openclaw-quickstart-onboarding-over-ssh](https://intercom.help/lumadock/en/articles/13548567-openclaw-quickstart-onboarding-over-ssh)
