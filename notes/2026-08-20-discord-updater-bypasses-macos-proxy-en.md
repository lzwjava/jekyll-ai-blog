---
audio: false
generated: true
image: false
lang: en
layout: post
title: Discord Updater Bypasses macOS Proxy
translated: false
type: note
---

## Summary

### Root cause of "Discord checking for updates but never finishing"
The **Discord app updater** (`.../Discord.app/Contents/Resources/updater.node`, a Rust `reqwest` client) does a **raw TCP connection** to `https://updates.discord.com/` → `54.89.135.129:443`. That client **ignores** the macOS HTTP/S proxy (`127.0.0.1:7890`) and the `HTTPS_PROXY` env.

Proof from its own log (`~/Library/Application Support/discord/logs/Discord_updater_rCURRENT.log`), repeating every ~75s:
```
ERROR [updater_client]: ... host: updates.discord.com ...
  hyper::Error(Connect, ConnectError("tcp connect error",
  Os { code: 60, kind: TimedOut, message: "Operation timed out" }))
```

Live tests confirmed the asymmetry:
- **via mihomo** `127.0.0.1:7890` → ✅ HTTP 200 (0.34s)
- **true direct** (`--noproxy '*'`) → ❌ `Connection timed out`

The `DOMAIN-SUFFIX,discord.com → Proxy` rule was already correct — but it only matters once traffic *reaches* mihomo, which doesn't happen because mihomo runs in **proxy mode with no TUN**. My shell's `curl` worked only because the terminal env carries `https_proxy=...`; the updater launched from Finder/Dock doesn't.

### What I did
1. Backed up config → `config.yaml.bak.20260820203217`.
2. Added a `tun:` block to `~/.config/mihomo/config.yaml`:
   ```yaml
   tun:
     enable: true
     stack: gvisor
     dns-hijack:
       - "any:53"
     auto-route: true
     auto-detect-interface: true
   ```
3. Pushed config reloads via the controller API (`PUT /configs?force=true`) — returned **HTTP 204** each time.

### ⚠️ TUN is NOT active
`/configs` still reports:
```
tun: {enable: False, stack: gVisor, inet4-address: ['198.18.0.1/30'], ...}
```
Key observations:
- `enable` stays `False`.
- `inet4-address` shows the **default** `198.18.0.1/30`, not the `.2/30` I wrote in the file — so the running instance **hasn't applied** my tun block (only some fields).

### Why TUN isn't starting (blocked at OS level)
Your mihomo:
- Runs as normal user `lzwjava` (no sudo/root).
- Is **unsigned** (`code object is not signed at all`).
- On macOS, creating / routing a `utun` interface requires the `com.apple.security.network.tunnel` entitlement (or elevated privileges). A normal-user unsigned process cannot do it — so TUN silently stays disabled.

### Recommended next steps (you pick)
1. **Most reliable — use a GUI that manages admin TUN:** You already have **ClashX Pro** installed, which handles the privileged helper/entitlement for you and persists config. Use its config editor (mihomo under the hood) and enable "TUN / enhanced mode" in its UI — it will correctly elevate and start the interface. This is the cleanest fix given your setup.
2. Manually run mihomo via `sudo` (prompts for password, TUN will work), e.g. `sudo ~/bin/mihomo...`. Trade-off: runs as root, manual supervision.
3. Sign the binary with a tunnel entitlement + run a privileged helper to set up the interface — more invasive.

**If you want, I can instead revert my edit** to the config to keep just the proxy-level fix and go the ClashX Pro route — or help you set up the `sudo` launch. Which direction do you want?
