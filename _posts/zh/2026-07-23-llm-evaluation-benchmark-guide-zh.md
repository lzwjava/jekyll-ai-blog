---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM评估基准指南
translated: true
type: note
---

以下是关于使用标准基准评估大语言模型的全面指南，根据你的项目设置定制：

---

## 评估大语言模型的流行基准

### 1. **LM Evaluation Harness**（标准工具）

几乎每个开源大模型发布（Llama、Qwen、Mistral 等）都使用它。支持 60 多个基准测试。

```bash
# 安装
pip install lm-eval

# 在微调模型上运行基础基准测试
lm_eval --model hf \
  --model_args pretrained=./finetune/lzw-notes-merged \
  --tasks mmlu,gsm8k,hellaswag,arc_easy,truthfulqa \
  --batch_size auto \
  --output_path ./eval_results
```

**关键任务：**

| 基准测试 | 衡量内容 | 重要性 |
| --------- | ---------- | -------- |
| **MMLU**（57 个学科） | 世界知识、多任务准确率 | 引用最多的 LLM 基准 |
| **GSM8K** | 小学数学推理 | 测试思维链 |
| **HumanEval** | 代码生成（pass@1） | 针对代码模型 |
| **HellaSwag** | 常识推理 | 检测“随机鹦鹉” |
| **ARC（Easy/Challenge）** | 科学问答 | 事实性知识 |
| **TruthfulQA** | 真实性 | 对抗幻觉 |

### 2. **OpenCompass**（更适合中英双语）

由于你的数据集包含中英文笔记：

```bash
pip install opencompass
python run.py --models hf_lzw-notes-merged --datasets mmlu ceval cmmlu
```

- **C-Eval** / **CMMLU**：中文知识基准
- **MMLU**：英文多任务

### 3. **针对代码模型**（你的 codeparrot 流程）

```bash
# BigCode Evaluation Harness（专门用于代码）
pip install bigcode-evaluation-harness

# HumanEval + MBPP
accelerate launch main.py \
  --model codeparrot \
  --tasks humaneval \
  --n_samples 50 \
  --temperature 0.2 \
  --allow_code_execution
```

### 4. **自定义评估 → 基准差异**

你当前的 `eval_sft.sh` 和 `finetune/eval.py` 是**定性/手动**的——适合快速检查。要获得人们信任的数值，可以像这样将它们封装在 **lm-eval** 中：

```python
# quick_bench.py — 站在巨人的肩膀上
import lm_eval
from lm_eval.models.huggingface import HFLM

model = HFLM(pretrained="./finetune/lzw-notes-merged")
results = lm_eval.simple_evaluate(
    model=model,
    tasks=["mmlu", "gsm8k", "hellaswag"],
    num_fewshot=5,
    batch_size="auto",
)
print(results["results"])
```

### 5. **你的特定模型——推荐评估方案**

| 模型 | 最佳基准 | 设置 |
| ------ | ---------- | ------ |
| **lzw-notes-merged**（Qwen3-8B SFT） | MMLU, GSM8K, C-Eval | `lm_eval --model hf` |
| **CodeParrot** | HumanEval, MBPP | `bigcode-eval-harness` |
| **GPT-2 760M**（你的预训练模型） | HellaSwag, ARC-Easy, LAMBADA | `lm_eval` — 小于 1B 的模型在 MMLU 上表现不佳 |

### 6. **VLLM 集成（最快）**

你的 `finetune/eval.py` 已经使用了 vLLM。将 lm-eval 与 vLLM 后端结合使用：

```bash
lm_eval --model vllm \
  --model_args pretrained=./finetune/lzw-notes-merged,tensor_parallel_size=1 \
  --tasks mmlu,gsm8k \
  --batch_size auto
```

### 7. **排行榜对比**

以标准格式报告结果，以便进行对比：

```json
{
  "model": "lzw-notes-merged",
  "base": "Qwen3-8B",
  "mmlu": 0.682,
  "gsm8k": 0.754,
  "hellaswag": 0.811,
  "ceval": 0.703
}
```

当你说“我微调了一个模型”时，人们期望看到的就是这些数据。

---

**快速开始你的项目：** 安装 `lm-eval` 并在你合并后的模型上运行——你将在 10 分钟内获得 MMLU/GSM8K/HellaSwag 的数值，而这正是社区真正关注的指标。
