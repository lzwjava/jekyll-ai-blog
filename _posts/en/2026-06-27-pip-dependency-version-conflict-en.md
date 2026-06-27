---
audio: false
generated: true
image: false
lang: en
layout: post
title: Pip Dependency Version Conflict
translated: false
type: note
---

Because `torch 2.11.0` or `sglang` likely declares a dependency constraint like `triton>=3.5`. When you run `pip install triton==3.4.0` normally, pip checks all installed packages' constraints and either:

1. **Refuses** the downgrade (conflict error)
2. **Accepts** it but later gets upgraded back when pip resolves dependencies (which is what happened — it went back to 3.6.0)

`--no-deps` tells pip: "install exactly this version, don't check or install any dependencies." It forces the pin.

But honestly, even `--no-deps` might not hold — torch could load-triton-at-runtime and version-check it. vLLM is the cleaner path here.
