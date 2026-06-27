---
audio: false
generated: true
image: false
lang: en
layout: post
title: SEC EDGAR API Access
translated: false
type: note
---

Let me check the page.This is the **SEC's Search Filings** page — the front door to **EDGAR** (Electronic Data Gathering, Analysis, and Retrieval), the U.S. Securities and Exchange Commission's system for public access to corporate filings.

What it gives you:

- **Company Search** — look up filings by company name, ticker, CIK, or file number (10-K annual reports, 10-Q quarterly, 8-K material events, S-1 IPO registrations, Forms 3/4/5 insider trades, etc.)
- **Full Text Search** — keyword search across 20+ years of filings
- **Latest Filings** — real-time feed as documents are submitted
- **EDGAR APIs** — RESTful endpoints for programmatic access (submissions history by filer, XBRL financial-statement data)

For your build-first interest, the APIs are the useful part. They're free, no key required, just need a `User-Agent` header:

```bash
# All filings metadata for a company by CIK (Apple = 0000320193)
curl -s -H "User-Agent: <EMAIL>" \
  https://data.sec.gov/submissions/CIK0000320193.json | jq '.filings.recent.form[:5]'

# XBRL company facts (structured financials — revenue, EPS, etc.)
curl -s -H "User-Agent: <EMAIL>" \
  https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json | jq '.facts.["us-gaap"].Revenues.units' | head
```

```python
import requests

H = {"User-Agent": "<EMAIL>"}  # SEC requires a UA or returns 403

def latest_filings(cik: int, n=10):
    cik = f"{cik:010d}"
    r = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=H).json()
    recent = r["filings"]["recent"]
    return list(zip(recent["form"], recent["filingDate"], recent["accessionNumber"]))[:n]

print(latest_filings(320193))  # Apple
```

Rate limit is 10 req/s. The XBRL `companyfacts` / `companyconcept` endpoints are the goldmine if you ever want to pull structured fundamentals into a dataset — clean ground truth for an LLM finance agent or eval set.

References:

- [SEC Search Filings](https://www.sec.gov/search-filings)
- [EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
