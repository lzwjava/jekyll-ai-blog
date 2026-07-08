---
audio: false
generated: true
image: false
lang: en
layout: post
title: Token ID mismatch prevents data reuse
translated: false
type: note
---

**Question:** Why can't nanochat reuse the FineWeb-Edu data that's already tokenized on disk, instead of needing raw parquet + a fresh custom tokenizer?

**Answer:**

Because token IDs are not portable across tokenizers, and nanochat's model architecture is hard-wired to its own vocab.

**1. The embedding table is a fixed-size lookup, keyed to one specific vocab**

```python
# nanochat's GPT model init (paraphrased from nanochat/gpt.py)
self.transformer.wte = nn.Embedding(vocab_size, n_embd)  # e.g. 65536 x d_model
self.lm_head = nn.Linear(n_embd, vocab_size, bias=False)
```

`vocab_size` here comes from the tokenizer nanochat trains itself (`rustbpe`, roughly tiktoken-style BPE, default ~65536 merges). Your existing `.npy` files were tokenized with **GPT-2's tiktoken** (`gpt2` encoding, vocab 50257). Token ID `464` under GPT-2 BPE means `"The"`. Under nanochat's freshly trained BPE, ID `464` is some arbitrary merge learned from whatever corpus statistics happened to produce it — it means nothing, or means something else entirely. You cannot feed one tokenizer's IDs into a model whose embedding table was built for a different tokenizer's ID space. It's not a format mismatch, it's a semantic mismatch — the integers don't refer to the same strings.

**2. nanochat trains its own tokenizer as an explicit pipeline step, not a config option**

```bash
# actual nanochat pipeline order
python -m nanochat.dataset -n 240          # download raw parquet shards
python -m scripts.tok_train --max_chars=... # train BPE on a *sample of raw text*
python -m scripts.tok_eval                  # sanity check compression ratio
python -m scripts.base_train                # pretrain, tokenizing on the fly (or pre-shards) with the tokenizer just trained
```

`tok_train.py` needs raw UTF-8 text, not existing integer arrays, because BPE merge learning operates on byte pairs in raw strings. Your `.npy` files already collapsed the text into GPT-2's IDs — that information is lossy/one-directional, you can't "detokenize" GPT-2 ids back to get nanochat-compatible training data for its own tokenizer without just re-decoding to text (which you can do — GPT-2 tokenizer is invertible), but at that point you're paying decode+re-tokenize cost anyway with zero benefit over just keeping the raw parquet.

**3. Why Karpathy designed it this way instead of reusing tiktoken/gpt2**

The point of nanochat's own tokenizer stage is pedagogical/control — vocab size, special tokens (`<|bos|>`, tool-use tokens, etc.), and merge behavior are all tuned to nanochat's specific chat-format and training recipe. It's not meant to be swapped for an off-the-shelf tokenizer; the whole d-model/vocab_size/rotary-embedding config in `gpt.py` assumes you ran their tokenizer stage first.

**So concretely, your two options were:**

- **A.** Keep (don't delete) the raw FineWeb-Edu parquet, train nanochat's tokenizer + retokenize on that corpus, skip re-downloading ClimbMix — saves the 60G ClimbMix download but you lose the "recipe-matched" data quality/mix nanochat's authors validated their loss curves against.
- **B.** Delete FineWeb-Edu entirely, download ClimbMix as nanochat's default recipe expects — matches the published training run exactly (reproducible loss curves, known-good hyperparameters), costs the 60G download + bandwidth/time.

Given you're mid-1.5B-scale run and want results that match known nanochat benchmarks rather than debug your own data-mix effects, **B is the safer default** — reuse-the-old-data optimization isn't worth introducing a confound into a run you're trying to validate against the reference implementation.

If you want, I can write the actual `du -sh` + `rm` + `uv venv` + tokenizer-train sequence as a single script so you're not doing this step by step by hand.
