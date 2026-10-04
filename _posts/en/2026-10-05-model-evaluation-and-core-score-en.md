---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Evaluation and CORE Score
translated: false
type: note
---

Let me explain more simply, with a concrete example.

## The big picture

You trained a model. **How smart is it?** This file answers that by giving it a standardized test — like exam questions — and grading the answers. The final grade is called the **CORE score**.

`scripts/base_eval.py` runs the test; this file contains the actual test-taking logic.

## The 3 question types

**Type 1: Multiple choice** (`multiple_choice`)
> Q: The capital of France is ___
> - A) London  - B) Paris  - C) Berlin

The model scores each option by how "surprised" it is (loss). Least surprised = its guess. If it guesses "Paris" and that's the gold answer → correct.

**Type 2: Schema** (`schema`) — basically multiple choice, backwards
> Complete: "The ___ was delicious"
> - A) "car"  - B) "meal"

Same idea: score each option, pick the lowest-loss one.

**Type 3: Language modeling** (`language_modeling`)
> Context: "The capital of France is" → Continuation: " Paris"

The model must predict **every token** of " Paris" correctly, one by one. All correct → correct, any mistake → wrong. (This is the strictest type.)

## How one question gets graded (the flow)

```
evaluate_task()        ← grades the whole exam, splits work across GPUs if distributed
  └─ evaluate_example()  ← grades ONE question
       1. pick a few example Q&As to show the model first (few-shot)
       2. render_prompts_*()   → turn question into text prompt
       3. batch_sequences_*()  → tokenize, note WHERE the answer part starts/ends
       4. forward_model()      → run model, get per-token loss & predictions
       5. compare against gold answer → correct or not
```

The trick in step 3: prompts share a long common prefix (the question). We only score the **answer portion** (found via `find_common_length`), so the model isn't penalized for the shared setup text.

## Final score

`base_eval.py` runs this on ~10 different tasks, gets an accuracy per task, and averages them → **CORE score** (0–100, higher = better).

## One practical note

There's a known bug noted in the file's TODO: everything matches reference numbers except **SQuAD** (31% vs expected 37%).

Want me to walk through any specific function in detail, or show how `base_eval.py` combines the results?