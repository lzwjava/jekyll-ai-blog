---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: GPU SM Limit for Max Autotune
translated: false
type: note
---

The warning "Not enough SMs to use max_autotune_gemm" comes from PyTorch's TorchInductor backend (used in `torch.compile` with `mode="max-autotune"` or similar aggressive autotuning modes). It indicates that your GPU has fewer Streaming Multiprocessors (SMs) than the threshold required for the most exhaustive GEMM (matrix multiplication) autotuning options, which search over a huge space of Triton/CUTLASS kernel configurations for peak performance.

PyTorch considers a GPU "big enough" only if it has a substantial number of SMs (typically ≥68–80, depending on the exact PyTorch version; e.g., RTX 3080/3090 borderline, A100/H100/RTX 4090 comfortably above). On smaller GPUs (e.g., RTX 3060, 3070, 2080 Ti, T4, etc.), it disables the full `max_autotune_gemm` path to avoid excessive compilation time or suboptimal choices.

### Why it happens and impact

- Autotuning benchmarks many kernel variants at compile time. Full GEMM autotuning needs enough parallelism (SMs) to make the most aggressive templates worthwhile.
- The warning is **harmless** — compilation still succeeds, and you get good (but not absolute maximum) performance. Other autotuning (non-GEMM parts, less aggressive GEMM search) still runs.
- It does **not** mean padding/inefficiency due to batch size or model architecture in the way you might think. The user's suggested interpretation is close but not quite accurate here — this specific warning is purely about GPU size, not input/shape padding.

### How to improve or work around it

1. **Use a GPU with more SMs** (best fix for true max performance):
   - Recommended minimum for reliable full `max_autotune_gemm`: RTX 4090 (128 SMs), A100 (108 SMs), H100 (132+ SMs), or newer datacenter cards.
   - Consumer cards below ~80 SMs (e.g., RTX 3070 = 46 SMs, RTX 3080 = 68 SMs) will trigger this.

   | GPU example      | SM count | Full max_autotune_gemm? |
   |------------------|----------|--------------------------|
   | RTX 3060/3070    | 46–58   | No                       |
   | RTX 3080/3090    | 68–82   | Borderline (sometimes yes) |
   | RTX 4090         | 128     | Yes                      |
   | A100             | 108     | Yes                      |
   | H100             | 132+    | Yes                      |

2. **Change torch.compile mode** (no hardware change needed):
   - Use `mode="max-autotune-no-cudagraphs"` — keeps most autotuning benefits but skips CUDA graphs and the SM-gated GEMM path. Often nearly as fast with much shorter compile times on smaller GPUs.
   - Or `mode="reduce-overhead"` — lighter, uses CUDA graphs for low latency, good for inference.
   - Example:

     ```python
     compiled_model = torch.compile(model, mode="max-autotune-no-cudagraphs", fullgraph=True)
     ```

3. **Enable high-precision matmuls** (helps any mode/GPU):

   ```python
   torch.set_float32_matmul_precision("high")  # or "highest"
   ```

   This allows TensorFloat-32 / better cuBLAS kernels.

4. **Force more aggressive tuning anyway** (hacky, not officially supported):
   - Monkey-patch the check in PyTorch source (edit `torch/_inductor/utils.py` or runtime patch) to lower the SM threshold. Risky and may hurt performance or explode compile time.

5. **Other general tips for better alignment/efficiency** (unrelated to this exact warning but addresses your padding concern):
   - Pad batch/sequence dimensions to multiples of 8/16/32 if possible (common for Tensor cores).
   - Increase batch size if your workload allows — larger GEMMs utilize the GPU better.
   - For inference-focused workloads, consider alternatives like vLLM, TensorRT-LLM, or Hugging Face Optimum if `torch.compile` limitations persist.

In most real-world cases, the performance difference from missing full `max_autotune_gemm` is small (a few percent), and `max-autotune-no-cudagraphs` gets you 95%+ of the way there on consumer GPUs.

[PyTorch Inductor utils.py source](https://github.com/pytorch/pytorch/blob/main/torch/_inductor/utils.py)
[Torch.compile warning discussion](https://discuss.pytorch.org/t/torch-compile-warning-not-enough-sms-to-use-max-autotune-gemm-mode/184405)
[Dissecting torch.compile](https://themlsurgeon.substack.com/p/dissecting-torchcompile-surgical)
