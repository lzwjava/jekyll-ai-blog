---
audio: false
generated: true
image: false
lang: en
layout: post
title: IPsec Tunnel Mode Explained
translated: false
type: note
---

**Question:** What is IPsec, and how does tunnel mode work?

---

**Answer:**

## What is IPsec?

**IPsec (Internet Protocol Security)** is a suite of protocols designed to secure IP communications by authenticating and encrypting each IP packet in a data stream. It operates at the **network layer (Layer 3)** of the OSI model, making it transparent to applications.

IPsec provides three core security services:

- **Confidentiality** — encrypts data so it can't be read in transit
- **Integrity** — ensures data hasn't been tampered with (via HMAC)
- **Authentication** — verifies the identity of communicating parties

---

## IPsec Core Protocols

| Protocol | Full Name | Purpose |
|---|---|---|
| **AH** | Authentication Header | Integrity + authentication (no encryption) |
| **ESP** | Encapsulating Security Payload | Encryption + integrity + authentication |
| **IKE** | Internet Key Exchange | Negotiates keys and security associations |

In practice, **ESP** is used almost universally because it provides both encryption and authentication.

---

## Two IPsec Modes

IPsec operates in two modes:

### 1. Transport Mode
- Only the **payload** (data) of the original IP packet is encrypted/authenticated.
- The original IP header is **preserved**.
- Used typically for **host-to-host** communication.

```
[ Original IP Header | ESP Header | Payload | ESP Trailer ]
  ← not encrypted →   ←——— encrypted ———————→
```

### 2. Tunnel Mode ← **(your focus)**
- The **entire original IP packet** (header + payload) is encrypted and encapsulated inside a **new IP packet** with a new outer header.
- The inner packet is completely hidden from the network.
- Used for **gateway-to-gateway** (site-to-site VPN) or **host-to-gateway** (remote access VPN).

```
[ New IP Header | ESP Header | Original IP Header + Payload | ESP Trailer ]
  ← visible →              ←————————— encrypted ————————————→
```

---

## Tunnel Mode — How It Works

```
Host A (10.0.1.5)                                         Host B (10.0.2.8)
     |                                                          |
     |── Original Packet ──▶ Gateway A ──── Internet ──── Gateway B ──▶|
                              (1.2.3.4)  [Encrypted Tunnel]  (5.6.7.8)
```

**Step-by-step:**

1. Host A sends a normal packet to Host B (`src: 10.0.1.5`, `dst: 10.0.2.8`).
2. **Gateway A** intercepts it, encrypts the entire original packet using ESP, and wraps it in a new IP packet (`src: 1.2.3.4`, `dst: 5.6.7.8`).
3. The encapsulated packet travels across the internet — intermediate routers only see the outer header.
4. **Gateway B** receives it, strips the outer header, decrypts the inner packet, and forwards the original packet to Host B.

---

## Key Advantages of Tunnel Mode

| Feature | Benefit |
|---|---|
| **Hides inner IP addresses** | Private addressing is invisible to the internet |
| **Protects full packet** | Even routing info is encrypted |
| **Ideal for VPNs** | Standard for site-to-site and remote access VPNs |
| **Works across NAT** | Easier with NAT-Traversal (NAT-T, UDP port 4500) |

---

## IKE — Setting Up the Tunnel

Before any data flows, **IKE (Internet Key Exchange)** negotiates a **Security Association (SA)** — a set of agreed-upon algorithms and keys:

- **Phase 1 (IKE SA):** Establishes a secure, authenticated channel between peers (uses Diffie-Hellman).
- **Phase 2 (Child SA / IPsec SA):** Negotiates the actual ESP/AH parameters for protecting traffic.

Modern deployments use **IKEv2**, which is faster, more reliable, and supports MOBIKE (mobility).

---

## Quick Summary

```
IPsec Tunnel Mode = Encrypt(Original IP Header + Payload) + New Outer IP Header
```

It's the backbone of virtually all modern VPN solutions (Cisco, Palo Alto, AWS Site-to-Site VPN, strongSwan, etc.).

---

**References:**
- [RFC 4301 — Security Architecture for IP](https://datatracker.ietf.org/doc/html/rfc4301)
- [RFC 4303 — IP Encapsulating Security Payload (ESP)](https://datatracker.ietf.org/doc/html/rfc4303)
- [RFC 7296 — IKEv2](https://datatracker.ietf.org/doc/html/rfc7296)
- [Cloudflare — What is IPsec?](https://www.cloudflare.com/learning/network-layer/what-is-ipsec/)
