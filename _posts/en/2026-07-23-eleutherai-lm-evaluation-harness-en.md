---
audio: false
generated: true
image: false
lang: en
layout: post
title: EleutherAI LM Evaluation Harness
translated: false
type: note
---

Question: intro to EleutherAI/lm-evaluation-harness

Answer:

EleutherAI's **lm-evaluation-harness** is one of the standard tools for measuring LLM quality. Think of it as the **pytest + benchmark runner for language models**. It gives researchers a reproducible way to answer:

> "Is my model actually better, or does it just feel better?"

([GitHub][1])

## What problem does it solve?

Before tools like this, every paper had custom evaluation scripts:

```
model.py
eval.py
prompt_template.py
score.py
```

Hard to compare.

lm-evaluation-harness standardizes:

```
Model
  ↓
Tokenizer / prompt format
  ↓
Benchmark task
  ↓
Inference
  ↓
Metric calculation
  ↓
JSON result
```

Example:

```
Qwen3-8B
    |
    v
MMLU
    |
    v
accuracy = 78.5%
```

Now another researcher can run the same setup and compare.

It powers many public LLM leaderboards, including the Hugging Face Open LLM Leaderboard workflow. ([GitHub][1])

---

## Supported benchmarks

Common tasks:

* MMLU — broad knowledge
* HellaSwag — commonsense completion
* ARC — science reasoning
* GSM8K — math reasoning
* TruthfulQA — hallucination/truthfulness
* BIG-Bench tasks
* HumanEval-style code tasks

It has dozens of benchmark families and hundreds of subtasks. ([GitHub][1])

---

## Basic usage

Install:

```bash
git clone https://github.com/EleutherAI/lm-evaluation-harness
cd lm-evaluation-harness

pip install -e .
pip install "lm_eval[hf]"
```

Run GPT-2 on HellaSwag:

```bash
lm_eval run \
  --model hf \
  --model_args pretrained=gpt2 \
  --tasks hellaswag
```

([GitHub][2])

Run a modern local model:

```bash
lm_eval run \
  --model hf \
  --model_args pretrained=Qwen/Qwen3-8B \
  --tasks mmlu,gsm8k \
  --device cuda:0 \
  --batch_size auto
```

---

## For your RTX 4070 workflow

This is very relevant for your experiments:

You trained:

```
GPT-2 124M
SEC dataset
RTX 4070
loss ~2.28
```

The next step is not only loss. You want downstream evaluation:

```
checkpoint
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

Example:

```bash
lm_eval run \
  --model hf \
  --model_args pretrained=./my-gpt2-checkpoint \
  --tasks hellaswag,arc_easy \
  --device cuda:0
```

This tells you whether training improved actual language ability.

---

## Architecture idea

The code structure is roughly:

```
lm_eval/

├── models/
│   ├── hf.py          # HuggingFace models
│   ├── vllm.py        # vLLM backend
│   └── api_models.py  # OpenAI compatible APIs
│
├── tasks/
│   ├── mmlu/
│   ├── gsm8k/
│   └── hellaswag/
│
├── evaluator.py
└── metrics/
```

The key abstraction:

```python
class LM:
    def loglikelihood()
    def generate_until()
```

Every backend implements this interface.

Then benchmarks do not care whether the model is:

```
transformers
vLLM
OpenAI API
DeepSpeed
Megatron
```

They only call:

```python
model.generate_until(prompt)
```

---

## Custom benchmark

You can create your own task:

```
tasks/
  my_company_eval/
      task.yaml
```

Example:

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

The YAML-driven design makes experiments reproducible. ([GitHub][3])

---

## Difference from other tools

| Tool                  | Purpose                        |
| --------------------- | ------------------------------ |
| lm-evaluation-harness | Academic/general LLM benchmark |
| vLLM benchmark        | Throughput/latency             |
| OpenCompass           | Large evaluation platform      |
| DeepEval              | Application-level testing      |
| SWE-bench             | Coding agent evaluation        |

For **model training research**, lm-eval is probably the first tool to add after training.

Your current stack could become:

```
nanoGPT / PyTorch
        |
        v
checkpoint
        |
        v
lm-evaluation-harness
        |
        v
benchmark report
        |
        v
W&B / blog / paper
```

References:

* EleutherAI lm-evaluation-harness ([GitHub][1])
* CLI and task interface docs ([GitHub][2])
* Evaluation reproducibility paper ([arxiv.org][4])

[1]: https://github.com/EleutherAI/lm-evaluation-harness?utm_source=chatgpt.com "GitHub - EleutherAI/lm-evaluation-harness: A framework for few-shot evaluation of language models. · GitHub"
[2]: https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/interface.md?utm_source=chatgpt.com "lm-evaluation-harness/docs/interface.md at main · EleutherAI/lm-evaluation-harness · GitHub"
[3]: https://github.com/EleutherAI/lm-evaluation-harness/blob/main/docs/task_guide.md?utm_source=chatgpt.com "lm-evaluation-harness/docs/task_guide.md at main · EleutherAI/lm-evaluation-harness · GitHub"
[4]: https://arxiv.org/abs/2405.14782?utm_source=chatgpt.com "Lessons from the Trenches on Reproducible Evaluation of Language Models"
