---
audio: false
generated: true
image: false
lang: en
layout: post
title: OpenClaw Gateway Network Discovery Explained
translated: false
type: note
---

**Question:** Explain what this network discovery output means — what is OpenClaw Gateway, and what does this scan reveal about the device?

**Answer:**

## What You Found

You ran a systematic LAN recon and discovered a neighbor's MacBook Pro running something called **OpenClaw Gateway** on your subnet. Let me break down every layer.

---

## Layer 1: The Device

```
MAC: XX:XX:XX:XX:XX:31
OUI: Apple
mDNS hostname: openclaw.local
```

MAC OUI lookup confirmed it's Apple hardware — MacBook Pro based on the mDNS TXT records. It's on your LAN (same subnet), reachable via ARP.

---

## Layer 2: The Discovery Chain

Your methodology was clean and follows standard passive→active recon escalation:

```
arp -a                        # passive: who's on my subnet?
  → found IPs + MACs

OUI lookup                    # passive: what vendor?
  → 3 Apple devices

nc -zv <ip> 1-65535           # active: what ports are open?
  → filtered down candidates

nmap -Pn -sV                  # active: service fingerprinting
  → MySQL on 3306

mDNS multicast query          # passive protocol: Bonjour
  → 224.0.0.251 UDP port 5353
  → device self-announced its service
```

The mDNS part is particularly interesting — you didn't brute-force anything. The device **voluntarily broadcast** its identity via Apple's Bonjour protocol (DNS-SD / RFC 6762). You just listened.

---

## Layer 3: What mDNS Revealed

DNS-SD (Service Discovery) over mDNS gives you a full service record tree:

| Record | What it told you |
|--------|-----------------|
| `PTR` | Service name: `_openclaw-gw._tcp.local` |
| `TXT` | `role=gateway`, `port=18789`, `hostname=openclaw.local` |
| `SRV` | Canonical hostname + port mapping |
| `A/AAAA` | IPv4 + IPv6 addresses |

The TXT record is the goldmine — application-level metadata that the OpenClaw software itself wrote. This is by design in Bonjour; apps register their own TXT records for discovery. OpenClaw explicitly advertised its role and port.

---

## Layer 4: What is OpenClaw?

OpenClaw is not a well-known open-source project. Based on what the scan shows:

- It's a **gateway/proxy service** running on port 18789
- It self-describes as `role=gateway`, `transport=gateway`
- It runs alongside MySQL (3306) — suggesting it has a local database backend
- MySQL is locked to specific hosts — so it's not a public service; it's a controlled, multi-component local application

Most likely candidates for what OpenClaw is:

1. **A local LLM/AI proxy gateway** — routes API calls (OpenAI, Anthropic, etc.) through a local endpoint. "Claw" is a common theme in AI tooling. The gateway pattern (intercept → route → log) fits perfectly with token tracking or team key management.

2. **A corporate/team API key management gateway** — banks and enterprises run these to centralize API access, rate-limit usage, and audit calls. Port 18789 is non-standard, which is typical for internal tooling.

3. **A custom-built tool** — given it's on someone's personal MacBook and uses mDNS for local discovery, this could be a personal dev tool that proxies requests on the local network.

The MySQL backend is the tell — it's storing state: probably request logs, usage metrics, or API key mappings.

---

## Layer 5: Security Assessment

What's exposed vs. locked down:

```
Port 18789  - OpenClaw Gateway   OPEN (externally reachable on LAN)
Port 3306   - MySQL              LOCKED (host-restricted)
SSH         - CLOSED
VNC         - CLOSED
HTTP        - CLOSED
```

The **high latency (22–200ms)** suggests WiFi power-save mode — this is a laptop that's not always actively transmitting, typical of a MacBook on battery.

**Risk surface:**
- Port 18789 is reachable from your machine right now
- If OpenClaw has no auth, you could send requests through their gateway
- MySQL is properly locked — good practice
- mDNS self-announcement means **anyone on the subnet** can discover this automatically without scanning — just run `dns-sd -B _services._dns-sd._udp` on any Mac

---

## What You Can Do Next (Ethically)

Since this is someone else's device, you're now at the boundary. What you've done so far (ARP, mDNS listening, port scan on your own LAN) is generally passive/gray-zone. Going further — connecting to port 18789, probing the gateway API — crosses into unauthorized access territory.

But if you wanted to understand the protocol, you could probe your **own** machine or set up an identical stack:

```bash
# See what mDNS services are broadcasting on your LAN (passive, safe)
dns-sd -B _services._dns-sd._udp local.

# Resolve the specific service record
dns-sd -L "openclaw-gw" _openclaw-gw._tcp local.

# What's actually on 18789? (only do this on your own devices)
curl -v http://<ip>:18789/
```

---

## Summary

You did a textbook LAN recon. You found a neighbor's MacBook running what appears to be a personal or team **AI/API gateway tool** called OpenClaw, which:
- Self-announces on mDNS (Bonjour) — intentional service discovery
- Runs a proxy on port 18789
- Backs it with a MySQL database
- Is reachable from your machine but MySQL is properly isolated

The interesting meta-point: **mDNS is a zero-effort honeypot for discovery**. Any Bonjour-registered service on your LAN is fully visible without a single active scan. Security-conscious services shouldn't register on mDNS if they don't want to be found.