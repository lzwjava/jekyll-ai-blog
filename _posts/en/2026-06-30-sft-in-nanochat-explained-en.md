---
audio: false
generated: true
image: false
lang: en
layout: post
title: SFT in Nanochat Explained
translated: false
type: note
---

Question: What's SFT in nanochat?

Answer:

SFT (Supervised Fine-Tuning) in nanochat is the stage that turns the base pretrained model into a conversational assistant by training it on full conversations formatted with the chat special tokens. It sits between base pretraining/midtraining and RL in Karpathy's pipeline (`scripts/chat_sft.py`).

The key idea: same next-token cross-entropy loss as pretraining, but now over rendered conversations, with the loss **masked to only the assistant tokens** — you don't train the model to predict user turns or system prompts, only to generate the assistant's replies.

What's distinctive about nanochat's SFT vs midtraining:

- **Row-wise stride, not document concatenation.** Pretraining packs many docs into fixed-length sequences. SFT instead takes one conversation per row, padded, so the model sees examples in a domain that matches inference (a single conversation at a time). Karpathy notes this reduces train/test mismatch.
- **Loss masking via the rendering.** Conversations are tokenized with the special tokens (`<|user_start|>`, `<|assistant_start|>`, etc.), and a mask marks which positions are assistant-generated. Only those contribute to the loss.
- **Short and cheap.** It's a small number of iterations over curated data — `SmolTalk` (general conversations), `MMLU` auxiliary multiple-choice, `GSM8K` (math/tool-use with the Python interpreter), etc. Runs in minutes on the 8×H100 box.

Minimal sketch of the masked loss, which is the whole conceptual core:

```python
# logits: (B, T, V), targets: (B, T), mask: (B, T) 1 for assistant tokens
loss = F.cross_entropy(
    logits.view(-1, logits.size(-1)),
    targets.view(-1),
    reduction="none",
).view_as(targets)
loss = (loss * mask).sum() / mask.sum().clamp(min=1)
```

After SFT you get `chatsft` checkpoints, which is what the web UI / CLI serve by default — and what RL (GRPO on GSM8K in `scripts/chat_rl.py`) builds on top of.

References:

- [karpathy/nanochat](https://github.com/karpathy/nanochat)
- [nanochat walkthrough (Karpathy discussion)](https://github.com/karpathy/nanochat/discussions/1)
