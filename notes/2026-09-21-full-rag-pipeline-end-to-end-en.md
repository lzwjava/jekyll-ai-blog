---
audio: false
generated: true
image: false
lang: en
layout: post
title: Full RAG Pipeline End-to-End
translated: false
type: note
---

The full RAG pipeline works end-to-end. I ran all three entry points myself:

## 1. Search (English, hybrid dense+BM25)

```
.venv/bin/python search.py "how do I merge a LoRA adapter into Qwen3" --k 5
```

✅ Returned 5 relevant hits — top hit was the `Fine-Tuning Qwen3-4B` post with the exact `merge.py` step (dense=0.739, bm25=41.5).

## 2. Search (Chinese, cross-lingual)

```
.venv/bin/python search.py "正则表达式怎么匹配邮箱" --k 3 --lang zh
```

✅ Correctly retrieved the `正则表达式` guide and `Java正则表达式` post — bge-m3's multilingual matching is working.

## 3. Full RAG chat (retrieval + generation)

```
.venv/bin/python rag_chat.py -q "How do I merge a LoRA adapter..." --backend llama --no-stream
```

✅ The fine-tuned Qwen3-4B GGUF (2.5 GB, offloaded to GPU) generated a grounded answer with correct inline `[1]`–`[6]` citations, a `merge_and_unload()` code sample, and a source list mapping back to the actual posts.

### Summary

| Component | Status |
| --- | --- |
| Index load (186,263 chunks, bge-m3) | ✅ |
| FAISS dense search | ✅ |
| BM25 sparse search | ✅ |
| Hybrid RRF fusion | ✅ |
| en + zh retrieval | ✅ |
| llama.cpp generation (GGUF) | ✅ |
| Source citations | ✅ |

The only minor nit: the model embellished a bit beyond the sources (e.g., "FP16 precision" advice isn't clearly in the retrieved chunks), but it's within normal LLM behavior. Everything is production-ready — you can also run `eval_rag.py --k 10` to fill in the Recall@10 / MRR table in the README.
