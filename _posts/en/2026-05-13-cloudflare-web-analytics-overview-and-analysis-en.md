---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cloudflare Web Analytics Overview and Analysis
translated: false
type: note
---

Question: What can you do in Cloudflare Web Analytics (like checking visited URLs, countries, etc.), and can you analyze the report from lzwjava.github.io?

Answer:

## What Cloudflare Web Analytics Can Do

Cloudflare Web Analytics offers interactive exploration in Core Web Vitals by allowing you to filter data by **URL, Browser, Operating System, Country, and Element**. It is a privacy-first, cookie-less tool — it collects performance data via a lightweight JavaScript beacon directly from the user's browser without tracking users or storing client-side state.

Key things you can check:

- **Which URLs are being visited** — see which pages get the most traffic
- **What countries visitors come from**
- **Which browsers and operating systems are used**
- **Core Web Vitals per page** — LCP, INP, CLS for each URL
- **Debug View** — pinpoints the exact DOM elements causing performance issues
- **Page load metrics** — percentile breakdowns (P50, P75, P90, P99)

---

## Analysis of lzwjava.github.io (Apr 13 – May 13, 2026)

### 1. Largest Contentful Paint (LCP) — Loading Speed

**Result: 89% Good / 5% Needs Improvement / 6% Poor**

A good LCP score is under 2.5 seconds. Your site is largely passing, but the outliers are concerning:

| Percentile | Value | Assessment |
|---|---|---|
| P50 (median) | 560ms | Excellent |
| P75 | 1,404ms | Good |
| P90 | 2,608ms | Borderline / Needs Improvement |
| P99 | 11,368ms | Very Poor |

The P99 spike of **11 seconds** suggests that a small group of users (possibly on slow networks or mobile) experience very slow loads. The heaviest-traffic URLs are `/notes-en`, `/` (homepage), `/notes-zh.html`, and `/index-zh.html`.

---

### 2. Interaction to Next Paint (INP) — Responsiveness

**Result: 98% Good / 2% Needs Improvement / 0% Poor**

INP measures a page's overall responsiveness to user interactions by observing the latency of all clicks, taps, and keyboard interactions. This is an excellent score.

However, the **Debug View** reveals two specific elements with slow interactions:

- `#moonIcon > path` — **312ms** (10 counts) — this is likely the dark mode toggle button
- `html.dark-mode > body` — **472ms** (10 counts) — this suggests the dark mode switch triggers a slow repaint of the entire page body

A good INP threshold is under 200ms. Both of these are above the threshold, meaning the dark mode toggle is the main interactivity bottleneck on your site.

---

### 3. Cumulative Layout Shift (CLS) — Visual Stability

**Result: 100% Good / 0% Needs Improvement / 0% Poor**

A good CLS score is under 0.1. Your site scores perfectly here — no unexpected layout shifts affecting users.

However, the Debug View shows one element of note:

- `#content > div.language-bash.highlighter-rouge > div.highlight > pre.highlight` — CLS score of **0.301** (10 counts)

This means a **bash code block** in one of your notes pages is causing layout shift with a score of 0.301, which technically falls in the "poor" range (above 0.1). It affects only 10 page views, so it is not widespread, but it is worth fixing (e.g., by reserving space for code blocks or using `overflow: auto`).

---

## Summary & Recommendations

| Metric | Score | Status |
|---|---|---|
| LCP | 89% Good | ✅ Mostly fine; investigate P99 spike |
| INP | 98% Good | ✅ Great; fix dark mode toggle lag |
| CLS | 100% Good | ✅ Perfect overall; fix bash code block shift |

**Top action items:**

1. **Dark mode toggle** (`#moonIcon`) is slow at 312–472ms — consider debouncing or optimizing the CSS class swap instead of repainting the whole body.
2. **Bash code blocks** cause a CLS of 0.301 — add fixed dimensions or `min-height` to prevent layout shift when they load.
3. **P99 LCP of 11s** — investigate if large images or render-blocking resources affect slow visitors, especially on the homepage (`lzwjava.github.io/`).

References:

- [Cloudflare Core Web Vitals Docs](https://developers.cloudflare.com/web-analytics/data-metrics/core-web-vitals/)
- [Core Web Vitals Explained (2026)](https://www.corewebvitals.io/core-web-vitals)
- [Cloudflare Vitals Explorer Blog](https://blog.cloudflare.com/web-analytics-vitals-explorer/)
