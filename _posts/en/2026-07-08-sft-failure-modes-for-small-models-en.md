---
audio: false
generated: true
image: false
lang: en
layout: post
title: SFT Failure Modes for Small Models
translated: false
type: note
---

Your analysis is directionally right. It is actually a good empirical observation of the common failure modes of **small models after SFT**. A few refinements:

1. **"没办法做数学推理"**

Mostly right, but the root cause is not simply "small model". SFT often teaches *patterns* rather than improving the underlying reasoning ability.

Example:

Before SFT:

```
Q: If Alice has 3 apples and buys 2 more, how many?
A:
```

A base model may have learned some arithmetic patterns from pretraining.

After bad SFT:

```
Q: If Alice has 3 apples...
A: We need to consider the situation carefully. Alice initially...
```

The model learns the *style of answering* but not necessarily the multi-step computation.

Math reasoning usually needs:

* high-quality chain-of-thought / reasoning traces
* RL/post-training optimization
* tool usage
* larger model capacity

---

2. **"循环 loops，车轱辘说"**

Yes. Very common.

Small SFT models often have:

```
User: explain TCP

Model:
TCP is a protocol...
It provides reliable communication...
Reliable communication means...
TCP is important because reliable communication...
```

Why?

Because SFT optimizes:

[
\max_\theta \sum_t \log P(y_t|x,y_{<t})
]

It learns local token prediction. If the dataset contains repetitive explanations, the model learns the repetition pattern.

Common fixes:

* better SFT data filtering
* remove duplicated samples
* preference optimization (DPO/RLHF)
* stronger base model
* longer context training

---

3. **"只会记住事实，参数越大的模型记住事实越好"**

Mostly correct.

Model scale improves:

* memorization capacity
* representation richness
* generalization

A 7B model and 70B model trained on the same corpus:

70B usually:

* remembers more rare facts
* handles more abstraction
* follows instructions better

Because parameter count roughly increases the model's capacity:

[
\text{capacity} \propto N_{params}
]

But facts are not simply stored like a database. They are distributed in weights.

---

4. **"代码总体表现更好"**

Also correct.

Code is special because:

* syntax is rigid
* feedback is binary (compile/pass/fail)
* training data has huge volume
* code has internal structure

Example:

Python:

```python
def add(a,b):
    return a+b
```

There are strong statistical constraints.

Natural language:

```
The economy is...
```

has much higher ambiguity.

So even small models often become surprisingly good coding assistants after SFT.

---

Your pipeline:

```
text small model
        |
code small model
        |
finance small model
        |
merge datasets
        |
SFT
        |
evaluate
```

The interesting observation is:

**different domains produce different surface behavior, but SFT failure modes are shared.**

Because they come from the same optimization mechanism:

```
dataset
   |
   v
supervised token prediction
   |
   v
learn distribution of answers
```

not necessarily:

```
learn reasoning algorithm
learn world model
learn planning
```

Your idea of using Hermes to record all input/output pairs is actually the right debugging workflow:

```
prompt
  |
  v
model
  |
  v
response
  |
  v
save jsonl/txt
  |
  v
manual inspection
```

For example:

```json
{
  "instruction": "Solve this math problem...",
  "output": "....",
  "failure": "looping"
}
```

Then cluster failures:

```
math:
  - wrong arithmetic
  - no reasoning

coding:
  - syntax error
  - hallucinated API

finance:
  - outdated facts
  - overconfident answer

general:
  - repetition
  - refusal
```

This is basically how modern post-training teams debug SFT models. The next step after SFT is usually not "more SFT", but building a **preference dataset**:

```
prompt
 |
 +-- good answer
 |
 +-- bad answer
```

then optimize:

[
P_\theta(y_{good}) > P_\theta(y_{bad})
]

using DPO/IPO/RL.

Your observations are very close to what many teams discover when they train their first small instruction models.
