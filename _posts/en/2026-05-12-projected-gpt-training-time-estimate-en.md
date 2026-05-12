---
audio: false
generated: true
image: false
lang: en
layout: post
title: Projected GPT Training Time Estimate
translated: false
type: note
---

Can't pin it sharply yet — only `iter 0` has printed (the next log line is at iter 20, due any moment). But here's the math using the projected ~11 s/iter from smoke:

| Phase                            | Cost                      |
| -------------------------------- | ------------------------- |
| 19,073 training iters × ~11 s    | ~58.3 hrs                 |
| Initial warmup (iter 0 overhead) | ~17 s                     |
| 38 evals × 9 s (every 500 iters) | ~6 min                    |
| 38 checkpoint writes × ~8 s      | ~5 min                    |
| **Total**                        | **~59.5 hrs (~2.5 days)** |

That's for the **full configured run** ending at iter 19073 (~10 B tokens seen).

If you don't want to wait that long:

| Stop at iter        | Tokens seen | Time      | Loss expected |
| ------------------- | ----------- | --------- | ------------- |
| 5,000               | ~2.6 B      | ~15.5 hrs | ~3.5–3.8      |
| 10,000              | ~5.2 B      | ~31 hrs   | ~3.2–3.4      |
| 19,073 (configured) | ~10 B       | ~59.5 hrs | ~2.9–3.1      |

You can kill at any 500-iter checkpoint boundary and the model is usable — `sample.py --out_dir=out-fineweb-gpt3` will load the latest checkpoint.

I'll refine this estimate once the first `iter 20:` line lands (within ~1 min from now). Ping me back then if you want a tighter number.