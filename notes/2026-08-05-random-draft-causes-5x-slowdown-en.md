---
audio: false
generated: true
image: false
lang: en
layout: post
title: Random Draft Causes 5x Slowdown
translated: false
type: note
---

The run is done — and now it's much easier to read. Here's the full analysis.

## Bottom line

The machinery works end-to-end, but the **draft model is a statistically random guesser**: its acceptance is at the level of a coin flip drawn from an unrelated distribution, so this run is speculative decoding with 100% overhead and 0% benefit — roughly **5× slower than just sampling the target model directly**.

## What the numbers say

| dataset | #propose | accept_len | verify_rate | accept@0 | accept@1..6 |
|---|---|---|---|---|---|
| gsm8k | 7.00+1 | 1.01 | 0.1261 | 0.0086 | 0 |
| math500 | 7.00+1 | 1.01 | 0.1262 | 0.0096 | 0 |
| humaneval | 7.00+1 | 1.01 | 0.1262 | 0.0095 | 0 |
| mbpp | 7.00+1 | 1.01 | 0.1259 | 0.0073 | 0 |
| alpaca | 7.00+1 | 1.01 | 0.1260 | 0.0079 | 0 |

Three things jump out:

1. **`accept_rate@0 ≈ 0.7–1%` is the acceptance rate of an *independent* draft.** With temperature-1 rejection sampling, the expected acceptance of a draft that carries no information about the target is `Σ_t min(q_t, p_t)` — for a near-uniform `q` over the 151,936-vocab, that lands around 0.5–1%. You're seeing exactly that. A draft with *any* real signal would show 30–90% at position 0.

2. **The numbers are identical across all 5 domains** (math, code, chat). This is the strongest diagnostic: a draft that learned *something* would accept more on datasets resembling its training distribution and less elsewhere. Identical accept@0 across gsm8k/math500/humaneval/mbpp/alpaca means the proposals carry **zero signal** about the target's conditionals.

3. **Every round commits 1.01 tokens** (1 guaranteed target token + 0.01 draft). So per output token you pay: a 7-token draft forward **plus** an 8-position verification forward through all 36 layers of the 4B target. That's ~8× the target FLOPs of plain autoregressive decoding — pure loss at 0% acceptance.

## Why the draft is dead — the training evidence

From `toy_run/train.log`:

```
epoch=1 step=2/12  loss=3.3414   # 0.1 min elapsed
epoch=2 step=8/12  loss=2.6916
epoch=3 step=12/12 loss=2.6636   # total: 12 steps, 3 epochs, 0.3 minutes (~20 s)
```

- **Total training: ~20 seconds, 12 optimizer steps, 114 samples.** The final loss 2.66 (vs `ln(151936) ≈ 11.9` for uniform) just means it learned token *frequency*, not the *conditional* structure needed for acceptance.
- The toy config gutted everything that makes DSpark work, compared to the real `config/dspark/dspark_qwen3_4b.py`:

| | toy (this run) | real |
|---|---|---|
| draft layers | 2 | 5 |
| target layers | [1, 33] | [1, 9, 17, 25, 33] |
| markov rank | 32 | 256 |
| anchors | 4 | 512 |
| confidence head | **off** (alpha=0.0) | on (alpha=1.0) |
| training data | 114 samples | full blend, max_len 4096 |

- Note the confidence head is **disabled** in this checkpoint (`enable_confidence_head = False`), so `--confidence-threshold` is dead code here — the draft always proposes the full 7-token block, maximizing wasted verification.

## Throughput math

~10 min per 100-sample dataset ⇒ ~6 s/sample ⇒ **~21 tokens/s end-to-end** (128 tokens/sample). Plain bsz-1 sampling of Qwen3-4B-FP8 on a 4070 is ~100+ tok/s, so this run is **~5× slower than the no-draft baseline** — consistent with the 8× compute amplification minus prefill being relatively cheap.

## What I'd check next

1. **One cheap diagnostic first**: run the toy draft on *its own* training set (perfectblend). If acceptance is high there too, something is structurally broken (wiring, target-layer conditioning, cache alignment) and data scale won't fix it. If it accepts on-train but not on eval, it's purely the 114-sample scale.

2. **Train the real draft** with `config/dspark/dspark_qwen3_4b.py` (5 layers, rank 256, 512 anchors, confidence head on, real blended data), then re-run this eval. Success criteria: `accept_rate@0 ≥ ~0.5`, `accept_len ≥ 2–3` at block 7, `verify_rate ≥ ~0.4` — then you should see a real 2–3× wall-clock speedup.

3. **Add a plain-autoregressive baseline to the eval** (same target, same samples, same temperature) reporting tokens/sec next to the spec metrics — it converts these acceptance tables into an unambiguous speedup/slowdown number.

Want me to add that baseline comparison to `eval_smoke.py`, or write the on-training-distribution acceptance check?