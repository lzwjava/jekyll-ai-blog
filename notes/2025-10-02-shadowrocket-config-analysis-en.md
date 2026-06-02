---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Shadowrocket Configuration File Analysis
translated: false
type: note
---

This appears to be a configuration file for Shadowrocket, a rule-based proxy app for iOS (similar to tools like Surge or Quantumult). It's structured as a text-based config file that defines how the app routes traffic, handles DNS, applies rules, and performs rewrites or MITM (man-in-the-middle) interception. The file is dated "2025-10-02 20:25:43," which could be a timestamp or placeholder.

I'll explain it section by section, breaking down each part, what it does, and why it might be configured this way. This config seems optimized for users in regions with internet restrictions (e.g., China), routing certain global/f blocked services through a proxy server while keeping local/domestic traffic direct for better speed and to avoid unnecessary redirection. It's not a complete setup— you'd still need to configure a proxy server (e.g., via Shadowsocks, V2Ray, etc.) separately in the app, and this config references external rule-sets that auto-update from GitHub.

### Key Assumptions and Notes
- **Proxy Setup**: This config assumes you have a working proxy server configured in Shadowrocket (e.g., SOCKS5, HTTP, or encrypted protocols). Without that, "PROXY" rules won't work.
- **Purpose**: It looks like it's for circumventing censorship (e.g., Great Firewall in China). AI services (like OpenAI/ChatGPT) are proxied, while Chinese domains/IPs go direct to avoid throttling.
- **TUN Mode**: References "tun" (tunnel mode) for routing all traffic through the device.
- **External Dependencies**: Some rules load from GitHub URLs (e.g., rule lists). Ensure you trust these sources, as they can update automatically.
- If anything's unclear or you need help applying it, let me know details about your setup.

### Section Breakdown

#### **[General]**
This sets global app behaviors, DNS resolution, and network routing. It's like the "preferences" or "system settings" for Shadowrocket.

- `bypass-system = true`: Ignore iOS's system proxy settings. Shadowrocket handles all proxying itself instead of relying on system-wide configs.

- `skip-proxy = 192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,localhost,*.local,captive.apple.com,*.ccb.com,*.abchina.com.cn,*.psbc.com,www.baidu.com`: A comma-separated list of domains/IP ranges to **always route directly** (no proxy). This includes:
  - Private networks (e.g., home Wi-Fi IPs like 192.168.x.x).
  - Local domains (*.local) and localhost.
  - Apple's captive portal check.
  - Chinese bank domains (*.ccb.com for China Construction Bank, *.abchina.com.cn for Agricultural Bank of China, *.psbc.com for Postal Savings Bank).
  - Baidu (www.baidu.com), a major Chinese search engine.
  - *Why?* Domestic Chinese sites (especially banks and search) are accessible without proxy and might be throttled or flagged if routed through one.

- `tun-excluded-routes = 10.0.0.0/8, 100.64.0.0/10, 127.0.0.0/8, 169.254.0.0/16, 172.16.0.0/12, 192.0.0.0/24, 192.0.2.0/24, 192.88.99.0/24, 192.168.0.0/16, 198.51.100.0/24, 203.0.113.0/24, 224.0.0.0/4, 255.255.255.255/32, 239.255.255.250/32`: In tunnel (TUN) mode, these IP ranges are **excluded** from the proxy tunnel. This prevents interference with local/routing traffic like loopback IPs, multicast, and test ranges.

- `dns-server = https://doh.pub/dns-query,https://dns.alidns.com/dns-query,223.5.5.5,119.29.29.29`: Prioritized list of DNS resolvers for proxy traffic. These are DoH (DNS over HTTPS) servers and plain DNS (Tencent's 119.29.29.29 and Aliyun's 223.5.5.5). It starts with encrypted/public ones (doh.pub and alidns.com) for privacy/security.

- `fallback-dns-server = system`: If the primary DNS fails, fall back to iOS's system DNS.

- `ipv6 = true`: Enable IPv6 support. `prefer-ipv6 = false`: Prefer IPv4 over IPv6 for connections (e.g., stability or compatibility).

- `dns-direct-system = false`: Don't use system DNS for direct connections—use the configured DNS instead.

- `icmp-auto-reply = true`: Automatically reply to ICMP (ping) requests. Useful for connectivity checks.

- `always-reject-url-rewrite = false`: Allow URL rewrites (used later in the config) to be triggered.

- `private-ip-answer = true`: Allow DNS responses with private IPs (e.g., your router).

- `dns-direct-fallback-proxy = true`: If a direct DNS query fails, retry via proxy.

- `tun-included-routes = `: (Empty) No custom routes included in TUN mode—use defaults.

- `always-real-ip = `: (Empty) No forced real IP exposure—standard behavior.

- `hijack-dns = 8.8.8.8:53,8.8.4.4:53`: Intercept DNS traffic from Google's public DNS (8.8.8.8/8.8.4.4 on port 53) and route it through the proxy. This forcibly uses your configured DNS instead of public ones, which might be blocked or monitored.

