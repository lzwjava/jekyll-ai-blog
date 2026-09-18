---
audio: false
generated: true
image: false
lang: en
layout: post
title: Verifiable RL Training Pipeline
translated: false
type: note
---

Yes, your understanding is basically correct.

**Question:**
RL uses generated data + reward scores + verifiable rules (Lean/code execution) to guide a model toward desired behavior?

**Answer:**

A simplified RL pipeline looks like this:

```
LLM policy πθ
    |
    | generate output y
    v
Environment / Verifier
    |
    | compute reward r
    v
RL algorithm updates θ
    |
    v
Better future outputs
```

The key idea:

> The model does not directly learn "the correct answer". It learns a policy that increases expected reward.

Mathematically:

$$
J(\theta)=E_{y\sim \pi_\theta}[R(y)]
$$

RL tries to adjust model parameters:

$$
\theta \leftarrow \theta + \alpha \nabla_\theta J(\theta)
$$

so outputs with higher rewards become more likely.

---

## Example 1: Code generation

Prompt:

```
Write a Python function to sort a list
```

Model generates:

```python
def sort(x):
    return x[::-1]
```

Verifier runs:

```bash
pytest tests.py
```

Result:

```
FAILED
```

Reward:

```
r = 0
```

Another sample:

```python
def sort(x):
    return sorted(x)
```

Test:

```
PASSED
```

Reward:

```
r = 1
```

RL learns:

```
outputs that pass tests
↑ probability
```

---

## Example 2: Lean theorem proving

The model generates:

```lean
theorem add_zero (n : Nat) :
  n + 0 = n := by
  rfl
```

Lean compiler:

```
SUCCESS
```

Reward:

```
+1
```

Bad proof:

```lean
by
  sorry
```

Lean rejects:

```
FAIL
```

Reward:

```
0
```

The verifier becomes a **ground truth machine**.

---

## Why this is powerful

Traditional RLHF:

```
Human:
"This answer feels better"
        |
        v
Reward model
        |
        v
RL
```

Problem:

* subjective
* expensive
* reward hacking

---

Verifiable RL:

```
Computer:
"Does it compile?"
"Does theorem prove?"
"Does simulator succeed?"
        |
        v
Exact reward
```

Examples:

| Domain          | Verifier            |
| --------------- | ------------------- |
| Programming     | unit tests/compiler |
| Math            | Lean/Coq/Isabelle   |
| Robotics        | simulator           |
| Games           | game score          |
| SQL             | database execution  |
| Hardware design | EDA tools           |

The reward is almost binary:

```
correct = 1
wrong   = 0
```

---

This is the core idea behind recent **reasoning models**:

```
Base model
    +
large-scale generated problems
    +
verifiable reward
    +
RL optimization
    =
stronger reasoning model
```

For example, math:

```
Generate 1000 solutions

Solution A:
proof checker PASS
reward=1

Solution B:
wrong algebra
reward=0

RL pushes probability toward A-like reasoning patterns
```

The interesting part is that the model can discover **new internal strategies** because RL only says:

> "This output succeeded."

It does not explicitly teach every reasoning step.

That is why verifiable environments (Lean, code execution, games, simulators) are becoming important for training reasoning models.
