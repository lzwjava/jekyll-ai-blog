---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rust Powers OXC Speed Revolution
translated: false
type: note
---

Question: Why is oxc.rs (the JavaScript Oxidation Compiler) so fast?

Answer:

## What is OXC?

OXC (oxc.rs) is a collection of high-performance JavaScript and TypeScript tools — parser, linter, formatter, transformer, minifier, and resolver — written entirely in Rust. It is part of VoidZero's vision for a unified, high-performance toolchain for JavaScript, and it powers Rolldown (Vite's future bundler).

---

## Why Is It Fast?

### 1. Written in Rust

OXC leverages Rust's memory safety guarantees and zero-cost abstractions to achieve performance levels previously impossible in JavaScript-based tooling. Unlike ESLint (Node.js/JS) or Babel (JS), Rust compiles to native machine code with no garbage collector pauses and no JIT warm-up overhead.

---

### 2. Memory Arena Allocation

Memory arena allocates memory upfront in chunks or pages and deallocates altogether when the arena is dropped. The AST is allocated on the arena so dropping the AST is a fast operation.

Additionally, the AST is constructed in a specific order, and tree traversal also follows the same order, resulting in linear memory access during the visitation process. This access pattern is efficient since all nearby memory will be read into the CPU cache in pages, resulting in faster access times.

Switching to a memory arena for the AST resulted in roughly a **20% performance improvement**.

---

### 3. Small and Cache-Friendly AST Enum Sizes

In a typical JavaScript AST, enums like `Expression` (45 variants) and `Statement` (20 variants) can exceed 200 bytes per node if naively implemented. OXC carefully boxes enum variants to keep them small. This reduces the data that must be passed around and read during pattern matching — improving **CPU cache efficiency** significantly.

---

### 4. Shared Compiler Stack (No Redundant Parsing)

The shared parser architecture means that all OXC tools operate on the same Abstract Syntax Tree (AST), eliminating the redundant parsing that traditionally occurs when multiple tools process the same codebase. In traditional setups, ESLint, Babel, and Prettier each parse files independently — OXC only parses once.

---

### 5. Optimized Parser Internals

The parser uses several optimization techniques: AST nodes are allocated in a memory arena for fast cleanup, span offsets use `u32` instead of `usize` for memory efficiency, and complex syntax errors are delegated to a separate semantic analyzer to keep parsing fast.

---

### 6. Parallelism Without Contention

The team removed global locking mechanisms (like the `string-cache` library) that were blocking threads during parallel parsing. Removing this global lock improved the performance of parallel parsing by about **30%**, achieving full CPU core utilization via Rayon (Rust's data-parallelism library).

---

### 7. Speed Is Treated as a First-Class Requirement

Oxc treats speed as a product requirement. Faster tools improve the local feedback loop and reduce CI cost. Performance regressions are treated as bugs.

---

## Benchmark Summary

Oxc's parser is at least 3x faster than SWC and 5x faster than Biome. The OXC transformer is 4x faster than SWC and 40x faster than Babel, using 70% less memory. Oxlint is 50–100x faster than ESLint depending on the number of CPU cores. Oxfmt is 3x faster than Biome and 35x faster than Prettier. The oxc-resolver is 30x faster than webpack's enhanced-resolve.

---

## Summary Table

| Tool | Compared To | Speed Gain |
|---|---|---|
| Parser | SWC | ~3x faster |
| Parser | Biome | ~5x faster |
| Linter | ESLint | 50–100x faster |
| Formatter | Prettier | ~35x faster |
| Transformer | Babel | ~40x faster |
| Resolver | webpack enhanced-resolve | ~30x faster |

References:

- [oxc.rs — What is Oxc?](https://oxc.rs/docs/guide/what-is-oxc.html)
- [oxc.rs — Performance Deep Dive](https://oxc.rs/docs/learn/performance)
- [oxc.rs — All Benchmarks](https://oxc.rs/docs/guide/benchmarks.html)
- [OXC Deep Dive Article](https://alisoueidan.com/blog/oxc-rust-powered-next-gen-javascript-tooling)
- [GitHub — oxc-project/oxc](https://github.com/oxc-project/oxc)