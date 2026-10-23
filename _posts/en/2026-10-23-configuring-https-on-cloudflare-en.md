---
audio: false
generated: true
image: false
lang: en
layout: post
title: Configuring HTTPS on Cloudflare
translated: false
type: note
---

Question: How to add HTTPS support for a domain in Cloudflare?

Answer:

Cloudflare makes enabling HTTPS straightforward. Here are the main steps:

**Quick recommendation:**

- For most sites: use **Full (Strict)** mode + **Always Use HTTPS** toggle. This gives you proper end-to-end encryption.
- If your origin server has no SSL cert yet: start with **Flexible** temporarily, then install a Cloudflare Origin Certificate and switch to **Full (Strict)**.

**SSL Mode Summary:**

| Mode | Visitor ↔ Cloudflare | Cloudflare ↔ Origin |
| --- | --- | --- |
| Flexible | HTTPS | HTTP |
| Full | HTTPS | HTTPS (self-signed OK) |
| Full (Strict) | HTTPS | HTTPS (valid cert required) |

---

References:

- [Cloudflare SSL/TLS Overview](https://developers.cloudflare.com/ssl/get-started/)
- [Cloudflare Edge Certificates](https://developers.cloudflare.com/ssl/edge-certificates/)
- [Cloudflare Origin CA Certificates](https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/)
- [Always Use HTTPS Setting](https://developers.cloudflare.com/ssl/edge-certificates/additional-options/always-use-https/)
