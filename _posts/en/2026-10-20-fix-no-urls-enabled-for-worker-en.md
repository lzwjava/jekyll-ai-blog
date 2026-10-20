---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix No URLs Enabled for Worker
translated: false
type: note
---

**Question:** Why does my Cloudflare Worker show "No URLs enabled," and how do I bind a domain to it?

**Answer:**

**Why "No URLs enabled" appears**

Your worker (`zhiwei-software`) is deployed and ready, but it has no routes or domains attached — so there is no URL through which requests can reach it. Cloudflare does not automatically assign a public URL; you must enable at least one of the two options below.

---

**Option 1 — Enable the free `workers.dev` subdomain (quickest)**

1. Go to your worker → **Settings** tab
2. Find **Workers.dev subdomain** (or "Domains & Routes")
3. Toggle it **On**
4. Your worker becomes reachable at `https://zhiwei-software.<your-subdomain>.workers.dev`

---

**Option 2 — Bind your custom domain `zhiweisoft.site`**

Since you already have `zhiweisoft.site` in your account:

1. Open your worker → **Domains** tab (or **Settings → Domains & Routes**)
2. Click **Add** → choose **Custom Domain**
3. Enter `zhiweisoft.site` or a subdomain like `api.zhiweisoft.site`
4. Cloudflare will automatically create the DNS record and provision a TLS certificate — no extra config needed
5. Wait ~1–2 min for propagation; the worker will then respond at that domain for all paths (`/*`)

> **Note:** For a custom domain to work, `zhiweisoft.site` must be **proxied through Cloudflare** (orange cloud in DNS settings), which it already is since it appears in your Cloudflare account.

---

**Option 3 — Add a Route (for partial path matching)**

If you only want the worker to handle specific paths (e.g. `zhiweisoft.site/api/*`):

1. Worker → **Domains** tab → **Add** → **Route**
2. Enter a pattern like `zhiweisoft.site/api/*`
3. Select the zone (`zhiweisoft.site`)

---

**Summary of the difference:**

| Method | URL | Use case |
| --- | --- | --- |
| workers.dev | `zhiwei-software.xxx.workers.dev` | Testing / no custom domain |
| Custom Domain | `zhiweisoft.site` | Production, all traffic |
| Route | `zhiweisoft.site/api/*` | Only specific paths |

For a production site, **Custom Domain** (Option 2) is the cleanest approach.

**References:**

- [Cloudflare Workers – Custom Domains](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)
- [Cloudflare Workers – Routes](https://developers.cloudflare.com/workers/configuration/routing/routes/)
- [Get started with Workers (domains & routing)](https://developers.cloudflare.com/workers/get-started/guide/)
