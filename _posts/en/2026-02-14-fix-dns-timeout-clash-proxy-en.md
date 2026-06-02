---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fix DNS Timeout via Clash Proxy
translated: false
type: note
---

**Question: Without exporting proxy environment variables, the Python script times out when querying Cloudflare DoH (https://1.1.1.1/dns-query). How to find a proper DNS server in China, or can we route DNS requests through the Clash proxy?**

**Answer:**

Your test shows the classic problem in mainland China: direct access to foreign DoH servers like `https://1.1.1.1/dns-query` often fails or times out because of **GFW-level blocking** on the DoH endpoint (TLS handshake or SNI filtering), even when plain UDP DNS to 1.1.1.1 might partially work.

When you set `HTTP_PROXY`/`HTTPS_PROXY` to Clash (127.0.0.1:7890), the `requests` library automatically tunnels the DoH HTTPS request through your proxy → it succeeds because the proxy node bypasses the block.

When you unset the proxies (`stop_proxy`), Clash no longer handles the outgoing HTTPS connection → direct connection from your machine times out.

### Solution 1: Route Clash's own DNS queries (DoH/DoT) through a proxy (recommended)

Clash (especially Meta/Mihomo core) supports sending its upstream DNS queries (nameserver / fallback) **through a specific proxy** or group. This is perfect for your case.

Update your Clash config like this:

```yaml
dns:
  enable: true
  ipv6: false
  enhanced-mode: fake-ip          # or redir-host
  fake-ip-range: 198.18.0.1/16
  listen: 0.0.0.0:53              # optional, for TUN/system-wide

  # Fast domestic DNS for resolving proxy node domains + bootstrap
  default-nameserver:
    - 119.29.29.29                # DNSPod
    - 223.5.5.5                   # AliDNS

  # Primary DoH – force through your proxy group
  nameserver:
    - https://1.1.1.1/dns-query#PROXY     # ← #PROXY means use the group named "PROXY"
    - https://1.0.0.1/dns-query#PROXY

  # Fallback for polluted results
  fallback:
    - https://cloudflare-dns.com/dns-query#PROXY
    - tls://1.1.1.1#PROXY                 # DoT alternative

  # Optional: only fallback for non-CN sites
  fallback-filter:
    geoip: true
    ipcidr:
      - 240.0.0.0/4

  # Prevent chicken-egg: resolve proxy node domains directly
  proxy-server-nameserver:
    - 119.29.29.29
    - 223.5.5.5
```

- Assume you have a proxy-group named `"PROXY"` (or change to your actual group name, e.g. `🐟 漏网之鱼`).
- `#PROXY` syntax tells Clash to route **that specific DoH connection** through the named proxy/group instead of direct.
- After reload/restart Clash → your Python script should work **even without** `HTTP_PROXY` env vars, because Clash's built-in DNS (if you use it) or your script (if tunneled) benefits indirectly.

If your core is older Clash (not Meta), the `#proxyname` syntax may not be supported → upgrade to Clash Meta / Mihomo / Clash Verge Rev.

### Solution 2: Use domestic / China-optimized DoH / DoT servers (no proxy needed for DNS)

Many work reliably in China without proxy:

- `https://doh.pub/dns-query` (very popular, fast, DoH)
- `https://dns.alidns.com/dns-query` (AliDNS DoH)
- `https://doh.360.cn/dns-query` (360 DoH)
- `tls://223.5.5.5:853` (AliDNS DoT)
- `tls://223.6.6.6:853` (AliDNS secondary DoT)

Example minimal config:

```yaml
dns:
  enable: true
  nameserver:
    - https://doh.pub/dns-query
    - https://dns.alidns.com/dns-query
  fallback:
    - tls://223.5.5.5:853
```

These are usually unblocked, fast for domestic + international resolution (though may have some pollution on sensitive domains → use fallback-filter).

### Solution 3: Keep using env vars for your script (simple, no config change)

Just always run your DNS test script with proxies enabled:

```bash
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
python ./scripts/clash/try_dns.py
```

Or wrap it in your `start_proxy` alias/script.

### Quick test commands (terminal)

- Test DoH through Clash proxy: `curl -x http://127.0.0.1:7890 -H "accept: application/dns-json" "https://1.1.1.1/dns-query?name=www.google.com&type=A"`
- Test direct (should timeout/fail): `curl -H "accept: application/dns-json" "https://1.1.1.1/dns-query?name=www.google.com&type=A"`

This confirms the block is on direct outbound HTTPS to Cloudflare DoH.

Use the `#PROXY` method for cleanest long-term fix.

**References:**

- [MetaCubeX mihomo DNS Configuration (nameserver #proxy support)](https://wiki.metacubex.one/en/config/dns)
- [Clash DNS upstream through proxy discussion](https://github.com/MetaCubeX/mihomo/discussions/1434)
- [Common Clash DNS setups for China](https://github.com/Loyalsoldier/clash-rules)
