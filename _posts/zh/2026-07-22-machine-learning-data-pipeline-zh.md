---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 机器学习数据管道
translated: true
type: note
---

该项目是一个**机器学习数据处理流水线**——它负责：

- **下载**大规模数据集（FineWeb、Wikimedia 等），来源包括 Hugging Face 及其镜像站
- **提取与分词**——将 parquet 格式的数据转换为分词的 `.npy` 分片（使用 GPT-2 BPE）
- **分析**——根据日志估算训练时长并评估指标
- **模型推理**——运行量化后的 LLM（如 DeepSeek-V2-Lite-Chat）

此外还有若干子目录，用于**微调**（`finetune/`）、**特定数据集**（`finemath/`、`spgispeech/`、`codeparrot/`、`climbmix/`）以及**训练脚本**（`fineweb-code-sec-gpt.sh`、`eval_sft.sh` 等）。看起来是训练/评估一个专注于代码的模型。

想深入了解某个具体部分吗？
