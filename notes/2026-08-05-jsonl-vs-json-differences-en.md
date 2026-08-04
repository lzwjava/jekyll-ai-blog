---
audio: false
generated: true
image: false
lang: en
layout: post
title: JSONL vs JSON Differences
translated: false
type: note
---

Question: Why is it called JSONL instead of JSON, and how do they differ?

Answer:

**JSONL = "JSON Lines"** — one valid JSON value per line, newline-delimited. Not a single JSON document.

```
{"id": 1, "prompt": "what is 2+2", "answer": "4"}
{"id": 2, "prompt": "capital of france", "answer": "paris"}
{"id": 3, "prompt": "1+1", "answer": "2"}
```

vs standard **JSON** — one single top-level value (usually an array wrapping everything):

```json
[
  {"id": 1, "prompt": "what is 2+2", "answer": "4"},
  {"id": 2, "prompt": "capital of france", "answer": "paris"},
  {"id": 3, "prompt": "1+1", "answer": "2"}
]
```

**Why JSONL exists — the actual reasons it wins for eval/training data:**

1. **Streaming/append-friendly.** You can `open(path, "a")` and append one line at a time as you generate eval results, without re-parsing or re-writing the whole file. A JSON array requires rewriting the entire structure (or careful bracket surgery) to append.

2. **No full-file parse required.** `json.load()` on a giant JSON array means loading the entire tree into memory before you can touch a single record. JSONL lets you stream line-by-line — that's why the generator pattern I gave you (`for line in f: json.loads(line)`) never holds more than one record in memory.

3. **Crash-resistant.** If a JSONL write gets truncated mid-run (OOM, kill -9), you lose only the last partial line — the rest of the file is still valid. A truncated JSON array is corrupt garbage from the first missing bracket onward, and `json.loads` fails on the entire file.

4. **Line-based tools just work.** `wc -l`, `grep`, `head`, `tail`, `split`, `sed`, `awk`, `jq` (in streaming mode) all operate naturally on lines. This is why every major eval harness (OpenAI evals, lm-eval-harness, your own eval scripts) and every LLM training pipeline (pretraining corpora, SFT datasets, RLHF preference pairs) standardized on it — you're literally shuffling, sharding, and concatenating training data with `cat` and `shuf` at the 2B-tokens/mo scale you're running.

5. **Trivial parallelism.** Split a JSONL file into N chunks for N workers with `split -n l/8 data.jsonl` — each chunk is independently valid. Splitting a JSON array requires understanding the structure.

**Tradeoffs of JSONL vs JSON:**

| | JSON | JSONL |
|---|---|---|
| Structure | one tree, arbitrary nesting at top level | flat list of independent records |
| Parse cost | full file must parse before use | parse incrementally, line by line |
| Append | requires rewrite | just write a new line |
| Corruption blast radius | whole file | one line |
| Pretty-print/readability | nicer for deeply nested single objects | nicer for tabular/record-shaped data |
| Tooling | `jq`, full JSON parsers | same tools + all Unix line tools |
| Not valid JSON itself | — | correct — a `.jsonl` file will fail `json.loads()` on the whole thing; you must split by line first |

Bottom line: JSON is for one structured document; JSONL is for a dataset — which is exactly why every eval/training corpus uses it.

References:
- [JSON Lines spec](https://jsonlines.org/)