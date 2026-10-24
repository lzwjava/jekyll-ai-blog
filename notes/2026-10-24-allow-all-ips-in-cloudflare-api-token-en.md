---
audio: false
generated: true
image: false
lang: en
layout: post
title: Allow All IPs in Cloudflare API Token
translated: false
type: note
---

**Question:** How to allow all IP addresses in the Cloudflare API token IP address filtering field?

**Answer:**

The simplest way to allow all IP addresses is to **leave the IP address filtering field completely empty** — adding no entries means no restriction, so the token can be used from any IP.

If you specifically need to enter explicit "allow all" CIDR ranges, add these two entries:

| Entry | Covers |
| --- | --- |
| `0.0.0.0/0` | All IPv4 addresses |
| `::/0` | All IPv6 addresses |

Type each one into the input field and press **Enter** (or click the add button) to confirm it before submitting the form.

**Recommended approach:** Just leave the field blank. Cloudflare's IP filtering is opt-in — an empty list means unrestricted access, which is functionally identical to `0.0.0.0/0` + `::/0` but cleaner.

---

**References:**

- [Cloudflare API Tokens – Create and manage tokens](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)
- [Cloudflare API Token IP restrictions](https://developers.cloudflare.com/fundamentals/api/reference/restrictions/)
