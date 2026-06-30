---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FinGPT在RTX 4070上：问题与修复
translated: true
type: note
---

以下是完整情况：

---

## GPU 状态

```
RTX 4070  |  12GB VRAM (12,282 MiB)  |  230MiB 已用  |  CUDA 13.0
```

余量充足，只有 Xorg 在使用。

---

## 代码 — 功能说明

FinGPT 是一个用于金融大语言模型的 **LoRA 微调框架**。它封装了 HuggingFace `Trainer` + PEFT + DeepSpeed。关键子项目：

| 子项目 | 功能 |
|---|---|
| **FinGPT_Benchmark** | 在 7B 模型上进行多任务训练（情感分析、NER、标题信息抽取、关系抽取、ConvFinQA） |
| **FinGPT_Forecaster** | 基于新闻的股票走势预测 — Llama-2-7B，max_length 4096 |
| **FinGPT_Sentiment_Analysis** | 金融情感分类器 |
| **FinGPT_RAG / MultiAgentsRAG** | 用于金融问答的 RAG 流水线 |
| **FinGPT_FinancialReportAnalysis** | PDF 报告分析 |

支持的模型大小：

| 模型 | 大小 (fp16) | 8-bit | 4-bit |
|---|---|---|---|
| ChatGLM2-6B / Falcon-7B / Qwen-7B / Llama-2-7B | ~13-14 GB | ~6.5 GB | ~3.5 GB |
| Llama-2-13B | ~26 GB | ~13 GB | ~7 GB |

训练使用 **LoRA**（非全参数微调）——适配器权重极小（约几 MB）。

---

## 我发现的问题

**1. `load_in_8bit=True` 被注释掉了**（两个 `train_lora.py` 文件中第 50 行）

```python
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    # load_in_8bit=True,       <-- 被注释掉
    # device_map="auto",
    trust_remote_code=True
)
```

这意味着模型以完整的 fp16 加载——**7B 模型约 13GB 无法装进 12GB VRAM**。除非取消注释或使用 4-bit，否则必然遇到 CUDA OOM。

**2. 设计用于 4 张 GPU，而非 1 张**

- Forecaster 的 `train.sh` 包含 `--include localhost:2,3` —— 硬编码为多 GPU 机器上的 GPU 2-3
- DeepSpeed 配置使用 **ZeRO stage 0**（无分片）—— 能减少优化器内存，但不会拆分模型
- 原论文称每次训练成本低于 $300，但假设使用 4× A100 或类似配置

**3. 需要本地模型文件**

- `from_remote=False` 为默认值 → 在本地 `base_models/Llama-2-7b-hf` 等路径下寻找模型
- 需要先下载模型，或者设置 `--from_remote`（并且需要 HuggingFace token 来访问 Llama-2 这类受限模型）

**4. 依赖版本过时**

- 使用 PEFT 的 `prepare_model_for_int8_training` —— 在新版本中已弃用，由 `prepare_model_for_kbit_training` 替代
- 没有 flash attention、没有梯度检查点、没有 QLoRA（4-bit NF4）

---

## 你实际能在 RTX 4070 12GB 上做什么

### ✅ 轻松容纳 —— 很宽裕

| 任务 | 配置 |
|---|---|
| **情感分析 / NER / 标题** 微调 **7B 模型** | 4-bit QLoRA，batch_size 4，max_length 512 → ~5-6 GB |
| **Forecaster** 微调 **7B 模型** | 4-bit，batch_size 1，max_length 4096 → ~6-7 GB |
| **推理** 任意 **7B 模型** | fp16 或 8-bit，轻松容纳 |
| **推理** **13B 模型** | 4-bit 量化 → ~7-8 GB |

### ⚠️ 勉强可用 —— 需要调优

| 任务 | 配置 |
|---|---|
| **Forecaster** 微调 **7B 模型**（8-bit） | batch_size 1，grad_accum 16（与原版一致），max_length 2048 |
| **13B 模型** LoRA 微调 | 仅 4-bit QLoRA，极小 batch_size 1，max_length 512 |

### ❌ 无法运行

| 任务 | 原因 |
|---|---|
| 任何 7B+ 模型的完整 fp16 微调 | 13GB > 12GB |
| 13B 模型以 8-bit 运行 | ~13GB 刚超 12GB，没有余量给激活值 |
| 任何需要 fp32（无混合精度）的操作 | 每个 7B 模型需要 26GB+ |

---

## 快速修复使其运行

在 `train_lora.py` 中取消注释 `load_in_8bit=True` 并添加 `device_map="auto"`。或者升级为 4-bit QLoRA：

```python
from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)
```

然后去掉 DeepSpeed（单 GPU 上过于冗余），直接使用 HuggingFace Trainer。对于 Forecaster，还需启用梯度检查点并设置 `batch_size=1`、`gradient_accumulation_steps=16`。

需要我进行这些修改并设置一个测试运行吗？
