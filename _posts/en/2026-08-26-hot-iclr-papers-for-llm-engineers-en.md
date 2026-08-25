---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hot ICLR Papers for LLM Engineers
translated: false
type: note
---

Question: What are the hottest ICLR papers in recent years?

Answer:

For someone focused on **LLM training, inference, agents, and model engineering**, I would not read ICLR randomly. The highest ROI is papers that changed how we build models.

The recent ICLR hot areas:

1. **LLM alignment / post-training**
2. **LLM scaling + training dynamics**
3. **Model editing / knowledge manipulation**
4. **Efficient inference**
5. **Multimodal foundation models**
6. **Data quality and training efficiency**

([ICLR Blog][1])

---

## 1. Learning Dynamics of LLM Finetuning (ICLR 2025)

**Why hot:** Understanding SFT/DPO/RLHF behavior.

Core question:

> Why does fine-tuning sometimes improve capability but destroy general knowledge?

Instead of treating fine-tuning as a black box:

```
pretrained model
        |
        v
      SFT
        |
        v
    aligned model
```

They study the dynamics:

```
parameter update
        |
        v
which knowledge moves?
which capability disappears?
```

Useful for:

* Qwen/Llama fine-tuning
* LoRA
* DPO
* RLHF

If you train your own models, this is very relevant.

([ICLR Blog][1])

---

## 2. Safety Alignment Should be Made More Than Just a Few Tokens Deep (ICLR 2025)

Interesting because it challenges current RLHF.

The idea:

Many safety behaviors are shallow:

```
Prompt:
"How to make a bomb?"

Model:

first few tokens:
"I cannot help..."

but hidden continuation:
maybe unsafe
```

They argue alignment needs deeper representation changes.

This connects to:

* jailbreak resistance
* mechanistic interpretability
* representation engineering

([ICLR Blog][1])

---

## 3. AlphaEdit: Null-Space Constrained Model Editing (ICLR 2025)

Very interesting technically.

Problem:

A neural network stores knowledge:

```
W -> knowledge

Paris -> France
Einstein -> physicist
```

How do you update:

```
Einstein -> painter
```

without destroying:

```
Paris -> France
```

Naive editing:

```
change weights
       |
       v
new fact
       |
       v
forget old knowledge
```

AlphaEdit:

Find directions in parameter space:

```
ΔW

but constrain:

ΔW ⟂ important knowledge space
```

similar idea:

```
update only safe dimensions
```

Useful for:

* enterprise LLM customization
* continual learning
* avoiding full retraining

([ICLR Blog][1])

---

# 4. SAM 2: Segment Anything Model 2 (ICLR 2025)

Meta AI.

Huge CV foundation model.

Old CV:

```
image
 |
CNN
 |
classifier
```

Modern:

```
image/video
     |
foundation model
     |
"segment anything"
```

SAM2 extends segmentation from images to videos.

Applications:

* robotics
* video agents
* autonomous systems

([ICLR Blog][1])

---

# 5. Faster Cascades via Speculative Decoding (ICLR 2025)

Very practical.

LLM inference:

Normal:

```
large model

token1
 |
token2
 |
token3
```

slow.

Speculative decoding:

```
small model:
token1 token2 token3 token4

        |
        v

large model verifies
```

Like:

```
student proposes
teacher checks
```

Can dramatically improve serving throughput.

Relevant to:

* vLLM
* llama.cpp
* OpenAI-style serving

([ICLR Blog][1])

---

# 6. OLMoE: Open Mixture-of-Experts Language Models

Very important direction.

Dense model:

```
70B parameters

every token uses all 70B
```

MoE:

```
70B total

token
 |
router
 |
expert 3
expert 7

only 10B active
```

Benefits:

* cheaper inference
* larger capacity

Related to:

* Mixtral
* DeepSeek MoE
* Qwen-MoE

([Kaggle][2])

---

# 7. Data Shapley in One Training Run

Very relevant because frontier AI is becoming:

> data engineering > architecture engineering

Question:

Which training samples matter?

Traditional:

```
train model
remove data
train again
compare
```

Impossible at trillion-token scale.

They propose estimating importance in one run.

Useful for:

* dataset cleaning
* FineWeb filtering
* synthetic data selection

([ICLR Blog][1])

---

## If I were you (training GPT-2, nanoGPT, vLLM), I would read in this order:

### Tier 1 (direct engineering impact)

1. Speculative Decoding
2. Learning Dynamics of LLM Finetuning
3. OLMoE
4. Data Shapley

### Tier 2 (deep understanding)

5. AlphaEdit
6. Safety Alignment

### Tier 3

7. SAM2

---

The bigger pattern:

2020:

```
Architecture innovation

Transformer
     |
     v
BERT/GPT
```

2023:

```
Scaling

bigger model
more data
more GPU
```

2025:

```
Efficiency + control

better data
better training
better inference
better alignment
```

The frontier moved from:

> "How do we make a bigger model?"

to:

> "How do we make the model learn exactly what we want with limited compute?"

That matches your current direction (nanoGPT → GPU lab → LLM infra) very closely.

References:

* [ICLR 2025 Outstanding Paper Awards](https://blog.iclr.cc/2025/04/22/announcing-the-outstanding-paper-awards-at-iclr-2025/?utm_source=chatgpt.com)
* [ICLR 2025 Paper Rankings](https://www.kaggle.com/general/546726?utm_source=chatgpt.com)

[1]: https://blog.iclr.cc/2025/04/22/announcing-the-outstanding-paper-awards-at-iclr-2025/?utm_source=chatgpt.com "Announcing the Outstanding Paper Awards at ICLR 2025 – ICLR Blog"
[2]: https://www.kaggle.com/general/546726?utm_source=chatgpt.com "Top-rated papers from ICLR 2025 | Kaggle"
