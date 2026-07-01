---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Domestic DNS Skips Fake IP
translated: false
type: note
---

Question: Why in this case (using domestic DoH/DoT servers like doh.pub and AliDNS) do we not need to configure enhanced-mode: fake-ip and fake-ip-range?

Answer:

You **do not strictly need** `enhanced-mode: fake-ip` (and its `fake-ip-range`) when using **purely domestic / China-based DNS servers** like:

- `https://doh.pub/dns-query`
- `https://dns.alidns.com/dns-query`
- `tls://223.5.5.5:853` (AliDNS DoT)

because these servers usually do **not suffer from serious DNS pollution / poisoning** for the domains most users care about in this setup.

### Why fake-ip is normally recommended (and why it's often not needed here)

| Situation | DNS Pollution / Hijacking Risk | Need fake-ip? | Reason |
| ------------------------------------ | -------------------------------- | --------------- | -------- |
| Using foreign DoH/DoT (1.1.1.1, 8.8.8.8, etc.) directly | High (especially for Google, Twitter, YouTube, OpenAI, etc.) | Strongly recommended | Fake-ip prevents local ISP/GFW from seeing real query and returning fake/wrong IPs |
| Using domestic DoH/DoT (doh.pub, AliDNS, 360, etc.) | Low to medium (mostly only poisons very sensitive foreign domains) | Usually **not required** | These resolvers are operated inside China → they return mostly clean results for domestic sites and reasonably accurate results for international sites (or at least no wild fake IPs) |
| You are in TUN mode + want maximum privacy / anti-leak | Always useful | Recommended anyway | Fake-ip hides real destination IPs from apps and kernel |
| You only care about basic connectivity + speed | Low priority | Can skip | Domestic DoH is fast and rarely completely broken |

### In your specific case (the config you showed)

```yaml
dns:
  enable: true
  nameserver:
    - https://doh.pub/dns-query
    - https://dns.alidns.com/dns-query
  fallback:
    - tls://223.5.5.5:853
```

- All listed servers are **domestic** → low chance of severe poisoning on common proxy/test domains.
- doh.pub in particular is known to be quite clean for international resolution (many Clash users in China use it as primary).
- AliDNS (223.5.5.5) is generally reliable and fast inside China.
- No foreign upstream DNS is used → no need to hide queries from GFW via fake-ip trick.

So in this configuration:

- DNS resolution is already reasonably trustworthy.
- You avoid the small overhead / complexity of fake-ip mode.
- Most apps get correct IPs → proxy works fine.
- You can still browse, use ChatGPT via proxy, etc., without obvious DNS-related breakage.

### When you **should** still add fake-ip even with domestic DNS

Add it back if you notice any of these symptoms:

- Certain foreign domains resolve to wrong / Chinese IPs (e.g. google.com → some random mainland server)
- You frequently visit very sensitive / heavily censored domains
- You are paranoid about DNS leaks or want maximum isolation
- You combine with TUN mode and want apps to never see real destination IPs

In that case, just add:

```yaml
dns:
  enable: true
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  nameserver:
    - https://doh.pub/dns-query
    - https://dns.alidns.com/dns-query
  fallback:
    - tls://223.5.5.5:853
```

Most Clash Verge / Mihomo users in China run **without fake-ip** when they stick to domestic DoH/DoT — and it works perfectly fine for daily proxy use.

Bottom line:
In this exact config → **you can safely skip fake-ip** for simplicity and speed.
If you later switch back to Cloudflare/Google DoH or notice any weird resolution → add fake-ip then.

References:

- [MetaCubeX mihomo DNS enhanced-mode explanation](https://wiki.metacubex.one/en/config/dns)
- [Clash fake-ip vs redir-host discussion (Chinese community)](https://github.com/MetaCubeX/mihomo/discussions/456)
- [Common China Clash DNS setups without fake-ip](https://github.com/Loyalsoldier/clash-rules)
