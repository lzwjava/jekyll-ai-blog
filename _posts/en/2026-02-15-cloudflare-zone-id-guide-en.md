---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cloudflare Zone ID Explained Simply
translated: false
type: note
---

**Question:** What is a Zone ID in Cloudflare?

**Answer:**

In Cloudflare, a **Zone ID** is a unique identifier (a long alphanumeric string) assigned to each **zone** in your account.

A **zone** in Cloudflare refers to a domain (or sometimes a subdomain) that you have added to Cloudflare for management. This includes services like DNS hosting, caching, security features (WAF, DDoS protection), performance optimizations, Workers, and more. In simple terms, each domain you connect to Cloudflare becomes one zone.

The Zone ID serves as the primary way to reference a specific domain/zone when using:

- The Cloudflare API (most common use case)
- API tokens with zone-level permissions
- Cloudflare Workers routes or bindings (when targeting a specific domain)
- Third-party integrations or tools that interact with Cloudflare on a per-domain basis
- Certain advanced configurations (Terraform, CLI tools like wrangler, automation scripts, etc.)

It is **not sensitive information** — unlike API keys or tokens, the Zone ID (and Account ID) can be safely shared publicly without compromising security, as they only identify resources and do not grant any access on their own.

**How to find your Zone ID:**

1. Log in to the Cloudflare dashboard at <https://dash.cloudflare.com>
2. Select the domain/zone you want from the list
3. Go to the **Overview** tab for that domain
4. Scroll down to the right-hand sidebar or bottom section labeled **API**
5. You will see **Zone ID** listed there (usually next to **Account ID**)
6. Click "Click to copy" to copy the value (it looks something like `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

The same information appears in the URL when viewing zone settings (something like `/[account_id]/[zone_id]/...`).

**References:**

- [Find account and zone IDs · Cloudflare Fundamentals docs](https://developers.cloudflare.com/fundamentals/account/find-account-and-zone-ids)
- [Accounts, zones, and profiles · Cloudflare Fundamentals docs](https://developers.cloudflare.com/fundamentals/concepts/accounts-and-zones)
- [Cloudflare Community discussions on Zone ID](https://community.cloudflare.com/t/about-zone-id/47514)
