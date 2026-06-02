---
audio: false
generated: true
image: false
lang: en
layout: post
title: TPROXY DNS Conflict Explained
translated: false
type: note
---

**Question:** In a Clash TPROXY setup, can we set `dns: enable: false` and use `systemd-resolved` instead?

**Answer:**

Short answer: **Technically yes, but it will break domain-based routing rules.** Here is why.

---

## Why Clash DNS Cannot Simply Be Disabled in TPROXY Mode

### The Core Problem: TPROXY Sees IPs, Not Domain Names

When iPad traffic arrives at the TPROXY port, Clash only sees raw TCP/UDP packets with **IP addresses**. It has no idea what domain name was originally requested. For example:

```
Clash sees:  192.168.201.136:54321 → 142.250.80.46:443
Clash needs: "this is google.com → route via proxy"
```

Without its own DNS intercepting the original query, Clash **cannot match domain-based rules** like:

```yaml
- DOMAIN-SUFFIX,google.com,Proxy
- DOMAIN-SUFFIX,baidu.com,DIRECT
- GEOSITE,cn,DIRECT
```

DNS queries are sent by UDP and cannot be redirected by standard iptables rules, which can produce incorrect results. This is why Clash's built-in DNS is used to replace systemd-resolved — it remembers the mapping from domain to IP, so Clash knows the domain of a redirected connection and can apply domain-related rules.

---

## What Happens in Each Scenario

### Scenario A: `dns: enable: false` + systemd-resolved

```
iPad → DNS query → systemd-resolved → returns real IP (e.g. 142.250.80.46)
iPad → connects to 142.250.80.46:443
iptables TPROXY → Clash receives packet
Clash: "What domain is this? I don't know." → can only match by IP/GEOIP
→ Domain rules like DOMAIN-SUFFIX,google.com ALL FAIL
→ Only IP-CIDR and GEOIP rules still work
```

Your proxy routing becomes very coarse — everything either goes DIRECT or PROXY with no domain-level control.

### Scenario B: `dns: enable: true` + Clash DNS (current recommended)

```
iPad → DNS query → Clash DNS (port 53) → Clash records "198.18.0.5 = google.com"
iPad → connects to 198.18.0.5:443 (real IP in redir-host mode)
iptables TPROXY → Clash receives packet
Clash: "I know 142.250.80.46 = google.com" → matches DOMAIN rules correctly
→ Full domain-based rule matching works ✅
```

---

## The Port 53 Conflict Problem

The real reason people want to disable Clash DNS is because **systemd-resolved already occupies port 53**, causing Clash to fail to start. You may have to kill systemd-resolved and any other processes occupying UDP port 53 before Clash's DNS module can work.

The correct fix is **not** to disable Clash DNS, but to free up port 53:

```bash
# Stop systemd-resolved from occupying port 53
sudo systemctl stop systemd-resolved
sudo systemctl disable systemd-resolved

# Point resolv.conf to Clash directly
sudo rm /etc/resolv.conf
echo "nameserver 127.0.0.1" | sudo tee /etc/resolv.conf

# Now Clash can listen on 0.0.0.0:53
```

Or, the more elegant approach — make Clash listen on `127.0.0.53:53` (the exact address systemd-resolved uses), then point systemd-resolved upstream to Clash:

```yaml
# Clash config: listen on systemd-resolved's stub address
dns:
  enable: true
  listen: 127.0.0.53:53     # takes over systemd-resolved's slot
  enhanced-mode: redir-host
  nameserver:
    - 223.5.5.5
    - 119.29.29.29
```

After configuring Clash to listen on `127.0.0.53:53`, use dnsmasq as a DNS cache layer with `server=127.0.0.53` pointing to Clash, and set `/etc/resolv.conf` to use dnsmasq as the local resolver.

---

## Decision Tree: When Can You Disable Clash DNS?

| Your Rules | Can Disable Clash DNS? |
|---|---|
| Only `IP-CIDR` and `GEOIP` rules | ✅ Yes, works fine |
| `DOMAIN-SUFFIX`, `DOMAIN-KEYWORD` rules | ❌ No, domain matching breaks |
| `GEOSITE` rules (e.g. `cn` sites DIRECT) | ❌ No, GEOSITE needs domain data |
| `MATCH` catchall only | ✅ Yes (everything goes one proxy) |

For your use case (Chinese sites DIRECT, everything else via Hysteria2), you **must keep Clash DNS enabled** because you rely on domain-based routing decisions.

---

## Recommended Setup (Avoid Port Conflict Cleanly)

```bash
# 1. Disable systemd-resolved stub listener (but keep the service)
sudo mkdir -p /etc/systemd/resolved.conf.d/
sudo tee /etc/systemd/resolved.conf.d/no-stub.conf << EOF
[Resolve]
DNSStubListener=no
EOF
sudo systemctl restart systemd-resolved

# 2. Now Clash can freely take port 53
# In Clash config:
# dns:
#   enable: true
#   listen: 0.0.0.0:53
```

This keeps systemd-resolved running (for laptop's own name resolution) but lets Clash own port 53 for the iPad-facing interface.

References:

- [Setup Clash TPROXY on Linux Router - DEV Community](https://dev.to/jysperm/setup-clash-redir-proxy-on-a-linux-router-4jnh)
- [Clash as TPROXY Gateway - GitHub Gist](https://gist.github.com/phlinhng/38a141862de775b10c613f7f2c6ade99)
- [systemd-resolved - ArchWiki](https://wiki.archlinux.org/title/Systemd-resolved)
