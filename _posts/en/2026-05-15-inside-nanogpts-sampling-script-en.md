---
audio: false
generated: true
image: false
lang: en
layout: post
title: Inside NanoGPT's Sampling Script
translated: false
type: note
---

It's an 89-line script that does three things: build the model, encode your prompt, generate tokens one at a time. Let me walk through each part.

## 1. Config + setup (`sample.py:11–32`)

Lines 12–22 declare defaults as plain module-level variables (`init_from`, `start`, `num_samples`, `temperature`, `top_k`, etc.). Then line 23 does the magic:

```python
exec(open('configurator.py').read())   # overrides from command line
```

This runs `configurator.py` which walks `sys.argv` and overwrites those globals with your `--init_from=gpt2-xl --start="Hello, my name is" ...` flags. That's why you saw `Overriding: init_from = gpt2-xl` in the log.

Lines 26–32 set the RNG seed, enable TF32 matmul (free speedup), and set up an `autocast(bfloat16)` context — every forward pass inside `with ctx:` runs in bf16 while keeping master weights in fp32.

## 2. Build the model (`sample.py:35–54`)

Two paths depending on `init_from`:

- `resume` → load `out/ckpt.pt` (your own trained checkpoint).
- `gpt2*` → call `GPT.from_pretrained('gpt2-xl', dict(dropout=0.0))` at line 49.

That second path lives in `model.py:228–283`. It:

1. Picks the right `n_layer/n_head/n_embd` from a hardcoded dict (`model.py:238–243`). For `gpt2-xl`: **48 layers, 25 heads, 1600 embed dim, 1.5B params**.
2. Builds an **empty nanoGPT** with those dims.
3. Downloads HuggingFace's `GPT2LMHeadModel.from_pretrained('gpt2-xl')` weights (this is the 6.5 GB you just downloaded).
4. Copies tensors one by one into nanoGPT's state dict. Four weight matrices are transposed because OpenAI's original code used a `Conv1D` layer where nanoGPT uses `nn.Linear` (`model.py:267`, `274–276`).

Then `model.eval()` (disables dropout) and `model.to(device)` — done.

## 3. Tokenizer (`sample.py:56–74`)

Since you used `gpt2-xl` (not `resume`), it falls into the `else` branch at line 70:

```python
enc = tiktoken.get_encoding("gpt2")
encode = lambda s: enc.encode(s, ...)
decode = lambda l: enc.decode(l)
```

`tiktoken` is OpenAI's fast Rust BPE tokenizer. `"Hello, my name is"` → `[15496, 11, 616, 1438, 318]` (5 tokens).

## 4. Encode prompt (`sample.py:77–81`)

```python
start_ids = encode(start)
x = (torch.tensor(start_ids, dtype=torch.long, device=device)[None, ...])
```

Shape: `(1, 5)` — batch of one, sequence of 5 tokens. This goes to the GPU.

## 5. The generation loop (`sample.py:84–89` → `model.py:327–352`)

```python
for k in range(num_samples):          # 3 outer samples
    y = model.generate(x, max_new_tokens=200, temperature=0.8, top_k=200)
    print(decode(y[0].tolist()))
```

The actual sampling lives in `model.py:generate()`. For each of the 200 new tokens:

```python
idx_cond = idx if idx.size(1) <= block_size else idx[:, -block_size:]  # crop to 1024
logits, _ = self(idx_cond)             # full forward pass (line 338)
logits = logits[:, -1, :] / temperature  # only the last position, scaled
if top_k is not None:
    v, _ = torch.topk(logits, k=top_k)
    logits[logits < v[:, [-1]]] = -float('Inf')  # mask everything outside top-200
probs = F.softmax(logits, dim=-1)
idx_next = torch.multinomial(probs, num_samples=1)  # sample one token
idx = torch.cat((idx, idx_next), dim=1)              # append, repeat
```

This is **autoregressive sampling**: at each step the model sees everything generated so far, predicts a distribution over the ~50K vocab tokens for the *next* token, samples one, appends, repeats.

The two knobs that matter:

- **`temperature=0.8`** — divides logits before softmax. <1.0 sharpens the distribution (more conservative); >1.0 flattens it (more random).
- **`top_k=200`** — at each step, keep only the 200 highest-probability tokens, zero out the rest. Prevents low-probability garbage from being sampled.

After 200 steps, `y` is a `(1, 205)` tensor of token IDs. `decode(y[0].tolist())` turns it back into text.

## Why the output looks good

It's **not** because nanoGPT is doing anything clever — `sample.py` is a textbook generation loop. The quality comes entirely from two facts:

**1. GPT-2 XL is genuinely strong for its era.** It's 1.5B params trained on ~40GB of web text (WebText) for ~300B tokens. It learned English syntax, topic coherence over a few hundred tokens, and a lot of world knowledge. Your prompt `"Hello, my name is"` lands in a region of the distribution that the model has seen *millions* of times — personal blog posts, forum intros, bios — so it has very confident, well-shaped continuations.

**2. Your sampling settings are well-tuned.**

- `temperature=0.8` is the sweet spot. At 1.0 the model gets wild; at 0.5 it gets repetitive. 0.8 keeps it interesting but coherent.
- `top_k=200` filters out the tail of nonsense tokens without forcing greediness.
- That's why each sample is *different* (it's stochastic) but each one *holds together* (no random-word salad).

What you're seeing **isn't reasoning** — the model has no idea Esteban Galaviz exists or doesn't, it just knows "professor names sound like X" and "Chilean universities pair with Spanish names." It's high-quality pattern completion. The hallucinations (Haverford College is in Pennsylvania, not Chile; Kainos Dental probably doesn't exist) are the giveaway.

## The whole script in one paragraph

Read a config, build either a from-scratch GPT or a HuggingFace-pretrained GPT-2 into nanoGPT's structure, tokenize the prompt with tiktoken, run an autoregressive loop that for each new token does *one full forward pass through all 48 transformer blocks* and samples from the top-200 highest-probability next tokens with temperature 0.8, then decode the resulting IDs back to text. Run that 3 times for 3 samples. Each new token requires recomputing attention over the entire growing context — which is why generation gets slower as the sequence lengthens, and why `block_size=1024` is a hard cap (line 336 crops if you'd exceed it).
