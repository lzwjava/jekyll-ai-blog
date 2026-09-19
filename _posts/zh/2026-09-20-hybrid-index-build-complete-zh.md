---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 混合索引构建完成
translated: true
type: note
---

这就是 `python build_index.py` 成功完成后的尾部输出。逐行解释如下：

## 1. `embedded …` 进度行
来自 `/mnt/data/zz/rag/build_index.py` 中的 `encode_chunks()` 函数。它每 10 个批次打印一次，使用默认的 `--batch-size 32` 时，即每 **320 个块** 打印一次——因此计数呈现 +320 的固定跳变。这些计数含义如下：

- `186,263` = 语料库中文本块的总数
- `461/s` = 编码器（GPU）的每秒处理块数吞吐量
- `ETA 0.0 min` = 剩余时间估计

## 2. 三行 "wrote …" = 稠密索引产物

| 文件 | 含义 |
|---|---|
| `embeddings.npy`（273 MB） | `(186263, 384) float32` — 每个块的原始向量 |
| `index.faiss`（273 MB） | `IndexFlatIP` — 相同向量的 FAISS 副本，用于快速余弦搜索（向量经过 L2 归一化，因此内积等于余弦相似度） |
| `chunks.jsonl`（281 MB） | FAISS 第 *i* 行所指向的实际源记录（每行一个 JSON） |

`IndexFlatIP` 是**精确/暴力搜索**类型——没有近似，但每次查询都会扫描整个 186k × 384 的矩阵。

## 3. BM25 块 = 稀疏索引
```
628,745 个词项，16,397,020 个倒排记录，186,263 个文档，avgdl 114.7
```
- `628,745` 个词汇表中的唯一词元
- `16,397,020` 条 (term, doc, tf) 倒排记录总数 → 每个块约 88 个词元
- `avgdl 114.7` = 平均文档长度（以词元计）（用于 BM25 长度归一化）
- 用时 9.7 秒构建完成 → 写入 `bm25_postings.npy`、`bm25_offsets.npy`、`bm25_vocab.txt`、`bm25_doclen.npy`、`bm25_meta.json`

因此，您现在拥有一个**混合检索索引**：稠密（FAISS）+ 稀疏（BM25），由 `retriever.py` 进行融合。

## 4. 语料库事实（来自 `rag_index_e5/index_meta.json`）
- 模型：`intfloat/multilingual-e5-small`，维度 `dim=384`
- 来源：`/home/lzw/projects/jekyll-ai-blog/_posts`
- 共 108,533 个英文块 + 77,730 个中文块
- 分块方式：900 字符，150 字符重叠
- 构建时间：2026-09-19，磁盘占用约 962 MB

## 5. 两件值得了解的事项
1. **e5 前缀很重要。** `passage_prefix()` 在索引时添加 `"passage: "` 前缀，`query_prefix()` 在搜索时添加 `"query: "` 前缀。由于此索引是使用 e5 模型构建的，查询必须通过 `retriever.py`/`search.py` 进行——它们会处理这个问题。如果您手动嵌入查询而不加 `"query: "` 前缀，召回率会明显变差。
2. **`rag_index/`（4 KB）是空的**——只有 `rag_index_e5/` 被填充。您之前的文档/`--out-dir` 默认值指向 `rag_index`，因此请传递 `--out-dir rag_index_e5`（或使用 `search.py` 的默认值）以保持一致。

接下来的步骤正是它打印的内容：
```bash
python search.py "您的查询"
python rag_chat.py --question "您的问题"
```

由于索引包含约 1 GB 的数组，预计每次搜索进程会加载数百 MB 到内存中。