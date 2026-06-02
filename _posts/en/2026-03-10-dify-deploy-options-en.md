---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dify Deployment Options Explained
translated: false
type: note
---

**Question:** What is the relationship between the Dify open-source project and the dify.ai web portal, and do they offer enterprise deployment?

---

**Answer:**

## Overview: Same Product, Multiple Delivery Models

Dify is created by **LangGenius, Inc.**, and both the open-source GitHub project ([github.com/langgenius/dify](https://github.com/langgenius/dify)) and the web portal at [dify.ai](https://dify.ai) are the same platform — just accessed in different ways. The cloud service hosts all the capabilities of the self-deployed version. Think of it like WordPress.com vs WordPress.org: same core software, different hosting arrangements.

---

## The Three Deployment Options

### 1. Dify Cloud (dify.ai — Hosted SaaS)

This is the web portal at dify.ai. Dify.ai offers a cloud-hosted service with a tiered subscription model. You sign up and use it immediately with zero setup. Pricing tiers are roughly:

- **Sandbox (Free):** Trial tier, limited to a small number of apps and storage.
- **Professional (~$59/month):** Aimed at independent developers and small teams building production AI apps.
- **Team (~$159/month):** Geared towards medium-sized teams, allowing up to 50 team members to collaborate in one workspace.
- **Enterprise (Custom Pricing):** Contact sales; unlimited quotas plus advanced features (see below).

### 2. Self-Hosted Community Edition (Open Source)

Dify's core platform is open-source. You can download it from GitHub and run it on your own servers or cloud instances without paying a license fee. The software is free; you incur only the infrastructure costs to host it. It is deployed via Docker Compose or Kubernetes Helm charts. This is ideal for teams with strict data control requirements or those wanting to avoid recurring SaaS fees.

The repository is available under the Dify Open Source License, which is essentially Apache 2.0 with a few additional restrictions.

### 3. Enterprise Edition (On-Premises / Private Cloud)

Yes, Dify does offer enterprise deployment. Dify Enterprise delivers the full power of Dify in a secure, customizable, and enterprise-ready package. Built for Kubernetes, this edition supports official Helm chart deployment, giving organizations the flexibility to run Dify on their own cloud infrastructure or in on-premise environments, meeting strict compliance, data residency, and regulatory requirements.

Enterprise features include:

- Multiple workspaces, SSO (SAML and OIDC), deployment assistance, extensive white-labeling, negotiable SLA, model load-balancing, centralized workspace and user management, custom roles, dedicated Slack channel, phone, and email support, and enterprise-level usage insights.
- Multi-tenant management, two-step verification, and MFA support, along with a paid commercial license that enables full branding customization.

---

## Key Relationship Summary

| Aspect | Open Source (GitHub) | dify.ai Cloud | Enterprise |
|---|---|---|---|
| Cost | Free (infra costs only) | Tiered subscriptions | Custom (contact sales) |
| Hosting | You manage it | Dify manages it | You manage it (on-prem/VPC) |
| Data control | Full | Limited (Dify's cloud) | Full |
| SSO / Multi-tenant | Manual setup | Limited | Yes, built-in |
| Support | Community / GitHub | Email | Dedicated private channels |
| License | Apache 2.0 + conditions | SaaS ToS | Commercial license |

---

## Bottom Line

The platform offers both self-hosted and cloud deployment options, catering to users with different preferences in control, scalability, and ease of use. The open-source project and dify.ai are the same product at their core — the portal is simply the managed cloud version of the open-source code. For enterprises needing on-premises deployment, compliance, SSO, and SLAs, a dedicated Enterprise license is available by contacting Dify's sales team.

---

**References:**

- [Dify GitHub Repository (langgenius/dify)](https://github.com/langgenius/dify/)
- [Dify Official Website](https://dify.ai/)
- [Dify Enterprise Page](https://dify.ai/enterprise)
- [Dify Pricing Page](https://dify.ai/pricing)
- [Dify Enterprise on Microsoft Marketplace](https://marketplace.microsoft.com/en-us/product/saas/sosgrouplimited.sos-dify-enterprise)
- [Dify Strategic Overview & Pricing Breakdown (Baytech Consulting)](https://www.baytechconsulting.com/blog/what-is-dify-ai-2025)
