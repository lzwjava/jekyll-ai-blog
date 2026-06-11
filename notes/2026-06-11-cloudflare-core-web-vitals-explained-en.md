---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cloudflare Core Web Vitals Explained
translated: false
type: note
---

**Question:** What do LCP, INP, and CLS (Core Web Vitals) mean in Cloudflare's dashboard?

**Answer:**

These are Google's Core Web Vitals — three user-experience metrics measured from real visitors' browsers (RUM, real user monitoring). Cloudflare surfaces them in **Web Analytics** (and Observatory) by injecting a small beacon script that reports what actual users experienced, then aggregates the 75th percentile per metric.

What each one measures:

**LCP — Largest Contentful Paint** (loading speed)
Time from navigation start until the largest visible element (hero image, big `<h1>`, video poster) finishes rendering.
- Good: ≤ 2.5s | Needs improvement: 2.5–4s | Poor: > 4s
- Dominated by: TTFB, render-blocking CSS/JS, image size, server location. Cloudflare levers: caching at edge, Polish/image resizing, Early Hints, HTTP/3.

**INP — Interaction to Next Paint** (responsiveness)
Worst-case latency between a user interaction (click, tap, keypress) and the next frame paint. Replaced FID in March 2024 because FID only measured the *first* input's delay; INP samples all interactions across the session.
- Good: ≤ 200ms | Needs improvement: 200–500ms | Poor: > 500ms
- Dominated by: long main-thread JS tasks, heavy event handlers, hydration cost. This is almost entirely your client-side JS — Cloudflare can't fix it for you (though deferring third-party scripts via Zaraz helps).

**CLS — Cumulative Layout Shift** (visual stability)
Unitless score summing how much visible content unexpectedly jumps around during load (images without `width`/`height`, late-injected ads, web fonts swapping).
- Good: ≤ 0.1 | Needs improvement: 0.1–0.25 | Poor: > 0.25

Quick local check before trusting the dashboard:

```bash
npx lighthouse https://lzwjava.github.io --only-categories=performance --view
```

Or measure in the browser console with the same library Cloudflare's beacon uses:

```js
import {onLCP, onINP, onCLS} from 'https://unpkg.com/web-vitals@4?module';
onLCP(console.log); onINP(console.log); onCLS(console.log);
```

One caveat on Cloudflare's numbers: they're field data from your actual traffic, so they'll differ from Lighthouse lab runs (lab uses throttled synthetic devices). If Cloudflare shows poor LCP but Lighthouse looks fine, your real users are likely far from your origin or on slow networks — exactly the case edge caching solves. For a GitHub Pages blog like yours, LCP and CLS are the ones worth watching; INP is rarely an issue on static sites with minimal JS.
