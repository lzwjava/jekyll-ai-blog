---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rust Projects for AI Engineers
translated: false
type: note
---

Question: What are good Rust open source projects or tools worth studying / contributing to?

## Answer

Given your trajectory (AI engineering, developer tooling, systems depth), here's a curated list beyond the obvious:

### **ML/AI Infrastructure**

**Candle** (Hugging Face)

- Minimal ML framework in Rust, ~2-3k LOC for core ops
- Study it to understand: tensor shapes, autograd, GPU kernels
- Relevant: you're training models, this teaches GPU memory management in idiomatic Rust
- Repo: `huggingface/candle`

**Ort** (ONNX Runtime Rust bindings)

- Thin wrapper around ONNX Runtime for inference
- Good starting point if you want to ship LLM inference without learning CUDA yet
- Study the binding patterns — you'll do this repeatedly

**llm.rs** (ollama-like)

- Pure Rust LLM inference, small codebase, readable
- Teaches: tokenization, attention caching, sampling strategies in low-level code
- Repo: `rustformers/llm` (or check `ollama` source for a production version)

### **Developer Tools (Ship-Worthy)**

**Ruff** (Astral)

- Python linter written in Rust, ~50k LOC, very clean architecture
- Study: AST traversal, visitor pattern, parallel processing (rayon)
- Why: you understand Python deeply; seeing it reimplemented in Rust teaches language design
- Repo: `astral-sh/ruff`

**Helix** (modal text editor)

- Better code study than Zed for learning Rust patterns
- Smaller scope, tree-sitter integration, async event loop
- Teaches: UI architecture, incremental parsing, buffer management
- Repo: `helix-editor/helix`

**Ripgrep** (BurntSushi)

- ~9k lines, incredibly dense with Rust idioms
- Study: regex engines, parallel file iteration, error handling
- Repo: `BurntSushi/ripgrep`

### **Systems & Infrastructure**

**Tokio** (async runtime)

- Non-negotiable study material if you're building agents/CLI tools
- Learn: task scheduling, channels, testing async code
- Repo: `tokio-rs/tokio`

**tree-sitter** (Rust bindings)

- Incremental parser generator; pairs with your build-your-own-compiler instinct
- Use case: code analysis for your AI agents
- Repo: `tree-sitter/tree-sitter` (look at Rust bindings)

**Qdrant** (vector database)

- Purpose-built for embeddings/semantic search; relevant to your AI pipeline
- Study: HNSW indexing, RPC protocols, async web services
- Repo: `qdrant/qdrant`

**Nix** (package manager)

- Functional, immutable approach; deep systems thinking
- Hard to learn but worthwhile if you care about reproducibility
- Repo: `NixOS/nix`

### **What to Contribute To**

For your specific growth:

1. **Candle** — add a new operator (matrix ops, activation), submit PR
2. **Ruff** — new lint rule or performance optimization
3. **Helix** — LSP feature, keybinding improvement
4. **Qdrant** — vector search algorithm enhancement

### **Study Strategy**

Read code in this order:

1. Clone repo
2. Find the main entry point (`src/main.rs` or lib root)
3. Trace a single user action all the way through (grep the flow)
4. Study error handling and async patterns in that path
5. Rewrite one small module from scratch in your own repo

Don't read "Rust best practices" blogs — read their code. Better signal.

### **If You're Building AI Agents in Rust**

Look at how **Cursor** and **Claude Code** structure tool invocation, then study how Tokio handles concurrency. You'll likely rebuild patterns from:

- `tokio::select!` for multi-tool parallelism
- `serde` for JSON serialization (model standardization)
- `reqwest` for API calls
- `tree-sitter` for code understanding

Pick one of the above and ship something small with it within 2 weeks. That's how you learn Rust at your level — friction through building, not tutorials.
