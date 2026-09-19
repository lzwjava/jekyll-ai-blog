---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hybrid Index Build Complete
translated: false
type: note
---

That output is the tail end of `python build_index.py` finishing successfully. Line by line:

## 1. The `embedded …` progress lines
From `encode_chunks()` in `/mnt/data/zz/rag/build_index.py`. It prints every 10 batches, and with the default `--batch-size 32` that's every **320 chunks** — hence the constant +320 jumps. The counters mean:

- `186,263` = total number of text chunks in the corpus
- `461/s` = chunks-per-second throughput of the encoder (GPU)
- `ETA 0.0 min` = remaining time estimate

## 2. The three "wrote …" lines = the dense index artifacts

| File | Meaning |
|---|---|
| `embeddings.npy` (273 MB) | `(186263, 384) float32` — the raw vectors for every chunk |
| `index.faiss` (273 MB) | `IndexFlatIP` — FAISS copy of the same vectors for fast cosine search (vectors are L2-normalized, so inner product == cosine) |
| `chunks.jsonl` (281 MB) | The actual source records (one JSON per line) that FAISS row *i* points back to |

`IndexFlatIP` is **exact / brute-force** — no approximation, but the whole 186k × 384 matrix is scanned per query.

## 3. BM25 block = the sparse index
```
628,745 terms, 16,397,020 postings, 186,263 docs, avgdl 114.7
```
- `628,745` unique tokens in the vocabulary
- `16,397,020` (term, doc, tf) postings total → ~88 terms per chunk
- `avgdl 114.7` = average document length in tokens (used by the BM25 length normalization)
- built in 9.7 s → written as `bm25_postings.npy`, `bm25_offsets.npy`, `bm25_vocab.txt`, `bm25_doclen.npy`, `bm25_meta.json`

So you now have a **hybrid retrieval index**: dense (FAISS) + sparse (BM25), which `retriever.py` blends.

## 4. Corpus facts (from `rag_index_e5/index_meta.json`)
- Model: `intfloat/multilingual-e5-small`, `dim=384`
- Source: `/home/lzw/projects/jekyll-ai-blog/_posts`
- 108,533 English + 77,730 Chinese chunks
- Chunking: 900 chars with 150 char overlap
- Built 2026-09-19, ~962 MB on disk

## 5. Two things worth knowing
1. **e5 prefixing matters.** `passage_prefix()` prepends `"passage: "` at index time and `query_prefix()` prepends `"query: "` at search time. Since this index was built with an e5 model, queries must go through `retriever.py`/`search.py` — they handle it. If you embed a query manually without `"query: "`, recall will be noticeably worse.
2. **`rag_index/` (4 KB) is empty** — only `rag_index_e5/` is populated. Your earlier docs/`--out-dir` default says `rag_index`, so pass `--out-dir rag_index_e5` (or whatever `search.py` defaults to) to be consistent.

Next steps are exactly what it printed:
```bash
python search.py "your query"
python rag_chat.py --question "your question"
```

Since the index is ~1 GB of arrays, expect each search process to load a few hundred MB into RAM.