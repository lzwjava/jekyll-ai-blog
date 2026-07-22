---
audio: false
generated: true
image: false
lang: zh
layout: post
title: EleutherAI语言模型评估框架
translated: true
type: note
---

问题：EleutherAI/lm-evaluation-harness 简介

回答：

EleutherAI 的 **lm-evaluation-harness** 是衡量 LLM 质量的标准工具之一。可以将其视为**语言模型的 pytest + 基准测试运行器**。它为研究人员提供了一种可复现的方式来回答：

> "我的模型真的更好，还是只是感觉更好？"

（[GitHub][1]）

## 它解决了什么问题？

在此类工具出现之前，每篇论文都有自定义的评估脚本：

```
model.py
eval.py
prompt_template.py
score.py
```

难以比较。

lm-evaluation-harness 标准化了以下流程：

```
模型
  ↓
分词器 / 提示格式
  ↓
基准测试任务
  ↓
推理
  ↓
指标计算
  ↓
JSON 结果
```

示例：

```
Qwen3-8B
    |
    v
MMLU
    |
    v
准确率 = 78.5%
```

现在，其他研究人员可以运行相同的设置并进行比较。

它为许多公开的 LLM 排行榜提供支持，包括 Hugging Face Open LLM 排行榜工作流。（[GitHub][1]）

---

## 支持的基准测试

常见任务：

* MMLU — 广泛知识
* HellaSwag — 常识补全
* ARC — 科学推理
* GSM8K — 数学推理
* TruthfulQA — 幻觉/真实性
* BIG-Bench 任务
* HumanEval 风格代码任务

它拥有数十个基准测试系列和数百个子任务。（[GitHub][1]）

---

## 基本用法

安装：

```bash
git clone https://github.com/EleutherAI/lm-evaluation-harness
cd lm-evaluation-harness

pip install -e .
pip install "lm_eval[hf]"
```

在 HellaSwag 上运行 GPT-2：

```bash
lm_eval run \
  --model hf \
  --model_args pretrained=gpt2 \
  --tasks hellaswag
```

（[GitHub][2]）

运行现代本地模型：

```bash
lm_eval run \
  --model hf \
  --model_args pretrained=Qwen/Qwen3-8B \
  --tasks mmlu,gsm8k \
  --device cuda:0 \
  --batch_size auto
```

---

## 适用于您的 RTX 4070 工作流

这与您的实验非常相关：

您训练的：

```
GPT-2 124M
SEC 数据集
RTX 4070
损失 ~2.28
```

下一步不仅仅是损失。您需要下游评估：

```
检查点
    |
    v
lm-evaluation-harness
    |
    +--> lambada
    +--> hellaswag
    +--> arc_easy
    +--> piqa
    +--> winogrande
```

示例：

```bash
lm_eval run \
  --model hf \
  --model_args pretrained=./my-gpt2-checkpoint \
  --tasks hellaswag,arc_easy \
  --device cuda:0
```

这会告诉您训练是否确实提升了实际语言能力。

---

## 架构思路

代码结构大致如下：

```
lm_eval/

├── models/
│   ├── hf.py          # HuggingFace 模型
│   ├── vllm.py        # vLLM 后端
│   └── api_models.py  # OpenAI 兼容 API
│
├── tasks/
│   ├── mmlu/
│   ├── gsm8k/
│   └── hellaswag/
│
├── evaluator.py
└── metrics/
```

关键抽象：

```python
class LM:
    def loglikelihood()
    def generate_until()
```

每个后端都实现此接口。

然后基准测试不关心模型是：

```
transformers
vLLM
OpenAI API
DeepSpeed
Megatron
```

它们只调用：

```python
model.generate_until(prompt)
```

---

## 自定义基准测试

您可以创建自己的任务：

```
tasks/
  my_company_eval/
      task.yaml
```

示例：

{% raw %}
```yaml
task: my_eval

dataset_path: json
dataset_kwargs:
  data_files:
    test: test.json

output_type: multiple_choice

doc_to_text: "{{question}}"

doc_to_choice:
  - A
  - B
  - C
  - D

metric_list:
  - metric: acc
```
{% endraw %}

YAML 驱动的设计使实验具有可复现性。（[GitHub][3]）

---

## 与其他工具的区别

| 工具                  | 用途                         |
| --------------------- | ---------------------------- |
| lm-evaluation-harness | 学术/通用 LLM 基准测试       |
| vLLM benchmark        | 吞吐量/延迟                  |
| OpenCompass           | 大规模评估平台               |
| DeepEval              | 应用级测试                   |
| SWE-bench             | 编程智能体评估               |

对于**模型训练研究**，lm-eval 很可能是训练后首先添加的工具。

您当前的流程可以变成：

```
nanoGPT / PyTorch
        |
        v
检查点
        |
        v
lm-evaluation-harness
        |
        v
基准测试报告
        |
        v
W&B / 博客 / 论文
```

参考文献：

* EleutherAI lm-evaluation-harness（[GitHub][1]）
* CLI 和任务接口文档（[GitHub][2]）
* 评估可复现性论文（[arxiv.org][4]）

[1]: https://github.com/EleutherAI/lm-evaluation-harness?utm_source=chatgpt.com "GitHub - EleutherAI/lm-evaluation-harness: 一种用于语言模型少样本评估的框架"
[2]: https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/interface.md?utm_source=chatgpt.com "lm-evaluation-harness/docs/interface.md at main · EleutherAI/lm-evaluation-harness · GitHub"
[3]: https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/task_guide.md?utm_source=chatgpt.com "lm-evaluation-harness/docs/task_guide.md at main · EleutherAI/lm-evaluation-harness · GitHub"
[4]: https://arxiv.org/abs/2405.14782?utm_source=chatgpt.com "来自前线的语言模型可复现评估经验教训"