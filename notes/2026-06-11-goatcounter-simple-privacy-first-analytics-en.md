---
audio: false
generated: true
image: false
lang: en
layout: post
title: "GoatCounter: Simple privacy-first analytics"
translated: false
type: note
---

**Question:** What is GoatCounter (goatcounter.com), and how would I use it?

**Answer:**

GoatCounter is an open-source web analytics platform you can use either as a free hosted service at goatcounter.com or self-hosted on your own server. It's written by Martin Tournoij (arp242) as a privacy-first alternative to Google Analytics — no unique user identifiers, no GDPR consent banner needed, and the tracking script adds only ~3.5KB to your page.

Architecture, briefly: it's a single Go binary using SQLite by default, with optional PostgreSQL for self-hosted installs. That makes it one of the simplest self-hostable analytics stacks around — one binary, one embedded DB, no Redis/queue/JS-framework sprawl. Very much the "simple, understandable systems" school you like.

Integration on your Jekyll blog (lzwjava.github.io) is one line in your layout:

```html
<script data-goatcounter="https://lzwjava.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
```

If you'd rather not run JS, there's a no-JS tracking pixel, backend-middleware integration, or log-file import — useful if you ever want to pipe nginx access logs from your Ubuntu workstation into it.

Self-hosting it on `lzw@192.168.x.x`:

```bash
# grab the release binary (it's Go, single static binary)
wget https://github.com/arp242/goatcounter/releases/latest/download/goatcounter-dev-linux-amd64.gz
gunzip goatcounter-*.gz && chmod +x goatcounter-*

# create a site + serve (SQLite db auto-created)
./goatcounter db create site -vhost stats.example.com -user.email you@example.com
./goatcounter serve -listen :8081 -tls none
```

You can also hit its API to pull stats programmatically — handy for a CLI agent that reports weekly blog traffic:

```bash
curl -s -H "Authorization: Bearer <API_KEY>" \
  "https://lzwjava.goatcounter.com/api/v0/stats/hits" | jq '.hits[:5]'
```

What it tracks: pageviews, referrers, browser/OS, screen size, country — and that's roughly it. It's intentionally basic compared to Matomo/Plausible/Umami, no funnels, no session replay, no conversion tracking. The hosted goatcounter.com tier is free (donation-supported) for reasonable public usage — personal sites and small projects are fine, millions of pageviews/day are not.

When to pick it over alternatives: GoatCounter if you want zero-maintenance, free, "which posts get traffic" answers; Umami or Plausible if you want a prettier dashboard and events; Matomo if you actually need GA-class features. For a ~400-post technical blog, GoatCounter's hosted free tier is basically the correct lazy answer — one script tag and done.

**References:**

- [GoatCounter — official site](https://www.goatcounter.com/)
- [arp242/goatcounter — GitHub](https://github.com/arp242/goatcounter)
- [GoatCounter on Hacker News](https://news.ycombinator.com/item?id=34265127)
