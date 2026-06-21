---
audio: false
generated: true
image: false
lang: en
layout: post
title: MLIR Compiler Infrastructure Overview
translated: false
type: note
---

**Question:** Give me an introduction to MLIR (mlir.llvm.org).

**Answer:**

## MLIR: Multi-Level Intermediate Representation

MLIR is a compiler infrastructure framework that sits **between high-level ML frameworks and low-level code generation**. It was originally developed at Google, now lives inside the LLVM project, and is the backbone of how TensorFlow/XLA, JAX, PyTorch (via Torch-MLIR), and most serious ML compilers work today.

### The Core Problem It Solves

Before MLIR, every ML framework built its own IR, its own graph optimizer, its own lowering pipeline. TensorFlow had XLA HLO, PyTorch had TorchScript IR, TOSA existed for edge targets, CUDA had PTX. Reusing passes between these was essentially impossible — **N frameworks × M hardware targets = N×M bespoke compilers**.

MLIR's answer: one extensible IR with a **dialect system** that lets multiple abstraction levels coexist in the same IR and progressively lower into each other.

### Key Concepts

#### 1. Operations (Ops)

Everything in MLIR is an `Op`. An op has:

- A name (`linalg.matmul`, `arith.addi`, `func.call`)
- Operands (SSA values in)
- Results (SSA values out)
- Attributes (compile-time constants)
- Regions (nested scopes — how loops and functions are represented)

```mlir
// A simple MLIR snippet
func.func @matmul(%A: memref<4x4xf32>, %B: memref<4x4xf32>, %C: memref<4x4xf32>) {
  linalg.matmul ins(%A, %B : memref<4x4xf32>, memref<4x4xf32>)
               outs(%C : memref<4x4xf32>)
  return
}
```

#### 2. Dialects

A dialect is a namespace of ops, types, and attributes that model a specific abstraction level. Think of each dialect as a "mini-IR":

| Dialect | Level | Purpose |
|---------|-------|---------|
| `linalg` | High | Named tensor contractions (matmul, conv) |
| `affine` | High | Polyhedral loop modeling |
| `scf` | Mid | Structured control flow (for/if/while) |
| `memref` | Mid | Memory reference semantics |
| `arith` | Low | Scalar arithmetic |
| `llvm` | Very Low | Maps 1:1 to LLVM IR |
| `gpu` | Parallel | GPU kernel abstractions |
| `amdgpu` / `nvgpu` | HW-specific | ROCm / CUDA intrinsics |

For your MI300X work, the `amdgpu` and `rocdl` dialects are directly relevant — they model AMD-specific ops that eventually lower to AMDGPU ISA.

#### 3. Progressive Lowering (The Core Idea)

You don't jump from `linalg.matmul` directly to PTX. You lower through a **pipeline of dialect conversions**:

```
linalg.matmul
    ↓  (tile + vectorize)
scf.for + vector.contract
    ↓  (bufferization)
memref + scf
    ↓  (lower to GPU)
gpu.launch
    ↓  (convert to LLVM)
llvm.func  →  LLVM IR  →  PTX / AMDGPU ISA
```

Each step is a **pass** — a transformation that rewrites ops from one dialect to another. Passes compose into pipelines.

#### 4. Regions and SSA

MLIR extends SSA (like LLVM) with **regions** — blocks of ops that can be nested inside other ops. This lets a single IR represent both high-level dataflow graphs *and* low-level loops without switching representations. It's how `scf.for` holds a body, or how `func.func` holds a function body.

### Why It Matters for AI/ML Compilers

- **TensorFlow → XLA → StableHLO → MLIR** pipeline
- **PyTorch 2.0 (torch.compile)** uses `torch-mlir` to lower to `linalg` on tensors
- **IREE** (Google's inference runtime) is almost entirely MLIR
- **Triton** (OpenAI's GPU kernel DSL) compiles through MLIR passes before hitting PTX/AMDGPU
- **JAX's mosaic** for TPU is MLIR-based

Given your MI300X training work, this is the layer that sits between your PyTorch model and the actual ROCm kernel execution. Understanding it lets you write custom MLIR passes to fuse ops, tile for HBM bandwidth, or inspect what the compiler is actually emitting.

### Minimal Hands-On Entry Point

The Toy Tutorial is the standard entry — it builds a small language and lowers it all the way to LLVM IR through MLIR. But for AI engineering, I'd start with the Python bindings:

```python
# pip install mlir-python-bindings (or build from llvm-project)
from mlir.ir import Context, Module
from mlir.dialects import func, arith

with Context():
    module = Module.parse("""
        func.func @add(%a: i32, %b: i32) -> i32 {
            %c = arith.addi %a, %b : i32
            return %c : i32
        }
    """)
    print(module)
```

For your GPU/training path: look at **IREE** and **Triton**'s MLIR backends — those are real production uses directly relevant to your MI300X work.

### Mental Model

Think of MLIR as **git for compiler IRs** — it gives you a common substrate, version-controlled abstraction layers, and composable transforms, instead of every project reinventing the wheel. The dialect system is the killer feature: you can mix `linalg` + `gpu` + `affine` in one IR file and lower them independently.

**References:**

- [MLIR Homepage](https://mlir.llvm.org)
- [MLIR Language Reference](https://mlir.llvm.org/docs/LangRef/)
- [Toy Tutorial (Ch 1–7)](https://mlir.llvm.org/docs/Tutorials/Toy/)
- [MLIR Rationale](https://mlir.llvm.org/docs/Rationale/Rationale/)
- [AMDGPU Dialect](https://mlir.llvm.org/docs/Dialects/AMDGPU/)
