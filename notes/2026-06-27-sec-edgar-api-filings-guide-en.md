---
audio: false
generated: true
image: false
lang: en
layout: post
title: SEC EDGAR API Filings Guide
translated: false
type: note
---

Question: What is this? (referring to the SEC EDGAR mention)

Answer:

There's no image or file in your message — just the text "SEC EDGAR filings (10-K, 10-Q, 8-K, etc.)." So I'll answer what that string refers to.

**EDGAR** (Electronic Data Gathering, Analysis, and Retrieval) is the SEC's public system where U.S. public companies file mandatory disclosures. Free, full-text searchable, with a clean JSON/REST API — which makes it a great data source for AI/agent pipelines.

The filing types:

- **10-K** — annual report. Audited financials, risk factors, MD&A. The big one.
- **10-Q** — quarterly report. Unaudited, lighter than the 10-K.
- **8-K** — material events between periodic reports (acquisitions, exec changes, bankruptcy, etc.). Filed ad hoc.

For your purposes, the useful part is the API. Everything's keyed by CIK (Central Index Key):

```bash
# Resolve ticker -> CIK
curl -s 'https://www.sec.gov/files/company_tickers.json' \
  -H 'User-Agent: <​EMAIL>' | jq '.[] | select(.ticker=="AAPL")'

# All filings metadata for a CIK (zero-padded to 10 digits)
curl -s 'https://data.sec.gov/submissions/CIK0000320193.json' \
  -H 'User-Agent: <​EMAIL>' | jq '.filings.recent.form'

# XBRL financial facts (structured, no HTML parsing)
curl -s 'https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json' \
  -H 'User-Agent: <​EMAIL>'
```

The `companyconcept`/`companyfacts` XBRL endpoints give you clean structured financials (revenue, EPS, etc.) as JSON — skip the messy HTML filing parsing entirely. SEC requires a `User-Agent` header with contact info or they 403 you. Rate limit is 10 req/s.

AI-native angle: pipe the 10-K's MD&A and risk-factor sections into an LLM for diffing year-over-year changes, or build a retrieval agent over the full-text search endpoint (`https://efts.sec.gov/LATEST/search-index?q=...`).

References:

- [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- [EDGAR full-text search](https://efts.sec.gov/LATEST/search-index)
