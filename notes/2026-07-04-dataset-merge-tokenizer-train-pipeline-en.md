---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dataset Merge Tokenizer Train Pipeline
translated: false
type: note
---

Question: Is this the correct workflow for completing dataset merging, tokenizer training, and then starting Nanochat training once the downloads finish?

Answer:

Yes — your pipeline is fundamentally correct, and the order you laid out is the standard and sensible progression for training a small LLM from mixed corpora. The only thing worth doing is tightening a few operational details to avoid silent issues during the merge step and validation split.

### 1. Overall pipeline correctness

Your intended flow:

1. Finish dataset downloads (FineWeb-Edu + existing datasets)
2. Create unified dataset directory (`NANOCHAT_DATA_DIR`)
3. Merge / standardize all shards
4. Train tokenizer on full mixed corpus
5. Launch base training (`base_train`)

This is correct and matches how most nanoGPT-style or nanochat-style pipelines are structured.

---

### 2. Key things to double-check (important)

#### A. File format consistency

You already have:

* GitHub code → parquet with `text`
* SEC EDGAR → parquet with `text`
* FineWeb → likely JSONL or parquet (depending on loader)

Make sure all datasets end up in a **single consistent schema**, e.g.:

```text
text: string
```

If FineWeb-Edu is not yet converted to parquet, do that during the final step, not during training.

---

#### B. Validation split rule (your note is slightly risky)

> “last alphabetically file becomes validation set”

This is simple but can be **unstable**.

Better options:

* Random 0.5–1% sampling across all shards (recommended)
* Or explicitly reserve FineWeb-Edu last shard as validation (OK but biased)

If you keep your method, just ensure:

* File ordering is deterministic (`ls -1`)
* No later reordering changes the split accidentally

---

#### C. Merging step (missing explicit command)

You currently describe copying files, but most pipelines benefit from a **single merge script step**, e.g.:

* concatenate parquet shards
* or build an index manifest like:

```json
[
  {"path": ".../github/*.parquet"},
  {"path": ".../sec/*.parquet"},
  {"path": ".../fineweb/*.parquet"}
]
```

This avoids duplication and makes tokenizer training reproducible.

---

#### D. Tokenizer training dependency

Make sure:

* tokenizer is trained on **final merged corpus only**
* not on partial FineWeb (you’re currently mid-download)

Otherwise vocabulary distribution will shift after training starts.

---

#### E. Training command sanity check

Your training config:

```bash
--depth=12
--device-batch-size=8
--max-seq-len=2048
--window-pattern=L
--num-iterations=50000
```

This is reasonable for ~300M-scale models on a 4070-class GPU, but:

* 50k iterations may be low depending on tokens (~100B+ tokens → likely undertrained)
* monitor:

  * loss plateau
  * validation perplexity
  * tokens/sec stability

You may later want:

* 100k–300k iterations for better convergence

---

### 3. Execution readiness check (what you should wait for)

You can safely proceed when:

* FineWeb download = 9/9 shards complete
* All parquet files verified readable
* Total dataset size stable (~34GB as expected)
* Disk headroom still >20GB (for shuffle + tokenization cache)

---

### 4. Summary

Yes, your plan is correct:

* download → unify → tokenize → train → evaluate

The only real improvements are:

* make validation split more stable (optional but recommended)
* ensure tokenizer is trained on final merged dataset
* consider a cleaner dataset manifest instead of manual copying

Once FineWeb finishes, your next step is exactly:

1. finalize dataset directory
2. run tokenizer training
3. start `base_train`

If you want, I can help you turn this into a **single reproducible bash + Python pipeline (one-command training setup)**.