---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD ROCm Open GPU Compute Platform
translated: false
type: note
---

Here's what this project is:

**AMD ROCm (Radeon Open Compute) -- the official open-source GPU compute platform**

Cloned from: `git@github.com:ROCm/ROCm.git`

It is AMD's counterpart to NVIDIA's CUDA -- an open-source software stack for GPU computation, targeting HPC, AI/ML, scientific computing, and CAD workloads.

**Key components of this repo:**

1. **Documentation** (`docs/`) -- The main ROCm documentation site (Sphinx-based), covering installation guides, API references, compatibility matrices, conceptual overviews, how-to guides, and release notes. This is actually the primary content of this repository.

2. **Build system** (`tools/rocm-build/`) -- 97 shell scripts and configs for building the various ROCm sub-projects from source. These include build scripts for:
   - Math libraries: rocBLAS, rocFFT, rocRAND, rocSOLVER, rocSPARSE, hipBLAS, etc.
   - ML/CV: MIOpen, MIVisionX, AMDMIGraphX
   - Communication: RCCL (collective communication)
   - Compilers/runtimes: HIP, LLVM, ROCclr, HSA runtime
   - Profiling: ROCm Profiler, Omniperf, Omnitrace
   - Docker build environments for Ubuntu 22/24

3. **Repo manifest** (`default.xml`) -- A repo-tool manifest that pins ~30+ sub-projects to `rocm-7.2.0` tags (ROCK kernel driver, HIPIFY, LLVM, ROCgdb, composable kernels, etc.). This is how you'd `repo sync` the full source tree.

4. **CMakeLists.txt** -- A thin CMake wrapper (v5.7.1) that primarily builds the documentation.

5. **CHANGELOG.md** (490KB) -- Detailed release history across all ROCm versions.

**In summary:** This repo is the umbrella/manifest repository for the entire ROCm platform. It doesn't contain the actual runtime or library source code (those live in separate repos like `ROCm/rocm-systems`, `ROCm/llvm-project`, etc.). Instead, it provides: the documentation, the build orchestration scripts, and the repo manifest to assemble all sub-projects into a coherent release.