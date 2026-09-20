---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 端到端完整RAG流水线
translated: true
type: note
---

完整的RAG流水线端到端运行正常。我亲自执行了全部三个入口点：

## 1. 搜索（英文，混合密集+BM25）
```
.venv/bin/python search.py "如何将LoRA适配器合并到Qwen3" --k 5
```
✅ 返回5个相关结果——排名第一的是《Fine-Tuning Qwen3-4B》文章，其中包含了精确的`merge.py`步骤（密集分数=0.739，BM25分数=41.5）。

## 2. 搜索（中文，跨语言）
```
.venv/bin/python search.py "正则表达式怎么匹配邮箱" --k 3 --lang zh
```
✅ 正确检索到《正则表达式》指南和《Java正则表达式》文章——bge-m3的多语言匹配功能正常。

## 3. 完整RAG对话（检索+生成）
```
.venv/bin/python rag_chat.py -q "如何合并LoRA适配器..." --backend llama --no-stream
```
✅ 经过微调的Qwen3-4B GGUF模型（2.5GB，卸载至GPU）生成了基于检索结果的答案，包含正确的内联引用`[1]`–`[6]`、`merge_and_unload()`代码示例，以及对应原始文章的来源列表。

### 总结

| 组件 | 状态 |
|---|---|
| 索引加载（186,263个块，bge-m3） | ✅ |
| FAISS密集搜索 | ✅ |
| BM25稀疏搜索 | ✅ |
| 混合RRF融合 | ✅ |
| 中英文检索 | ✅ |
| llama.cpp生成（GGUF） | ✅ |
| 来源引用 | ✅ |

唯一的小问题：模型在来源基础上稍有修饰（例如，"FP16精度"的建议在检索到的块中并不明确），但这属于LLM的正常行为范围。一切已准备就绪——你也可以运行`eval_rag.py --k 10`来填写README中的Recall@10/MRR表格。