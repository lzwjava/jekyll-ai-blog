---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI-Driven Experiment Tracking Value
translated: false
type: note
---

Question: Why do we need MLflow in nanoGPT/nanochat training? Is it worth using? If we already have an AI agent like Hermes that can analyze logs, do we still need MLflow?

Answer:

The short answer is: **MLflow is not required**, but it becomes increasingly valuable once you're running many experiments.

Think of the stack like this:

```
Training script
    |
    +--> stdout/log.txt          (human readable)
    +--> TensorBoard             (loss curves)
    +--> Weights & Biases        (hosted dashboard)
    +--> MLflow                  (experiment database)
```

For someone training one GPT-2 model:

```
python train.py
```

MLflow is probably overkill.

For someone doing 500 experiments:

```
124M
286M
760M
1.3B

lr = 3e-4
lr = 6e-4
lr = 1e-3

batch = 64
batch = 128
batch = 256

FineWeb
FineWeb-Edu
SEC
Python
Code
...
```

then MLflow starts saving enormous amounts of time.

---

## What MLflow actually stores

Instead of just

```
step 12000
loss 2.83
```

it stores

```
Run #381

git commit:
4e3bc91

model:
GPT2-124M

dataset:
SEC-EDGAR

tokens:
15.5B

learning_rate:
3e-4

batch_size:
512

optimizer:
AdamW

validation loss:
2.281

checkpoint:
step_18000.pt

training time:
7h54m
```

Now every experiment is searchable.

---

## Why OpenAI, Anthropic, DeepMind need this

Imagine running

```
2000 experiments/day
```

Without experiment tracking:

```
which checkpoint produced Figure 5?

...

no idea.
```

With MLflow:

```
SELECT *
WHERE
dataset="FineWeb"
AND lr=3e-4
AND val_loss<2.3
```

Done.

---

## Hermes Agent + MLflow

This is actually where things become interesting.

Instead of a human opening dashboards:

```
MLflow
      ↑
Hermes Agent
      ↑
LLM
```

The agent can query experiments automatically.

Example prompt

```
Compare all runs using cosine LR.

Why did run 381 outperform run 412?

Suggest three new hyperparameters.
```

The agent fetches

```
loss curves
GPU utilization
learning rate schedule
gradient norm
validation loss
```

and produces a report.

So MLflow becomes structured memory for the agent.

---

## Even better than MLflow

For an AI-native workflow, I'd store everything in a SQL database.

Example schema:

```
experiments

id
git_hash
dataset
tokens
lr
batch
optimizer
val_loss
train_loss
wall_time
checkpoint
notes
```

Then Hermes simply executes

```sql
SELECT *
FROM experiments
ORDER BY val_loss
LIMIT 20;
```

Feed the result into an LLM.

No dashboard required.

---

## What I would build

Given your workflow (nanoGPT/nanochat, many small-model experiments, CLI agents), I'd build something like:

```
nanochat
    |
    +--> checkpoint
    |
    +--> metrics.json
    |
    +--> sqlite/postgres
             |
             +--> Hermes
                     |
                     +--> "Compare last 50 runs"
                     +--> "Find unstable runs"
                     +--> "Generate training report"
                     +--> "Predict best LR"
```

This feels more AI-native than manually opening MLflow.

---

## My recommendation

For your current scale:

* **<20 experiments:** simple JSON logs + TensorBoard are enough.
* **20–200 experiments:** MLflow starts providing real value.
* **Hundreds or thousands of experiments with AI agents:** I'd treat MLflow (or an equivalent SQL-backed experiment store) as the backend, and let Hermes be the frontend. The agent becomes the interface for querying, comparing, and analyzing experiments, rather than humans browsing dashboards.

Many research labs are moving in this direction: experiment tracking systems remain the source of truth, while LLM agents sit on top to automate analysis, summarize trends, and propose the next set of experiments.

References:

* MLflow Documentation: [https://mlflow.org/docs/latest/](https://mlflow.org/docs/latest/)
* nanoGPT: [https://github.com/karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
* TensorBoard: [https://www.tensorflow.org/tensorboard](https://www.tensorflow.org/tensorboard)
