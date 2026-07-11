---
audio: false
generated: true
image: false
lang: en
layout: post
title: Why GoatCounter Shows Far Fewer Visits
translated: false
type: note
---

**Question:** Cloudflare Web Analytics shows ~60k visits over the past 30 days on my blog (lzwjava.github.io), but GoatCounter shows only ~4,000. What's going on with GoatCounter, and is it true that agent/bot traffic now accounts for a large share of this discrepancy?

**Answer:**

Your 15x gap is almost certainly a **methodology mismatch, not a GoatCounter bug**. You're comparing two fundamentally different measurement layers.

## The core issue: which Cloudflare product are you actually looking at?

Cloudflare ships two things people call "analytics" and they measure completely different things:

| Product | Where | Mechanism | Counts bots? |
| --- | --- | --- | --- |
| **Web Analytics** (aka Browser Insights) | Speed tab / dedicated Web Analytics section | JS beacon, client-side, no cookies | Mostly no (bots that don't execute JS are invisible), but does **not fully filter** JS-executing bots — Cloudflare classifies them as `Unknown` browser and historically has not excluded them by default Cloudflare Web Analytics doesn't exclude bot traffic in their website statistics; bots are classified as 'Unknown' browser types and are a significant percentage in Cloudflare's website statistics |
| **Analytics & Logs** (the "Traffic"/Overview tab near DNS, zone-level) | Dashboard overview | Server-side, edge/proxy log-based — every HTTP request that touches Cloudflare's edge | **Yes, everything** — bots, crawlers, monitoring pings, curl, scrapers |

This is a very common confusion and Cloudflare's own community forum has the exact answer: Cloudflare reports all visits to your site, including bots, crawlers, and users with privacy measures. Google Analytics, on the other hand, only counts visitors who execute their JavaScript. GoatCounter behaves like the Google Analytics side of that comparison — it's a JS beacon too, so it structurally cannot see non-JS-executing bots at all.

If your 60k number is coming from the zone-level **Analytics & Logs / Traffic** overview (not the dedicated Web Analytics widget), that number includes literally every crawler, AI scraper, uptime monitor, and RSS reader that hit `lzwjava.github.io` through Cloudflare's proxy. That's not "60k readers" — it's "60k HTTP requests Cloudflare's edge logged." Not comparable to GoatCounter at all.

**Action item #1:** go check which exact panel you were reading. If it's the dashboard "Traffic" overview, this whole discrepancy is explained already — no need for a third analytics platform to "resolve" it, because you weren't comparing like-for-like in the first place.

## Yes, agent/bot traffic really has exploded — this isn't paranoia

Your instinct is correct and it's not a small effect anymore: Cloudflare's Radar dashboard puts bots at 57.5% of all HTTP requests to HTML content, humans at 42.5% as of June 2026 — Cloudflare CEO Matthew Prince posted that automated bot traffic had crossed a threshold no one in the industry expected this soon: for the first time in the internet's history, machines now generate more web traffic than people. And it's not just old-school scraping — agentic AI, bots acting on behalf of users rather than scraping for training data, made up just 1.7% of automated traffic at the start of last year, and by the end of 2025 that category had grown 8,000%. Cloudflare has been actively monetizing this shift: Cloudflare launched Pay Per Crawl in 2025, letting publishers charge AI scrapers for content access, blocked over 416 billion AI bot requests at site owners' request, and rolled out a Markdown-for-Agents format explicitly designed for machine consumption. Your blog has ~8,000 notes + 400 posts — that's exactly the kind of long-tail technical content GPTBot/ClaudeBot/PerplexityBot/Bytespider crawl heavily for training/RAG.

## GoatCounter's own blind spots (why 4k might be *undercounting* real humans too)

Don't assume 4k is ground truth either:

- GoatCounter's script domain (`gc.zgo.at` or your custom counting domain) is on some ad-blocker/privacy-list filter sets, so a nontrivial fraction of privacy-conscious readers (exactly the crowd reading a self-hosted, open-source-adjacent blog) will silently never fire the beacon.
- If you're self-hosting GoatCounter and it's slow/unreachable at the moment the beacon fires (e.g. cold VM, DNS hiccup), pageviews just silently don't record — no error surfaces to you.
- JS-beacon tools miss anyone reading via RSS reader, `curl`, `wget`, or increasingly, an **agent fetching markdown on a human's behalf** (exactly the `Markdown-for-Agents` pattern Cloudflare just built) — that traffic is real reader intent but invisible to both GoatCounter and Cloudflare Web Analytics.

## Don't add a third analytics platform — use Cloudflare's own bot classification as your cross-reference

Since you're already Cloudflare-proxied, the actual "third data source" you want isn't Plausible/Umami/Fathom, it's Cloudflare's own **bot score** on the exact same request stream, via the GraphQL Analytics API (works on free/Pro zones, not Enterprise-only):

```bash
curl -s -X POST "https://api.cloudflare.com/client/v4/graphql" \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
  "query": "query {
    viewer {
      zones(filter: { zoneTag: \"<ZONE_ID>\" }) {
        httpRequestsAdaptiveGroups(
          limit: 10000,
          filter: { datetime_geq: \"2026-06-11T00:00:00Z\", datetime_leq: \"2026-07-11T00:00:00Z\" }
        ) {
          count
          dimensions { botScore }
        }
      }
    }
  }"
}'
```

Bucket the returned `botScore` (0–99, lower = more bot-like) into human (>30) vs automated (<=30) and sum `count` per bucket. Compare **that human-only subtotal** against GoatCounter's 4k. If they land in the same ballpark, you've confirmed GoatCounter is roughly right and the 60k was mostly bot noise from the wrong Cloudflare panel. If GraphQL's human-bucket is still way higher than GoatCounter, then you have a real beacon-firing/adblock problem worth fixing (e.g. switch to a first-party proxied path like `/api/count` instead of a third-party JS domain, which also dodges most adblock lists).

This is a more useful signal than adding Plausible/Fathom/Umami as a fourth beacon — you'd just be adding another tool with the exact same JS-execution blind spot as GoatCounter, rather than actually separating human from bot on the request stream you already have.

**References:**

- [Types of analytics · Cloudflare Analytics docs](https://developers.cloudflare.com/analytics/types-of-analytics/)
- [Cloudflare Bot Analytics · Cloudflare bot solutions docs](https://developers.cloudflare.com/bots/bot-analytics/)
- [Cloudflare Analytics vs Web Analytics — Cloudflare Community discussion](https://community.cloudflare.com/t/traffic-report/561155)
- [Simple Analytics: why Cloudflare Web Analytics doesn't exclude bots](https://www.simpleanalytics.com/blog/why-simple-analytics-is-a-great-alternative-to-cloudflare-web-analytics)
- [Bots Now Outnumber Humans Online — Forbes, June 2026](https://www.forbes.com/sites/josipamajic/2026/06/04/bots-now-outnumber-humans-online-and-the-internet-was-never-built-for-this/)
