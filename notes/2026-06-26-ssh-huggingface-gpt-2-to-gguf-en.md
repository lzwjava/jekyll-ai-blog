---
audio: false
generated: true
image: false
lang: en
layout: post
title: SSH HuggingFace GPT-2 to GGUF
translated: false
type: note
---

**Question:** Explain what this SSH one-liner does — it converts a HuggingFace GPT-2 model to GGUF format.

**Answer:**

This runs a Python script over SSH on a remote GPU box (`root@<​IP_ADDRESS>`) that converts your fine-tuned `sec-edgar-gpt-124m` GPT-2 model from HuggingFace format into a single `.gguf` file for `llama.cpp`/`ollama` inference.

Walking through it layer by layer:

**1. Tokenizer reconstruction**
```python
vocab = td["model"]["vocab"]          # {token_str: id}
nv = len(vocab)
toks = [""] * nv
for s, i in vocab.items(): toks[i] = s   # invert to id-ordered list
for i, c in added.items():               # overlay added_tokens
    if i < nv: toks[i] = c
tb = [t.encode("utf-8") for t in toks]   # token bytes
mb = ["".join([a,b]).encode("utf-8") for a,b in td["model"]["merges"]]  # BPE merges
```
GGUF stores the tokenizer inline. It inverts the `{token: id}` map into an id-indexed list, overlays special/added tokens, then encodes both the token list and the BPE merge pairs as UTF-8 bytes. The merges are what let llama.cpp rebuild the exact BPE encoder.

**2. Config → GGUF metadata (KV pairs)**
```python
gw.add_context_length(c.n_positions)     # 1024
gw.add_embedding_length(c.n_embd)        # 768
gw.add_block_count(c.n_layer)            # 12
gw.add_head_count(c.n_head)              # 12
gw.add_feed_forward_length(...n_inner... or 4*n_embd)  # 3072
```
Standard GPT-2 124M hyperparameters written as GGUF KV metadata so the runtime knows the architecture shape. BOS/EOS both set to `50256` (`<|endoftext|>`), which is correct for GPT-2.

**3. Weight transposition — the key subtlety**

GPT-2's HF implementation uses `Conv1D`, not `nn.Linear`. `Conv1D` stores weights as `[in, out]`, whereas llama.cpp expects linear weights as `[out, in]`. Hence every projection gets `.T`:
```python
gw.add_tensor("blk.{i}.attn_qkv.weight",  sd[...c_attn.weight].numpy().T)
gw.add_tensor("blk.{i}.attn_output.weight", sd[...c_proj.weight].numpy().T)
gw.add_tensor("blk.{i}.ffn_up.weight",    sd[...mlp.c_fc.weight].numpy().T)
gw.add_tensor("blk.{i}.ffn_down.weight",  sd[...mlp.c_proj.weight].numpy().T)
```
Biases are **not** transposed (1-D). The `np.ascontiguousarray(...)` after `.T` is necessary because transpose returns a non-contiguous view, and the GGUF writer needs contiguous memory to dump raw bytes.

**4. Tensor name remapping**

HF names → GGUF canonical names:

| HF | GGUF |
|---|---|
| `transformer.wte.weight` | `token_embd.weight` |
| `transformer.wpe.weight` | `position_embd.weight` |
| `h.{i}.ln_1` | `blk.{i}.attn_norm` |
| `h.{i}.attn.c_attn` | `blk.{i}.attn_qkv` |
| `h.{i}.attn.c_proj` | `blk.{i}.attn_output` |
| `h.{i}.mlp.c_fc` | `blk.{i}.ffn_up` |
| `h.{i}.mlp.c_proj` | `blk.{i}.ffn_down` |
| `transformer.ln_f` | `output_norm` |
| `lm_head` | `output` |

**5. Embedding/head slicing**
```python
wte = sd["transformer.wte.weight"].numpy()[:nv]   # trim to real vocab
lm  = sd["lm_head.weight"].numpy()[:nv].T
```
The `[:nv]` trims any padding rows (GPT-2 often pads vocab to a multiple of 64 for tensor-core alignment — 50257 → 50304). It slices back to the true tokenizer size so embeddings and tokenizer agree.

**6. Write order**
```python
gw.write_header_to_file()
gw.write_kv_data_to_file()
gw.write_tensors_to_file()
```
GGUF is laid out as header → KV metadata → tensor data, written in that exact sequence.

**Things to flag:**

- `gw.add_parallel_residual(True)` is **wrong** for GPT-2. GPT-2 uses sequential residuals (attn → add → MLP → add), not parallel (GPT-J/NeoX style where attn and MLP run on the same normed input). This metadata likely gets ignored by llama.cpp's GPT-2 path, but it's semantically incorrect.
- `add_token_scores([0.0]*nv)` — fine, GPT-2 BPE doesn't use unigram scores.
- Output is `f32` (no quantization). Run `llama-quantize sec-edgar-gpt-124m.gguf out-q8.gguf Q8_0` afterward to shrink it.

You could replace this entire script with `python convert_hf_to_gguf.py hf-model/ --outfile sec-edgar-gpt-124m.gguf` from llama.cpp, which handles the Conv1D transposition and naming automatically — worth it unless you specifically want control over the tokenizer reconstruction.
