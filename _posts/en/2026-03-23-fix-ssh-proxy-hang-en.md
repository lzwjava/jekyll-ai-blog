---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing SSH Hang Caused by Proxy
translated: false
type: note
---

Question: Why does SSH hang (stuck at "Connecting to...") to my OpenWrt router at 192.168.2.1 while ping works fine, and how do I fix it?

Answer:

## Root Cause: Your HTTP/HTTPS Proxy Is Intercepting SSH

Looking at your terminal output carefully, the smoking gun is right there at the top:

```
🚀 Proxy Settings Detected:
  - HTTP_PROXY: http://127.0.0.1:7890
  - HTTPS_PROXY: http://127.0.0.1:7890
```

SSH uses TCP port 22. When `HTTP_PROXY` or `HTTPS_PROXY` env vars are set, some proxy tools (like Clash, V2Ray, Shadowsocks clients running on port 7890) intercept **all outgoing TCP connections**, including SSH. The proxy tries to tunnel your SSH connection through an HTTP CONNECT proxy — but the target `192.168.2.1` is a private LAN IP, so the proxy either **refuses it**, **can't route it**, or just **hangs**.

Ping (ICMP) is unaffected because ICMP is not TCP and proxies don't touch it — which is exactly why ping works but SSH doesn't.

---

## Fix Options

### ✅ Fix 1: Bypass Proxy for Private/LAN IPs (Best Long-Term Fix)

Add `NO_PROXY` to exclude all private subnets:

```bash
export NO_PROXY="localhost,127.0.0.1,192.168.0.0/16,10.0.0.0/8,172.16.0.0/12"
```

Then retry SSH:

```bash
ssh root@192.168.2.1
```

To make it permanent, add the export line to your `~/.zshrc` or `~/.bashrc`.

---

### ✅ Fix 2: Unset Proxy Variables Just for This SSH Command

```bash
env -u HTTP_PROXY -u HTTPS_PROXY ssh root@192.168.2.1
```

This temporarily clears proxy settings only for that one command, without changing your environment.

---

### ✅ Fix 3: Use `ProxyCommand none` in `~/.ssh/config`

Your SSH config already has a `*` block applying options for all hosts. Add a specific override for your router:

```
Host 192.168.2.1
    ProxyCommand none
    User root
```

This tells SSH to connect directly, bypassing any proxy command that might be set.

---

### ✅ Fix 4: Configure Your Proxy App to Bypass LAN

If you're using **Clash**, **V2Ray**, **Mihomo**, or similar (port 7890 is typical for Clash):

Open the proxy app's config and add LAN bypass rules. In Clash for example:

```yaml
bypass:
  - localhost
  - 127.*
  - 10.*
  - 172.16.*
  - 192.168.*
  - "*.local"
```

This is the cleanest solution if you want everything (SSH, curl, etc.) to bypass proxy for LAN addresses automatically.

---

## Why Your SSH Config Made It Worse

From your verbose output:
```
debug1: /Users/lzwjava/.ssh/config line 4: Skipping Host block because of negated match for 192.168.*.*
debug1: /Users/lzwjava/.ssh/config line 6: Applying options for *
```

You have a negated rule `!192.168.*.*` in your SSH config, then a catch-all `*` block. The `*` block likely sets a `ProxyCommand` or proxy-related option (common when people configure SSH to use a SOCKS proxy for all connections). That wildcard rule is being applied to `192.168.2.1`, routing the SSH handshake through your proxy.

**The permanent solution** combining both issues:

```
# ~/.ssh/config

# Bypass proxy for all LAN addresses
Host 192.168.* 10.* 172.16.*
    ProxyCommand none
    ServerAliveInterval 30

# Your existing catch-all (with proxy settings) stays below
Host *
    ...your existing options...
```

---

## Quick Summary

| Symptom | Cause |
|---|---|
| Ping works | ICMP bypasses HTTP proxy |
| SSH hangs at "Connecting to" | Proxy intercepts TCP/22, can't reach LAN IP |
| No error message, just hangs | Proxy silently fails or waits for timeout |

**TL;DR** — Run `env -u HTTP_PROXY -u HTTPS_PROXY ssh root@192.168.2.1` to confirm this is the cause. If it connects immediately, add a permanent `NO_PROXY` or fix your `~/.ssh/config`.

References:

- [https://discussions.apple.com/thread/255263733](https://discussions.apple.com/thread/255263733)
- [https://www.theregister.com/2020/04/01/apples_macos_catalina_ssh/](https://www.theregister.com/2020/04/01/apples_macos_catalina_ssh/)