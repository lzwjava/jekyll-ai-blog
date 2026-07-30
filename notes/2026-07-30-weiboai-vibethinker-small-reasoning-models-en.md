---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeiboAI VibeThinker Small Reasoning Models
translated: false
type: note
---

Question: Intro to Hugging Face organization `WeiboAI`

Answer:

WeiboAI is the official Hugging Face organization of the AI team behind Weibo. It publishes open-weight large language models, especially focusing on **small reasoning models**. ([Hugging Face][1])

The interesting part is that WeiboAI is following the recent trend:

> **"Small models + strong reasoning training can compete with much larger models."**

Their main releases are:

| Model                    |             Size | Purpose                              |
| ------------------------ | ---------------: | ------------------------------------ |
| WeiboAI/VibeThinker-1.5B | ~1.5B parameters | Tiny reasoning model                 |
| WeiboAI/VibeThinker-3B   |    3B parameters | Stronger reasoning/coding/math model |

([Hugging Face][1])

---

## 1. VibeThinker: the idea

The name gives the direction:

* **Vibe** → exploration / intuition
* **Thinker** → reasoning

Instead of scaling from 7B → 70B → 700B, they explore:

```
small base model
        |
        v
high-quality reasoning data
        |
        v
RL / verifiable rewards
        |
        v
small model with strong reasoning ability
```

Similar philosophy to:

* DeepSeek-R1 distilled models
* Qwen reasoning models
* OpenAI o-series style reasoning

---

## 2. Why 3B is interesting

A normal 3B model historically was:

```
3B model:
- chat okay
- simple coding
- weak math
- weak planning
```

But VibeThinker-3B targets:

```
3B model:
- mathematical reasoning
- competition problems
- code reasoning
- chain-of-thought style tasks
```

Community discussions highlighted that VibeThinker-3B showed unusually strong benchmark numbers for its size, while also noting that benchmark specialization may not equal general intelligence. ([Reddit][2])

The important engineering lesson:

**Parameter count is not the only axis.**

A useful mental model:

```
Capability ≈ Model capacity × Training signal quality × Inference compute
```

A 3B model with:

* better data
* better RL
* longer reasoning budget

can beat an old 13B/34B model.

---

## 3. Architecture intuition

Likely pipeline:

```
Base LLM
(Qwen/Llama-like transformer)
        |
        |
Supervised fine tuning
(reasoning traces)
        |
        |
RL / verifiable reward
(math/code checking)
        |
        |
VibeThinker
```

The key difference is the reward function.

For normal chat:

```
human preference reward
"does this answer sound good?"
```

For reasoning:

```
verifiable reward
"did the program run?"
"did math proof pass?"
"did answer match?"
```

Example:

```
Prompt:
Solve x^2 + 5x + 6 = 0

Model:
thinking...
x = -2,-3

Verifier:
correct ✅

Reward:
+1
```

This creates much stronger optimization signals.

---

## 4. Why this matters for AI engineers

For someone doing LLM infra, this is a very interesting direction.

The future stack is probably:

```
Huge foundation models
        |
        |
        +----------------+
        |                |
large general model   small specialists
                       |
                       |
              +--------+--------+
              |
        reasoning model
        coding model
        agent planner
        local assistant
```

A 3B model can run locally:

```
RTX 4070 12GB

3B BF16:
~6GB weights

3B INT4:
~2GB weights
```

So you can run:

```
vLLM
llama.cpp
Ollama
SGLang
```

locally and experiment.

---

## 5. Compared with your nanoGPT experiments

Your GPT-2 124M training experience is actually close philosophically.

You trained:

```
small transformer
        |
        |
large token dataset
        |
        |
emergent capability
```

VibeThinker does:

```
small transformer
        |
        |
high-quality reasoning trajectories
        |
        |
reasoning capability
```

The difference:

Your experiment optimized:

```
next-token prediction loss
```

VibeThinker optimizes:

```
answer correctness / reasoning behavior
```

The training objective changed.

---

## 6. How I would test it locally

On your RTX 4070:

```bash
pip install transformers accelerate

python - <<'PY'
from transformers import pipeline

pipe = pipeline(
    "text-generation",
    model="WeiboAI/VibeThinker-3B",
    device_map="auto"
)

print(pipe(
    "Explain why attention uses Q,K,V matrices",
    max_new_tokens=500
))
PY
```

For production inference:

```bash
vllm serve WeiboAI/VibeThinker-3B \
  --dtype half
```

---

My take: WeiboAI is interesting not because it created another LLM, but because it is exploring the same direction that DeepSeek popularized:

**reduce parameter size, increase reasoning training quality.**

For AI infra engineers, models like VibeThinker are actually more valuable than giant models because they expose the whole stack:

* tokenizer
* training data
* RL pipeline
* inference optimization
* quantization
* local deployment

References:

* Hugging Face WeiboAI organization ([Hugging Face][1])
* WeiboAI VibeThinker model listings ([Hugging Face][3])
* Community discussion on VibeThinker-3B benchmarks ([Reddit][2])

[1]: https://huggingface.co/WeiboAI?utm_source=chatgpt.com "WeiboAI (WeiboAI)"
[2]: https://www.reddit.com/r/LocalLLM/comments/1u7ixap/a_3b_model_is_suddenly_scoring_near_frontier/?utm_source=chatgpt.com "A 3B model is suddenly scoring near frontier models on math/coding benchmarks. Is this real or just benchmarkmaxxing?"
[3]: https://huggingface.co/models?search=WeiboAI%2FVibeThinker-1.5B&utm_source=chatgpt.com "Models – Hugging Face"