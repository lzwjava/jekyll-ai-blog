---
audio: false
generated: true
image: false
lang: en
layout: post
title: Google Trends API and Alternatives
translated: false
type: note
---

**Question:** Does Google Trends have an API?

**Answer:**

Yes — and it's actually a recent development. Here's the full picture:

---

## Official Google Trends API (Alpha, July 2025)

Google announced the official Google Trends API on July 24, 2025 — the first time they've shipped an API for Trends after years of requests.

Key facts:
- Data goes back 5 years — a rolling 1,800-day window, updated to within 2 days ago.
- It provides structured data: interest over time, top trends, and related queries.
- Currently in alpha with limited access — you have to apply. Google is doing a controlled rollout to gather feedback before wider availability.

Apply/read more: [developers.google.com/search/blog/2025/07/trends-api](https://developers.google.com/search/blog/2025/07/trends-api)

---

## Practical Alternatives (Since Alpha Access Is Restricted)

### 1. `pytrends` (unofficial Python wrapper)
The classic go-to, but increasingly unreliable:

```python
pip install pytrends

from pytrends.request import TrendReq
import pandas as pd

pt = TrendReq(hl='en-US', tz=360)
pt.build_payload(kw_list=['Claude AI', 'ChatGPT'], timeframe='today 12-m')

df = pt.interest_over_time()
print(df)

# Related queries
related = pt.related_queries()
print(related)
```

PyTrends is no longer actively maintained and breaks frequently as Google updates its internal endpoints — unreliable for production pipelines.

### 2. SerpApi (paid, reliable)
Paid scraping service with a proper Google Trends endpoint. Works well if you need stability:

```python
import serpapi

client = serpapi.Client(api_key="YOUR_KEY")
results = client.search({
    "engine": "google_trends",
    "q": "Claude AI",
    "date": "today 12-m"
})
print(results["interest_over_time"])
```

### 3. Apify Actor (free tier available)
A hosted alternative that handles cookie rotation, proxy management, and retry-on-429 automatically — no captchas, no IP rotation to manage yourself. Supports pytrends-style timeframe strings like `today 12-m`, `today 5-y`.

### 4. Glimpse API (enterprise)
Adds absolute search volume on top of Google Trends' 0–100 relative scores. More accurate for production dashboards.

---

## TL;DR

| Option | Cost | Stability | Notes |
|---|---|---|---|
| Official API | Free (alpha) | High | Need to apply |
| pytrends | Free | Low | Breaks often |
| SerpApi | Paid | High | Per-query pricing |
| Apify Actor | Free tier | Medium | Good for scripts |
| Glimpse | Paid (enterprise) | High | Absolute volume |

For your use case (building agents, CLI tools), I'd start with `pytrends` for quick prototyping and apply for official alpha access. If you're piping trend signals into an LLM pipeline at any scale, SerpApi or Glimpse is worth it over debugging `pytrends` 429s.

**References:**

- [Google Trends API Alpha announcement](https://developers.google.com/search/blog/2025/07/trends-api)
- [Best Google Trends Scraping APIs 2026 — ScrapingBee](https://www.scrapingbee.com/blog/best-google-trends-api/)
- [pytrends alternatives — Glimpse](https://meetglimpse.com/software-guides/pytrends-alternatives/)
- [Apify Free Google Trends Actor](https://apify.com/s-r/free-google-trends-scraper)