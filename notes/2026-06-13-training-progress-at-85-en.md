---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress at 85%
translated: false
type: note
---

Training is running well in tmux 34. Here's the current status:

  Progress:  85% (2247/2656 steps), ~1:35 remaining
  Epoch:     1.69
  Tokens:    ~27.4M processed
  Loss:      1.45 (latest), trending around 1.43-1.52 range
  Accuracy:  ~64.9% mean token accuracy
  LR:        1.27e-05 (decaying nicely via cosine schedule)
  Grad norm: 0.035 (stable)

Training looks healthy - loss is stable in the 1.4-1.5 range, gradient norms are low and steady (~0.03), and the learning rate is in its final decay phase. Should be done in about 1.5 hours.
