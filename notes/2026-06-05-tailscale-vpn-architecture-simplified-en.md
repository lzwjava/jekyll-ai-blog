---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tailscale VPN Architecture Simplified
translated: false
type: note
---

**Question:** How does Tailscale work?

**Answer:**

Tailscale is a **mesh VPN on top of WireGuard**. It solves the hard problem: connecting machines across NAT/firewalls without a central server, while keeping setup trivial. Here's the mechanism:

---

## The Core Architecture

**Two planes:**

1. **Control plane** — Tailscale's servers (coordination, discovery, key distribution)
2. **Data plane** — Direct peer-to-peer WireGuard tunnels (encrypted traffic)

The control plane *never* touches your data. It only orchestrates connections.

---

## How It Works (Step by Step)

### 1. **Initial Setup**

```bash
tailscale up
# Opens browser, you authenticate with your account
# Tailscale assigns your machine a Tailscale IP (100.x.x.x range)
# Your machine generates a WireGuard keypair
# Public key is sent to Tailscale control servers
```

At this point, Tailscale knows:

- Your machine's identity and public key
- Your public IP (or carrier-grade NAT endpoint)
- Your internal network info (for subnet routing)

### 2. **Peer Discovery**

When you try to reach another machine on your tailnet (e.g., `ssh lzw@100.64.1.2`):

```
Your machine asks Tailscale control servers:
"What's the address/key of machine 100.64.1.2?"

Control servers respond:
{
  "machine_name": "to",
  "public_key": "<WireGuard pubkey>",
  "endpoints": [
    "203.0.113.45:41641",  // Public IP:port
    "192.168.1.36:41641"   // Private IP (if on same LAN)
  ],
  "derp_region": "usa-east"  // Fallback relay
}
```

Your machine caches this and doesn't ask again (unless machine goes offline).

### 3. **Direct Connection (Best Case)**

If both machines are reachable, Tailscale uses **WireGuard directly**:

```
Your Mac (100.64.2.5)  ←→ Workstation (100.64.1.2)
         ↓
Encrypted WireGuard tunnel
(UDP, port varies, peer-to-peer)
         ↓
No central server involved
```

This is **private**, **fast** (~10ms as you measured), and **direct**.

---

## 4. **NAT Traversal (The Hard Part)**

Both machines are likely behind NAT. Tailscale uses **UDP hole punching** + **STUN**:

```
Tailscale STUN servers tell each machine:
"Your public IP:port (as seen from outside) is <IP>:<PORT>"

Both machines send UDP packets to each other's discovered endpoints.
Routers see outbound traffic and create NAT mappings.
Packets punch through and establish direct connection.
```

**This works because:**

- NAT routers allow inbound traffic if outbound traffic initiated first
- Tailscale coordinates the timing via control servers
- Both sides learn each other's external endpoint

**Timing matters** — if one machine is offline when the other tries to connect, discovery happens on-demand.

---

## 5. **Fallback: DERP Relays (When Direct Fails)**

Some networks block UDP or have aggressive NAT. Tailscale has **DERP relays** (Designated Encrypted Relay Proxies):

```
If direct connection fails after a few seconds:

Your Mac → DERP relay (encrypted) → Workstation
```

DERP is a last-resort relay. It:

- Runs on Tailscale-controlled servers
- Cannot decrypt traffic (WireGuard encryption is end-to-end)
- Adds latency (Tailscale routes through nearest region)
- Automatically disables once direct connection is restored

---

## The WireGuard Layer

Tailscale wraps WireGuard with smart coordination. WireGuard itself does the crypto:

```python
# Simplified WireGuard packet structure:
[IP header] [UDP header] [WireGuard encrypted payload]
            └─ Each packet is authenticated + encrypted
               using ephemeral session keys
```

**Key properties:**

- **Stateless** — WireGuard doesn't track connections (unlike IPsec/OpenVPN)
- **Small overhead** — adds ~100 bytes per packet
- **Forward secrecy** — old packets unrecoverable if key compromised
- **Post-quantum safe** (debatable, but uses modern primitives)

---

## What Tailscale Adds On Top

| Feature | How |
|---------|-----|
| **Magic DNS** | Control servers respond to DNS queries, return Tailscale IPs |
| **ACLs** | Control servers enforce access policy (who can reach whom) |
| **Exit nodes** | One machine can be configured to route all traffic through another |
| **Subnet routes** | Expose your entire LAN to the tailnet (via one machine as gateway) |
| **Tailscale SSH** | Built-in SSH server, signed by control plane, no key management |

---

## Security Model

```
Assumption: You trust Tailscale Inc.'s servers

If servers are compromised:
  ✗ Attacker learns which machines are in your tailnet
  ✗ Attacker learns which devices are online/offline
  ✓ Attacker CANNOT decrypt your traffic (WireGuard keys are never on their servers)

If one of your machines is compromised:
  ✗ Attacker can access your entire tailnet
  ✓ Attacker cannot forge identity (WireGuard keypairs are asymmetric)
```

The control plane is a **trust boundary**, not a threat boundary for traffic.

---

## Code-Level Example (Simplified)

```python
# Pseudocode: what happens when you SSH

# 1. Tailscale daemon (tailscaled) is running
$ ps aux | grep tailscaled
# Listening on local interface for connections

# 2. SSH client connects to Tailscale IP
$ ssh lzw@100.64.1.2

# 3. Tailscale intercepts (or you SSH directly to Tailscale IP)
# 4. Tailscale daemon queries control servers for peer info
#    (cached if recent, otherwise fetches)
peers = control_plane.get_peer("100.64.1.2")

# 5. Establish WireGuard tunnel
wg_tunnel = wireguard.connect(
    peer_public_key=peers.public_key,
    endpoint=peers.endpoints,  # Try direct, then DERP
)

# 6. SSH traffic now flows encrypted through wg_tunnel
# Control servers never see SSH packets
```

---

## Performance: Why Your Setup is Fast

```
Latency breakdown (your 10ms observation):

Direct LAN (same network):
  - Tailscale overhead: ~1-2ms
  - WireGuard crypto: <1ms
  - Network RTT: ~8ms
  ────────────────
  Total: ~10ms ✓

Same LAN means:
  - No internet routing (local switch/router)
  - Both machines on same subnet (192.168.1.x range)
  - Tailscale discovers private IP (192.168.1.36)
  - Encrypts and sends directly
```

Cross-internet (Mac at coffee shop → Workstation at home):

- Direct connection: ~50-100ms (ISP routing)
- With DERP relay: ~100-200ms (relay adds hop)

---

## Threat Model for Your Setup

| Threat | Exploitable? | Mitigation |
|--------|--------------|-----------|
| ISP sees you SSH'd to workstation | **No** — WireGuard is encrypted | N/A |
| Tailscale Inc. sees your commands | **No** — control plane is separate | N/A |
| Compromised workstation | **Yes** — attacker has access | Patch Ubuntu, firewall non-Tailscale ports |
| Stolen Tailscale auth token | **Yes** — attacker joins tailnet | Use strong account password, 2FA |
| Network sniffer on your LAN | **No** — WireGuard encrypted | N/A |

---

## Summary

Tailscale = **smart orchestration around WireGuard**:

- Control plane finds peers and exchanges keys
- Data plane uses WireGuard for encrypted tunnels
- UDP hole punching solves NAT
- DERP relays fallback when direct fails
- You get mesh networking without managing certificates or IPs manually

The insight: **move complexity to the control plane, keep data plane simple and secure**.