- `udp-policy-not-supported-behaviour = REJECT`: If UDP traffic isn't supported by a policy, reject it instead of allowing.

- `include = `: (Empty) No additional config files included.

- `update-url = `: (Empty) No automatic config updates from a URL.

#### **[Rule]**
This defines traffic routing rules, processed in order. It's like an ACL (access control list) telling Shadowrocket what to proxy, what to send direct, based on domains, keywords, GEOIP, etc. If no rule matches, it falls to `FINAL,DIRECT`.

- `DOMAIN-SUFFIX,anthropic.com,PROXY`: Route all subdomains of anthropic.com through the proxy (e.g., api.anthropic.com). Anthropic is an AI company—probably to bypass blocks.

- `DOMAIN-SUFFIX,chatgpt.com,PROXY`: Route ChatGPT domains through proxy. ChatGPT is often restricted in certain regions.

- `DOMAIN-SUFFIX,openai.com,PROXY`: Route OpenAI domains through proxy (similar reason).

- `DOMAIN-SUFFIX,googleapis.com,PROXY`: Route Google's API services through proxy (might be for accessing Google services indirectly).

- `DOMAIN-SUFFIX,zhs.futbol,DIRECT`: Route this specific domain (likely a sports site in Spanish/Chinese) directly.

- `RULE-SET,https://github.com/lzwjava/lzwjava.github.io/raw/refs/heads/main/scripts/auto-ss-config/AI.list,PROXY`: Load an external rule-set from GitHub (a list of AI-related domains) and proxy them. This auto-updates and expands the AI proxy rules.

- `RULE-SET,https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/Lan/Lan.list,DIRECT`: Load a rule-set for local network (LAN) domains and route them direct. Avoids proxying home/internal traffic.

- `DOMAIN-KEYWORD,cn,DIRECT`: Any domain containing the keyword "cn" (e.g., anything.cn) goes direct. Useful for Chinese sites.

- `GEOIP,CN,DIRECT`: Any IP geolocated to China (CN) goes direct. Prevents proxying domestic traffic, which is fast and unrestricted.

- `FINAL,DIRECT`: Default action—if no rules match, route directly. Keeps most traffic unproxied for efficiency.

*Overall Effect*: This is a "proxy for blocked globals" setup. AI/ChatGPT/OpenAI traffic is forced through VPN/proxy to bypass regional restrictions, while Chinese/local stuff stays direct.

#### **[Host]**
Manual host mappings (like a local hosts file).

- `localhost = 127.0.0.1`: Map "localhost" to the loopback IP. Standard—ensures app can connect to local services.

#### **[URL Rewrite]**
Rewrites incoming URLs before requests are made. Uses regex matching.

- `^https?://(www.)?g.cn https://www.google.com 302`: Rewrite any HTTP/HTTPS URL for g.cn (or www.g.cn) to redirect to google.com with a 302 status (temporary redirect). g.cn is Google's China domain— this bypasses it.

- `^https?://(www.)?google.cn https://www.google.com 302`: Same for google.cn to google.com. China often blocks or redirects google.com, so this forces a clean redirect.

*Why?* In censored regions, google.cn might serve altered/banned results. This ensures you hit the global Google site directly.

#### **[MITM]**
Man-in-the-middle settings for intercepting and modifying HTTPS traffic (requires a root CA certificate in Shadowrocket).

- `hostname = *.google.cn`: Intercept traffic for any subdomain of google.cn. Combined with the URL rewrite, this might decrypt/redirect traffic for Google CN domains.

*Why?* This could be to enforce the rewrites or handle certificate pinning issues in China, where google.cn uses different certs.

### How to Use This Config
1. **Import**: In Shadowrocket, import this as a config file.
2. **Proxy Server**: Add your actual proxy (e.g., Shadowsocks server) under the "Servers" section—rules like "PROXY" depend on it.
3. **Enable**: Switch to this config and enable tunnel mode (VPN) if needed.
4. **CA Cert**: For MITM, install and trust Shadowrocket's CA if not already done.
5. **Test**: Check sites like whatismyipaddress.com to see if IPs/routing work as expected. Monitor for slow Chinese sites.
6. **Troubleshooting**: If rule-sets fail to load, they might be rate-limited or changed. IPv6 prefs might need toggling for connectivity.

### Potential Issues/Security Notes
- **Privacy**: Exposed rule-sets (GitHub links) could leak what you're routing. MITM can intercept sensitive traffic—only use trusted CAs.
- **Updates**: Rule-sets auto-load; if GitHub is blocked, use a proxy for them.
- **Future Date**: The config is labeled Oct 2025—might be a typo or future-proofing, but no features depend on it.
- **Legality**: Proxying for censorship evasion is fine in some places but restricted in others—use at your own risk.
- If you share error logs or what you're trying to achieve, I can refine advice!
