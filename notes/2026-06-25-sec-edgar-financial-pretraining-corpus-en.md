---
audio: false
generated: true
image: false
lang: en
layout: post
title: SEC EDGAR Financial Pretraining Corpus
translated: false
type: note
---

**Question:** What is the `kapilrao/SEC-EDGAR` dataset on Hugging Face?

**Answer:**

It's a massive financial document pretraining corpus — 590 GB, 8M filings, 43B tokens — scraped from the SEC EDGAR database. Built by Datamule, Teraflop AI, and Eventual.

**Schema per row:**

| Field | Description |
|---|---|
| `content` | Raw SEC SGML filing content |
| `text` | Parsed plaintext (HTML/XML stripped) |
| `metadata_accession-number` | Unique SEC filing ID |
| `metadata_filing-date` | Filing date |
| `metadata_period` | Period covered |
| `metadata_filer` | Company name, CIK, SIC code, address, etc. |
| `metadata_documents` | Filing type, sequence, description |

**Filing breakdown (token-heavy ones):**

- 10-Q: 17.5B tokens (quarterly reports)
- 10-K: 14.5B tokens (annual reports)
- 8-K: 3.5B tokens (material events)
- S-1: 2.9B tokens (IPO filings)
- 20-F: 2.9B tokens (foreign private issuers)

**Why it matters for you specifically:** You're an AI engineer at a global bank. This is exactly the kind of domain-specific corpus you'd use to:

1. **Fine-tune or continue-pretraining** a financial LLM (LoRA on Llama/Mistral using 10-K + 10-Q filings)
2. **Build RAG pipelines** over SEC filings for earnings analysis, risk disclosure extraction
3. **Train financial NER/classification** models (SIC codes are already in metadata — free labels)
4. **Evaluate LLMs on financial reasoning** — the structured metadata makes it easy to construct QA pairs

The `datamule-python` library is worth bookmarking too — it lets you pull filings by ticker + type programmatically, bypassing the 10 req/s EDGAR rate limit overhead.
