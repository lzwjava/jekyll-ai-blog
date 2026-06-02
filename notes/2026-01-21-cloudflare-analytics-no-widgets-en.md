---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Display Cloudflare Analytics Without Widgets
translated: false
type: note
---

**Question: How to display Cloudflare Web Analytics data such as last 30 days visits and page views on my blog?**

**Answer:**

Cloudflare Web Analytics (the privacy-focused, JS-based product) does **not** offer any official embeddable widgets, badges, charts, or public sharing options to directly display stats (like total visits or page views for the last 30 days) on your own blog/website.

Cloudflare's dashboard shows this data only to the account owner, and there is no built-in public-facing badge or embed code like some other analytics services provide.

Here are the realistic options people commonly use:

1. **Manual update (simplest, no coding)**
   Check your Cloudflare dashboard → Web Analytics → Overview once a month (or week), note the "Visits" and "Page views" numbers shown for the previous 30 days, and manually write them in your blog footer/sidebar/about page, e.g.:

   ```
   Last 30 days: ≈ 12,400 visits • 38,700 page views (via Cloudflare Web Analytics)
   ```

   Many small/personal blogs do exactly this.

2. **Use the Cloudflare GraphQL Analytics API (most accurate but requires programming)**
   Cloudflare provides a GraphQL API that can return HTTP-level metrics (page views, visits) for zones/domains.
   - You need to create an **API token** with "Analytics: Read" permission.
   - Query the last 30 days aggregated data using something like `httpRequests1dGroups` or `httpRequestsAdaptiveGroups`.
   - Run this query periodically (cron job, GitHub Actions, Cloudflare Worker) → store the result → display it on your blog (static file, shortcode, etc.).

   Example rough GraphQL query structure (you need to adjust dates and zoneTag):

   ```graphql
   query {
     viewer {
       zones(filter: {zoneTag: "YOUR_ZONE_ID"}) {
         httpRequests1dGroups(
           filter: {date_geq: "2025-12-23", date_lt: "2026-01-22"}
           limit: 31
         ) {
           sum { pageViews visits requests }
           dimensions { date }
         }
       }
     }
   }
   ```

   You can sum the `pageViews` and unique-approx visits over the period. Many people build small dashboards or simple counters this way.

3. **Cloudflare Workers + KV / D1 (custom counter/badge)**
   If you want a live "views this month" badge:
   - Use a Worker to count page views (via fetch event).
   - Store totals in KV or D1.
   - Serve an SVG badge similar to shields.io / badgen style.
   This is not using Web Analytics data but recreating a similar metric.

4. **Third-party alternatives if you want easy embed**
   If a public badge/widget is important, consider switching to (or adding) tools that offer this natively:
   - Plausible Analytics (has shareable dashboards + simple embeds)
   - Umami (self-hosted, has public sharing)
   - Fathom Lite
   - GoatCounter
   - Simple analytics with export → Hugo/Jekyll shortcode

**Quick summary – what most people do for static blogs**
→ Manually paste the numbers every month or two (very common for indie blogs).
→ If you want automation → build a tiny script using the GraphQL API + your SSG's data files / API routes.

**References:**

- <https://developers.cloudflare.com/web-analytics/>
- <https://developers.cloudflare.com/analytics/graphql-api/>
- <https://community.cloudflare.com/t/api-for-web-analytics/644351>
- <https://developers.cloudflare.com/analytics/account-and-zone-analytics/zone-analytics>
