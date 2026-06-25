---
audio: false
generated: true
image: false
lang: en
layout: post
title: Troubleshooting Garbage Model Output
translated: false
type: note
---

**Question:** The generation output is mostly whitespace, with occasional `<div>`, `}`, `;`, `<`, `*` tokens. Given a model trained on dirty GitHub code, is this expected?

**Answer:**

Yes — given everything in your diagnosis, this is exactly the failure mode you'd predict. But there are two distinct things going on, and only one of them is "expected/benign." Let me separate them.

### What's expected (benign)

**Whitespace and `}` `;` `<div>` `*` `<` are the highest-frequency tokens in your corpus.** A high-perplexity model (PPL ~32) that can't reliably distinguish contexts collapses toward the unconditional unigram distribution — it emits whatever is most common on average, ignoring context. In github-code that's: spaces, newlines, indentation, closing braces, semicolons, and HTML/javadoc fragments (`<div>` comes straight from your ~12% HTML pollution). So the *identity* of the garbage tokens is consistent with "model fell back to the prior." That part is expected.

This is the same phenomenon as a language model outputting "the the the and of" when undertrained — it's emitting the marginal distribution, not a conditional one.

### What is NOT expected — and is the real signal here

Look at your tensor shapes:

```
x after transformer: (1, 3, 768) | logits: (1, 1, 50304)
```

Two red flags:

**1. Sequence length is 3.** You're feeding a 3-token prompt and the transformer output is `(1, 3, 768)`. Fine so far. But that means during generation you're operating on extremely short context. If your generation loop isn't appending sampled tokens back into the input (or your KV cache / context window is broken), the model never sees a real prefix — it's predicting from almost nothing every step. From a 1–3 token context, *even a good model* leans hard on the prior. Verify your autoregressive loop actually grows the context:

```python
for _ in range(max_new):
    idx_cond = idx[:, -block_size:]          # must include generated tokens
    logits, _ = model(idx_cond)
    logits = logits[:, -1, :] / temperature  # last position only
    probs = F.softmax(logits, dim=-1)
    next_id = torch.multinomial(probs, 1)
    idx = torch.cat([idx, next_id], dim=1)   # <-- append, or you regenerate from scratch
```

If that `torch.cat` is missing or `idx_cond` is wrong, you'd see exactly this: structureless high-frequency tokens forever, regardless of how well the model trained.

**2. `logits: (1, 1, 50304)` — vocab is 50304, not 50257.** That's the GPT-2 vocab padded to a multiple of 64 (nanoGPT does `50304` for efficiency). Fine *if* training used the same padded vocab. But it's worth confirming your tokenizer and the model's `vocab_size` match exactly between training and inference — a mismatch shifts every token ID and produces precisely this kind of "valid tokens, no coherence" output. The fact that the emitted tokens are still *plausible code tokens* (not random Unicode) suggests the mapping is probably right, but confirm it.

### How to tell which problem you have (one test)

Before blaming data, **prompt with a long, in-distribution prefix and sample greedily** (`temperature → 0`, i.e. argmax):

```python
prompt = "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = "
# encode, feed full prompt, argmax-decode 50 tokens
```

- If greedy decoding on a real code prefix produces *somewhat* sensible continuation (more indentation, an identifier, `arr[`) → the model learned something; your earlier garbage was sampling temperature + short context, and the remaining fix is data/tokenizer quality (your diagnosis stands).
- If greedy decoding on a long prefix *still* outputs spaces and `<div>` → the model genuinely didn't learn conditional structure, OR your inference loop/vocab is broken. Given train loss dropped to 3.46 from a random baseline of 50k PPL, the model *did* learn something measurable, so pure-garbage-on-good-prompt would point at the inference loop, not the weights.

### Bottom line

The *content* of the garbage (whitespace, braces, `<div>`) being the corpus's most frequent tokens is expected for a high-perplexity model. But "mostly whitespace at PPL 32" is also the classic symptom of **sampling from near-empty context** or a **broken generation loop**, and your `seq_len=3` makes me want to rule that out first — it's a 5-minute check and a far cheaper fix than re-tokenizing 50GB.

So: run the greedy-decode-on-long-prefix test. If it's still garbage, audit the `torch.cat` append and the train/infer `vocab_size` match *before* you touch the data. The data cleaning is still worth doing — but don't let it mask a trivial inference bug.
