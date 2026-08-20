---
audio: false
generated: true
image: false
lang: en
layout: post
title: Discord updater bypasses proxy
translated: false
type: note
---

## Diagnosis — root cause confirmed

I traced exactly why Discord hangs on "Checking for updates". It's **not** a problem with your proxy rules — it's the Discord **updater subprocess not using the proxy at all**.

**What's happening** (evidence from the updater's own log):

`~/Library/Application Support/discord/logs/Discord_updater_rCURRENT.log` repeats every ~75s:

```
ERROR [updater_client]: Failed 16 ... host: updates.discord.com
  source: hyper::Error(Connect, ConnectError("tcp connect error",
  Os { code: 60, kind: TimedOut, message: "Operation timed out" }))
```

**Why:**

1. Discord's app updater (`.../Resources/updater.node`, a Rust `reqwest` client) does a **raw TCP socket** to `https://updates.discord.com/...` → resolves to `54.89.135.129:443`.
2. That client does **not honor** the HTTP(S) system proxy (127.0.0.1:7890) nor `HTTPS_PROXY` env.
3. That IP/domain is unreachable directly from this network.

I confirmed the asymmetry with live tests:

| Connection | Result |
| --- | --- |
| **Direct (no proxy)**, `--noproxy '*'` | ❌ `Connection timed out after 15s` |
| **Through mihomo** `127.0.0.1:7890` | ✅ HTTP 200 in 0.34s |

My shell's `curl` worked only because the terminal env has `https_proxy=http://127.0.0.1:7890` — the updater launched from Finder/Dock doesn't inherit that.

**Why your rule isn't catching it:** `DOMAIN-SUFFIX,discord.com → Proxy` already exists in `~/.config/mihomo/config.yaml`, so `updates.discord.com` is correctly matched. The trouble is that rule only matters once traffic **reaches mihomo**. The updater's raw socket never traverses mihomo because you're running mihomo in **proxy mode only (no TUN)**.

## The proper fix: enable mihomo TUN mode

Your binary is already a `with_gvisor` build (supports TUN), so the durable solution is to let mihomo intercept **all** traffic — including raw sockets that bypass the proxy. With TUN on, the updater's direct connection to `54.89.135.129` gets captured, rule-matched (`discord.com → Proxy`), and tunneled through your Hysteria2/SS node.

To apply that I'd add to the config:

```yaml
tun:
  enable: true
  stack: system        # or gvisor
  auto-route: true
  auto-redirect: true
  auto-detect-interface: true
  dns-hijack:
    - any:53
```

and restart mihomo. ⚠️ This needs **admin privileges** (TUN requires a root/network entitlement) and a **brief disconnect** while mihomo restarts — so I don't want to change it mid-session and cut off your current connection.

## Immediate workaround (until TUN is on)

The updater will work if running in the proxy env — but you need it to. Two quick options:

- **Best quick fix:** On macOS, make the updater use your `HTTPS_PROXY` — since the updater honors `HTTPS_PROXY` env, launching Discord so it inherits that works (e.g., from your Terminal), but that only persists if kept set.
- **More reliable:** enable TUN (above).

Want me to apply the TUN config change and restart mihomo now? I need to confirm two things first: (1) you're OK with a brief drop in connectivity, and (2) mihomo can get admin/network privileges (do you run it from a privileged helper/agent, or should we wire it up to use a utun). Alternatively, if you tell me how mihomo is started (plain terminal? login item?) I can give you the exact safe procedure.
