---
audio: false
generated: true
image: false
lang: en
layout: post
title: No API for Web Analytics Data
translated: false
type: note
---

**Question:** In this case (using Cloudflare Web Analytics for a GitHub Pages blog without adding a domain), how to use the API to get monthly visits?

**Answer:**

Cloudflare **does not provide a public API** to programmatically retrieve monthly (or any historical) visit / pageview / visitor data from **Web Analytics** when the site is set up via the JavaScript beacon (token-based, no domain/zone added).

Key reasons and current status (as of early 2026):

- **Web Analytics API access is very limited**
  The only public endpoints related to Web Analytics are for **management** (e.g., list/create/delete sites via the RUM / site_info endpoints under `/accounts/{account_id}/rum/site_info`), not for querying metrics like visits, pageviews, or uniques.

- **No dedicated GraphQL or REST endpoint for Web Analytics metrics**
  The main **GraphQL Analytics API** (`https://api.cloudflare.com/client/v4/graphql`) covers proxied traffic (HTTP requests through Cloudflare), Workers, Firewall events, etc., but **does not include** data from the standalone Web Analytics beacon tracker. Community reports and docs confirm this separation.

- **No monthly rollups or long-term aggregation via API**
  Even for proxied zones, monthly unique visitors are not directly available (you'd need to sum daily data yourself over many days, but uniques can't be accurately summed across days anyway — Cloudflare itself doesn't expose true monthly uniques via API in most cases). For Web Analytics, there is no equivalent daily/hourly breakdown exportable via API.

### What you can do instead
1. **Manual export from dashboard (recommended for most users)**
   - Go to **Analytics & Logs** → **Web Analytics** → select your site (e.g., `username.github.io`)
   - View the **Visitors** or **Page views** chart
   - Use the date range picker to select a full month (or custom range)
   - Cloudflare shows totals for the selected period (e.g., "Total visitors: X" at the top, or sum the chart)
   - Export the data as CSV (button usually available in the top-right of the chart view) for any period you select — this is the easiest way to get monthly numbers without code.

2. **If you need automation / programmatic access**
   - Switch your blog to **Cloudflare Pages** (free, import from GitHub repo in ~2 minutes) → enable built-in Web Analytics there → still JS-based, but Cloudflare auto-handles injection.
     Unfortunately, even Cloudflare Pages Web Analytics metrics are **not exposed via public API** (same limitation).
   - Use a third-party analytics tool with API support (e.g., Plausible, Fathom, Umami, PostHog, or even self-hosted Matomo) — most have REST/GraphQL APIs for monthly aggregates.
   - For very custom needs, some users scrape the dashboard (not recommended, against TOS, fragile), or use browser automation tools.

In short: For pure Web Analytics (non-proxied, token-based setup like yours), **monthly visits are dashboard-only** — no API endpoint exists to fetch them programmatically.

**References:**

- [Cloudflare Web Analytics docs - About](https://developers.cloudflare.com/web-analytics/about)
- [GraphQL Analytics API docs](https://developers.cloudflare.com/analytics/graphql-api)
- [Cloudflare Community - API for Web Analytics](https://community.cloudflare.com/t/api-for-web-analytics/644351)
- [Cloudflare API - RUM / Site Info endpoints](https://developers.cloudflare.com/api/resources/rum/subresources/site_info/methods/list) (management only, no metrics)
