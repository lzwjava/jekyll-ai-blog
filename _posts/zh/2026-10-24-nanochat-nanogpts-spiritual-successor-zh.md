---
audio: false
generated: true
image: false
lang: zh
layout: post
title: nanochat：nanoGPT的精神继承者
translated: true
type: note
---

nanochat 并非 nanoGPT 的分支——它是其**继承者和精神上的进化**（同源，Karpathy 的 "nano" 系列，从头重写为一个结构完善的包）。nanoGPT 是最小化的概念验证（"最简单、最快速的训练/微调中型 GPT 的仓库"，约 300 行代码在单个 `train.py` 中）；nanochat 则是围绕相同核心 GPT 理念构建的完整工业流程。

## 范畴（"全栈" vs 仅预训练）

**nanoGPT** — 单一任务：

- `train.py`（在 OpenWebText 上预训练，DDP，autocast，AdamW），`model.py`（GPT-2 块，学习式位置嵌入），`sample.py`，数据准备脚本
- 单一阶段：预训练 → 文本采样。仅此而已。

**nanochat**（约 7000 行）涵盖了 LLM 的每个阶段：

- 分词 (Tokenization)：训练**自己的 BPE 分词器**，风格类似 GPT-4（`tokenizer.py`，`scripts/tok_train.py`），而非 nanoGPT 所使用的 tiktoken 依赖
- 预训练（`base_train.py`），**SFT**（`chat_sft.py`），**RL**（`chat_rl.py`），**评估**（CORE 评分，bits-per-byte，MMLU/GSM8K/ARC/humaneval 任务），以及**聊天 CLI**（`chat_cli.py`）
- 带有 **KV cache** 的推理引擎（`engine.py`）和作为工具的沙盒化 **Python 代码执行**（`execution.py`）

## "一键调节"设计——重大的哲学差异

nanoGPT：手动设置 `n_layer`、`n_head`、`n_embd`、`learning_rate` 等。
nanochat：你只需设置一个 `--depth` 整数；其他所有参数（宽度、注意力头数、学习率、权重衰减、训练周期）都根据 Scaling Laws 自动推导出来，以确保任何规模都能达到计算最优。`--depth=26` ≈ GPT-2 的能力。这就是该仓库的目标是"达到 GPT-2 能力的耗时排行榜"的原因——在 8×H100 上以不到 1.65 小时、成本低于 50 美元（而 2019 年的成本是 43,000 美元）超越 GPT-2 的 CORE 评分。

## 模型架构与训练差异（`gpt.py`，`optim.py`）

| | nanoGPT | nanochat |
| --- | --- | --- |
| 位置编码 | 学习式 | **旋转位置嵌入 (RoPE)** |
| 注意力机制 | 全因果 | 因果 + **每层滑动窗口**（平铺） |
| QK 缩放 | 1/√d | 分离缩放，`q *= 1.2` |
| 优化器 | AdamW | **MuonAdamW**（矩阵参数按形状分组使用 Muon，其余部分使用 AdamW），附带分布式变体，可收集梯度用于 Muon 的正交化操作 |
| 混合精度 | `torch.amp.autocast` | **显式 `COMPUTE_DTYPE`** 全局设置（bf16/fp16/fp32，可通过环境变量覆盖）—— 任何地方均不使用 autocast |
| FP8 | — | **支持** — `fp8.py`，正是我们讨论过的：围绕 `torch._scaled_mm` 的自定义 `_Float8Matmul` autograd 函数，激活值和权重使用 e4m3，梯度使用 e5m2 |
| 注意力实现 | SDPA | flash_attention.py 封装器（可用时使用 FA3，否则回退到 SDPA） |
| 日志记录 | print + plot.py | mlflow + wandb + 检查点管理器 |

## 操作差异

- **数据**：nanoGPT 下载 OpenWebText 并预先分词一次；nanochat 拥有一个基于分布式分片的分词数据加载器（`dataloader.py`，`dataset.py`）—— 数据格式对于 CORE 排行榜至关重要
- **并行性**：两者都使用 DDP；nanochat 添加了梯度累积自动处理（也能在单 GPU 上运行），`DistMuonAdamW` 中的异步梯度约简，以及适合 `allow_in_graph` 的编译训练
- **交付物**：nanoGPT 提供一个原始采样器；nanochat 提供一个你可以实际对话的聊天助手（支持工具使用）

## 实践总结

如果说 nanoGPT 是"所有内容都在一个文件里，请通读全篇"的教学产物，那么 nanochat 就是"同样的精神，但产品化了"：相同的 GPT 核心，但配备了 Scaling Laws 调优的超参数系统、Muon 优化器、FP8、显式精度控制、滑动窗口 + RoPE 注意力、SFT/RL 阶段、排行榜优化的快速运行，以及包含测试的正确包结构。我们之前看到的 `fp8.py` 就是 nanochat 哲学的一个很好的例子：将 2000 行的 torchao 子系统压缩成 150 行，精确针对仓库所需。
