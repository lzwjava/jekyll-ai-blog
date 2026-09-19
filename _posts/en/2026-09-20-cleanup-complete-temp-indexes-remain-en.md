---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cleanup Complete, Temp Indexes Remain
translated: false
type: note
---

Killed — process is gone, GPU is idle (1.2 GB used by the desktop), and `rag_index/` is empty (nothing was written yet, since writes only happen after all embeddings finish).

What's left in place:

- `rag/` scripts + `README.md` + `requirements.txt` + working `.venv`
- Smoke-tested indexes at `/tmp/rag_smoke` (e5-small, 423 chunks) and `/tmp/rag_m3` (bge-m3, 652 chunks)
- `rag/logs/build_bge_m3.log` (partial run, ~20k/186k chunks)

Say the word if you want me to run it again (full, or the fast `--model intfloat/multilingual-e5-small` variant) or clean up the temp indexes.
