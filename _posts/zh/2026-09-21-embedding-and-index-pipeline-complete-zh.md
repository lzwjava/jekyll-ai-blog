---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 嵌入与索引管线完成
translated: true
type: note
---

embedding 已完成 ✅

来自 tmux 会话 `2`：

- **Embedding**：已完成所有 **186,263/186,263 chunks**（约 58/s）
- **输出已写入**到 `/mnt/data/zz/rag/rag_index/`：
  - `embeddings.npy` — (186263, 1024) float32
  - `index.faiss` — 186,263 vectors
  - `chunks.jsonl` — 186,263 records
- **BM25 索引**：构建成功 — 628,745 个词项，16,397,020 个 posting，平均文档长度 114.7（耗时 9.8 秒）

整个流程已完成，你已返回 shell 提示符。现在你可以：
- `python search.py "your query"`
- `python rag_chat.py --question "your question"`