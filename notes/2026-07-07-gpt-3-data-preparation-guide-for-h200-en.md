---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-3 Data Preparation Guide for H200
translated: false
type: note
---

Question: **For training a GPT-3 style model on an H200, what data should we get? Is FineWeb-Edu 25B tokens enough?**

Answer:

For a GPT-3 style pretraining run, the dataset choice matters more than the GPU. H200 only changes **how fast** you train, not **what data you need**.

The original NVIDIA H200 Tensor Core GPU can handle much larger models/batches, but your bottleneck will usually become **data quality + token count + training budget**.

Your current script:

```
HuggingFaceFW/fineweb-edu
25B tokens
~100GB parquet
```

is a good **ablation dataset**, but not a GPT-3 reproduction dataset.

---

## 1. What GPT-3 actually trained on

Original GPT-3 used roughly:

| Dataset               |       Tokens | Purpose          |
| --------------------- | -----------: | ---------------- |
| Common Crawl filtered |        ~410B | general web      |
| WebText2              |         ~19B | high-quality web |
| Books1                |         ~12B | books            |
| Books2                |         ~55B | books            |
| Wikipedia             |          ~3B | encyclopedia     |
| Total                 | ~500B tokens |                  |

The famous GPT-3 ratio:

```
model parameters : training tokens

175B params : 300B tokens
```

roughly follows Chinchilla scaling:

```
tokens ≈ 20 × parameters
```

---

## 2. If you train a small GPT-3 clone today

Assume:

### 1B model

```
parameters = 1B

recommended tokens:
20B tokens
```

### 7B model

```
parameters = 7B

recommended tokens:
140B tokens
```

### 13B model

```
parameters = 13B

recommended tokens:
260B tokens
```

### 70B model

```
parameters = 70B

recommended tokens:
1.4T tokens
```

---

## 3. FineWeb-Edu is good, but incomplete

FineWeb-Edu is excellent because:

* educational filtering
* high quality web
* modern crawl
* permissive license

But:

```
FineWeb-Edu only
        |
        v
mostly web text
```

Missing:

```
books
code
papers
Wikipedia
math
conversation
```

A better mix:

```
FineWeb-Edu          60%
Books                15%
Code                 10%
Wikipedia             5%
Arxiv/papers          5%
Synthetic/instruction 5%
```

---

## 4. For your H200, I would prepare this

For a serious experiment:

```
datasets/

fineweb-edu/
    100B tokens

fineweb/
    100B tokens

starcoder-data/
    20B tokens

wikipedia/
    5B tokens

arxiv/
    5B tokens

books/
    20B tokens
```

Total:

```
~250B tokens
```

Enough for:

```
7B model
```

---

## 5. Storage calculation

Your script:

```
25B tokens
≈100GB
```

because:

```
1 token ≈ 4 bytes
```

Therefore:

```
100B tokens
≈400GB raw parquet

250B tokens
≈1TB raw
```

After tokenization:

```
uint16 token ids

250B tokens × 2 bytes

≈500GB
```

You need:

```
1-2TB NVMe
```

for comfortable preprocessing.

---

## 6. For H200, I would not train GPT-3 175B

Even with H200:

175B:

```
weights FP16:
350GB

optimizer states Adam:
~1.4TB

total training memory:
>2TB
```

Need:

```
8-64 H200 GPUs
```

Instead:

good H200 projects:

### 1.3B

```
tokens:
30B

time:
hours-days
```

### 7B

```
tokens:
140B

time:
days
```

### 13B

```
tokens:
260B

time:
week+
```

---

## 7. Your current downloader design

This:

```python
DEFAULT_TOKENS = 25_000_000_000
```

is good for:

```
GPT-3 ablation
```

meaning:

```
Can we reproduce scaling curves?
Can architecture work?
Can training pipeline work?
```

But not:

```
competitive LLM
```

For H200 I would change:

```python
DEFAULT_TOKENS = 100_000_000_000
```

and add:

```
FineWeb-Edu
+
FineWeb
+
StarCoder
+
Wikipedia
+
Arxiv
```

---

My recommended first H200 run:

```
Model:
Llama-style decoder

Params:
1.3B

Dataset:
50B tokens FineWeb-Edu

Context:
4096

Tokenizer:
GPT-NeoX tokenizer

Optimizer:
AdamW

Precision:
BF16

GPU:
1x H200
```

Then scale:

```
1.3B -> 7B
50B -> 150B tokens
```

This gives a real GPT-style training pipeline without wasting H200 time.
