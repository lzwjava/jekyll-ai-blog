---
audio: false
generated: true
image: false
lang: en
layout: post
title: "LFortran: Interactive Fortran Compiler"
translated: false
type: note
---

**Question:** What is LFortran?

**Answer:**

LFortran is a modern, open-source (BSD licensed), interactive Fortran compiler built on top of LLVM. It supports two modes: interactive/REPL execution (like Python or Julia) and AOT compilation targeting modern architectures including multi-core CPUs and GPUs.

**Why it matters architecturally:**

The stack is: Fortran source → LFortran frontend (C++) → **ASR** (Abstract Semantic Representation, their custom IR) → LLVM IR → native binary or WASM. The ASR layer is interesting — it's a typed, semantics-rich IR that sits between the parse tree and LLVM IR, making it easier to do analysis and optimization passes.

**Key facts:**

- Written ~67% C++, ~22% Fortran, ~5% Python
- Supports Jupyter kernels (interactive notebooks for Fortran)
- Can compile to WASM (`build_to_wasm.sh`)
- Has a `CLAUDE.md` and `AGENTS.md` in the repo — meaning they're actively integrating AI coding assistants
- v0.61.0 released March 2026, actively developed (25k+ commits)
- Backed by NumFOCUS (same org as NumPy, pandas, etc.)

**Why Fortran in 2026?** Scientific computing and HPC — weather modeling, plasma physics, numerical linear algebra. A lot of legacy Fortran code underpins critical scientific infrastructure, and there's no modern interactive compiler for it. LFortran is essentially trying to be to Fortran what Julia is to scientific Python — fast, compiled, but with a REPL.

**Connection to your world:** Given your MI300X work and GPU compute interests, the GPU compilation target is the most relevant angle. LFortran aims to compile Fortran directly to GPU backends via LLVM, which matters for porting legacy HPC codes to AMD/NVIDIA hardware without rewriting in CUDA/HIP.

**References:**

- [LFortran GitHub](https://github.com/lfortran/lfortran)
- [LFortran Docs](https://docs.lfortran.org/)
- [Try Online](https://dev.lfortran.org/)
