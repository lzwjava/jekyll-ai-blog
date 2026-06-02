---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: FineWeb Training Iteration Recommendation
translated: false
type: note
---

For your ~3.68B token FineWeb dataset and this 40M-parameter model, here’s the clear recommendation:

### Keep max_iters = 20,000 (or at least 15,000+)

Don’t drop to 10,000 or 6,000 — you’ll leave a lot of performance on the table.

#### Why 20k is better than 10k or 6k

| max_iters | Total tokens seen | Epochs on your data | Expected final val loss (typical on FineWeb-Edu) | Relative quality |
|-----------|-------------------|---------------------|--------------------------------------------------|------------------|
| 6,000     | ~3.15 B           | ~0.85×                      | ~2.9–3.1                                        | OK, but weak     |
| 10,000    | ~5.24 B           | ~1.42×                      | ~2.65–2.8                                       | Decent           |
| 15,000    | ~7.86 B           | ~2.13×                      | ~2.50–2.65                                      | Very good        |
| 20,000    | ~10.5 B           | ~2.85×                      | ~2.42–2.55                                      | Excellent (beats original GPT-2 124M on most benchmarks) |

Real-world runs with similar-sized models (40–125M) on FineWeb-Edu show that loss is still dropping noticeably even after 2–3 epochs on this data, because FineWeb-Edu is extremely high-quality and diverse. People routinely go to 10–15B tokens now for 124M-class models and get significantly better coherence, knowledge, and reasoning.

#### Time difference isn’t huge on your 4070

- 10,000 iters → ~8–11 hours total
- 20,000 iters → ~15–20 hours total

That’s only ~8–9 extra hours of runtime for a model that will be noticeably smarter and more useful. Totally worth it unless you’re in a big hurry or electricity is extremely expensive where you are.

#### Practical sweet-spot compromise (if you’re impatient)

Set max_iters = 15,000 → ~8B tokens, ~2.1 epochs
You’ll finish in 11–15 hours and still get 90–95 % of the possible performance.

#### When you could stop early (monitor this!)

Run with 20,000 but watch the validation loss curve:

- If val loss flattens completely before ~12–15k iters → you can stop early.
- In practice on FineWeb-Edu with small models, it rarely flattens that early — most people see steady improvement all the way to 20k+.

#### Bottom line

- Want the best possible 40M model from this data? → 20,000 iters
- Want to save ~5–8 hours and still crush the original GPT-2 124M? → 15,000 iters
- 10,000 or less → you’ll regret it once you see how much better it gets with just a few more hours

Just let it run overnight with 20k (or 15k). You’ll thank yourself tomorrow when you have a genuinely strong little model instead of a merely “okay” one.
