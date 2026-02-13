---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix Clash DNS Configuration Guide
translated: false
type: note
---

I can help you fix your Clash DNS configuration. The issue is likely with the `fallback` URL format or your overall DNS setup. Here's a corrected configuration to use global DNS:

```yaml
dns:
  enable: true
  ipv6: false
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  nameserver:
    - 8.8.8.8
    - 1.1.1.1
  fallback:
    - 1.0.0.1
    - 8.8.4.4
```

**Key changes:**

1. **Remove the HTTPS URL in fallback** — The `fallback` section should only contain DNS servers (IP addresses or DNS-over-HTTPS URLs that Clash actually supports), not arbitrary HTTP paths. Your `192.168.0.1/dns-query` won't work as written.

2. **Use standard public DNS servers** — For global DNS, stick with proven providers like:
   - `8.8.8.8` and `8.8.4.4` (Google)
   - `1.1.1.1` and `1.0.0.1` (Cloudflare)
   - `208.67.222.222` and `208.67.220.220` (OpenDNS)

**If you want DNS-over-HTTPS (DoH)**, use this format instead:
```yaml
dns:
  enable: true
  ipv6: false
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  nameserver:
    - https://dns.google/dns-query
    - https://1.1.1.1/dns-query
  fallback:
    - 8.8.4.4
    - 1.0.0.1
```

What specific error or issue are you seeing? That would help me give you a more precise fix.