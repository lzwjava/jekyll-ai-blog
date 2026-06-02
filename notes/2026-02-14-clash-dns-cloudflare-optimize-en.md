---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Optimize Clash DNS With Cloudflare
translated: false
type: note
---

Question: How about changing to Cloudflare DNS servers in the Clash configuration, like using nameserver 8.8.8.8 and 1.1.1.1 with fallback <https://1.1.1.1/dns-query>?

Answer:

Yes, switching to **Cloudflare DNS** (1.1.1.1) is a very good and popular choice in Clash configurations — especially when you want fast, privacy-focused, and leak-resistant DNS resolution. Your proposed snippet is already quite solid, but let’s improve and explain it properly for best results in 2026.

### Recommended Cloudflare DNS setup for Clash (2026 best practice)

Replace or add the `dns:` section in your config like this:

```yaml
dns:
  enable: true
  ipv6: false                     # disable unless your proxy node supports IPv6 well
  listen: 0.0.0.0:53              # optional: let Clash act as local DNS server (useful with TUN)
  enhanced-mode: fake-ip          # or redir-host — fake-ip is usually better for privacy & speed
  fake-ip-range: 198.18.0.1/16    # standard fake-ip CIDR
  use-hosts: true                 # respect /etc/hosts if needed

  nameserver:                     # primary resolvers (fast DoH/DoT preferred)
    - https://1.1.1.1/dns-query   # Cloudflare DoH (encrypted, recommended)
    - https://1.0.0.1/dns-query   # Cloudflare secondary DoH
    # - tls://1.1.1.1               # DoT alternative (if you prefer)

  fallback:                       # fallback when primary fails or for polluted results
    - https://cloudflare-dns.com/dns-query   # same as 1.1.1.1 but different domain
    - https://1.1.1.1/dns-query              # you can keep this
    - tls://1.0.0.1                          # optional DoT fallback

  fallback-filter:
    geoip: true                   # only use fallback for non-CN IPs (prevents leakage)
    ipcidr:
      - 240.0.0.0/4               # discard bogus private/reserved ranges
    domain:
      - +.google.com
      - +.facebook.com
      - +.twitter.com
      # add more domains that are often polluted in your region
```

### Why this is better than plain 8.8.8.8 + 1.1.1.1

| Setting                  | Your Proposal                          | Recommended (above)                          | Why better?                                                                 |
|--------------------------|----------------------------------------|----------------------------------------------|-----------------------------------------------------------------------------|
| `nameserver`             | 8.8.8.8, 1.1.1.1 (plain DNS)           | DoH: <https://1.1.1.1/dns-query>               | Encrypted → prevents ISP/government from seeing or tampering with DNS queries |
| `fallback`               | <https://1.1.1.1/dns-query>              | Multiple DoH + DoT                           | Redundancy + avoids single-point failure or temporary blocks                   |
| `enhanced-mode`          | not set                                | fake-ip                                      | Hides real destination IPs from apps, reduces DNS pollution/leak risk         |
| `fallback-filter`        | not set                                | geoip + domain rules                         | Smart fallback: only use foreign DNS for foreign sites, direct for local/CN   |

### Quick comparison: Cloudflare vs Google DNS in Clash

- **Cloudflare (1.1.1.1)**: Faster in many Asia-Pacific regions, strong privacy focus, supports encrypted DoH/DoT, family-safe variants (1.1.1.2/1.1.1.3) if needed.
- **Google (8.8.8.8)**: Very reliable, huge cache, but Google logs more metadata (even if anonymized), sometimes slower in China-adjacent regions.
- **Best combo in 2026**: Use Cloudflare DoH as primary, keep Google as backup if you want.

### Minimal change (if you want to keep it simple)

If you just want to swap quickly without fake-ip or advanced filtering:

```yaml
dns:
  enable: true
  ipv6: false
  nameserver:
    - https://1.1.1.1/dns-query
    - https://1.0.0.1/dns-query
  fallback:
    - https://cloudflare-dns.com/dns-query
```

### Final tips

- After changing DNS settings → restart Clash completely.
- Test for leaks: Visit <https://ipleak.net> or <https://dnsleaktest.com> in browser (should show only 1.1.1.1 or your proxy IP).
- If using **TUN mode**, make sure `dns-hijack: [any:53]` is also enabled — it forces all system DNS through Clash.
- If you see slow resolution or failures → try removing 8.8.8.8 entirely and stick to DoH only.

This setup gives you fast, encrypted, and leak-resistant DNS — much better than plain UDP DNS servers in most proxy/VPN scenarios.

References:

- [Clash DNS Configuration Guide](https://github.com/MetaCubeX/mihomo/wiki/DNS)
- [Cloudflare 1.1.1.1 DoH/DoT Endpoints](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/)
- [Recommended Clash DNS Setup (Loyalsoldier)](https://github.com/Loyalsoldier/clash-rules)
