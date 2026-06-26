---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模型修复与部署
translated: true
type: note
---

完成。以下是具体情况：

**根本原因**：RunPod上的旧模型产生退化输出，因为它来自原始的nanoGPT检查点（相同权重循环）。新的HF模型（`lzwjava/sec-edgar-gpt-124m-hf`）具有不同的、经过正确训练的权重，但以原始的nanoGPT布局保存（转置权重，无偏置）。

**所做工作**：

1. **本地 server.py** — 删除了18行的嵌入修剪hack
2. **RunPod** — 从HF下载新模型，并进行了转换：
   - 将线性权重转置 `[out, in]` → `[in, out]`（GPT2Conv1D布局）
   - 添加了零偏置（原始训练使用了 `bias=False`）
   - 词汇表保持50257（无填充）
3. **服务器重启** 在端口8888，生成真正的SEC-EDGAR财务文本

**RunPod上的文件**（`/workspace/model/`）：

- `hf-model/` — 转换后的模型（622MB，正确的transformers布局）
- `hf-model-new/` — 原始HF下载（备份）
- `hf-model-old/` — 具有退化权重的原始模型（备份）
- `hf-model-trimmed/` — 修剪至50257的旧模型（备份）
- `server.py` — 已更新，无修剪hack

模型在长输出时会重复（124M的典型情况），但不再出现'ivableivable'这样的垃圾内容。
