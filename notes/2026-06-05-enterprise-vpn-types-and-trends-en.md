---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enterprise VPN Types and Trends
translated: false
type: note
---

**Question:** Explain the VPN providers in this form.

**Answer:**

This is a mixed bag spanning three categories. Here's what matters:

## Enterprise/Legacy VPNs
These are client-based, device-level tunnels (IPsec or proprietary protocols):

- **Cisco AnyConnect**, **Palo Alto GlobalProtect**, **FortiClient**, **Ivanti** — The old guard. Require endpoint agents. Heavy, proprietary, but deeply integrated into corporate networks. You'll encounter these at banks and large enterprises. Pain to manage at scale.

## Zero Trust / Modern Enterprise
These shifted from "VPN as a tunnel" to "identity-first access":

- **Cloudflare** (Warp) — ZT network for individuals + orgs. DNS-level filtering. Lightweight. Works well if your org is Cloudflare-native.
- **Twingate** — Pure identity-based access. No client VPN model. You authenticate, get mTLS certs, access specific resources. Most developer-friendly.
- **Zscaler** — Inline security gateway. Inspects all traffic. Enterprise favorite for DLP/threat prevention.
- **Google IAP** (Identity-Aware Proxy) — GCP-native. IAM-driven access to internal resources. Perfect if you're GCP-heavy. Can replace VPN entirely for internal infrastructure.

## Cloud-Native / Open-Source
- **AWS Client VPN** — Managed OpenVPN-compatible tunnel in AWS. Useful if your workload is entirely on AWS.
- **OpenVPN**, **Pritunl** — Commodity tunneling protocols. Pritunl adds centralized management. Both are self-hostable.

## Niche/Specialized
- **Cato Networks** — SD-WAN + security. More for multi-site infrastructure than per-user access.
- **Netskope** — Cloud security posture. Similar to Zscaler.

---

## What You Actually Need

**If you're building AI/ML systems at a bank** (like you mentioned): You'll probably face Cisco AnyConnect or GlobalProtect. No choice — legacy requirement.

**If you're self-hosting** (AMD Dev Cloud): OpenVPN or Pritunl if you want managed access. Or use Twingate for zero-trust.

**For your workstations** (MacBook Air + Ubuntu workstation): Likely not relevant unless the organization mandates it. Cloudflare Warp is fine if you just need privacy for personal use.

**The trajectory**: Enterprise is moving away from "connect to VPN, get all access" → "authenticate, get granular access to specific resources." Twingate and IAP represent this future. Cisco/Palo Alto represent the past trying to stay relevant.

Don't overthink this unless you're building the access layer for a company. If you're just asked to pick one, ask: Is it Zero Trust (Twingate, IAP, Zscaler) or Legacy (anything else)?
