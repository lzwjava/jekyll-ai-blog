---
audio: false
generated: true
image: false
lang: en
layout: post
title: Knowledge Without Reasoning
translated: false
type: note
---

Here's the full evaluation summary for the d12 training run:

```
================================================================
  NANOCHAT d12 TRAINING RUN — EVALUATION REPORT
================================================================

MODEL
  Architecture:  d12 (depth=12, dim=768, heads=6)
  Parameters:    286M
  Sequence len:  2048
  Vocab size:    32,768

TRAINING PERFORMANCE
  Total steps:     200,000
  Total time:      3,921 min (~65.3 hours)
  Step time:       ~1,175ms per step
  Throughput:      ~55,800 tok/sec
  Peak memory:     9,435 MiB (~9.2 GB)
  Tokens/param ratio: 5.95 (well under Chinchilla-optimal 20)

LOSS & CONVERGENCE
  Initial loss:    ~10.4 (random init)
  Final loss:      ~2.72
  Min val bpb:     0.7800 (best checkpoint)
  Final val bpb:   0.8534 (step 200k — was past the minimum)

NOTE: Min bpb was 0.7800 but final is 0.8534 — the model
started degrading after its best point. Tokens:param ratio
of 5.95 is very low (Chinchilla says ~20), meaning this
model was severely overtrained for its size.

================================================================
  CORE BENCHMARKS (22 tasks)
================================================================
  CORE metric (mean centered): 0.1641

  Highlights:
  PIQA              0.706  (centered: 0.412)  — good commonsense
  COPA              0.610  (centered: 0.220)  — causal reasoning
  ARC Easy          0.562  (centered: 0.416)  — science QA
  Winograd          0.568  (centered: 0.136)  — coreference
  BoolQ             0.518  (centered:-0.268)  — barely above random
  Winogrande        0.530  (centered: 0.060)
  HellaSwag (0s)    0.390  (centered: 0.187)
  HellaSwag (10s)   0.386  (centered: 0.181)

  Weak areas:
  BigBench Repeat   0.031  — near zero
  Jeopardy          0.026  — trivia recall poor
  Dyck Languages    0.086  — structural parsing weak
  BigBench Operators 0.138

================================================================
  SAMPLE QUALITY (temperature=0.8)
================================================================

1. "The capital of France is..."
   ✅ Correctly says Paris
   ❌ Then hallucinates: "Paris is the biggest city in Europe"
   ❌ Claims it's near the Mississippi River!

2. "Once upon a time..."
   ✅ Coherent story setup, characters named
   ❌ Dialogue gets repetitive and nonsensical

3. "The meaning of life is..."
   ✅ Produces essay-like structure
   ❌ Surface-level, repetitive ("love" repeated)

4. "def fibonacci(n):"
   ❌ Completely broken — returns 3, then just whitespace
   Code generation is very weak

5. "import torch"
   ❌ Gibberish — "num_num_num_num" loops
   Code generation essentially non-functional

6. "The theory of relativity..."
   ❌ Starts OK, then contradictory nonsense
   ("light is slower than the speed of light")

7. "The quick brown fox..."
   ✅ Decent encyclopedia-style entry
   ❌ Repeats characteristics in a loop

================================================================
  OVERALL ASSESSMENT
================================================================

  This 286M model at 200k steps is a mixed bag:

  STRENGTHS:
  - Basic factual recall works (capitals, symbols)
  - Can produce coherent paragraph-level text
  - Commonsense reasoning (PIQA 0.706) is its best skill
  - Grammar and sentence structure are generally correct

  WEAKNESSES:
  - Factually unreliable (hallucinates freely)
  - Code generation is completely broken
  - Repetition loops (loses coherence after ~50 tokens)
  - Math reasoning essentially absent
  - The model was past its peak — val_bpb degraded from
    0.78 to 0.85, suggesting it overfit

  RECOMMENDATION:
  - Best checkpoint was around step ~100k-130k (where min
    bpb=0.78 was hit), not 200k
  - For a 286M model, 200k steps = 65B tokens is way past
    Chinchilla-optimal. Sweet spot is ~5.7B tokens (~87k steps)
  - To get meaningfully better quality, scale up the model
    (d16/d20) with fresh data, don't keep training d12
================================================================
```

Key takeaways:

- The model KNOWS things but can't reason about them reliably
- It was trained ~3.5x past its optimal point (5.95 ratio vs 20 ideal)
- Code is a dead zone — 286M params simply can't learn programming
- If you want to keep going, a larger model (d16/d20) with more data would be the next step, not more training on this one
