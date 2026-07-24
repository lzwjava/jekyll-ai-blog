---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在RTX 4070上运行nano-vllm
translated: true
type: note
---

好的，以下是您笔记本电脑的完整配置以及运行 **nano-vllm** 的步骤：

---

## 硬件规格

| 组件 | 规格 |
|-----------|------|
| **GPU** | NVIDIA GeForce RTX 4070（12GB 显存） |
| **CUDA 驱动** | 13.0 |
| **内存** | 62 GB |
| **Python** | 3.12.3 ✅（项目要求 3.10–3.13） |

---

## 已满足的先决条件

- **torch** 2.11.0+cu130 ✅
- **transformers** 5.12.1 ✅
- **triton** 3.6.0 ✅
- **huggingface-cli** ✅

---

## 运行步骤

### 1. 安装缺失的依赖

Flash Attention 和 xxhash 尚未安装。使用 Python 3.12 安装它们：

```bash
python3.12 -m pip install flash-attn xxhash
```

### 2. 安装 nano-vllm（从本地源码）

```bash
cd /mnt/data/nano-vllm
python3.12 -m pip install -e .
```

### 3. 下载模型

示例使用 **Qwen3-0.6B**（约 1.2GB）：

```bash
huggingface-cli download --resume-download Qwen/Qwen3-0.6B \
  --local-dir ~/huggingface/Qwen3-0.6B/ \
  --local-dir-use-symlinks False
```

> **可选**：您也可以使用任意 HuggingFace 模型替代——只需更新 `example.py` 中的 `path`。

### 4. 运行推理

```bash
cd /mnt/data/nano-vllm
python3.12 example.py
```

或者运行基准测试：

```bash
python3.12 bench.py
```

---

## 快速一行命令

```bash
python3.12 -m pip install flash-attn xxhash && \
cd /mnt/data/nano-vllm && \
python3.12 -m pip install -e . && \
huggingface-cli download --resume-download Qwen/Qwen3-0.6B \
  --local-dir ~/huggingface/Qwen3-0.6B/ \
  --local-dir-use-symlinks False && \
python3.12 example.py
```

---

**重要提示**：请始终显式使用 `python3.12` —— 默认的 `python3` 是 3.14 版本，不在本项目的支持范围内。RTX 4070 拥有 12GB 显存，当前仅使用约 2.6GB，因此您有足够空间运行更大模型，如 Qwen3-4B 或 Qwen3-8B。