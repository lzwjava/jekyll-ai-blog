---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding TVM's Compiler Architecture Simply
translated: false
type: note
---

Question: **Intro to Apache TVM — what is it, and how should I think about the codebase?**

Answer:

Apache TVM is essentially a **compiler stack for turning ML programs into fast code for specific hardware**.

The easiest mental model is:

```text
PyTorch / model
      │
      ▼
   Relax IR          ← "what computation do I want?"
      │
      │ graph optimization / fusion / legalization
      ▼
   TensorIR           ← "how exactly do I implement the kernels?"
      │
      │ scheduling / lowering / codegen
      ▼
 CUDA / ROCm / LLVM / Metal / Vulkan / ...
      │
      ▼
 native executable
```

That's the modern TVM architecture: **Relax + TensorIR**, rather than the older "Relay + TE" mental model. ([GitHub][1])

---

## 1. What problem is TVM solving?

Suppose you write:

```python
y = softmax(x @ W + b)
```

in PyTorch.

At the Python level, this says almost nothing about how it should execute:

```text
matmul
  ↓
add
  ↓
softmax
```

But an A100 wants something closer to:

```text
for block in CUDA grid:
    load tiles from HBM
    shared-memory staging
    tensor-core MMA
    warp-level reduction
    vectorized stores
```

An AMD GPU wants a different implementation.

A CPU wants another implementation.

So TVM's fundamental job is:

```text
        high-level ML program
                 │
                 │ compiler transformations
                 ▼
       hardware-specific program
```

The important distinction is that TVM isn't merely an **operator library**.

It's a **program transformation system**.

The official project describes itself as an open ML compilation framework whose current design focuses on cross-level optimization between graph-level Relax and tensor-level TensorIR. ([GitHub][1])

---

# 2. The two things you should understand first

Forget most of the repository initially.

Learn these two:

```text
Relax
  ↓
TensorIR
```

### Relax = graph/program level

Relax represents something like:

```text
x
│
├── matmul
│
├── add
│
└── softmax
```

It understands:

* tensors
* functions
* dataflow
* control flow
* shape information
* operator composition
* graph transformations
* operator fusion

For example:

```python
@R.function
def main(
    x: R.Tensor((M, K), "float32"),
    w: R.Tensor((K, N), "float32"),
):
    y = R.matmul(x, w)
    return R.softmax(y)
```

Conceptually:

```text
Relax
 ┌──────────────────────────────┐
 │                              │
 │ x ──► matmul ──► softmax     │
 │             │                │
 │             ▼                │
 │             y                │
 │                              │
 └──────────────────────────────┘
```

Relax is therefore somewhat analogous to an **IR for the model/program as a whole**. ([Apache TVM][2])

---

# 3. TensorIR is where it gets interesting

Suppose Relax eventually says:

```text
C = A @ B
```

That's still too abstract to generate efficient GPU code.

TensorIR can represent the actual tensor program:

```python
for i, j, k in T.grid(M, N, K):
    with T.block("matmul"):
        ...
```

Now the compiler can transform the implementation:

```text
naive
   ↓
tile
   ↓
reorder loops
   ↓
bind CUDA threads
   ↓
vectorize
   ↓
shared memory
   ↓
tensor cores
```

This is the key idea behind TVM:

> **The algorithm and the implementation strategy are separate things.**

For example:

```text
C[i,j] = Σk A[i,k] * B[k,j]
```

is the algorithm.

These are implementation decisions:

```text
tile size
thread mapping
memory layout
vectorization
unrolling
shared memory
tensor core instructions
```

TensorIR gives you a programmable representation where these decisions can be transformed systematically. ([Apache TVM][3])

---

# 4. Think of TVM as "LLVM for tensor programs"

A useful analogy:

```text
LLVM:

C/C++
  ↓
LLVM IR
  ↓
optimization
  ↓
machine code
```

TVM:

```text
ML model
  ↓
Relax
  ↓
TensorIR
  ↓
optimization / scheduling
  ↓
CUDA / ROCm / LLVM / ...
```

But there's an important difference.

LLVM mostly optimizes **general-purpose programs**.

TVM is specifically designed to optimize **tensor computations**, where things like:

```text
tiling
layout
memory hierarchy
tensor cores
vectorization
parallelism
```

are first-class concerns.

---

# 5. The compiler pipeline

The architecture docs describe the flow roughly as:

```text
                   IRModule
                      │
          ┌───────────┴───────────┐
          │                       │
       Relax                    TensorIR
          │                       │
          │ transformations      │ schedules
          ▼                       ▼
      optimized graph        optimized kernels
          │                       │
          └───────────┬───────────┘
                      ▼
                   codegen
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
        CUDA        LLVM        ROCm
          │           │           │
          └───────────┼───────────┘
                      ▼
                 runtime.Module
                      │
                      ▼
                   execute
```

