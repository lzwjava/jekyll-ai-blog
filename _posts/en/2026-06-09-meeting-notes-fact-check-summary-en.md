---
audio: false
generated: true
image: false
lang: en
layout: post
title: Meeting Notes Fact-Check Summary
translated: false
type: note
---

Here's a fact-check of the meeting notes with corrections:

---

Factual Corrections for meeting_01.organized.md

1. "SGLAN" → Should be "SGLang"
   - Appears 7 times in the document. The correct name is SGLang (https://github.com/sgl-project/sglang), developed by LMSYS. It's a high-performance serving framework for LLMs.

2. "VLLM" → Should be "vLLM"
   - The correct casing is vLLM (lowercase v). It's the other major open-source LLM serving framework.

3. "QDA" → Likely meant "CUDA Graph"
   - The entire QDA paragraph describes CUDA Graph functionality (recording CPU→GPU kernel launches, replaying them without CPU involvement). There's no well-known framework called "QDA" that does this. The speaker was likely discussing CUDA Graphs.

4. "GrokQ" → Should be "Groq"
   - The company is Groq (https://groq.com), known for their LPU (Language Processing Unit) custom inference chips. "GrokQ" is not a real entity. (Note: Groq is separate from xAI's Grok model.)

5. "cuBLAS LTE" → Should be "cuBLAS LT" (Light)
   - The correct name is cuBLASLt (cuBLAS Light), a more flexible API on top of cuBLAS. "LTE" is not a thing.

6. SGLang description is inaccurate
   - The notes say SGLang "provides distributed processing optimization, handling multiple devices by pre-processing and isolating each user's memory." This is vague/wrong. SGLang's key innovations are:
     - RadixAttention: prefix caching using radix trees (not just "distributed processing")
     - Compressed finite state machine for structured output (3x faster JSON decoding)
     - Zero-overhead CPU batch scheduler
     - Prefill-decode disaggregation
     - Expert parallelism for MoE models like DeepSeek
   - It's NOT primarily about "user memory isolation" — that's more of a vLLM PagedAttention concern.

7. "Triton is a simplified version of CUDA"
   - Slightly misleading. Triton (by OpenAI) is a DSL (domain-specific language) for writing GPU kernels. It operates at a higher abstraction level than CUDA — you write tile-based operations rather than thread-level code. It can target both NVIDIA and AMD GPUs via LLVM backends. It's not "simplified CUDA" but rather a different programming model.

8. "parameters are generally handled by the CPU, while weights are the GPU's concern"
   - This is an oversimplification. "Weights" and "parameters" are largely synonymous in deep learning (weights are the learnable parameters). The distinction the speaker probably meant: model weights live in GPU VRAM for inference, while the CPU handles control flow, tokenization, and orchestration. Weights include both weight matrices (W) and biases (b), plus embedding tables, LayerNorm parameters, etc.

9. "HBM3 provides 192 GB of VRAM"
   - Only true for the AMD MI300X specifically. HBM3 is a memory standard — different GPUs have different amounts. H100 has 80 GB HBM3, H200 has 141 GB HBM3e. The 192 GB figure is specific to MI300X.

10. "Flash Attention author claimed... 500 tokens per second for DeepSeek V4"
    - No "DeepSeek V4" exists as of early 2026. The latest is DeepSeek-V3/V3.2. The claim about Flash Tri Dao's optimizations rivaling custom chips is directionally correct (he's made such arguments), but the specific model name is wrong.

11. "GrokQ's company may have been acquired by NVIDIA"
    - Groq has NOT been acquired by NVIDIA as of the knowledge cutoff. This appears to be speculation/confusion.

---

The main corrections: SGLAN→SGLang (7x), QDA→CUDA Graph, GrokQ→Groq, cuBLAS LTE→cuBLAS LT, and the SGLang technical description needs rewriting. Want me to patch the file with these fixes?
