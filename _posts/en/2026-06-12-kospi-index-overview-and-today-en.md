---
audio: false
generated: true
image: false
lang: en
layout: post
title: KOSPI Index Overview and Today
translated: false
type: note
---

**Question:** What is the KOSPI index, and where does it stand now?

**Answer:**

The KOSPI (Korea Composite Stock Price Index) is South Korea's primary stock market benchmark, tracking major companies listed on the Korea Exchange (KRX). It's a free-float market-cap-weighted index launched in 1980 with a base value of 100, dominated by tech/export giants like Samsung Electronics and SK hynix — so it's effectively a proxy for the global semiconductor and AI hardware cycle.

Current state (as of the last close): the KOSPI closed at 8,123.62, up 4.63% (+359.67), rebounding from a previous close of 7,763.95. It's been extremely volatile lately — it plunged 4.52% to 7,731 on Wednesday amid escalating US–Iran tensions and a US chipmaker selloff that hit Samsung and SK hynix hard, then snapped back. Zooming out, the index is in a historic AI-driven bull run: it hit an all-time high of 8,933.62 on June 2, 2026, and is up ~179% year-over-year, with a 52-week range of roughly 2,877 to 8,934 — nearly a 3x in a year, which explains why valuations are being questioned. Foreign investors have recently been dumping Korean stocks, and Barclays argued Japan's Nikkei is currently a safer bet than the Kospi.

Quick reference: ticker is `^KS11` (Yahoo) / `KS11` (Investing.com), priced in KRW, trades 9:00–15:30 KST. If you want to pull it programmatically:

```python
import yfinance as yf
kospi = yf.Ticker("^KS11")
print(kospi.history(period="5d")[["Close"]])
```

**References:**

- [KOSPI Composite Index — Yahoo Finance](https://finance.yahoo.com/quote/%5EKS11/)
- [South Korea Stock Market — Trading Economics](https://tradingeconomics.com/south-korea/stock-market)
- [KOSPI — CNBC](https://www.cnbc.com/quotes/.KS11)
