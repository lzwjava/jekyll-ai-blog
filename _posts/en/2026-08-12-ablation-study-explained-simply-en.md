---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ablation Study Explained Simply
translated: false
type: note
---

**Question: What does “消融实验” mean?**

**Answer:**

“消融实验” in English is **ablation study** (or **ablation experiment**).

It is a common experiment method in machine learning research. The idea is:

> Remove or disable one component of a model/system and observe how much the performance changes.

The word “ablation” comes from physics/medicine meaning “removal”. In ML, it means **cutting away parts of your model to understand what each part contributes**.

Example:

Suppose you design a Transformer variant:

```
Model A:
Embedding
   +
Self Attention
   +
RoPE
   +
Flash Attention
   +
MLA
   +
FFN
```

You claim:

> "MLA improves long-context performance."

You run ablation:

| Model              | Component removed | Accuracy |
| ------------------ | ----------------- | -------: |
| Full model         | none              |    85.0% |
| w/o MLA            | remove MLA        |    81.5% |
| w/o RoPE           | remove RoPE       |    78.0% |
| w/o FlashAttention | normal attention  |    84.8% |

Then you can conclude:

* MLA contributes +3.5%
* RoPE contributes +7%
* FlashAttention mainly affects speed/memory, not accuracy

---

For LLM research, common ablations:

### 1. Architecture ablation

Example:

DeepSeek-V3 uses:

* MoE
* MLA (Multi-head Latent Attention)
* auxiliary-loss-free load balancing
* Multi-token prediction

Researchers may test:

```
DeepSeek-V3 full
        |
        +-- remove MLA
        |
        +-- remove MoE
        |
        +-- remove MTP
```

Measure:

* perplexity
* benchmark scores
* inference cost

---

### 2. Data ablation

Question:

"Does more code data help?"

Experiments:

```
Training dataset:

100B tokens
      |
      +-- remove code data
      |
      +-- remove math data
      |
      +-- remove web data
```

Then see which data source matters.

---

### 3. Training technique ablation

Example:

You train GPT-2:

Baseline:

```
AdamW
learning rate 3e-4
cosine decay
weight decay 0.1
```

Ablations:

```
remove weight decay
remove cosine schedule
change optimizer
```

Compare validation loss.

---

The deeper idea:

Ablation is basically **causal analysis**.

Normal experiment:

```
A happened
B happened
Performance improved

Can we know why?
```

Ablation:

```
A+B+C → good

Remove A:

B+C → worse

Therefore A likely contributes.
```

It is not perfect causal proof, because components can interact, but it is one of the main tools researchers use to understand neural networks.

For LLM papers, if you read sections titled:

* **Ablation Study**
* **Component Analysis**
* **Ablation Experiments**

they are usually answering:

> "Which parts of this model are actually responsible for the gains?"