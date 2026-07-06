---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Systems Bootcamp in China
translated: false
type: note
---

Question: Is starting an AI bootcamp in China for high school / university students (model training, agents, etc.) a good idea?

Answer:

Yes — but only if you *don’t position it as “AI education”*. That market is already saturated with tutorial-style courses. The viable version is:

> **“AI systems bootcamp: build + deploy real agents and small-scale models in 2–4 weeks.”**

You’re not teaching theory. You’re compressing real production workflows (like what you already do with GPU training + CLI agents) into hands-on shipping.

---

## 1. Where the real opportunity is

Most China bootcamps:

* teach Python basics
* wrap HuggingFace pipelines
* stop at notebook-level demos

Gap you can exploit:

* **end-to-end systems thinking**

  * data → training → eval → deployment → agent loop
* **real infra exposure**

  * multi-GPU training, not Colab toys
* **agent engineering**

  * tool use, memory, planning, CLI-first workflows

This is closer to:

* “mini OpenAI applied lab”
* not “AI course”

---

## 2. What to teach (tight, production-first)

### Week 1 — LLM + inference core

* tokenization, attention (only intuition-level math)
* run local LLM (vLLM / llama.cpp)
* build CLI chat interface

```bash
python chat.py --model Qwen2.5-7B
```

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B")

prompt = "Design a trading agent architecture"
inputs = tok(prompt, return_tensors="pt")
out = model.generate(**inputs, max_new_tokens=200)
print(tok.decode(out[0]))
```

---

### Week 2 — Fine-tuning small models

* LoRA / QLoRA
* dataset building (critical skill most ignore)
* eval loops

```bash
accelerate launch train_lora.py \
  --model meta-llama/Llama-3-8B \
  --dataset data.jsonl
```

Key idea: students learn **data quality > model choice**

---

### Week 3 — Agents (core differentiator)

* tool calling
* memory (vector DB)
* planning loop

Minimal agent loop:

```python
while True:
    obs = env.observe()
    action = llm(f"Obs: {obs}\nWhat next action?")
    env.step(action)
```

Add:

* web tools
* code execution
* file system tools

---

### Week 4 — Capstone system

Examples:

* research agent (paper → summary → repo)
* trading simulator agent
* WeChat content generator pipeline
* code review bot for GitHub repos

Must deploy:

* FastAPI backend
* simple web UI or CLI (CLI preferred if you want engineering purity)

---

## 3. Stack (keep it realistic)

* Training: PyTorch + HF + DeepSpeed (optional)
* Inference: vLLM / llama.cpp
* Agents: pure Python loops (avoid frameworks first)
* Vector DB: FAISS (no overengineering)
* Deployment: Docker + simple VPS

Avoid:

* “no-code AI platforms”
* heavy SaaS abstractions

---

## 4. Business reality in China

### Strong signals

* parents pay for “future-proof skills”
* universities want “AI practical training”
* strong interest in agents + LLM apps

### Weak points

* regulatory sensitivity (content + minors)
* high churn unless output is visible (projects)

### Pricing structure

* 2–4 week intensive: 3k–10k RMB/student
* cohort-based (20–50 ppl)
* strong leverage if you show GitHub output

---

## 5. Your real moat

Given your background (training models, GPU infra, agent CLI tools), your edge is:

* you can show *real training runs*, not slides
* you can teach “how systems break in production”
* you can design curriculum from first principles

That’s rare. Most instructors are 2 layers removed from real infra.

---

## 6. Failure modes (important)

1. **Becoming tutorial factory**

   * students copy notebooks → no retention

2. **Too much theory**

   * kills perceived value fast

3. **No artifact output**

   * must force GitHub repos every week

4. **Over-frameworking agents**

   * LangChain-style abstraction early → confusion

---

## 7. MVP suggestion

Don’t start with a school.

Start with:

* 1 cohort (10–15 people)
* 2-week “agent sprint”
* goal: everyone ships 1 working agent repo

If retention + output quality is high → expand.

---

References:

* [https://github.com/karpathy/minGPT](https://github.com/karpathy/minGPT)
* [https://github.com/huggingface/transformers](https://github.com/huggingface/transformers)
* [https://course.fast.ai](https://course.fast.ai)
* [https://docs.vllm.ai/en/latest/](https://docs.vllm.ai/en/latest/)
