---
audio: false
generated: true
image: false
lang: en
layout: post
title: Learning vLLM via Hands-On Iteration
translated: false
type: note
---

Question: Why learning vLLM / inference requires the same iterative loop as nanoGPT training?

Answer:

Yes, exactly. The same **experimental loop** that made nanoGPT click is the right way to understand vLLM, nano-vLLM, and inference systems.

The difference is:

* nanoGPT → you learned **how a model learns**
* nano-vLLM → you learn **how a model runs efficiently**

But the methodology is identical:

```
hypothesis
   ↓
change one thing
   ↓
run experiment
   ↓
print logs / inspect tensors / measure
   ↓
build mental model
   ↓
repeat
```

That is basically how Karpathy learns systems too.

---

For nanoGPT, your loop was:

```
model.py
   |
   | print(loss)
   | print(tokens)
   | print(attention)
   | modify architecture
   |
train
   |
observe behavior
```

After running 13 small models, your brain accumulated:

* what loss curve looks like
* overfitting behavior
* under-training behavior
* effect of dataset quality
* parameter scaling
* context length impact
* optimizer behavior

You didn't "read transformer theory"; you built an internal simulator.

---

For vLLM the same thing happens, but the variables change.

A transformer forward pass:

```
tokens
  |
embedding
  |
attention
  |
MLP
  |
logits
  |
sampling
  |
next token
```

vLLM adds the serving layer:

```
HTTP request
      |
 tokenizer
      |
 scheduler
      |
 KV cache manager
      |
 GPU execution
      |
 sampling
      |
 streaming tokens
```

You need to observe:

### 1. Different input lengths

Example:

```
Prompt A:
"hello"

Prompt B:
10000 tokens document
```

Observe:

* prefill latency
* memory usage
* KV cache growth

You start understanding:

"Ah, long prompt cost is not the same as generation cost."

---

### 2. Different generation lengths

Example:

```
input:
Explain transformer

max_tokens=20

vs

max_tokens=2000
```

Observe:

* decode speed
* tokens/sec
* GPU utilization

You discover:

```
prefill = compute heavy

decode = memory bandwidth heavy
```

---

### 3. Different models

Run:

```
Qwen3-8B
Llama-8B
Mistral-7B
```

Same server.

Observe:

```
model size
      |
      v
VRAM
      |
      v
KV cache capacity
      |
      v
batch size
      |
      v
throughput
```

Then vLLM architecture becomes intuitive.

---

### 4. Change scheduler parameters

For example:

```
max_num_seqs
max_model_len
gpu_memory_utilization
```

Run:

```
10 users
50 users
100 users
```

Watch:

```
latency
throughput
OOM
```

You learn why vLLM invented PagedAttention.

---

The key experiment:

Run a tiny nano-vLLM.

Something like:

```
nano-vllm/
 ├── engine.py
 ├── scheduler.py
 ├── attention.py
 ├── kv_cache.py
 └── sampler.py
```

Add logs:

```python
print(
    "request",
    request_id,
    "prompt_len",
    len(tokens),
)

print(
    "kv blocks",
    len(kv_cache.blocks)
)

print(
    "batch size",
    len(active_requests)
)
```

Then send:

```
request 1:
short prompt

request 2:
long prompt

request 3:
code generation
```

Watch the scheduler.

The moment you see:

```
Request A:
tokens 0-4096

KV blocks:
[1][2][3][4]

Request B:
tokens 0-512

KV blocks:
[5]
```

PagedAttention stops being a paper concept.

It becomes a thing you have watched happen.

---

Your previous nanoGPT learning pattern is actually closer to how research engineers work:

Not:

```
read paper
memorize formula
implement
```

but:

```
implement
break it
measure it
make wrong assumptions
fix mental model
```

For vLLM, I would do the same progression:

```
Step 1:
llama.cpp inference

Step 2:
naive PyTorch generate()

Step 3:
batch multiple requests

Step 4:
add KV cache

Step 5:
continuous batching

Step 6:
PagedAttention

Step 7:
CUDA kernel optimization
```

Each step should be a "small model experiment".

The biggest jump is usually when you implement **continuous batching + KV cache management**. That is where inference systems become different from normal ML code. You stop thinking "one input → one output" and start thinking "GPU time scheduler managing many token streams."
