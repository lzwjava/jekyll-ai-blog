---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing GPT-2 Padded Vocab Mismatch
translated: false
type: note
---

Question: Why does llama.cpp complain "Shape mismatch! Model tensors are 50304 (padded) but vocab is 50257" when loading my GPT-2 124M GGUF, and how do I fix it?

Answer:

This is the classic nanoGPT padded-vocab problem. Your training code padded the vocab from 50257 → 50304 for GPU efficiency, but your GGUF metadata declares vocab_size = 50257 (the real GPT-2 BPE tokenizer count). llama.cpp cross-checks `output.weight` / `token_embd.weight` row count against the tokenizer vocab and aborts on the mismatch.

Why 50304 exists in the first place: GPT-2's true vocab is 50257. nanoGPT rounds up to the nearest multiple of 64 (50304 = 50257 + 47) because matmuls with dimensions divisible by 64/128 hit tensor-core tile boundaries cleanly — Karpathy's "the most beautiful 30% speedup" commit. The extra 47 rows are never produced by the tokenizer; they're dead logits trained to ~−inf usefulness (gradient only flows through real tokens).

```python
# nanoGPT model.py — this is where 50304 comes from
vocab_size: int = 50304  # GPT-2 vocab_size of 50257, padded up to nearest multiple of 64
```

The two embedding tensors carrying the pad:
- `transformer.wte.weight` → exported as `token_embd.weight`, shape `[50304, 768]`
- `lm_head.weight` → exported as `output.weight`, shape `[50304, 768]`

(With weight tying these are the same tensor, but you're exporting both.)

Fix: truncate both tensors to 50257 rows at export time, before `write_tensors_to_file()`. The dropped rows are pad — losing them changes nothing.

```python
REAL_VOCAB = 50257

def maybe_truncate_vocab(name, tensor):
    # token_embd / output are [vocab, n_embd]; trim row dim
    if name in ("token_embd.weight", "output.weight") and tensor.shape[0] > REAL_VOCAB:
        tensor = tensor[:REAL_VOCAB, :].contiguous()
    return tensor

# in your add() helper:
def add(name, tensor):
    tensor = maybe_truncate_vocab(name, tensor)
    gw.add_tensor(name, tensor.to(torch.float16).numpy())  # or whatever dtype you're writing
```

And make sure the GGUF header agrees:

```python
gw.add_uint32("gpt2.vocab_size", REAL_VOCAB)  # 50257, must match the tensor row count
# (key prefix matches your arch string passed to GGUFWriter)
```

Concretely in your snippet, the lines to guard are:

```python
add("token_embd.weight", sd["transformer.wte.weight"])  # truncate here
...
add("output.weight",     sd["lm_head.weight"])           # and here
```

The bias/norm tensors you showed (`output_norm.bias`, etc.) are `[768]` — not vocab-dimensioned — so leave them alone.

Quick sanity check after re-export:

```bash
python -c "from gguf import GGUFReader; r=GGUFReader('sec-edgar-gpt-124m.gguf'); \
print([(t.name, t.shape) for t in r.tensors if 'embd' in t.name or t.name=='output.weight'])"
# expect [('token_embd.weight', [768, 50257]), ('output.weight', [768, 50257])]
```

Note GGUFReader prints shapes reversed (`[n_embd, vocab]`) vs torch — that's just ggml's column-major convention, not another bug.

Alternative if you'd rather not re-export: bump the GGUF metadata vocab to 50304 and let the tokenizer carry 47 unused tokens. This loads, but it's the wrong fix — your tokenizer.json only knows 50257 merges, so token IDs 50257–50303 are unreachable and you've shipped 36K dead params (50304−50257 × 768 × 2 tensors). Truncating is cleaner.
