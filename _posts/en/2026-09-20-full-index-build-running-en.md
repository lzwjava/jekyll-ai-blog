---
audio: false
generated: true
image: false
lang: en
layout: post
title: Full Index Build Running
translated: false
type: note
---

The full index build is already running in the background (PID 888226, 20k/186k chunks, ~40 min ETA). Everything else is ready — here are the commands.

## 1. Watch the running build

```bash
cd /mnt/data/zz/rag
tail -f logs/build_bge_m3.log
```

Done when you see `Done. Index in /mnt/data/zz/rag/rag_index/`. (It ends with `wrote index.faiss`, a `bm25:` line, then `Done.`)

## 2. If it dies or you want to (re)start it

```bash
cd /mnt/data/zz/rag
nohup .venv/bin/python build_index.py --batch-size 32 --max-seq-length 1024 \
  > logs/build_bge_m3.log 2>&1 &
```

Fast alternative (~12 min instead of ~80 min, slightly lower quality) into a separate index:

```bash
cd /mnt/data/zz/rag
.venv/bin/python build_index.py --model intfloat/multilingual-e5-small \
  --out-dir rag_index_e5 --batch-size 32
```

## 3. Retrieval (no LLM) — after the build finishes

```bash
cd /mnt/data/zz/rag
.venv/bin/python search.py "how to export a Qwen3 LoRA to GGUF" --k 5
.venv/bin/python search.py "正则表达式" --k 5 --lang zh
.venv/bin/python search.py "vllm 部署" --alpha 0.0 --k 5   # BM25 only
.venv/bin/python search.py --interactive
```

## 4. RAG chat (llama.cpp + `finetune/lzw-notes-merged_gguf`)

```bash
cd /mnt/data/zz/rag
.venv/bin/python rag_chat.py --question "How do I merge a LoRA adapter and export it to GGUF?"
.venv/bin/python rag_chat.py --interactive
.venv/bin/python rag_chat.py -q "正则表达式" --backend none --show-context   # retrieval only
```

Other backends: `--backend hf --model ../finetune/lzw-notes-merged`, `--backend vllm --model ../finetune/lzw-notes-merged`.

## 5. Retrieval eval (fills the README results table)

```bash
cd /mnt/data/zz/rag
.venv/bin/python eval_rag.py --k 10                    # hybrid
.venv/bin/python eval_rag.py --mode dense --k 10
.venv/bin/python eval_rag.py --mode bm25 --k 10
```

## 6. Only if you ever need to recreate the env

```bash
cd /mnt/data/zz/rag
python3 -m venv --system-site-packages .venv
.venv/bin/pip install -r requirements.txt
```

Status: `rag/` contains `retriever.py`, `bm25.py`, `build_index.py`, `search.py`, `rag_chat.py`, `eval_rag.py`, `README.md`, `requirements.txt`; the venv is installed and smoke-tested (build + hybrid search + llama.cpp generation all verified on a 423-chunk test index). The only thing left is the full 186k-chunk index currently embedding.