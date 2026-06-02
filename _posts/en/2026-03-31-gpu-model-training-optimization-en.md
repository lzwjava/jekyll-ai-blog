---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cost Optimization for GPU Model Training
translated: false
type: note
---

Question: Is it a good cost-saving method to download 100GB of text data on a cheap DigitalOcean machine first, prepare everything, then spin up an H200 GPU instance and transfer the data internally for training?

Answer:

Yes — this is **a very good and commonly used cost-saving strategy**. Your idea is technically sound and many teams do exactly this. Here's why it works and how to do it correctly.

---

# Why this saves money

H200 GPU instances are extremely expensive. You want **GPU time = only training**, nothing else.

Bad workflow:

```
Start H200 → download 100GB → preprocess → tokenize → train
```

You waste **hours of GPU billing** doing CPU tasks.

Good workflow (your idea):

```
Cheap CPU machine:
  download data
  clean data
  tokenize
  pack dataset
  shard dataset

Then:
Start H200 → transfer → train immediately
```

Now GPU is used **only for training**.

This can save **50–90% cost**.

---

# Even better: do ALL preprocessing first

On the cheap machine, prepare everything:

### Step 1 — Download raw data

```
100GB text
```

### Step 2 — Clean & deduplicate

Remove:

* duplicates
* HTML junk
* bad encoding
* extremely short lines

This can reduce **100GB → 60GB**

---

### Step 3 — Tokenize (VERY IMPORTANT)

Do this BEFORE using GPU

Example:

```
python tokenize.py
```

Output:

```
dataset.bin
dataset.idx
```

Now GPU doesn't waste time tokenizing.

---

### Step 4 — Shard dataset

Split into chunks:

```
train_000.bin
train_001.bin
train_002.bin
...
```

This improves:

* loading speed
* distributed training
* resume training

---

### Step 5 — Then start H200

Only now create GPU instance:

```
H200 start
scp dataset to GPU
train immediately
```

Perfect.

---

# Even cheaper trick (pro level)

Don't transfer at all. Use **shared storage**:

Option A:

* Upload dataset to object storage
* Mount from GPU

Option B:

* Use internal VPC network
* mount via NFS

Option C (best):

* snapshot disk
* attach to H200

Then:

```
Start H200
Attach disk
Train immediately
```

This is **fastest and cheapest**.

---

# Best cost-optimized pipeline

Ideal workflow:

```
cheap CPU droplet
    ↓
download dataset
clean dataset
tokenize dataset
shard dataset
    ↓
snapshot disk
    ↓
create H200 from snapshot
    ↓
train immediately
```

This is how serious LLM training is done.

---

# Extra optimization (most people forget)

Also prepare:

* tokenizer files
* config.yaml
* training script
* wandb disabled or ready
* checkpoint folder ready

So GPU does:

```
python train.py
```

and starts immediately.

---

# Your idea verdict

Yes, your approach is:

* correct ✅
* professional ✅
* used in industry ✅
* saves lots of money ✅
* recommended ✅

You're thinking in **GPU-time optimization**, which is exactly how people train models cheaply.

This is the same mindset used when training:

* nanoGPT
* Qwen finetunes
* LLaMA finetunes
* custom LLMs

You're on the right track.
