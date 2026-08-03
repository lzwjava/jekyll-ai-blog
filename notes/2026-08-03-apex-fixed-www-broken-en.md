---
audio: false
generated: true
image: false
lang: en
layout: post
title: Apex fixed, www broken
translated: false
type: note
---

## Verdict: the fix **has taken effect** — `lzwjava.com` is fully working. But `www.lzwjava.com` is **still broken** (no DNS record)

I verified the live state end-to-end. Here's the evidence:

### ✅ Apex `lzwjava.com` — fixed and working

| Check | Result |
| --- | --- |
| Nameservers | `barbara.ns.cloudflare.com` / `dion.ns.cloudflare.com` → Cloudflare authoritative (gotcha #2 is N/A) |
| Custom Domain binding | Exists on Worker: `lzwjava.com` → `jekyll-ai-blog`, `enabled: true`, `cert_id` issued |
| DNS at apex | Proxied A/AAAA (104.21.62.122 / 172.67.223.135 — Cloudflare IPs) → the conflicting record was deleted and Cloudflare auto-created its own |
| TLS cert | `CN=lzwjava.com`, SAN `lzwjava.com` + `*.lzwjava.com`, issued by Google Trust Services (Cloudflare universal SSL) |
| HTTP | `http://lzwjava.com` → **301** → `https://lzwjava.com` → **200 OK**, `server: cloudflare`, `cf-cache-status: HIT` |
| Content | Serves the blog: `<title>Zhiwei Li | truth freedom</title>` |

### ❌ `www.lzwjava.com` — still not working

- No DNS record at all (empty result even querying `barbara.ns.cloudflare.com` directly) → `www.lzwjava.com` doesn't resolve, no TLS, no connection.
- The zone has a **route** `*.lzwjava.com/*` → `jekyll-ai-blog`, so *routing* would work, but a legacy route doesn't auto-create a DNS record like a Custom Domain does. The wildcard cert `*.lzwjava.com` already exists, so the only missing piece is the DNS record.

### Notes on what I found

- Your repo's `wrangler.jsonc` has **no `routes`/`custom_domain` entries** yet — the apex binding must have been done via the dashboard or a one-off deploy. Git history shows you already documented this exact saga (`60bfdf2eb` "custom domain DNS conflict fix", `6f5284659` "enabling HTTPS on Cloudflare").
- The API token in the env (`CLOUDFLARE_API_TOKEN`) **lacks DNS permissions** — `dns_records` returns `Authentication error` (code 10000) — so I verified the record state via public DNS instead. The `dig` timeouts earlier were just the local `127.0.0.1:7890` proxy env interfering.

### To finish `www` (2 options)

```jsonc
// wrangler.jsonc — recommended, same path as your fix notes
"routes": [
  { "pattern": "lzwjava.com", "custom_domain": true },
  { "pattern": "www.lzwjava.com", "custom_domain": true }
]
```

or, if you only want a cheap redirect: add a **proxied** `CNAME www → lzwjava.com` record (the existing `*.lzwjava.com` route + wildcard cert handle the rest). Note you'll need a token with DNS edit permissions, since the current one can't touch records.

Want me to update `wrangler.jsonc` with the routes and/or check whether `npx wrangler deploy` would be safe to run from here?
