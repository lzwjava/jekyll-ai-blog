---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT-2 760M 训练代码来源
translated: true
type: note
---

**问题：** 哪里可以获取训练 GPT-2 760M 规模模型（类似于我在 AMD MI300X 上所做的）的训练代码？

**回答：**

BigCode 专注于代码大语言模型（StarCoder 系列），而非 GPT-2 预训练。对于 GPT-2 760M 规模训练，以下是与你的配置最相关的权威代码库，按相关性排序：

---

## 1. nanoGPT — Karpathy 的参考实现（从这里开始）

```bash
git clone https://github.com/karpathy/nanoGPT
```

这是从头开始进行 GPT-2 规模预训练的最佳标准。你已在 MI300X 上使用过它。关键文件：

- `model.py` — GPT-2 架构（CausalSelfAttention、MLP、Block、GPT）
- `train.py` — 包含梯度累积、余弦学习率、评估的完整 DDP 训练循环
- `config/train_gpt2.py` — 124M、355M、774M、1558M 的配置

对于 760M 模型，你可以使用 `train_gpt2_medium.py` 或直接设置：

```python
n_layer = 36
n_head = 20
n_embd = 1280
```

这属于 GPT-2 XL 规模（约 760M 参数）。

---

## 2. Megatron-LM — 生产级，支持多 GPU/多节点

```bash
git clone https://github.com/NVIDIA/Megatron-LM
```

若在 MI300X 上使用，你可采用 ROCm 分支或 AMD 的自有版本：

```bash
git clone https://github.com/ROCm/Megatron-LM
```

支持张量并行 + 流水线并行。更复杂但可扩展至 100B+ 参数。对于 760M 模型有些大材小用，但值得了解。

---

## 3. LitGPT — Lightning AI 的简洁多模型训练器

```bash
git clone https://github.com/Lightning-AI/litgpt
```

涵盖 GPT-2、Llama、Mistral、Phi，并提供统一的训练接口。相比 nanoGPT，该工具更适用于生产环境，且内置 LoRA/QLoRA 支持。

---

## 4. BigCode 的训练代码库 — 若需要代码专用预训练

```bash
git clone https://github.com/bigcode-project/bigcode-dataset  # 数据管道
git clone https://github.com/bigcode-project/starcoder        # 训练脚本
```

StarCoder 底层使用 Megatron，并采用 FIM（Fill-in-Middle）目标。The Stack v2 是数据来源。

---

## 在 MI300X 上快速启动 760M 模型（nanoGPT 路线）

```bash
git clone https://github.com/karpathy/nanoGPT && cd nanoGPT

# 准备 FineWeb 或 OpenWebText
python data/openwebtext/prepare.py

# config/train_gpt2_760m.py
cat > config/train_gpt2_760m.py << 'EOF'
wandb_log = True
wandb_project = 'gpt2-760m'
dataset = 'openwebtext'

# 760M 参数
n_layer = 36
n_head = 20
n_embd = 1280
block_size = 1024
dropout = 0.0

# 训练
batch_size = 12
gradient_accumulation_steps = 40  # 有效批次 = 480 * 1024 tokens
max_iters = 600000
lr_decay_iters = 600000
learning_rate = 1e-4
min_lr = 1e-5
warmup_iters = 2000
EOF

# 在 MI300X 上使用 ROCm/HIP 启动
torchrun --nproc_per_node=1 train.py config/train_gpt2_760m.py
```

在 MI300X 上使用多 GPU（该设备拥有 192GB HBM3，单 GPU 即可轻松容纳）：

```bash
# 单 GPU，760M 模型权重约 6GB + 优化器状态约 24GB，总计约 30GB
# MI300X 有 192GB 显存，可提供大量余量以使用更大的批次大小
```

---

## 数据选项（优于 OpenWebText）

| 数据集 | 大小 | Hugging Face 路径 |
|---------|------|---------|
| FineWeb | 15T tokens | `HuggingFaceFW/fineweb` |
| FineWeb-Edu | 1.3T 教育级 tokens | `HuggingFaceFW/fineweb-edu` |
| OpenWebText | ~9B tokens | 通过 nanoGPT 的 prepare 脚本本地获取 |
| The Stack v2 | 67.5TB 代码 | `bigcode/the-stack-v2-dedup` |

若需获得强基准性能，FineWeb-Edu 是目前最适合 GPT-2 风格语言模型的数据集。

---

## 总结

| 代码库 | 最适合场景 |
|------|---------|
| `karpathy/nanoGPT` | 学习、简洁的 760M 训练、单节点 |
| `ROCm/Megatron-LM` | 生产环境、多节点、MI300X 上的张量并行 |
| `Lightning-AI/litgpt` | 简洁的多模型、LoRA、较少模板代码 |
| `bigcode/starcoder` | 使用 FIM 目标的代码专用预训练 |

鉴于你已熟悉 MI300X 上的 nanoGPT 运行经验，下一步自然可以选择扩展数据规模（使用 FineWeb 替代 OpenWebText），或切换到 Megatron 进行张量并行实验。

**参考链接：**

- [karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
- [ROCm/Megatron-LM](https://github.com/ROCm/Megatron-LM)
- [Lightning-AI/litgpt](https://github.com/Lightning-AI/litgpt)
- [FineWeb 数据集](https://huggingface.co/datasets/HuggingFaceFW/fineweb)
- [bigcode/starcoder 训练代码](https://github.com/bigcode-project/starcoder)
