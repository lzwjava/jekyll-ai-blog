---
audio: false
generated: true
image: false
lang: en
layout: post
title: GoatCounter vs Cloudflare Visit Discrepancy
translated: false
type: note
---

Question: Why does lzwjava.github.io show ~60k monthly hits in Cloudflare (roughly half agent traffic) but only ~4000 monthly in GoatCounter? Is GoatCounter only counting a "second click" and skipping the first?

Answer:

Your "second click" theory is backwards — check GoatCounter's actual visit logic:

```
session_key = site_id + user_agent + IP
if sessions[session_key] exists and < 8h old:
    if path not yet seen in this session:
        count_as_visit = true   # first load of THIS path counts
else:
    new session created
    count_as_visit = true       # first-ever load counts
```

So the **first** load of a page is exactly what gets counted as a visit. A reload or revisit to the same path within 8h does *not* count again. There's no mechanism where click #1 is dropped and click #2 is the one that registers.

The real gap comes from a stack of things, roughly in order of impact:

**1. GoatCounter only fires when JS actually executes in a browser.**
`count.js` runs on `DOMContentLoaded` and does a `fetch`/beacon POST to the count endpoint. Anything that doesn't run JS — `curl`, `GPTBot`, `ClaudeBot`, `Bytespider`, scrapers, most AI agents doing raw HTTP fetches — never touches GoatCounter at all. Your Cloudflare number is raw edge requests, so it captures every one of those. You already said ~half your 60k is agent traffic — that's ~30k gone right there, invisible to GoatCounter by design.

**2. Cloudflare's number is likely raw requests, not deduplicated sessions.**
If you're reading this off Cloudflare's zone-level analytics (not a JS-based Web Analytics beacon), it's counting every HTTP hit to the edge: HTML pages, CSS, JS, images, `robots.txt`, `sitemap.xml`, RSS feeds, favicon — anything. A single human "visit" that loads a notes page with a few assets can be 5-10 requests. GoatCounter counts 1 visit for that same event. This alone can produce a 5-10x gap on the human side even before bots are considered.

**3. GoatCounter has its own bot filter on top (`isbot`).**
Even for requests that do run JS, GoatCounter cross-checks user-agent against a bot list server-side and discards anything it identifies as a bot, so borderline automated traffic gets filtered a second time.

**4. Ad blockers / privacy tools block third-party analytics scripts.**
`*.goatcounter.com` subdomains are on some privacy blocklists (EasyPrivacy-style lists), and your audience (engineers, HN/lobste.rs referral traffic typically) skews toward uBlock/Brave/Pi-hole/NextDNS users. That's a real undercount on the human side that Cloudflare wouldn't miss since it's edge-level, pre-JS.

**5. Client-side navigation without a real page load.**
If any part of the site prefetches or navigates via `pushState` without a `DOMContentLoaded`, GoatCounter's default script won't fire on that navigation unless you manually call `goatcounter.count()` on route change. Worth checking if your site does anything SPA-like.

Napkin math for you: 60k requests → ~30k agent/bot (invisible to GC) → remaining ~30k human-driven requests, of which maybe 3-6 requests per real visit (assets) → lands you right around 4-5k actual unique-visit sessions. That's consistent with what you're seeing — no missing-first-click bug required.

If you want ground truth, check Cloudflare's own **Unique Visitors** metric (not total requests) for the same period — that's the number that should actually compare apples-to-apples with GoatCounter's "visits."

References:
- [GoatCounter: How sessions and visits work](https://www.goatcounter.com/help/sessions)
- [goatcounter/isbot bot detection source](https://github.com/zgoat/isbot/blob/master/isbot.go)
- [GoatCounter GitHub issue: pageviews vs unique visitors](https://github.com/arp242/goatcounter/issues/672)
- [GoatCounter GitHub issue: SPA navigation not counted](https://github.com/arp242/goatcounter/issues/482)
