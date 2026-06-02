---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-haiku-4.5
title: Clash Global Mode Explained Simply
translated: false
type: note
---

Great question! "Global mode" in Clash means all traffic goes through the proxy. Here's how it works:

**Global Mode Flow:**

1. **DNS Resolution** — When your device requests a domain (e.g., `google.com`), Clash intercepts it and uses its configured DNS servers to resolve it to an IP address.

2. **Routing Decision** — Clash then decides where to send the traffic:
   - In **global mode**, ALL traffic (not just specific domains/IPs) gets routed through your proxy/VPN.
   - This is different from **Rule mode**, where only certain traffic matching your rules goes through the proxy.

3. **Proxy Forwarding** — The resolved traffic is then sent through your configured proxy server(s) to reach the destination.

**Why use global mode?**

- Everything encrypted and routed through your proxy (more privacy)
- Bypasses geo-blocking or restrictions everywhere
- Useful when you want complete anonymity

**The DNS configuration's role:**

```yaml
nameserver:
    - 8.8.8.8
    - 1.1.1.1
```

These resolve domain names to IPs. When Clash gets a DNS query, it uses these servers. The `fallback` servers are backups if the primary ones fail.

**Fake-IP mode advantage:**

```yaml
fake-ip-range: 198.18.0.1/16
```

Instead of waiting for real DNS resolution, Clash assigns temporary fake IPs instantly and resolves in the background—faster response times.

**Common issue:** If you're getting DNS errors in global mode, it usually means either the nameservers are unreachable or there's a conflict with your system's DNS settings. Make sure your proxy connection is working first before enabling global mode.

Are you having trouble connecting with global mode enabled?
