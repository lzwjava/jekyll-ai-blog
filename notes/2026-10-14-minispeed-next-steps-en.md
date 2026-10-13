---
audio: false
generated: true
image: false
lang: en
layout: post
title: Minispeed Next Steps
translated: false
type: note
---

You've got a solid, complete project (minispeed — a mini DeepSpeed, ~1600 lines, tests passing). Here's what we could do next, roughly by payoff:

## Feature work (from the README's own ❌ list)

1. **ZeRO stage 3 (parameter sharding)** — the big one. You already have the hard parts (flat buffers, reduce-scatter/all-gather plumbing, sharded checkpoints); stage 3 adds param all-gather per forward/backward and a partitioned master-weight checkpoint. Natural extension of `zero/stage_1_and_2.py` into a `zero/stage_3.py`.
2. **Optimizer/CPU offload** — run AdamW on CPU shards, move only the updated shard back per step. Simpler than stage 3 and pairs well with it.
3. **Gradient compression / FP1 optimizer** — nice-to-have, lower value.

## Robustness / engineering

4. **Resharding on checkpoint load** — currently resume requires the same `world_size`; could load a `world_size=N` checkpoint at `world_size=M` by all-gathering and re-partitioning.
5. **Overlapping communication with backward** — bucketed reduce-scatter hooked into `grad_acc.register_hook` instead of doing it all at the boundary; the README already notes the flat buffer *is* the bucket, so it's set up for this.
6. **More tests / CI** — a GitHub Actions workflow (CPU/gloo tests + multi-proc), coverage of the skip-step paths and edge cases.

## Ecosystem

7. **Real-model benchmarks** — run a small Transformer (e.g. nanoGPT-scale) and produce a README table: memory & step-time for stage 0 vs 1 vs 2, fp16 vs bf16.
8. **Docs/pedagogy** — turn the "How it works" section into a longer design doc or blog-style walkthrough.

If I had to pick one: **ZeRO stage 3** — it completes the story the README tells and is the feature users would look for. Second choice would be **comm/bwd overlap**, since it's a real perf win and small in scope.

Which direction interests you?
