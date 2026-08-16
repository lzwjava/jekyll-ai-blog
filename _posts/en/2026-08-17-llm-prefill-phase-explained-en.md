---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLM Prefill Phase Explained
translated: false
type: note
---

Question: How does prefill work in LLM inference?

Answer:

LLM inference happens in two distinct phases: **prefill** and **decode**. Prefill is the first phase, where the model processes the entire input prompt at once before generating any output tokens.

**What happens during prefill**

1. **Tokenization**: The input prompt is converted into a sequence of token IDs.
2. **Parallel forward pass**: All input tokens are fed through the model's layers simultaneously in a single forward pass. Because the whole prompt is known in advance, this can be computed as one large matrix multiplication rather than token-by-token.
3. **KV cache construction**: For every attention layer, the model computes and stores the key (K) and value (V) vectors for each input token. These are cached in memory (the "KV cache") so they don't need to be recomputed later.
4. **First output token**: At the end of prefill, the model produces a probability distribution over the vocabulary for the *next* token, and samples/selects the first generated token.

**Why it's separated from decode**

- **Compute pattern**: Prefill is highly parallel and compute-bound (matrix-multiply heavy), since all tokens are processed together. Decode, by contrast, generates one token at a time, reusing the cached K/V from prefill and only computing K/V for the newest token. Decode is memory-bandwidth-bound rather than compute-bound.
- **Latency characteristics**: Prefill determines "time to first token" (TTFT). Longer prompts mean longer prefill time, since the work scales with input length. Decode determines the per-token latency ("time per output token") during generation.
- **Hardware utilization**: Prefill tends to use GPUs efficiently (large batched matmuls), while decode is less efficient per step because it computes on a single new token at a time — this is why techniques like continuous batching, speculative decoding, and chunked prefill exist, to improve GPU utilization during decode or to interleave prefill and decode work across requests.

**A simple analogy**: prefill is like reading and fully understanding a question before answering — you process everything at once and build up context (the KV cache). Decode is like speaking the answer one word at a time, where each new word only depends on what's already been read and said, so you reuse that stored context rather than re-reading the whole question each time.

**In serving systems**: Many production inference engines (e.g., vLLM, TensorRT-LLM, Hugging Face TGI) explicitly optimize prefill and decode differently, and some use techniques like "chunked prefill" to split large prefill workloads into pieces that can be interleaved with ongoing decode steps for other requests, improving overall throughput and reducing tail latency.

References:
- [Efficient Memory Management for Large Language Model Serving with PagedAttention (vLLM paper)](https://arxiv.org/abs/2309.06180)
- [How continuous batching enables 23x throughput in LLM inference](https://www.anyscale.com/blog/continuous-batching-llm-inference)
- [Transformer Inference Arithmetic](https://kipp.ly/transformer-inference-arithmetic/)