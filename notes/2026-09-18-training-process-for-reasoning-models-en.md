---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Process for Reasoning Models
translated: false
type: note
---

Question: How are reasoning models trained?

Answer:

Modern reasoning models (OpenAI o-series, DeepSeek-R1, Qwen reasoning models, etc.) are usually trained with a **multi-stage pipeline**. The key idea is: instead of only learning "predict the next token", the model is optimized to **search through possible solutions and receive feedback on correctness**.

A simplified pipeline:

```
Base LLM pretraining
        |
        v
Supervised Fine-Tuning (SFT)
        |
        v
Reasoning trace training
        |
        v
RL with verifiable rewards (RLVR)
        |
        v
Preference optimization / distillation
        |
        v
Deployment model
```

---

## 1. Start with a pretrained language model

Example:

```
Internet text
     |
     v
Transformer
     |
     v
Base model
```

Training objective:

Given tokens:

```
"The capital of France is"
```

predict:

```
" Paris"
```

Loss:

$$
L = -\sum_t \log P(x_t|x_{<t})
$$

At this stage the model knows language, code, math patterns, but it does not reliably reason.

---

## 2. Supervised Fine-Tuning (SFT)

Create examples:

```
Question:
Solve:
x^2 + 5x + 6 = 0

Answer:
Let's factor:
x^2+5x+6=(x+2)(x+3)

Therefore:
x=-2,-3
```

Dataset:

```
(input, reasoning, answer)
```

Train with normal next-token prediction.

The model learns:

```
problem
   |
   v
generate intermediate steps
   |
   v
final answer
```

However, SFT has a problem:

The model imitates reasoning style, but does not necessarily learn better reasoning.

A model can write:

```
Step 1...
Step 2...
Therefore...
```

and still be wrong.

---

# 3. RL with verifiable rewards (RLVR)

This is the important breakthrough.

Instead of humans scoring every answer, use automatic checkers.

Examples:

## Math

Model:

```
Solve:
12345 * 6789

<think>
...
</think>

answer:
83810205
```

Reward:

```
checker(answer)

correct -> +1
wrong   -> 0
```

---

## Code

Model generates:

```python
def two_sum(nums,target):
    ...
```

Run:

```
pytest tests/
```

Reward:

```
all tests pass:
+1

failed:
0
```

---

## Lean theorem proving

Model:

```
theorem foo :
  a+b=b+a := by
     ...
```

Lean compiler:

```
accepted -> +1
rejected -> 0
```

This creates a training loop:

```
          generate solution
                 |
                 v
              execute
                 |
                 v
            reward score
                 |
                 v
          update model weights
```

---

# 4. Policy optimization

The model is treated as a policy:

$$
\pi_\theta(y|x)
$$

Input:

```
math problem x
```

Output:

```
reasoning trace y
```

Reward:

$$
R(x,y)
$$

Training tries to maximize:

$$
E[R(x,y)]
$$

Typical algorithms:

* PPO
* GRPO
* RLOO
* DPO variants

Example GRPO idea:

Generate multiple answers:

```
answer A -> reward 1.0
answer B -> reward 0.2
answer C -> reward 0.0
```

Increase probability of A:

$$
\nabla_\theta \log \pi_\theta(y|x)R
$$

Decrease probability of bad trajectories.

---

# 5. Why reasoning emerges

A surprising thing happens:

The model discovers useful internal strategies:

Example:

Before RL:

```
Question:
What is 12345*6789?

Model:
12345*6789=...
```

After RL:

```
<think>

Break multiplication:

6789*12000
+
6789*345

...

</think>
```

The model learns:

* decomposition
* verification
* backtracking
* self-correction
* planning

because those strategies increase reward.

---

# 6. Synthetic reasoning data

Large labs also generate data:

```
Strong teacher model
        |
        v
Generate millions of problems
        |
        v
Solve automatically
        |
        v
Filter good solutions
        |
        v
Train student model
```

Example:

Generate:

```
100 million math problems
```

Filter:

```
correct solutions only
```

Train:

```
student model
```

This is how smaller reasoning models can become strong.

---

# 7. Test-time compute

Reasoning models also use more inference compute.

Normal LLM:

```
Question
   |
   v
one answer
```

Reasoning model:

```
Question
   |
   +---- solution A
   |
   +---- solution B
   |
   +---- solution C
             |
             v
          judge
             |
             v
          final answer
```

More thinking tokens = more search.

---

# The whole system

A modern reasoning model looks like:

```
                Internet/code/math data
                       |
                       v
                 Base Transformer
                       |
                       v
                    SFT
                       |
                       v
             reasoning demonstrations
                       |
                       v
                 RLVR environment
                       |
        +--------------+--------------+
        |                             |
   generate traces              execute/check
        |                             |
        +------------- reward --------+
                       |
                       v
                optimized model
```

The biggest conceptual shift:

**Old LLM training:**

> predict human text.

**Reasoning model training:**

> generate actions, receive feedback, optimize toward solutions.

This is why Lean, code execution, math verifiers, simulators, and games are becoming important: they provide cheap, scalable ground-truth rewards.

I can also walk through a minimal implementation of a DeepSeek-R1-style RLVR training loop in PyTorch (tiny model + math verifier) if useful.
