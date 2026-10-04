---
audio: false
generated: true
image: false
lang: en
layout: post
title: CORE Metric Evaluation Implementation
translated: false
type: note
---

`nanochat/core_eval.py` implements the **CORE metric** evaluation from the [DCLM paper](https://arxiv.org/abs/2406.11794) — a benchmark suite for evaluating language models on downstream tasks. It's consumed by `scripts/base_eval.py`, which averages per-task accuracies into the final CORE score.

## What it provides

**1. Prompt rendering (3 task types)** — Jinja2 templates that build few-shot prompts:
- `render_prompts_mc` — **multiple choice**: renders one prompt per choice (question + choice appended)
- `render_prompts_schema` — **schema**: renders one prompt per context option (context + fixed continuation)
- `render_prompts_lm` — **language modeling**: renders a prompt pair *without* and *with* the continuation

**2. Tokenization/batching helpers**:
- `find_common_length` — locates the common prefix (MC) or suffix (schema) across tokenized prompts, so only the differing answer/context tokens get scored
- `batch_sequences_mc/schema/lm` — tokenize, then compute `start_idxs`/`end_idxs` marking which token span to evaluate per prompt
- `stack_sequences` — right-pads prompts into a batch tensor

**3. Scoring** (`forward_model`, `evaluate_example`):
- Runs the model once, computes per-token cross-entropy losses (shifting targets autoregressively) and argmax predictions
- **LM task**: correct iff the model *predicts every token* of the continuation exactly
- **MC/schema**: computes mean loss over the answer span for each option; correct iff the gold option has the lowest loss
- Handles few-shot sampling (deterministic seed `1234 + idx`), truncation to `model.max_seq_len`, and returns a boolean per example

**4. Distributed evaluation** (`evaluate_task`):
- Strides examples across ranks when run under `torchrun` (`dist.is_initialized()`)
- `all_reduce`s the correctness vector, then returns mean accuracy for that task

## Known issue
The file's TODO notes that all tasks match reference numbers **except SQuAD**, where it gets 31% vs. the reference 37%.