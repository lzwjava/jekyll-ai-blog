---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cloudflare Worker Route Doesn't Cover Apex
translated: false
type: note
---

**Question:** Why is Cloudflare unable to access `http://truthlab.cc` even though a Worker route is configured?

**Answer:**

Looking at your Cloudflare dashboard, there are **two likely causes**:

---

### 1. ⚠️ Route Pattern Doesn't Cover the Apex Domain (Main Issue)

Your current route is:
```
*.truthlab.cc/*
```

The `*.` wildcard **only matches subdomains** (e.g., `www.truthlab.cc`, `api.truthlab.cc`), but it does **not** match the root/apex domain `truthlab.cc` itself. So visiting `http://truthlab.cc` simply has no matching Worker route.

**Fix:** Add a second route (or Custom Domain) for the apex:

| What to add | Type |
|---|---|
| `truthlab.cc/*` | Route |

Or better, switch from Routes to **Custom Domains** and add both:
- `truthlab.cc`
- `*.truthlab.cc`

Custom Domains are simpler — Cloudflare handles DNS automatically and HTTPS is included.

---

### 2. DNS Must Be Proxied (Orange Cloud) for Routes to Work

If you're using Routes (not Custom Domains), your `truthlab.cc` DNS record in Cloudflare must be:
- **Proxied** (orange cloud ☁️), not DNS-only (grey cloud)
- Pointing to any IP (e.g., `192.0.2.1` as a placeholder is fine — Cloudflare intercepts it)

---

### Quick Fix Steps

1. Go to **Workers & Pages → truth-lab → Settings → Domains & Routes**
2. Click **Add** → choose **Custom Domain**
3. Enter `truthlab.cc` (the apex domain)
4. Optionally also add `*.truthlab.cc` as a second Custom Domain

Cloudflare will automatically provision SSL and wire up DNS.

---

**References:**
- [Cloudflare Workers Routes vs Custom Domains](https://developers.cloudflare.com/workers/configuration/routing/)
- [How route matching works (wildcard patterns)](https://developers.cloudflare.com/workers/configuration/routing/routes/#matching-behavior)
- [Custom Domains for Workers](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)
