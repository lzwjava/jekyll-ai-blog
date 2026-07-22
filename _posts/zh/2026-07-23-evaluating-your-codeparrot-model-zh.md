---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 评估您的Codeparrot模型
translated: true
type: note
---

抱歉之前混用了语言。以下是完整的英文说明。

---

## 项目概述

你正在基于 `codeparrot-clean` 数据集（Python 代码）训练一个 **nanochat 的 GPT 模型**（286M 参数，depth=12）。检查点通过 MLflow 存储在 `~/.cache/nanochat/base_checkpoints/d12/`。

---

## 最近的评估相关提交

| 提交 | 描述 |
| -------- | ------------- |
| `9538f8b` | `eval_long`：Markdown 输出，带语法高亮的代码块 |
| `1df37d3` | `eval_long`：在日志输出中添加 PROMPT/OUTPUT 分隔符 |
| `efa3c1f` | 添加 eval 和 eval_long：codeparrot-d12 评估脚本和结果 |

这些全部位于 `zz/codeparrot/eval/` 和 `zz/codeparrot/eval_long/`。

---

## 如何评估你训练好的模型

### 1️⃣ BPB + 采样 + Python 代码生成（定量评估）

**脚本**：`zz/codeparrot/eval/run_eval.sh`

```bash
cd /mnt/data/nanochat
source .venv/bin/activate

python -m scripts.base_eval \
    --model-tag d12 \
    --eval bpb,sample \
    --device-batch-size=8 \
    --split-tokens=1048576
```

这会运行：

- **bpb** – 训练/验证集上的 bits-per-byte（衡量损失）
- **sample** – 从内置提示生成文本，定性检查输出

该脚本还包含一个内联 Python 部分，直接使用 nanochat Engine 测试 8 个 Python 代码提示（斐波那契、反转链表等）。

### 2️⃣ 长提示评估（代码生成）

**脚本**：`zz/codeparrot/eval_long/run_eval_long.sh`

```bash
cd /mnt/data/nanochat
source .venv/bin/activate
bash zz/codeparrot/eval_long/run_eval_long.sh
```

此脚本运行 `eval_long.py`，测试 8 个复杂的 Python 提示（BST、LCS、装饰器、文件 I/O 等），并将格式精美的 Markdown 文件（带语法高亮代码块）写入 `zz/codeparrot/eval_long/results/long_prompt_results.md`。

### 3️⃣ 快速交互式聊天 / 单提示

**脚本**：`zz/eval_sft.sh` 和 `zz/eval_sft_extra.sh`

```bash
cd /mnt/data/nanochat
source .venv/bin/activate

# 使用单个提示测试基础模型
python -m scripts.chat_cli \
    --source=base \
    --model-tag=d12 \
    --temperature=0.3 \
    --top-k=50 \
    --prompt="Write a Python function to check if a string is a palindrome"
```

或者交互模式：

```bash
python -m scripts.chat_cli --source=base --model-tag=d12
```

### 4️⃣ 完整 CORE 基准测试（ICL 准确率）

如果你想在少样本 NLP 任务上进行评估：

```bash
python -m scripts.base_eval \
    --model-tag d12 \
    --eval core \
    --max-per-task=100
```

这会下载一个评估包（约 1GB），并在多项选择/补全任务上运行准确率，计算“CORE metric”（中心化准确率）。

---

## 关键文件总结

| 文件 | 功能 |
| ------ | ------------- |
| `zz/codeparrot/eval/run_eval.sh` | 完整评估：BPB + 样本 + Python 代码生成 |
| `zz/codeparrot/eval_long/run_eval_long.sh` | 长上下文代码生成评估 |
| `zz/codeparrot/eval_long/eval_long.py` | 长提示评估的 Python 逻辑 |
| `zz/eval_sft.sh` | SFT 检查点评估（5 个通用提示） |
| `zz/eval_sft_extra.sh` | 更多 SFT 提示（数学、推理、SQL） |
| `zz/finetune/eval.py` | 针对微调 LoRA 检查点的 vLLM/transformers 评估 |
| `/mnt/data/nanochat/scripts/base_eval.py` | 主要评估 CLI：`core`、`bpb`、`sample` |
| `/mnt/data/nanochat/scripts/chat_cli.py` | 交互式聊天或单提示推理 |

---

## 快速评估你的最新检查点

**BPB 和采样：**

```bash
cd /mnt/data/nanochat && source .venv/bin/activate
NANOCHAT_DATA_DIR="/mnt/data/zz/datasets/codeparrot-clean-nanochat" \
python -m scripts.base_eval --model-tag d12 --eval bpb,sample --device-batch-size=8
```

**长提示代码评估：**

```bash
cd /mnt/data/nanochat && source .venv/bin/activate
bash /mnt/data/zz/codeparrot/eval_long/run_eval_long.sh
```

结果将输出到 `~/.cache/nanochat/base_eval/`（`base_eval.py`）和 `zz/codeparrot/eval_long/results/long_prompt_results.md`（长提示）。
