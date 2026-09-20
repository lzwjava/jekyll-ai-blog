---
audio: false
generated: true
image: false
lang: en
layout: post
title: Embedding and Index Pipeline Complete
translated: false
type: note
---

The embedding is **done** ✅

From tmux session `2`:

- **Embedding**: finished all **186,263/186,263 chunks** (~58/s)
- **Outputs written** to `/mnt/data/zz/rag/rag_index/`:
  - `embeddings.npy` — (186263, 1024) float32
  - `index.faiss` — 186,263 vectors
  - `chunks.jsonl` — 186,263 records
- **BM25 index**: built successfully — 628,745 terms, 16,397,020 postings, avg doc length 114.7 (took 9.8s)

The whole pipeline completed and you're back at the shell prompt. You can now:
- `python search.py "your query"`
- `python rag_chat.py --question "your question"`