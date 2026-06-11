---
audio: false
generated: true
image: false
lang: en
layout: post
title: The Stack v2 Dataset Overview
translated: false
type: note
---

**Question:** Give me an introduction to The Stack v2 dataset (huggingface.co/datasets/bigcode/the-stack-v2).

**Answer:**

The Stack v2 is the pretraining corpus behind StarCoder2, built by the BigCode project (Hugging Face + ServiceNow). It's the dataset to study if you care about how production-grade code LLMs source their data — and it's directly relevant to your nanoGPT/nanochat training work as a reference for what serious dataset engineering looks like.

**Scale and what changed from v1**

The full dataset is 67.5TB uncompressed (vs 6.4TB for v1), dedup is 32.1TB (vs 2.9TB), and the full training set is ~900B tokens (vs ~200B). It contains over 3B files across 658 programming and markup languages.

The key architectural shift: v1 scraped GitHub directly; v2 is derived from the Software Heritage archive — 3.28B unique files from 104.2M GitHub repositories, collected by traversing the SWH 2023-09-06 graph dataset, with repo metadata joined from GH Archive. This gives provenance (SWHIDs), better governance, and an opt-out path.

**The catch: it's an index, not the bytes**

The HF dataset only contains SWHIDs (blob IDs) plus metadata — the actual file contents live in Software Heritage's S3 bucket, and bulk download requires an agreement with Software Heritage/INRIA. So the workflow is: stream the parquet index from HF, then fetch blobs from `s3://softwareheritage/content/{blob_id}` yourself:

```python
import os, boto3
from smart_open import open as sopen
from datasets import load_dataset

s3 = boto3.Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
).client("s3")

def fetch(row):
    url = f"s3://softwareheritage/content/{row['blob_id']}"
    with sopen(url, "rb", compression=".gz", transport_params={"client": s3}) as f:
        return {"content": f.read().decode(row["src_encoding"])}

ds = load_dataset("bigcode/the-stack-v2", split="train", streaming=True)
ds = ds.map(fetch)
```

(`pip install 'smart_open[s3]' datasets boto3`. It's also gated — you accept terms on HF first.)

**The four variants**

There are 4 versions: the full `the-stack-v2`; `the-stack-v2-dedup` (near-deduplicated); `the-stack-v2-train-full-ids` (heuristic-filtered, 600+ languages, grouped by repository); and `the-stack-v2-train-smol-ids` (same but filtered to 17 languages). For a nanoGPT-scale code-model experiment, `smol-ids` is the practical choice. The repository grouping matters: it lets you pretrain with full-repo context (cross-file dependencies), which is part of why StarCoder2 handles repo-level completion well.

**Pipeline details worth stealing**

- Dedup: near-deduplication on top of exact dedup; roughly 40% of permissively licensed files were near-duplicates — that number alone justifies MinHash/LSH pipelines for any code corpus you build.
- Filtering: binary, empty, undecodable files and files >10MB are dropped; language detection via `go-enry`/linguist, with `is_vendor` and `is_generated` flags per file.
- Licensing: repo-level licenses come from GH Archive, but for the 96.93% of repos without one, ScanCode detects file-level licenses from LICENSE/README-style files and propagates them down the directory tree. Each row carries `detected_licenses` (SPDX) and `license_type`.
- Useful metadata per row: `star_events_count`, `fork_events_count`, `revision_date`, `branch_name` — enough to do your own quality-weighted sampling (e.g., upweight high-star repos, recency-filter).

**Why it matters for you specifically**

If you move from nanoGPT-on-FineWeb-style runs to a code model on your MI300X, this is the canonical open corpus, and the StarCoder2 paper (arXiv:2402.19173) is effectively the dataset-engineering playbook: dedup ratios, language filtering heuristics, PII redaction, repo-context packing. Note the data card itself warns the dataset may still contain emails, IP addresses, and API/SSH keys published in public repos — so if you train on it, run your own secrets-scrubbing pass (e.g., detect-secrets or the BigCode PII pipeline) before tokenizing.

**References:**

- [bigcode/the-stack-v2 — Hugging Face](https://huggingface.co/datasets/bigcode/the-stack-v2)
- [StarCoder 2 and The Stack v2: The Next Generation (arXiv:2402.19173)](https://huggingface.co/papers/2402.19173)
- [BigCode Project](https://www.bigcode-project.org/)
