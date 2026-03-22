---
audio: false
generated: true
image: false
lang: en
layout: post
title: macOS SSH Proxy Hang Issue Analysis
translated: false
type: note
---

Good references! Here's how they relate to your SSH proxy hang issue:

## Reference Analysis

**Reference 1 (Apple Discussions)** - Partially relevant
- **Similar symptoms**: SSH hangs with no error, tcpdump shows no traffic
- **Different root cause**: Cloudflare Warp VPN blocking SSH, not HTTP proxy env vars
- **Takeaway**: VPN/proxy software can silently block SSH in multiple ways

**Reference 2 (The Register - Catalina SSH bug)** - Highly relevant ✅
- **Direct match**: macOS SSH + proxy configuration causing hangs
- **Root cause**: Auto Proxy Discovery interfering with SSH
- **Key insight**: The bug affected SSH to ports >8192 using hostnames, and disabling proxy settings fixed it

## How They Support Your Answer

Your diagnosis (HTTP_PROXY/HTTPS_PROXY env vars intercepting SSH) is spot-on. Reference 2 confirms that **macOS SSH + proxy settings = known hang issue**. The Catalina bug was specifically about Auto Proxy Discovery, but the pattern is identical:

1. Proxy configuration active
2. SSH attempts connection
3. Proxy intercepts/mishandles the connection
4. SSH hangs silently

## Suggested Addition to Your Answer

You could add this context at the end:

```markdown
---

## Known macOS SSH + Proxy Issues

This is a recurring pattern on macOS:
- **macOS 10.15.4 bug**: Auto Proxy Discovery broke SSH to ports >8192 ([source](https://www.theregister.com/2020/04/01/apples_macos_catalina_ssh/))
- **VPN interference**: Apps like Cloudflare Warp can silently block SSH ([source](https://discussions.apple.com/thread/255263733))
- **HTTP_PROXY env vars**: Clash/V2Ray proxies intercept all TCP including SSH to LAN IPs (this case)

The common thread: proxy/VPN software treating SSH as HTTP traffic and failing to route it correctly.
```

Both references validate that your diagnosis is part of a well-documented class of macOS SSH issues related to proxy/VPN interference.