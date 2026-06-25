---
audio: false
generated: true
image: false
lang: en
layout: post
title: SEC-EDGAR 10-K Download Summary
translated: false
type: note
---

## SEC-EDGAR Dataset — Session Summary

**Dataset:** kapilrao/SEC-EDGAR on HuggingFace
**Source:** SEC EDGAR filings (10-K, 10-Q, 144, 20-F, 3, 4, 5, 8-K, S-1, S-8)
**Total available:** 2,551 shards, 274.8 GB

---

**What we downloaded:**

- Target: ~10 GB
- Downloaded: 17 shards of 10-K (annual reports), 10 GB total
- Location: `/mnt/data/zz/datasets/sec-edgar/10-K/`
- Rows: ~26,000 filings
- Time: ~55 min (first run) + 30 sec (retry)
- Speed: ~3 MB/s per shard, ~222 MB/s on retry (cached by CDN)

**File format (parquet schema):**

- `content` — raw HTML
- `text` — cleaned plain text
- `metadata_accession-number` — SEC accession ID
- `metadata_filing-date` — YYYYMMDD
- `metadata_period` — fiscal period end date
- `metadata_filer` — JSON with company name, CIK, SIC, state
- `metadata_documents` — JSON with filing document metadata

**Corrupt shard:**

- `002137a1-6454-4dca-9582-93b9d177efde-90.parquet` — broken upstream on HuggingFace (654 MB, correct size, but unreadable parquet). Deleted.

---

**Scripts created & pushed:**

| Script | Purpose | Commit |
|--------|---------|--------|
| `scripts/download/download_sec_edgar.py` | Download shards with size cap, skip cached, resume | `378bcdb` |
| `scripts/download/view_sec_edgar.py` | View/list/search samples from parquet files | `93138ec` + `70f83b5` |
| `scripts/download/fix_corrupt_shard.sh` | Re-download the broken shard (useless now) | `d153ec5` |

**Viewer commands:**

```
python3.11 scripts/download/view_sec_edgar.py --list
python3.11 scripts/download/view_sec_edgar.py --sample
python3.11 scripts/download/view_sec_edgar.py --sample -n 3 --text-only --chars 500
python3.11 scripts/download/view_sec_edgar.py --search "risk factors"
python3.11 scripts/download/view_sec_edgar.py --file 10-K/<shard>.parquet --head 5
```

**To get more data:** increase `--target-gb` (274.8 GB available across all filing types).