The central data structure is an **`IRModule`** containing functions. Relax functions describe high-level computation while TensorIR `PrimFunc`s describe low-level tensor programs. ([Apache TVM][3])

---

# 6. Why `IRModule` matters

If you browse the source, this is one abstraction I'd learn early.

Think:

```python
IRModule = {
    relax_function_1,
    relax_function_2,
    tir_primfunc_1,
    tir_primfunc_2,
    ...
}
```

Then compiler passes repeatedly transform it:

```text
IRModule
   │
   ▼
Pass A
   │
   ▼
IRModule'
   │
   ▼
Pass B
   │
   ▼
IRModule''
   │
   ▼
codegen
```

This is very compiler-ish.

Instead of:

```text
model → magic compiler → binary
```

you get:

```text
program
  ↓
IR
  ↓
IR transformation
  ↓
IR transformation
  ↓
IR transformation
  ↓
lowered IR
  ↓
machine code
```

That makes TVM hackable.

---

# 7. A concrete example

Imagine:

```python
y = x @ W
```

At the Relax level:

```text
call_tir(matmul, x, W)
```

Then TensorIR might contain something conceptually like:

```python
@T.prim_func
def matmul(
    A: T.Buffer((M, K), "float32"),
    B: T.Buffer((K, N), "float32"),
    C: T.Buffer((M, N), "float32"),
):
    for i, j, k in T.grid(M, N, K):
        with T.block("matmul"):
            C[i, j] += A[i, k] * B[k, j]
```

Then scheduling transforms this:

```text
             original
                │
                ▼
       ┌─────────────────┐
       │ i,j,k loops     │
       └─────────────────┘
                │
             tiling
                ▼
       ┌─────────────────┐
       │ io / jo / ko    │
       │ ii / ji / ki    │
       └─────────────────┘
                │
          thread binding
                ▼
       CUDA thread/block
                │
          memory layout
                ▼
       shared/register
                │
          instruction
                ▼
       CUDA kernel
```

That's the heart of TVM.

---

# 8. Where auto-tuning comes in

Here's another major idea.

You don't necessarily know the optimal schedule:

```text
tile_M = ?
tile_N = ?
tile_K = ?
num_warps = ?
vector_width = ?
shared_memory_layout = ?
```

TVM can search.

Historically this evolved into **AutoTVM / Ansor / MetaSchedule**. The current docs expose MetaSchedule as a search-based auto-tuning system, alongside DLight's rule-based scheduling. ([Apache TVM][4])

Conceptually:

```text
                  TensorIR
                     │
          ┌──────────┼──────────┐
          │          │          │
       schedule1  schedule2  schedule3
          │          │          │
        120 μs      80 μs      95 μs
          │          │          │
          └──────────┼──────────┘
                     ▼
                  80 μs
```

This is where TVM starts looking less like a traditional compiler and more like:

```text
compiler
   +
search
   +
performance engineering
```

---

# 9. The runtime

After compilation, TVM needs somewhere to execute the generated code.

So:

```text
compiler
   │
   ▼
runtime.Module
   │
   ▼
TVM runtime
   │
   ├── CPU
   ├── CUDA
   ├── ROCm
   ├── Vulkan
   ├── Metal
   └── ...
```

The runtime abstracts things like:

```text
memory allocation
device management
function invocation
module loading
RPC
```

For Relax specifically, the **Relax VM** executes high-level compiled programs and dispatches actual computation to compiled TIR kernels or external libraries. Its instruction set is deliberately tiny; the VM mostly orchestrates execution rather than doing numerical computation itself. ([Apache TVM][5])

So:

```text
Relax VM
   │
   ├── call kernel A
   ├── allocate tensor
   ├── call kernel B
   ├── branch
   └── return
```

while:

```text
CUDA kernel
```

actually performs:

```text
FMA
load
store
reduce
...
```

---

# 10. The repository layout

The current repository is huge, so don't read it top-to-bottom.

The interesting areas are roughly:

```text
tvm/
├── python/
│   └── tvm/
│       ├── relax/       # graph-level compiler
│       ├── tirx/        # TensorIR representation/lowering
│       ├── s_tir/       # scheduling / tuning
│       ├── target/      # target abstraction
│       ├── runtime/     # runtime
│       └── ...
│
├── src/
│   ├── relax/
│   ├── tir/
│   ├── runtime/
│   └── ...
│
├── include/tvm/
│
├── tests/
│
└── docs/
```

The repository itself currently describes the project as Python-first and specifically calls out its cross-level design around Relax and TensorIR. ([GitHub][1])

---

# 11. One important historical warning

If you search Google/old blog posts, you'll see:

```text
Relay
TE
TOPI
AutoTVM
AutoScheduler
```

Those are important historically, but **don't construct your mental model of current TVM around them**.

The architecture has gone through several redesigns. The current project explicitly describes its recent direction as:

