---
audio: false
generated: true
image: false
lang: en
layout: post
title: Native nanoGPT Model Serving Preferred
translated: false
type: note
---

Question: Is it a good idea to serve my nanoGPT-trained 124M model using the native nanoGPT model class instead of the HuggingFace `transformers` `GPT2LMHeadModel`?

Answer:

Yes — for your specific case (a model you trained yourself with nanoGPT), native is the correct call. The agent's reasoning in the transcript was right, and the `bias=False` issue is the crux. Let me make the tradeoff precise.

## Why native wins here

**1. Correctness — the `bias=False` mismatch is real.**

nanoGPT's `model.py` makes bias optional everywhere:

```python
class LayerNorm(nn.Module):
    def __init__(self, ndim, bias):
        self.weight = nn.Parameter(torch.ones(ndim))
        self.bias = nn.Parameter(torch.zeros(ndim)) if bias else None
    def forward(self, input):
        return F.layer_norm(input, self.weight.shape, self.weight, self.bias, 1e-5)
```

You trained with `bias=False`, so your checkpoint has **no** LayerNorm bias and **no** Linear bias params. HF's `GPT2LMHeadModel` has no such switch — GPT-2's architecture *always* includes biases (LayerNorm `beta`, attn/MLP `c_proj` bias, etc.). When you convert nanoGPT→HF, the converter has to **fabricate zero biases** to fill slots your training never used.

Now, mathematically a zero bias added to a pre-activation *is* a no-op at init — `x @ W + 0 == x @ W`. So why does the agent call it "subtly wrong"? Two reasons:

- **LayerNorm with `bias=None` vs `bias=zeros`**: numerically identical in the forward pass, so this one is genuinely harmless.
- **The risk is the conversion mapping itself.** nanoGPT stores attention as a single fused `c_attn` (3072×1024 for QKV) and HF expects `Conv1D` with transposed weight layout. Any off-by-transpose or wrong weight-tying in the converter silently degrades output without crashing. You only notice via gibberish or elevated loss — exactly the kind of bug that wastes an afternoon. Serving native skips the entire conversion surface.

**2. Sampling parity.** nanoGPT's `generate()` is ~10 lines and you know exactly what it does:

```python
@torch.no_grad()
def generate(self, idx, max_new_tokens, temperature=1.0, top_k=None):
    for _ in range(max_new_tokens):
        idx_cond = idx if idx.size(1) <= self.config.block_size else idx[:, -self.config.block_size:]
        logits, _ = self(idx_cond)
        logits = logits[:, -1, :] / temperature
        if top_k is not None:
            v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
            logits[logits < v[:, [-1]]] = -float('Inf')
        probs = F.softmax(logits, dim=-1)
        idx_next = torch.multinomial(probs, num_samples=1)
        idx = torch.cat((idx, idx_next), dim=1)
    return idx
```

HF's `model.generate()` is a 2000-line dispatcher with its own `top_k`/`temperature`/`do_sample`/`pad_token` semantics. Matching nanoGPT's eval-time behavior through HF's API means reverse-engineering which knobs map to what. Native = the same code path you used during training/eval.

**3. Dependency weight.** Native needs only `torch` + `tiktoken`. You drop `transformers` (and its `safetensors`/`tokenizers`/`huggingface_hub` tail). Faster cold start, smaller image, fewer version-pinning headaches on the RunPod box.

## Where HF would actually be better

Be honest about the other side — you'd choose HF `transformers` (or better, **vLLM**) when:

- You want **batched, high-throughput serving** with continuous batching, paged KV cache, and an OpenAI-compatible server out of the box. nanoGPT's `generate()` is single-sequence, no KV cache (it re-runs the full prefix every step → O(n²) compute). For a 124M toy that's fine; for real QPS it's not.
- You want the **ecosystem** — streaming, beam search, logit processors, quantization (bitsandbytes/GPTQ), `device_map` sharding.
- You're handing the model to someone else who expects a standard `from_pretrained` interface.

For a personal SEC-EDGAR 124M demo, none of those apply. Native is simpler and provably faithful to what you trained.

## The one upgrade worth doing

Since you're rolling your own server anyway, add a **KV cache** to `generate()` — it's the single highest-leverage change. Stock nanoGPT recomputes attention over the entire context every token. With a cache you keep past K/V and only attend the new token:

```python
# sketch: modify CausalSelfAttention.forward to accept/return past_kv
def forward(self, x, past_kv=None):
    B, T, C = x.size()
    q, k, v = self.c_attn(x).split(self.n_embd, dim=2)
    # reshape to (B, nh, T, hs) ...
    if past_kv is not None:
        pk, pv = past_kv
        k = torch.cat([pk, k], dim=2)
        v = torch.cat([pv, v], dim=2)
    present = (k, v)
    # F.scaled_dot_product_attention(q, k, v, is_causal=(past_kv is None))
    return y, present
```

Then `generate()` feeds only the last token each step. For a 1024-block model this turns per-token cost from O(T²) to O(T), which is the difference between sluggish and snappy on the RTX 4070. This is also a clean exercise in exactly the transformer-internals direction you're aiming at — it's the same mechanism vLLM's paged attention generalizes.

**Bottom line:** serve native for correctness and simplicity now; if you ever need throughput, skip HF and go straight to vLLM rather than the `transformers` middle ground.

References:

- [nanoGPT model.py](https://github.com/karpathy/nanoGPT/blob/master/model.py)
- [nanoGPT sample.py](https://github.com/karpathy/nanoGPT/blob/master/sample.py)
- [HF GPT-2 modeling source](https://github.com/huggingface/transformers/blob/main/src/transformers/models/gpt2/modeling_gpt2.py)
- [vLLM](https://github.com/vllm-project/vllm)
