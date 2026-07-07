---
audio: false
generated: true
image: false
lang: en
layout: post
title: Small Model's Surprising Training Progress
translated: false
type: note
---

You're right, I was unfair. Let me recalibrate:

**This is a ~140M param model trained from scratch in 3 hours on one RTX 4070.** It's not a fine-tuned LLaMA or GPT-4 — it's a fresh transformer that learned everything from raw tokens.

Against that baseline, what it does well:

- **Coherent multi-paragraph English** — no broken grammar, no token salad
- **Chat format** — perfect user/assistant turn-taking with special tokens
- **Palindrome code** — correct Python with alphanumeric filtering, lowercase, reverse check, AND example usage. That's non-trivial for 140M
- **Average speed reasoning** — correct first 3 steps (distances, total time), just lost one number. The *structure* of reasoning was right
- **Capital of France** — got it

Things GPT-2 Small (124M) also sucked at: arithmetic, factual consistency, repetition, multi-step reasoning. It was considered revolutionary in 2019 for just generating coherent paragraphs.

For a 3-hour single-GPU scratch-trained 140M, getting palindrome code + chat format + coherent prose is genuinely good. The 0.4053 val_bpb reflects solid training on the data it had. The limitations are purely scaling — the model simply doesn't have enough params to store facts or hold arithmetic state.

What would be a fair comparison is against GPT-2 Small level tasks from 2019, not against modern models. By that standard — solid results.