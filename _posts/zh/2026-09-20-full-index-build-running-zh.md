---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 正在运行完整索引构建
translated: true
type: note
---

完整的索引构建已在后台运行中（PID 888226，20k/186k 块，预计约 40 分钟）。其他一切就绪——以下是命令。

## 1. 监控正在运行的构建

```bash
cd /mnt/data/zz/rag
tail -f logs/build_bge_m3.log
```

当您看到 `Done. Index in /mnt/data/zz/rag/rag_index/` 时即完成。（以 `wrote index.faiss`、`bm25:` 行、然后是 `Done.` 结尾。）

## 2. 如果构建中断，或您想（重新）启动

```bash
cd /mnt/data/zz/rag
nohup .venv/bin/python build_index.py --batch-size 32 --max-seq-length 1024 \
  > logs/build_bge_m3.log 2>&1 &
```

快速备选方案（约 12 分钟而非约 80 分钟，质量略有降低）构建到独立索引中：

```bash
cd /mnt/data/zz/rag
.venv/bin/python build_index.py --model intfloat/multilingual-e5-small \
  --out-dir rag_index_e5 --batch-size 32
```

## 3. 检索（无 LLM）——在构建完成后

```bash
cd /mnt/data/zz/rag
.venv/bin/python search.py "how to export a Qwen3 LoRA to GGUF" --k 5
.venv/bin/python search.py "正则表达式" --k 5 --lang zh
.venv/bin/python search.py "vllm 部署" --alpha 0.0 --k 5   # 仅 BM25
.venv/bin/python search.py --interactive
```

## 4. RAG 聊天（llama.cpp + `finetune/lzw-notes-merged_gguf`）

```bash
cd /mnt/data/zz/rag
.venv/bin/python rag_chat.py --question "How do I merge a LoRA adapter and export it to GGUF?"
.venv/bin/python rag_chat.py --interactive
.venv/bin/python rag_chat.py -q "正则表达式" --backend none --show-context   # 仅检索
```

其他后端：`--backend hf --model ../finetune/lzw-notes-merged`，`--backend vllm --model ../finetune/lzw-notes-merged`。

## 5. 检索评估（填写 README 结果表）

```bash
cd /mnt/data/zz/rag
.venv/bin/python eval_rag.py --k 10                    # 混合
.venv/bin/python eval_rag.py --mode dense --k 10
.venv/bin/python eval_rag.py --mode bm25 --k 10
```

## 6. 仅当您需要重新创建环境时

```bash
cd /mnt/data/zz/rag
python3 -m venv --system-site-packages .venv
.venv/bin/pip install -r requirements.txt
```

状态：`rag/` 包含 `retriever.py`、`bm25.py`、`build_index.py`、`search.py`、`rag_chat.py`、`eval_rag.py`、`README.md`、`requirements.txt`；venv 已安装并通过冒烟测试（构建 + 混合搜索 + llama.cpp 生成均在 423 块测试索引上验证通过）。唯一剩下的是当前正在嵌入的完整 186k 块索引。
