---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微调管道构建与调试
translated: true
type: note
---

## 我们所做的工作 — 完整总结

### 1. 构建了微调流水线 (`/mnt/data/zz/finetune/`)

**数据集提取** (`build_dataset.py`):

- 从 `~/projects/jekyll-ai-blog/_posts/{en,zh}/` 解析了 16,107 篇 Jekyll Markdown 文章
- 提取 `{title, body}` 对作为 SFT 对话
- 清理了 Liquid 标签、kramdown 属性、图片引用、标题
- 10,726 英文 + 10,708 中文 = **21,434 个样本**
- **2510 万 tokens**，平均每个样本 1,169 tokens
- 200 个保留用于评估，21,234 个用于训练
- 输出为 `notes_sft_train.jsonl` (85MB) + `notes_sft_eval.jsonl` (820KB)

**训练脚本** (`train.py`):

- 最初使用基于 Unsloth 的 QLoRA，在 RTX 4070 上遇到 Triton 段错误
- 重写为 **纯 transformers + peft** (无 Unsloth 内核依赖)
- Qwen3-4B-unsloth-bnb-4bit, 4 位量化, LoRA r=32
- 6600 万可训练参数 (占 4B 的 1.6%)
- 冒烟测试：10 步，1.25秒/步，loss 下降 (2.86→2.11)

**辅助脚本**:

- `eval.py` — 在保留标题上比较微调模型与基础模型 (vLLM 或 transformers)
- `export_gguf.py` — 导出为 GGUF 供 ollama/llama.cpp 使用
- `README.md` + `requirements.txt`

### 2. 模型下载风波

尝试了 4 个模型后才找到可用的：

| 模型 | 大小 | 结果 |
|---|---|---|
| `unsloth/Qwen3-8B` (4-bit) | 7.5GB | 下载太慢 (300KB/s)，已终止 |
| `Qwen/Qwen3.5-9B` (缓存) | 18GB | VL 模型，类型错误 |
| `Qwen/Qwen3-4B-FP8` (缓存) | 4.9GB | Unsloth 加载时卡住 |
| **`unsloth/Qwen3-4B-unsloth-bnb-4bit`** | **3.4GB** | **通过 curl 下载，可用** |

从 `huggingface.co` 以约 37MB/s 下载（速度从之前的 300KB/s 恢复）。由于 `hf` CLI / `hf-mirror.com` 没有该模型，通过符号链接手动设置了 HF 缓存结构。

### 3. 从 Unsloth 转向纯 Transformers

Unsloth 的 Triton 内核在此设置上持续段错误：

- torch 2.10+cu128, CUDA 12.8, Triton 3.6.0, RTX 4070 (compute 8.9)
- 在训练和推理的第 0 步崩溃
- `UNSLOTH_DISABLE_TRITON=1` 无济于事

**修复**：完全放弃 Unsloth，改用：

- `transformers` 加载模型
- `peft` 进行 LoRA (`LoraConfig` + `get_peft_model`)
- `trl.SFTTrainer` 配合 `processing_class` (TRL 0.24 API)

### 4. TRL 0.24 API 修复

安装的 TRL 0.24.0 与文档中的 API 有变化：

- `tokenizer=` → `processing_class=`
- `SFTConfig` 没有 `max_seq_length` 参数
- `torch_dtype=` → `dtype=`
- `warmup_ratio` 已弃用（但仍有效）

### 5. Git 提交

```
8292db9  add finetune pipeline for lzwjava notes SFT
9aaa8f3  fix train.py: use pure transformers+peft, fix TRL 0.24 API
```

推送到 `github.com:lzwjava/zz.git`。JSONL 文件已被 gitignore。

### 6. 准备运行

```bash
cd /mnt/data/zz/finetune && python3.11 train.py
```

- 在 RTX 4070 上约 55 分钟 (2,656 步 × 1.25 秒/步)
- 将 LoRA 适配器保存到 `lzw-notes-lora/`
- 然后：运行 `python3.11 export_gguf.py` 供 ollama 使用，运行 `python3.11 eval.py` 进行测试
