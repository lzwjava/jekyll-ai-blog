---
audio: false
generated: true
image: false
lang: en
layout: post
title: Largest Model or Most Tokens?
translated: false
type: note
---

I checked all the training runs in the project. Here's the summary:

## Largest model (by parameters)

**`out-bilingual`** — the `~232M` param model (L18/H16/C896, vocab 65536)
- `iter_num`: 4500 / 5000 → **~2.36B tokens** seen (~6 epochs over 434M-token corpus)
- `best_val_loss`: 4.368
- Checkpoint file: **2.7 GB** (largest on disk)

`out-gpt2-200m` is the same body (~219M) with GPT-2's 50k vocab, but only reached 2500/8000 iters (~1.31B tokens).

## Largest run by tokens trained

**`out-github-code-124m`** — 124M model, fully completed:
- `iter_num`: 427000 / 427000 → **~14B tokens** (complete)
- `best_val_loss`: 3.466

## Full comparison

| Run | Params | Tokens seen | Progress | val_loss |
|---|---|---|---|---|
| **out-bilingual** | ~232M | 2.36B | 4500/5000 | 4.368 |
| **out-gpt2-200m** | ~219M | 1.31B | 2500/8000 | 3.459 |
| **out-fineweb-gpt3** | 124M | 7.86B | 15000/19073 | 3.026 |
| **out-github-code-124m** | 124M | **14B** | complete | 3.466 |
| **out-sec-edgar-124m** | 124M | 1.54B | 47000/47400 | **2.278** |
| **out-fineweb** | 124M | 6.29B | complete | 3.331 |
| out-wikipedia | ~85M | 0.59B | 18000/20000 | 4.054 |
| out-helloworld | 124M | smoke | — | — |
| out-shakespeare-char | tiny | smoke | — | — |

**Bottom line:** The **largest model** is `out-bilingual` (~232M params, 2.7 GB ckpt), and the **longest training run** is `out-github-code-124m` (14B tokens, complete). Best validation loss overall is `out-sec-edgar-124m` at 2.278.

Which one do you mean by "largest" — model size or tokens trained?