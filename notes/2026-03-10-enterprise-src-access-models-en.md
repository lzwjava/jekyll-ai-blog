---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enterprise Source Code Access Models
translated: false
type: note
---

**Question:** For enterprise on-premises/private deployment in open-core companies, is the source code provided to customers? And are the enterprise-tier features (SSO/SAML, RBAC, audit logging, HA, etc.) closed source?

---

**Answer:**

## Short Answer

**Yes, enterprise features are almost always closed source (proprietary).** But the situation around source code *access* for customers is more nuanced — it's not black-and-white.

---

## The Spectrum of Source Access

There are actually three distinct scenarios, not just "open" or "closed":

### 1. Fully Closed / Binary Only (Classic Enterprise)

The enterprise add-ons are compiled binaries or plugins. The customer gets no source code whatsoever. They deploy a pre-built artifact. The company creates a closed fork of the free software codebase, or provides the additional proprietary features as modules to avoid violating the free software license. Examples: older Elastic plugins, some Confluent connectors.

### 2. Source-Available (Modern Trend)

The enterprise code *is* visible to paying customers — they can read and even modify it — but they **cannot redistribute it or use it without a commercial agreement**. For enterprise software, providing source code is now table stakes. The days of source code escrow are over. Customers expect access. If you won't provide it, they'll find someone who will. This is rapidly becoming the dominant model because enterprise buyers — especially in regulated industries — demand code auditability for security reviews.

### 3. Fully Open Source (Rare for Enterprise Features)

Everything is open source, including enterprise features. Revenue comes from support, SLAs, and managed hosting. Red Hat/RHEL is the canonical example of this approach.

---

## Are the Enterprise Feature Themselves Closed Source?

Yes. The base product is open source, but significant features are proprietary and require a paid license. The "core" is open. Everything else is behind a paywall.

The features that enterprises need — SSO, audit logs, advanced alerting, role-based access — are enterprise-only. These aren't niche features; they're table stakes for any team operating in a regulated environment or at scale.

This is a deliberate product strategy: features that appeal most to management or an executive are proprietary and require a subscription. It's no longer about "where is that feature technically?" — it's about the end-user.

---

## Real-World Examples of How Each Company Handles This

| Company | Enterprise Code Access | License Model |
| --- | --- | --- |
| **Elastic** | Source-available to customers | Elastic License 2.0 (ELv2) — can read, cannot redistribute or offer as SaaS |
| **GitLab EE** | Source code visible on GitLab.com | Proprietary — can inspect but not use without a license |
| **HashiCorp (Vault/Terraform EE)** | Source-available | BSL (Business Source License) — reverts to open after 4 years |
| **Neo4j EE** | Binary only | Proprietary |
| **Grafana Enterprise** | Source-available to paying customers | Grafana Enterprise License |
| **MongoDB** | SSPL (partially open, highly restrictive) | SSPL — effectively source-available for most uses |

---

## Why This Split Is Intentional (Not Accidental)

The company develops an enterprise version with the proprietary value-add typically concentrated in areas where the open-source project falls short — usually targeting corporate customers' needs such as vertical scalability, third-party integration, improved security, and higher speed.

The criticism from the open-source community is real: a lot of so-called "enterprise" features end up being basic security features like TLS support — simple improvements you'd want in the free version — but these never make their way into the community edition, because the company intends that only individuals will use that version.

---

## The Lock-In Risk

Open core creates a subtle form of lock-in. You're not locked into the open source part — you can always fork that. You're locked into the proprietary features you've come to depend on. Open core vendors can change their license at any time. Elastic did it. HashiCorp did it. Redis Labs did it. MongoDB did it (SSPL). When the business model isn't working, the license gets more restrictive.

---

## Summary

- Enterprise features (SSO, RBAC, audit logs, HA clustering) → **always closed source / proprietary**
- Source code access for customers → **depends on company, but trend is toward "source-available"** (you can read it, not copy/redistribute it)
- Fully open-source enterprise features → **rare, mostly Red Hat's model**
- On-prem enterprise deployment = you run their proprietary binary/plugin on your own infrastructure, typically without the right to modify it

---

**References:**

- [Open-core model - Wikipedia](https://en.wikipedia.org/wiki/Open-core_model)
- [Open Source vs Open Core: What It Actually Means (OneUptime)](https://oneuptime.com/blog/post/2026-02-14-open-source-vs-open-core/view)
- [OCV Source Available License](https://www.opencoreventures.com/blog/ocvs-new-source-available-license-is-a-simple-alternative-to-closed-source-licenses)
- [Open Core is a Misunderstood Business Model](https://opencoreventures.com/blog/open-core-is-a-misunderstood-business-model)
- [Some Thoughts on Open Core - Linux Journal](https://www.linuxjournal.com/content/some-thoughts-open-core)
