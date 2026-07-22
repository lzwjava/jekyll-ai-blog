---
audio: false
generated: true
image: false
lang: en
layout: post
title: Machine Learning Data Pipeline
translated: false
type: note
---

This project is a **machine learning data processing pipeline** — it handles:

- **Downloading** large datasets (FineWeb, Wikimedia, etc.) from sources like Hugging Face and HF mirrors
- **Extracting & tokenizing** data from parquet files into tokenized `.npy` shards (using GPT-2 BPE)
- **Analysis** — training duration estimation and metric evaluation from logs
- **Model inference** — running LLMs like DeepSeek-V2-Lite-Chat with quantization

There are also subdirectories for **fine-tuning** (`finetune/`), **specific datasets** (`finemath/`, `spgispeech/`, `codeparrot/`, `climbmix/`), and **training scripts** (`fineweb-code-sec-gpt.sh`, `eval_sft.sh`, etc.). Looks like training/evaluation of a code-focused model.

Want to dive deeper into any specific part?
