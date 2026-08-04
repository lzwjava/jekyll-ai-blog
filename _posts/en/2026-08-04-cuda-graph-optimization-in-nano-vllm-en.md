---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA Graph Optimization in nano-vLLM
translated: false
type: note
---

Question: What is CUDA Graph, and why does nano-vLLM need it?

Answer:

CUDA Graph is a **GPU execution optimization mechanism** from NVIDIA. The core idea:

> Instead of launching thousands of CUDA kernels from Python/C++ every iteration, record the GPU execution once, then replay it with almost zero CPU overhead.

This matters a lot for LLM inference, especially **decode phase**.

nano-vLLM includes CUDA Graph optimization and captures decode batches like `[1,2,4,8,16,...512]` so repeated token generation can avoid Python/kernel launch overhead. ([Mintlify][1])

---

## 1. Normal PyTorch inference path

Imagine generating one token:

```
User
 |
 | input token
 v
Python
 |
 | model.forward()
 v
PyTorch dispatcher
 |
 | launch kernels
 v
GPU

  matmul kernel
  attention kernel
  layernorm kernel
  softmax kernel
  ...
```

For a 32-layer transformer:

```
Python
  |
  +-- launch GEMM
  +-- launch attention
  +-- launch RMSNorm
  +-- launch GEMM
  +-- launch RoPE
  +-- ...
       hundreds of kernel launches
```

The GPU computation itself may be fast, but every kernel launch has CPU overhead.

Typical overhead:

```
CPU prepares kernel
       |
       v
CUDA driver
       |
       v
GPU executes
```

Each launch costs microseconds.

For training, no big deal:

```
large batch
large matmul
GPU busy seconds
```

But LLM decode is different:

```
batch = 1 token
small matrix operations
many layers
repeat thousands times
```

The GPU spends more time waiting for CPU.

---

## 2. CUDA Graph idea

CUDA Graph changes:

### Without graph

Every token:

```
Python loop:

token 1:
 launch kernel A
 launch kernel B
 launch kernel C

token 2:
 launch kernel A
 launch kernel B
 launch kernel C

token 3:
 launch kernel A
 launch kernel B
 launch kernel C
```

Huge repeated overhead.

---

### With CUDA Graph

First time:

```
CUDA graph capture:

kernel A
   |
kernel B
   |
kernel C
   |
kernel D

record this execution graph
```

Later:

```
GPU replay(graph)

GPU:
 A -> B -> C -> D

(no Python involvement)
```

The CPU basically says:

```
"execute this graph"
```

instead of:

```
"launch kernel 1"
"launch kernel 2"
"launch kernel 3"
...
```

---

## 3. Why LLM decode is perfect for CUDA Graph

LLM inference has two phases:

```
Prompt:
   "Explain CUDA Graph"

        |
        v

Prefill phase
----------------
Process thousands tokens

big matrix multiplication
GPU utilization high


Decode phase
----------------
Generate:

token 1
token 2
token 3
...

small batch
repeated structure
```

Decode looks like:

```
while not EOS:

    logits = model(last_token, KV_cache)

    next_token = sample(logits)

```

Every iteration has almost identical computation.

That is exactly what CUDA Graph likes:

```
same operations
same shapes
same memory layout
repeat many times
```

---

## 4. Why nano-vLLM needs CUDA Graph

nano-vLLM is a minimal vLLM implementation. It already has:

* continuous batching
* KV cache
* paged attention ideas
* tensor parallel
* CUDA graph support

([Awesome Lists][2])

The scheduler creates decode batches:

Example:

```
batch size = 8

request:
 A -> generate token
 B -> generate token
 C -> generate token
 ...
```

The model execution shape is predictable:

```
input_ids:
[8,1]

positions:
[8]

KV cache:
fixed blocks
```

So nano-vLLM can capture:

```
graph[1]
graph[2]
graph[4]
graph[8]
graph[16]
...
graph[512]
```

Then:

```
current batch = 8

execute graph[8]
```

instead of rebuilding the PyTorch execution every token.

([Mintlify][1])

---

## 5. Simple PyTorch example

Without CUDA Graph:

```python
for i in range(10000):
    y = model(x)
```

Each loop:

```
Python
  |
  model.forward()
  |
  CUDA kernels
```

---

With CUDA Graph:

```python
graph = torch.cuda.CUDAGraph()

torch.cuda.synchronize()

with torch.cuda.graph(graph):
    y = model(x)


for i in range(10000):
    graph.replay()
```

Now:

```
Python
 |
 replay()
 |
 GPU executes recorded graph
```

---

## 6. Why not always use CUDA Graph?

Because CUDA Graph has constraints.

During capture:

```
shape must stay same
memory addresses must stay stable
no dynamic allocation
no random Python control flow
```

Bad:

```python
if batch_size == 7:
    do A
else:
    do B
```

Graph cannot easily handle this.

That is why vLLM/nano-vLLM architecture separates:

```
CPU side:
 scheduler
 request management
 KV cache allocation

GPU side:
 fixed execution
```

This design makes graph capture possible. ([Ashwing][3])

---

## 7. Why vLLM is fast

A modern LLM serving stack looks like:

```
                 requests
                    |
                    v

              Scheduler
              (CPU)

                    |
          choose batch size

                    |
                    v

          CUDA Graph replay

                    |
                    v

             GPU kernels

                    |
                    v

             next token
```

Performance comes from combining:

```
PagedAttention
+
continuous batching
+
KV cache management
+
CUDA Graph
+
optimized kernels (FlashAttention/Triton)
```

CUDA Graph is only one piece, but for decode-heavy workloads it can be a big win.

---

For your RTX 4070 experiments with Qwen/nano-vLLM, you can see the effect easily:

```bash
CUDA_LAUNCH_BLOCKING=1 python benchmark.py
```

or compare:

```python
LLM(
    model_path,
    enforce_eager=True   # no CUDA graph
)
```

vs

```python
LLM(
    model_path,
    enforce_eager=False  # CUDA graph enabled
)
```

The second one should improve decode throughput, especially with concurrent requests. ([Mintlify][1])

References:

* CUDA Graphs Programming Guide: [https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#cuda-graphs](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#cuda-graphs)
* nano-vLLM: ([Awesome Lists][2])
* nano-vLLM benchmarking notes: ([Mintlify][1])

[1]: https://www.mintlify.com/GeeeekExplorer/nano-vllm/guides/benchmarking?utm_source=chatgpt.com "Benchmarking - Nano-vLLM"
[2]: https://awesome.ecosyste.ms/projects/github.com%2FGeeeekExplorer%2Fnano-vllm?utm_source=chatgpt.com "https://github.com/GeeeekExplorer/nano-vllm | Ecosyste.ms: Awesome"
[3]: https://ashwing.github.io/vllm-guide/ch02.html?utm_source=chatgpt.com "nano-vLLM · Ch02 · Architecture"
