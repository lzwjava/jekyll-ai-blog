---
audio: false
generated: true
image: false
lang: en
layout: post
title: Q-First for Faster LLM Decoding
translated: false
type: note
---

Question: What is the point of arXiv:2608.15473 **“Q-First: Most of Attention Needs Only the Query in Disaggregated LLM Decoding”**? What is the usage? ([arXiv][1])

Answer:

This paper is about **making LLM inference faster by changing the execution order of Transformer decoding**. The target problem is **large-scale LLM serving**, not model quality. ([arXiv][1])

The core idea:

> During autoregressive decoding, attention does not need to wait for the full QKV computation. The attention KV-cache operation mainly needs the **Query (Q)** first.

They call this **Q-First**. ([arXiv][1])

---

## 1. Background: why LLM serving is slow

A Transformer decoder block:

```
input hidden state
        |
        v
   LayerNorm
        |
        v
   Attention
   (Q,K,V projection + KV cache lookup)
        |
        v
   Feed Forward Network (FFN)
        |
        v
   output
```

For decoding one token:

```
new token
   |
compute Q,K,V
   |
attention(Q, KV-cache)
   |
FFN
   |
next token
```

The problem:

* Attention is **memory bandwidth heavy**
* FFN is **compute heavy**
* They often run on different optimized hardware

Example:

```
GPU A: KV-cache memory server
GPU B: compute server
```

This is called **disaggregated LLM serving**. ([arXiv][1])

---

## 2. Current disaggregated design problem

People separate:

```
Memory side:
    KV cache
        |
        v
Compute side:
    FFN + projections
```

But Transformer has a dependency:

```
Attention
    |
    v
FFN
```

So:

```
GPU A:
  attention █████

GPU B:
  waiting ...
```

or:

```
GPU B:
  FFN █████

GPU A:
  waiting ...
```

Hardware is idle.

---

## 3. Their observation

The attention calculation:

[
Attention(Q,K,V)=softmax(\frac{QK^T}{\sqrt d})V
]

requires:

* Q immediately
* K,V from KV cache

But the FFN does not actually need the final attention output immediately.

They find:

```
Q can be moved earlier
```

So execution becomes:

```
Step 1:

Compute Q
       |
       +----------------+
                        |
                        v

             Attention reads KV cache


Meanwhile:

             FFN continues previous work
```

The two devices overlap.

---

## 4. The trick

Normal:

```
Attention
    |
    v
FFN
```

Q-First:

```
        Q
        |
        v

Attention starts

        |
        |
        v

FFN continues
```

They do not change:

* model architecture
* tensor shapes
* operators
* weights

Only scheduling/execution order changes. ([arXiv][1])

---

## 5. Practical usage

The usage is for companies running:

* GPT-like APIs
* Llama/Qwen/DeepSeek serving
* thousands of GPUs
* expensive inference clusters

Examples:

```
OpenAI API
Anthropic API
Google Gemini serving
Alibaba Qwen serving
```

A serving stack could do:

```
User request
      |
      v
Scheduler
      |
      +----------------+
      |                |
 KV-cache GPU       Compute GPU
      |                |
 Attention        FFN
      |
 merge
      |
 next token
```

Benefits:

### Higher GPU utilization

Instead of:

```
GPU utilization:

GPU-A  ████░░░░░
GPU-B  ░░░████░░
```

closer to:

```
GPU-A  ████████
GPU-B  ████████
```

---

### Lower latency

For chat:

```
first token latency ↓
tokens/sec ↑
```

---

### Lower cost

GPU clusters are expensive.

If you improve utilization:

```
1000 H100s
       |
       v

same throughput as

800 H100s
```

Huge savings.

---

## 6. Relation to your vLLM / Qwen experiments

This is very relevant to systems like:

* vLLM
* TensorRT-LLM
* SGLang
* DeepSpeed-Inference

because these systems are already optimizing:

* KV cache
* continuous batching
* paged attention
* tensor parallelism

Q-First is another layer:

```
Model optimization

        |
        v

Inference kernel optimization

        |
        v

Scheduling optimization   <-- this paper
```

---

## 7. Why it is interesting

The deeper idea:

Transformers look sequential:

```
Attention -> FFN -> Attention -> FFN
```

but some dependencies are artificial.

The paper asks:

> Which parts of Transformer computation truly depend on each other?

and removes unnecessary synchronization.

This is similar philosophy to:

* FlashAttention: reduce memory movement
* PagedAttention: manage KV memory better
* speculative decoding: remove unnecessary token steps

---

My summary:

**Q-First does not make LLM smarter. It makes LLM serving cheaper and faster by allowing attention and FFN computation to overlap in distributed inference systems.**

For someone building LLM infrastructure, this is the kind of paper to watch because future inference cost reductions will come less from new architectures and more from exploiting hardware/software execution details. ([arXiv][1])

References:

* ([arXiv][1])

[1]: https://arxiv.org/abs/2608.15473 "[2608.15473] Q-First: Most of Attention Needs Only the Query in Disaggregated LLM Decoding"
