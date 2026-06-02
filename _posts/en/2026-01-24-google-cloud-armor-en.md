---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud Armor DDoS and WAF Protection
translated: false
type: note
---

Question: What is an introduction to Google Cloud Armor?

Answer:

Google Cloud Armor is Google Cloud's **network security service** that protects applications and infrastructure from various internet-based threats, particularly **DDoS attacks** and common web application attacks.

### Main Purposes
- **DDoS protection** — Mitigates both volumetric network-level (Layer 3/4) and application-level (Layer 7) attacks.
- **Web Application Firewall (WAF)** — Blocks common exploits such as SQL injection (SQLi), cross-site scripting (XSS), remote code execution, and many other OWASP Top 10 threats.

### Key Features
- **Always-on Layer 3/4 DDoS protection** — Automatically provided for Google Cloud load balancers (no extra configuration needed for basic volumetric protection).
- **Layer 7 protection** — Configurable through security policies attached to HTTP(S) load balancers.
- **Security Policies** — The core mechanism:
  - Custom rules (you define match conditions → actions like allow, deny, redirect, rate-limit, etc.)
  - **Preconfigured WAF rules** — Ready-to-use OWASP-aligned rule sets with dozens of signatures.
  - **Preconfigured protection levels** (e.g., default rulesets for common threats).
- **Adaptive Protection** (Enterprise tier) — ML-based automatic threat detection and rule tuning.
- **Bot Management** (Enterprise) — Advanced bot detection and mitigation.
- **Edge security** — Rules are evaluated at Google's edge (close to the source of traffic), reducing load on your backends.

### Tiers / Editions (as of 2025–2026)
- **Cloud Armor Standard** — Basic DDoS protection + custom rules + some preconfigured WAF rules (pay-per-use, charged mainly on processed requests).
- **Cloud Armor Enterprise** — Full-featured version:
  - Advanced WAF rules
  - Adaptive Protection
  - Bot Management
  - Managed Protection (always-on curated defenses)
  - Predictable pricing via subscription (monthly/annual commitment options)

### Where It Attaches
Cloud Armor policies are primarily attached to:
- Global external **Application Load Balancers** (HTTP/HTTPS)
- Classic Application Load Balancers
- Some cross-project and multi-cloud scenarios (with proper configuration)

It does **not** directly protect Compute Engine VMs or non-load-balanced traffic unless routed through a supported load balancer.

### Common Use Cases
- Protecting public web applications from DDoS floods
- Blocking common web exploits without writing custom regex rules
- Rate limiting suspicious clients (e.g., brute-force login attempts)
- Geo-based or IP-based access control
- Defending APIs and mobile backends
- Adding defense-in-depth for internet-facing services

In short: Cloud Armor is Google’s combination of **always-on DDoS scrubbing** + **managed WAF** + **edge policy enforcement**, leveraging Google’s massive global network and threat intelligence.

References:

- [Google Cloud Armor Overview](https://docs.cloud.google.com/armor/docs/cloud-armor-overview)
- [Google Cloud Armor Product Page](https://cloud.google.com/security/products/armor)
- [Google Cloud Armor Documentation](https://docs.cloud.google.com/armor/docs)
