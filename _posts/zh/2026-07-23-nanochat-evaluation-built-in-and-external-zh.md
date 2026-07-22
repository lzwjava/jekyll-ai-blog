---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nanochat评估：内置与外部
translated: true
type: note
---

好消息——nanochat 已经内置了**任务评估**功能！但也存在一些优秀的外部库。以下是完整情况。

---

## ✅ 你已有的内置功能

**脚本**：`python -m scripts.chat_eval`

| 任务 | 类型 | 衡量内容 |
|------|------|----------|
| **HumanEval** | 生成式 | Python 函数补全 → 运行单元测试 → pass@k |
| **MMLU** | 分类式 | 57 个科目，多项选择知识 |
| **ARC-Easy / ARC-Challenge** | 分类式 | 小学科学推理 |
| **GSM8K** | 生成式 | 小学数学文字题 |
| **SpellingBee** | 生成式 | 字母计数与拼写 |
| **SmolTalk** | (位于 chat_sft.py 中) | 对话质量 |
| **CustomJSON** | (位于 chat_sft.py 中) | 加载自定义 JSONL 评估 |

**使用方法**（适用于你的 SFT 或基础模型）：
```bash
cd /mnt/data/nanochat && source .venv/bin/activate

# 运行 HumanEval（代码生成，运行单元测试）
python -m scripts.chat_eval --source=sft --model-tag=d12 --task-name=HumanEval

# 运行所有任务
python -m scripts.chat_eval --source=sft --model-tag=d12

# 运行特定任务
python -m scripts.chat_eval --source=base --model-tag=d12 --task-name="ARC-Easy|GSM8K"
```

---

## 📦 可添加的外部评估库

由于你的模型是**代码模型**（基于 Python 训练），以下是相关性最高的几个：

### 1️⃣ [LM Eval Harness](https://github.com/EleutherAI/lm-evaluation-harness) (EleutherAI)

行业标准，内置 100+ 基准测试。

```bash
pip install lm-eval
```

**支持：** MMLU、HellaSwag、ARC、GSM8K、HumanEval、MATH、BigBench 等。

**与你的模型配合使用**——你需要：
- 将 nanochat 模型导出为 HuggingFace 格式（添加转换脚本），或
- 使用 `--model local-completion` 接口通过 nanochat 引擎传递提示

```bash
# 如果转换为 HF 格式：
lm_eval --model hf --model_args pretrained=./my-model \
  --tasks mmlu,hellaswag,arc_challenge --device cuda:0
```

### 2️⃣ [HumanEval + MBPP](https://github.com/openai/human-eval)（直接使用）

你已集成了 HumanEval（nanochat/tasks/humaneval.py），但也可以独立运行以获取更详细的报告：

```bash
pip install human-eval
```

### 3️⃣ [BigCode Eval Harness](https://github.com/bigcode-project/bigcode-evaluation-harness)

专为**代码模型**构建。支持：

| 基准测试 | 描述 |
|----------|------|
| **HumanEval** | Python 函数补全 |
| **MBPP** | 约 1000 个 Python 编程任务 |
| **HumanEval-X** | 多语言（C++、Java、JS、Go 等） |
| **DS-1000** | 数据科学 / numpy / pandas 任务 |
| **APPS** | 竞争性编程 |
| **CodeContests** | Codeforces 级别问题 |

```bash
pip install bigcode-evaluation-harness
```

```bash
# 在代码任务上评估你的转换后模型
bigcode-eval-harness \
  --model hf \
  --model_args pretrained=./my-model \
  --tasks humaneval,mbpp --batch_size 8
```

### 4️⃣ [DeepEval](https://github.com/confident-ai/deep-eval)

现代框架，采用 LLM 作为评判者进行评估。适合对话质量评估。

```bash
pip install deepeval
```

### 5️⃣ [HuggingFace `evaluate`](https://github.com/huggingface/evaluate)

轻量级指标——BLEU、ROUGE、困惑度、准确率、F1。适合快速统计。

```bash
pip install evaluate
```

```python
from evaluate import load
perplexity = load("perplexity", module_type="metric")
results = perplexity.compute(predictions=[...], model_id="...")
```

---

## 🧱 注意事项——你的自定义分词器

你的 nanochat 模型使用**自定义 BPE 分词器**（vocab_size=32768，基于 codeparrot 代码训练）。外部评估库期望 HuggingFace `transformers` 模型具备 `AutoTokenizer` / `AutoModelForCausalLM` 接口。

**要使用外部库，你需要添加 HuggingFace 导出步骤。** 一个最小化的导出器需要：
1. 通过 `checkpoint_manager.load_model()` 加载你的模型
2. 将权重转换为 `transformers` 状态字典
3. 使用 `model.save_pretrained()` + 分词器配置保存

这是解锁所有外部评估工具的关键缺失环节。

---

## TL;DR 建议

| 使用什么 | 原因 |
|----------|------|
| **内置 `chat_eval.py`** | 已经可用，无需设置 |
| **内置 `base_eval.py`** | 基础模型的 BPB + CORE 基准 |
| **添加 BigCode Eval Harness** | 最适合代码特定基准（HumanEval、MBPP） |
| **添加 LM Eval Harness** | 最适合通用 LLM 基准（MMLU、ARC、GSM8K） |
| **添加 HF 导出脚本** | 使用上述库所必需 |

需要我为你写一个 **HuggingFace 导出脚本**，以便你的 nanochat 模型可以使用所有这些外部评估库吗？