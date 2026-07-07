---
audio: false
generated: true
image: false
lang: en
layout: post
title: SFT in LLM Training Pipeline
translated: false
type: note
---

Question: What is SFT in LLM?

Answer:

**SFT (Supervised Fine-Tuning)** is the stage where you take a pretrained language model and train it on **(prompt, response)** pairs using standard supervised learning.

Mathematically, it's just **next-token prediction again**, except on high-quality instruction data instead of internet text.

---

## The LLM training pipeline

```
Raw Internet Text
        │
        ▼
Pretraining
(next token prediction)
        │
        ▼
Base Model
        │
        ▼
SFT
(instruction dataset)
        │
        ▼
Instruction Model
        │
        ▼
Preference Optimization
(RLHF / DPO / GRPO / etc.)
        │
        ▼
Chat Model
```

---

## During pretraining

The model sees

```
The capital of France is Paris.

Python is a programming language.

...
```

Objective:

[
L = -\sum \log P(x_t|x_{<t})
]

Nothing special.

The model simply predicts the next token.

---

## During SFT

Now your dataset looks like

```json
{
    "instruction": "Translate to French",
    "input": "Hello",
    "output": "Bonjour"
}
```

or

```text
User:
How do I reverse a list in Python?

Assistant:
Use list.reverse() or reversed().
```

Training sample becomes

```
<user>
How do I reverse a list in Python?
</user>

<assistant>
Use list.reverse() or reversed().
</assistant>
```

The loss is computed **only on the assistant tokens**.

---

## Masking

Suppose tokens are

```
User:
How are you ?

Assistant:
I'm good .
```

Training labels

```
User:
X X X X X

Assistant:
I'm good .
```

where

```
X = ignore_index (-100)
```

Loss is

```
predict "I'm"
predict "good"
predict "."
```

NOT

```
predict User:
predict How
predict are
...
```

In PyTorch

```python
labels = input_ids.clone()

labels[user_tokens] = -100
```

Then

```python
loss = cross_entropy(
    logits.view(-1, vocab_size),
    labels.view(-1)
)
```

---

## Why does SFT work?

Pretraining teaches

> "What language looks like."

SFT teaches

> "How an assistant should respond."

Example:

Base model

```
Q: What's 2+2?

The question asks...
```

After SFT

```
User: What's 2+2?

Assistant: 4
```

The model learns the chat format and response style.

---

## Example dataset

A single SFT example:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Write Fibonacci in Python."
    },
    {
      "role": "assistant",
      "content": "def fib(n): ..."
    }
  ]
}
```

Thousands or millions of these are concatenated and tokenized.

---

## Training loop

Very little changes compared to pretraining.

```python
for batch in dataloader:

    logits = model(batch["input_ids"])

    loss = cross_entropy(
        logits,
        batch["labels"]   # masked with -100
    )

    loss.backward()
    optimizer.step()
```

The architecture is identical.

Only the **training data** and **label masking** differ.

---

## Common SFT datasets

Popular open datasets include:

* OpenAssistant conversations
* Hugging Face H4 datasets
* LMSYS Chat datasets
* OpenMathInstruct
* Tulu
* Proprietary instruction datasets from companies such as OpenAI, Anthropic, and Google.

---

## SFT vs RLHF vs DPO

| Method      | Training Signal                       | Goal                                     |
| ----------- | ------------------------------------- | ---------------------------------------- |
| Pretraining | Internet text                         | Learn language and world knowledge       |
| SFT         | Human-written demonstrations          | Learn to follow instructions             |
| RLHF        | Reward model + reinforcement learning | Optimize responses for human preferences |
| DPO         | Preferred vs rejected response pairs  | Learn preferences directly without RL    |

SFT is typically the **first post-training stage** because it provides a strong supervised initialization before preference optimization.

References:

* [TRL (Transformer Reinforcement Learning) documentation](https://huggingface.co/docs/trl?utm_source=chatgpt.com)
* [Hugging Face LLM Course – Supervised Fine-Tuning](https://huggingface.co/learn/llm-course?utm_source=chatgpt.com)
* [Stanford Alpaca paper and project](https://crfm.stanford.edu/2023/03/13/alpaca.html?utm_source=chatgpt.com)