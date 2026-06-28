---
audio: false
generated: true
image: false
lang: en
layout: post
title: Privacy-Focused Analytics for GitHub Pages
translated: false
type: note
---

**Question:** What's the best web analytics tool I can use for my GitHub Pages blog at lzwjava.github.io?

**Answer:**

For a static GitHub Pages blog, privacy-friendly and lightweight beats Google Analytics. Top picks by use case:

**Plausible** — open-source, self-hostable, ~1KB script, no cookies/GDPR banner needed. Cloud is ~$9/mo, but you self-host for free on your `lzw@192.168.1.36` workstation. This fits your stack best.

```html
<!-- in _layouts/default.html or _includes/head.html -->
<script defer data-domain="lzwjava.github.io"
        src="https://plausible.io/js/script.js"></script>
```

Self-host with Docker:
```bash
git clone https://github.com/plausible/community-edition plausible-ce
cd plausible-ce
docker compose up -d   # serves on :8000, put Caddy/nginx in front
```

**Umami** — also open-source, self-hostable, Postgres/MySQL backed. Lighter ops than Plausible, single Node service. Great if you want full control + SQL access to your own analytics data.

```bash
docker run -d --name umami \
  -e DATABASE_URL=postgresql://<USER>:<PASSWORD>@<IP_ADDRESS>:5432/umami \
  -p 3000:3000 ghcr.io/umami-software/umami:postgresql-latest
```

**GoatCounter** — dead simple, free hosted tier for non-commercial, no cookies, tiny script. Lowest effort, zero infra. Good if you just want pageview counts without running anything.

```html
<script data-goatcounter="https://lzwjava.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
```

**Cloudflare Web Analytics** — free, no script weight concern, but only useful if you proxy through Cloudflare. Since you're on raw GitHub Pages (no CF proxy on a `github.io` domain), this won't work unless you move to a custom domain behind Cloudflare.

**My recommendation for you:** Self-host **Umami** on your RTX 4070 workstation. It's one container + Postgres, gives you raw SQL access to your traffic data (you can run your own queries/embeddings/analysis on visitor patterns), no third-party data leakage, and aligns with your self-hosting/autonomy philosophy. Plausible is the runner-up if you prefer a more polished UI out of the box.

One caveat: your home workstation needs a stable public endpoint (Cloudflare Tunnel or Tailscale Funnel) for the tracking script to reach it. If you don't want to expose it, use GoatCounter's hosted tier as a zero-ops fallback.

**References:**

- [Plausible Community Edition](https://github.com/plausible/community-edition)
- [Umami](https://github.com/umami-software/umami)
- [GoatCounter](https://www.goatcounter.com/)
- [Cloudflare Web Analytics](https://www.cloudflare.com/web-analytics/)
