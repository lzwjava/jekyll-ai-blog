---
audio: false
generated: true
image: false
lang: en
layout: post
title: Layer Difference Causes Analytics Divergence
translated: false
type: note
---

**Question:** Why do GoatCounter and Cloudflare Web Analytics show significantly different results for the same website?

**Answer:**

They measure fundamentally different things at different layers of the stack. Here's the breakdown:

## Layer Difference — This Is the Core Reason

| | GoatCounter | Cloudflare Analytics |
|---|---|---|
| **Layer** | Application (JavaScript) | Network (CDN edge) |
| **What it counts** | Page views from JS execution | HTTP requests hitting Cloudflare |
| **Runs on** | Browser | Cloudflare's edge nodes |

Cloudflare sees **every HTTP request** — bots, crawlers, health checks, prefetches, asset fetches, API calls. GoatCounter only fires when a **human browser executes JavaScript** and the page actually loads.

## Specific Reasons for Divergence

**Cloudflare overcounts vs GoatCounter:**

- **Bots and crawlers** — Googlebot, Bingbot, scrapers all make HTTP requests. Cloudflare counts them. GoatCounter's JS never runs.
- **Static asset requests** — every `.css`, `.js`, `.png`, `.woff2` — Cloudflare logs each one. GoatCounter counts zero.
- **Health checks / uptime monitors** — tools like UptimeRobot hit your site every minute. Pure HTTP, no JS.
- **CDN cache hits for assets** — a page with 30 assets = 31 Cloudflare hits, 1 GoatCounter event.
- **Link prefetching** — browsers and search engines speculatively fetch URLs without "visiting" them.
- **Blocked JavaScript** — users with uBlock, NoScript, or aggressive privacy settings block tracking scripts. Cloudflare still sees their requests.

**GoatCounter overcounts vs Cloudflare (rare but possible):**

- **SPAs with client-side routing** — GoatCounter can fire multiple times per "page" if you instrument every route change. Cloudflare only sees the initial HTML request.
- **Manual `count()` calls** — if you accidentally double-fire the tracker.

## The Realistic Gap You'll See

For a typical static site / GitHub Pages / Jekyll blog:

- Cloudflare might show **3–10x** more "requests" than GoatCounter page views
- If you look at Cloudflare's **unique visitors** (not requests), it gets closer but still diverges due to bot traffic and asset requests being bucketed by IP

## What Each Is Actually Good For

**GoatCounter** → true human page views, bounce rates, referrers from actual users. More accurate for "how many humans read this post."

**Cloudflare** → bandwidth, attack detection, cache hit ratio, bot traffic volume, CDN performance. Good for infrastructure questions.

## How to Make Them More Comparable

In Cloudflare, filter to:

- **HTML requests only** (Content-Type: text/html)
- Exclude known bot user-agents
- Look at "page views" metric specifically (not total requests)

Even then, Cloudflare will be higher because it still counts:

- Users with JS disabled
- Users who blocked GoatCounter's domain
- Prefetch requests that never rendered

## Quick Mental Model

```
Cloudflare count
= human page views
+ bot requests
+ asset requests (CSS/JS/img)
+ health checks
+ prefetches
+ JS-blocked users

GoatCounter count
= human page views where JS executed successfully
- users who blocked the tracker
- users with JS disabled
```

For your blog at `lzwjava.github.io`, the gap is likely dominated by **Googlebot + other crawlers** (since a technical blog gets indexed aggressively) and **asset requests** if Cloudflare is proxying everything including static files.