```text
Relax
   +
TensorIR
   +
Python-first transformations
   +
cross-level optimization
```

and says the stack is also intended as infrastructure for vertical compilers, including LLM-oriented systems. ([GitHub][1])

---

# 12. Why this is interesting for LLM inference

This is probably the part I'd pay attention to given the kind of systems you're building.

An LLM isn't fundamentally special from the compiler's perspective.

At the bottom it's still:

```text
matmul
attention
RMSNorm
RoPE
softmax
elementwise
reduce
KV cache operations
```

But modern inference has nasty interactions between:

```text
graph structure
      +
kernel implementation
      +
memory layout
      +
quantization
      +
GPU architecture
      +
communication
```

A cross-level compiler can reason about more than one of these layers simultaneously.

For example:

```text
Relax

   attention
      │
      ├── Q projection
      ├── K projection
      ├── V projection
      ├── attention
      └── output projection
             │
             ▼
          TensorIR
             │
       ┌─────┴─────┐
       │           │
   kernel A     kernel B
       │           │
       ▼           ▼
      CUDA        CUDA
```

And TVM's current stack also includes **Disco**, its distributed runtime, for multi-device execution and collective communication such as allreduce/allgather. ([Apache TVM][3])

---

# 13. The fastest way I'd learn it

Don't read the entire TVM codebase.

I'd do this:

### Step 1 — Write one TensorIR kernel

Start with:

```text
vector add
```

then:

```text
matmul
```

then:

```text
softmax
```

Understand:

```text
PrimFunc
Buffer
Block
Loop
Schedule
```

### Step 2 — Learn scheduling

Take:

```text
C[i,j] = Σ A[i,k]B[k,j]
```

and manually implement:

```text
naive
→ tiled
→ parallel
→ vectorized
→ GPU
```

This is where the real TVM value becomes obvious.

### Step 3 — Learn Relax

Then:

```text
matmul → add → softmax
```

as a graph.

Understand:

```text
Relax Function
IRModule
DataflowBlock
Call
Shape
Tensor
Pass
```

### Step 4 — Follow lowering

Trace:

```text
Relax
  ↓
FuseOps
  ↓
LegalizeOps
  ↓
call_tir
  ↓
TensorIR
  ↓
schedule
  ↓
CUDA
```

The architecture documentation explicitly recommends starting with this overall compilation flow before diving into individual components. ([Apache TVM][3])

### Step 5 — Read the implementation

Then I'd jump into:

```bash
git clone https://github.com/apache/tvm
cd tvm

rg "class IRModule" python src
rg "class PrimFunc" python src
rg "class Schedule" python src
rg "FuseOps" python src
rg "MetaSchedule" python src
```

The key is to follow **one kernel end-to-end**, rather than trying to understand TVM globally.

---

## The one-sentence mental model

If you remember only this:

```text
TVM = a programmable compiler for tensor programs.

Relax    → what the ML program computes
TensorIR → how the computation is implemented
Schedule → how we optimize that implementation
Target   → which hardware we're compiling for
Runtime  → how the resulting program executes
```

And the whole thing is basically:

```text
        MODEL
          │
          ▼
       RELAX
    "what to compute"
          │
          ▼
     TENSORIR
   "how to compute"
          │
          ▼
      SCHEDULE
   "make it fast"
          │
          ▼
       CODEGEN
    "for this GPU"
          │
          ▼
       RUNTIME
       "execute"
```

That's the architecture I'd keep in my head while reading the repo.

### References

* [Apache TVM repository](https://github.com/apache/tvm?utm_source=chatgpt.com) ([GitHub][1])
* [TVM Design and Architecture](https://tvm.apache.org/docs/arch/?utm_source=chatgpt.com) ([Apache TVM][3])
* [TVM Relax documentation](https://tvm.apache.org/docs/deep_dive/relax/index.html?utm_source=chatgpt.com) ([Apache TVM][2])
* [Relax VM architecture](https://tvm.apache.org/docs/arch/relax_vm.html?utm_source=chatgpt.com) ([Apache TVM][5])

I can next walk through a **single `matmul` from Relax → TensorIR → CUDA, line by line**, which is probably the fastest way to make the architecture click.

[1]: https://github.com/apache/tvm "GitHub - apache/tvm: Open Machine Learning Compiler Framework · GitHub"
[2]: https://tvm.apache.org/docs/deep_dive/relax/index.html?utm_source=chatgpt.com "Relax — Apache TVM"
[3]: https://tvm.apache.org/docs/arch/?utm_source=chatgpt.com "Design and Architecture — Apache TVM"
[4]: https://tvm.apache.org/docs/?utm_source=chatgpt.com "Apache TVM Documentation — Apache TVM"
[5]: https://tvm.apache.org/docs/arch/relax_vm.html?utm_source=chatgpt.com "Relax Virtual Machine — Apache TVM"
