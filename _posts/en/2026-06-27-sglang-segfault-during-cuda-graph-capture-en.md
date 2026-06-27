---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang Segfault During CUDA Graph Capture
translated: false
type: note
---

Question: Why does my SGLang server segfault during CUDA graph capture (FlashInfer backend, Triton compilation), and how do I fix it?

Answer:

The segfault is in Triton JIT compilation, triggered from FlashInfer's `call_begin_forward` during CUDA graph capture. The crash chain is:

```
cuda_graph_runner.capture_one_batch_size
  → flashinfer_backend.init_forward_metadata_capture_cuda_graph
    → update_single_wrapper → call_begin_forward
      → triton jit.run → _do_compile → ast_to_ttir   ← segfault here
```

This is not an OOM (you have a separate, real OOM problem too — see below). The segfault itself is a known **FlashInfer + Triton + CUDA-graph-capture incompatibility**, usually one of: a Triton version mismatch against the FlashInfer kernels SGLang expects, a stale Triton autotune/JIT cache, or FlashInfer's graph-capture path tripping over a Triton codegen bug. The fact that it dies inside `code_generator.__init__` while building the IR (not at runtime) points at the compiler, not your model.

Fixes, in order of effort:

**1. Disable CUDA graph capture (fastest confirmation + workaround):**

```bash
python -m sglang.launch_server --model <MODEL> --disable-cuda-graph
```

If it boots, you've confirmed the capture path is the culprit. You lose graph-replay throughput but the server runs.

**2. Switch attention backend off FlashInfer:**

```bash
python -m sglang.launch_server --model <MODEL> --attention-backend triton
# or
--attention-backend torch_native
```

FlashInfer's capture path is what's invoking the bad Triton compile. The pure-Triton backend avoids `flashinfer_backend.py` entirely.

**3. Nuke the Triton cache (stale cache causes exactly this kind of segfault):**

```bash
rm -rf ~/.triton/cache
```

**4. Align FlashInfer / Triton / SGLang versions.** A segfault inside `triton/compiler/code_generator.py` almost always means the installed `triton` is newer/older than what your `flashinfer` wheel was built against:

```bash
pip show sglang flashinfer-python triton torch | grep -E 'Name|Version'
```

Then match against the versions pinned in your SGLang release's requirements rather than whatever pip resolved.

**Separately — you have a genuine memory problem on this run.** Look at the trace:

```
Load weight end ... avail mem=8.11 GB
KV Cache allocated ... K 3.28 GB + V 3.28 GB
Memory pool end. avail mem=0.97 GB
Capture cuda graph begin ... avail mem=0.39 GB
```

A 3.09 GB safetensors `Qwen2ForCausalLM` (~1.5B in bf16) on what looks like your RTX 4070 12 GB. By the time graph capture starts you're at **0.39 GB free**, and capture needs scratch for the FlashInfer wrappers. Even after you fix the Triton crash, capture may then OOM. Tighten:

```bash
--mem-fraction-static 0.80 \
--max-running-requests 8 \
--cuda-graph-max-bs 4   # you're already only capturing bs [1,2,4,8]
```

Also note `Load weight end. elapsed=945.52 s` — 15+ minutes to load a 3 GB checkpoint means weights are being staged through slow storage or swap; worth checking `dmesg` for OOM-killer / disk thrash, which can itself manifest as a segfault.

Recommended sequence: `rm -rf ~/.triton/cache` → relaunch with `--attention-backend triton --disable-cuda-graph`. If that's stable, re-enable graph capture; if it crashes again, it's the version mismatch in step 4.

If you paste `pip show sglang flashinfer-python triton torch` and the exact launch command, I'll pin the specific version conflict.

References:

- [SGLang server arguments](https://docs.sglang.ai/backend/server_arguments.html)
- [SGLang issues — FlashInfer CUDA graph capture segfaults](https://github.com/sgl-project/sglang/issues)
- [FlashInfer repo](https://github.com/flashinfer-ai/flashinfer)
