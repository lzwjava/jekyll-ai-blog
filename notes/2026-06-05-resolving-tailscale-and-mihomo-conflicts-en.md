---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resolving Tailscale and Mihomo Conflicts
translated: false
type: note
---

**Question:** Will Tailscale have conflicts with mihomo + hysteria2 + DMIT when used in China?

**Answer:**

Yes, there can be conflicts, but they're **manageable with proper configuration**. Here's what happens:

---

## The Conflicts

### 1. **Virtual Network Interface Conflict**
Both Tailscale and mihomo create virtual network interfaces:
- **Tailscale:** Creates `utun0` (macOS) or `tun0` (Linux) for kernel-mode networking
- **Mihomo:** Creates virtual interfaces for traffic interception (iptables on Linux, pf on macOS)

**Result:** Routing policy conflicts, packet loops, or dropped traffic.

### 2. **DNS Conflict**
Mihomo has recently fixed DNS resolution for Tailscale (commit: "use our internal DNS resolution logic for tailscale"), but:
- Both try to rewrite DNS queries
- Tailscale's MagicDNS (if enabled) conflicts with mihomo's DNS interception
- Conflicting nameserver configs

### 3. **IP Address Range Conflict**
If the other VPN uses IP addresses from the CGNAT range (100.64.0.0–100.127.255.255) that Tailscale uses, they will conflict with Tailscale's 100.x.y.z addresses.

### 4. **Traffic Routing Loop**
Mihomo tries to hijack `100.x.x.x` traffic (Tailscale IPs) but doesn't know how to route it → packets loop or drop.

---

## How to Resolve (3 Approaches)

### **Option 1: Tailscale in Userspace Mode (Recommended for China)**

Use Tailscale's userspace networking mode instead to work around conflicts with Tailscale IP addresses. Tailscale then exposes a SOCKS5 proxy on localhost (127.0.0.1) to let you connect out to your Tailscale network.

```bash
# Enable userspace networking
tailscale up --tun=userspace
```

Then configure mihomo to proxy Tailscale traffic through the local SOCKS5 port:

```yaml
# mihomo config.yaml
port: 7890
socks-port: 7891
mixed-port: 7893
allow-lan: true

proxy-groups:
  - name: "tailscale-proxy"
    type: socks5
    server: 127.0.0.1
    port: 1099  # Tailscale userspace SOCKS5 port

rules:
  # Route 100.x.x.x traffic through Tailscale SOCKS5
  - IP-CIDR,100.64.0.0/10,tailscale-proxy
  - RULE-SET,tailscale,tailscale-proxy
```

**Benefit:** Tailscale and mihomo don't fight for kernel-level networking. Hysteria2 flows through mihomo normally.

---

### **Option 2: Hybrid Mode (Tunnel Order)**

Chain them explicitly (for China use case):

```
System traffic → Mihomo (hysteria2 + DMIT) → If 100.x.x.x → Tailscale userspace SOCKS5 → actual destination
```

macOS `~/.config/mihomo/config.yaml`:

```yaml
proxies:
  - name: "hysteria2-dmit"
    type: hysteria2
    server: <dmit-server-ip>
    port: <port>
    auth_str: <password>
    obfs: salamander
    skip-cert-verify: true

proxy-groups:
  - name: "default"
    type: select
    proxies:
      - hysteria2-dmit
      - DIRECT

  - name: "tailscale"
    type: socks5
    server: 127.0.0.1
    port: 1099

rules:
  # Tailscale IPs go through Tailscale's SOCKS5
  - IP-CIDR,100.64.0.0/10,tailscale
  # Everything else goes through hysteria2
  - MATCH,default
```

---

### **Option 3: Split Tunnel (Linux only)**

If on Ubuntu workstation with kernel mode, use iptables to exempt Tailscale from mihomo:

```bash
# Let Tailscale traffic bypass mihomo
iptables -t mangle -I INPUT -i tailscale0 -j RETURN
iptables -t mangle -I OUTPUT -o tailscale0 -j RETURN
```

Then mihomo only intercepts non-Tailscale traffic.

---

## China-Specific Considerations

**Tailscale in China:**
- Users suggest using Hysteria2 as the primary tunnel for GFW bypass, since it's specifically designed to evade Chinese firewall detection.
- Tailscale + WireGuard are not explicitly blocked but may be deprioritized by QoS.
- **Better approach:** Use hysteria2 (primary) → access Tailscale mesh inside the tunnel

**Recommended setup for China:**

```
Machine → Mihomo (hysteria2 to DMIT server) → Inside tunnel: access Tailscale mesh
```

This way:
1. **Hysteria2 handles GFW evasion** (your primary concern)
2. **Tailscale runs inside** the hysteria2 tunnel (no conflicts)
3. **Fallback:** If P2P Tailscale breaks, hysteria2 relay works

---

## Actual Integration Status

Mihomo has explicit fixes for Tailscale compatibility (commits: "fix netlink permission denied on android for tailscale" and "use our internal DNS resolution logic for tailscale"), so the maintainers are aware of and addressing conflicts.

On Android with userspace mode, users use mihomo to route Tailscale's 100.x.x.x traffic to local proxy on port 1099.

---

## Bottom Line

| Setup | Conflicts? | Best For |
|-------|-----------|----------|
| Mihomo (hysteria2) + Tailscale kernel mode | **High** | Don't combine |
| Mihomo (hysteria2) + Tailscale userspace | **None** | China use case ✓ |
| Hysteria2 tunnel → Tailscale inside | **None** | Maximum reliability |

**For your China setup:** Use Option 1 (Tailscale userspace) or tunnel hysteria2 first, then Tailscale inside. Avoid kernel-mode conflicts entirely.

---

**References:**

- [Tailscale: Using alongside other VPNs](https://tailscale.com/docs/reference/faq/other-vpns)
- [Mihomo Tailscale fixes](https://github.com/MetaCubeX/mihomo/releases)
- [Tailscale + Clash integration guide](https://blog.l3zc.com/en/2025/04/tailscale-setup-recap/)
