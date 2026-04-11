---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cloudflare Analytics Sampling Explained
translated: false
type: note
---

Question: What does “sample by 10% requests” in Cloudflare mean? And why do all path counts end with 0?

Answer:

When Cloudflare shows **“sampled by 10% requests”**, it means:

* Cloudflare **does NOT count every request**
* It only **records about 10% of traffic**
* Then it **scales the numbers up** to estimate totals

Example:

* Real requests = 53,270
* Cloudflare samples 10% → collects ≈ 5,327
* Then multiplies by 10 → reports **≈ 53,270 (estimated)**

Cloudflare explicitly states that when sampling is 10%, it **samples a subset and multiplies to estimate the full dataset**. ([Cloudflare Docs][1])

---

## Why all numbers end with 0

Yes — this is exactly because of **10% sampling**.

If Cloudflare:

* samples 1 out of 10 requests
* then multiplies results by **10**

All returned values will usually be:

* multiples of **10**
* sometimes **rounded**
* sometimes slightly off

So you get:

```
430
290
210
170
150
130
120
```

instead of:

```
427
291
213
168
152
131
119
```

Because the **real counts are estimated**, not exact.

---

## Important: your data is approximate

This affects:

* Referers
* Paths
* Countries
* User agents
* Bots
* etc.

But NOT usually:

* total requests
* bandwidth
* top-level metrics

Cloudflare does this because your site may have **millions of events**, and sampling lets analytics load quickly. ([Cloudflare Docs][2])

---

## How to interpret your screenshot

Your data means:

* `None (direct)` → ~53k direct visits (estimated)
* `cn.bing.com` → ~750 visits (maybe actually ~734–766)
* `/upgrade-claude-code-en` → ~430 visits (estimated)

These are **trend-accurate**, not exact.

---

## When sampling happens

Cloudflare uses sampling when:

* traffic is high
* query is complex
* long time range selected
* many dimensions (referer + path + UA)

Then it switches to:

* 100% data (small traffic)
* 10% data (medium traffic)
* 1% data (very large traffic)

---

## Bottom line

Yes:

* "sample by 10%" → Cloudflare only looks at 1/10 of traffic
* numbers are **estimated**
* values often **end with 0**
* your interpretation is correct

Your analytics are **directionally correct**, not precise.

[1]: https://developers.cloudflare.com/analytics/graphql-api/sampling/?utm_source=chatgpt.com "Sampling · Cloudflare Analytics docs"
[2]: https://developers.cloudflare.com/analytics/sampling/?utm_source=chatgpt.com "Understanding sampling in Cloudflare Analytics · Cloudflare Analytics docs"