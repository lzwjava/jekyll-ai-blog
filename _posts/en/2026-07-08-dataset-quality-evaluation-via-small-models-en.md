---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dataset Quality Evaluation via Small Models
translated: false
type: note
---

Question: You're asking whether using a much smaller model (e.g. 64M) trained on the same amount of data is a good way to compare dataset quality, instead of repeating expensive 124M experiments.

Answer:

Yes. In fact, this is a very common scaling methodology.

The key idea is:

> **Fix everything except the dataset.**

That means:

* Same model architecture (GPT-2)
* Same optimizer
* Same LR schedule
* Same tokenizer
* Same number of training tokens
* Same random seed (or several seeds)
* Same batch size
* Same training steps

Only change

> Dataset A vs Dataset B

Then the model becomes a **measurement instrument** for dataset quality.

---

### Why 64M is better than 124M

A 124M GPT-2 is already fairly expensive.

If you want to compare

* SEC-EDGAR cleaned v1
* SEC-EDGAR cleaned v2
* SEC-EDGAR deduplicated
* SEC-EDGAR + earnings calls
* SEC-EDGAR + finance news

you might need dozens of runs.

64M lets you iterate much faster.

For dataset research,

> train many cheap models > one expensive model

This is exactly what organizations like OpenAI, Anthropic, and Meta do internally during data ablations.

---

### Think of the model as a microscope

Suppose you have

Dataset A

```
10GB
```

Dataset B

```
10GB
```

Same tokenizer

Same architecture

Same compute

Train

```
GPT2-64M
```

Now compare

Training

```
loss
```

Validation

```
loss
```

Perplexity

```
ppl
```

Downstream benchmarks

```
Finance QA
Financial IE
Ticker prediction
Next-token prediction
```

Whichever consistently wins is likely the better dataset.

---

### Loss alone isn't enough

Imagine

Dataset A

```
validation loss

2.18
```

Dataset B

```
validation loss

2.21
```

Very close.

But then evaluate on finance tasks.

Dataset A

```
80%
```

Dataset B

```
86%
```

Then Dataset B is probably better.

This is why you need both:

1. Pretraining metrics
2. Downstream evaluation

---

### Good dataset evaluation pipeline

```
Raw corpus
      │
      ▼
Tokenizer
      │
      ▼
64M GPT2
      │
      ▼
Validation loss
      │
      ▼
Perplexity
      │
      ▼
Downstream benchmark
      │
      ▼
Human inspection
```

Every stage gives information.

---

### You can infer data quality from learning curves

Suppose two datasets are trained identically.

Dataset A

```
step

1000
loss 5.1

5000
loss 3.8

10000
loss 2.7

20000
loss 2.35
```

Dataset B

```
step

1000
loss 5.0

5000
loss 3.6

10000
loss 2.5

20000
loss 2.20
```

Dataset B is easier to model.

Possible reasons include

* better cleaning
* fewer duplicates
* more consistent formatting
* higher information density
* less noise

---

### But beware of "easy" datasets

A dataset can have very low loss because it contains

* duplicated text
* boilerplate
* repetitive templates
* generated content

Example

```
Apple Inc.
Apple Inc.
Apple Inc.
Apple Inc.
Apple Inc.
```

Loss becomes tiny.

But the model learns almost nothing useful.

So you also need downstream evaluation to detect this failure mode.

---

### I would build the benchmark like this

```
Dataset
        │
        ▼
Train GPT2-64M
        │
        ├── Validation loss
        ├── Perplexity
        ├── Training speed
        ├── Gradient stability
        ├── Token entropy
        ├── Memorization rate
        ├── Finance benchmark
        ├── General benchmark
        └── Human generation quality
```

Then every new dataset gets exactly the same pipeline.

---

I think this is a strong direction for your work. Rather than viewing the 64M model as the end goal, treat it as a **dataset evaluation harness**. Once a dataset consistently outperforms alternatives at 64M under identical conditions, it's a much better candidate to invest GPU time training larger models (124M, 355M, or beyond). This is far more compute-efficient than repeatedly discovering data issues only after long, expensive training runs.
