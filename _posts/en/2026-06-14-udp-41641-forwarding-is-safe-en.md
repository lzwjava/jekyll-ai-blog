---
audio: false
generated: true
image: false
lang: en
layout: post
title: UDP 41641 Forwarding Is Safe
translated: false
type: note
---

**Question:** Does forwarding UDP 41641 on the home router to the `to` machine introduce security concerns?

**Answer:**

## Short Answer: Minimal risk, well-contained

### What You're Exposing

UDP 41641 is **Tailscale's WireGuard port**. Forwarding it means the internet can send UDP packets directly to `to` on that port.

But here's why it's not dangerous:

### Why It's Safe

**WireGuard rejects unauthorized packets by design.**
WireGuard is cryptographically silent — if a packet doesn't carry a valid handshake signed with a known peer's public key, it's **dropped with no response**. No fingerprinting, no banner, no error. A port scanner sees it as closed.

```
Attacker sends UDP to <IP_ADDRESS>:41641
WireGuard: no valid key → silently drops
Attacker learns nothing
```

**Tailscale adds another layer.**
Even if someone speaks WireGuard, they'd need to be in your Tailnet (authenticated via Tailscale's coordination server). Random internet nodes can't join.

**Attack surface comparison:**

| Exposure | Risk |
| ---------- | ------ |
| SSH on public IP (port 22) | High — login brute force possible |
| HTTP/HTTPS service | Medium — app vulns exposed |
| UDP 41641 (WireGuard) | Very low — crypto-gated, silent drop |

### Residual Risks (minor)

- **DDoS / UDP flood** — your port is now a reachable target for volumetric UDP floods. Unlikely to be targeted specifically, but theoretically possible.
- **WireGuard implementation bugs** — extremely rare, but a 0-day in WireGuard's handshake parsing could theoretically be exploited. WireGuard's codebase is tiny (~4k lines) and well-audited — lowest risk of any VPN protocol.

### Verdict

Forwarding UDP 41641 is standard practice and the officially recommended Tailscale setup for reliable direct connections. The cryptographic gating makes it effectively zero-knowledge to anyone not in your Tailnet.

Much safer than, say, exposing SSH publicly.
