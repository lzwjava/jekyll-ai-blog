---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek-V4-Pro Architecture and Code Overview
translated: false
type: note
---

Here's the full breakdown:

## DeepSeek-V4-Pro Inference Code

Location: ~/projects/deepseek-v4-inference/

### Architecture (from config.json)

DeepSeek-V4-Pro is a massive Mixture-of-Experts model:
- 129,280 vocab, 7168 hidden dim, 61 layers
- 384 routed experts, 1 shared expert, 6 activated per token
- 128 attention heads, 512 head dim (with 64-dim RoPE component)
- Low-rank Q projection: q_lora_rank=1536
- Low-rank O projection: o_lora_rank=1024, 16 groups
- Sliding window attention (128 tokens) + KV compression (various ratios per layer)
- Scoring: sqrtsoftplus with route_scale=2.5
- Default quantization: FP8 weights + FP4 experts (UE8M0 scale format)
- YaRN-scaled RoPE for long context (original_seq_len=65536)

### File-by-File

**model.py** (38K, 827 lines) — the core:
- `ModelArgs` dataclass: all hyperparameters
- `ParallelEmbedding`: vocab-sharded embedding with all-reduce
- `Linear` / `ColumnParallelLinear` / `RowParallelLinear`: supports BF16, FP8, FP4 weight formats with per-block scaling
- `RMSNorm`: standard, stored in fp32 for precision
- `precompute_freqs_cis`: YaRN-scaled rotary embeddings
- `Compressor`: learned gated pooling to compress KV cache (ratio 4 or 128). Handles both prefill and incremental decode. Overlapping windows for ratio==4
- `Indexer`: selects top-k compressed KV positions via learned scoring with its own Compressor (uses Hadamard-rotated FP4 quantization)
- `Attention`: Multi-head Latent Attention (MLA) — low-rank Q (wq_a -> q_norm -> wq_b), sliding window + compressed KV, grouped low-rank O projection (wo_a -> wo_b), learnable attn_sink bias
- `FFNSwiGLU`: standard SwiGLU with optional swiglu_limit clamping
- `MOE`: top-k routing with sqrtsoftplus scoring, shared expert, e_score_correction_bias
- `TransformerBlock`: layer types controlled by `compress_ratios` — hash layers (compression ratio 128) use HC attention, others use standard MLA + MoE
- `HCAttention`: Hash Compress attention — new mechanism with multi-head compress routing via Sinkhorn normalization
- `Transformer`: full model with `ParallelEmbedding`, layers, `RMSNorm`, `lm_head`, KV cache management

**kernel.py** (22K, 536 lines) — tilelang JIT kernels:
- `act_quant_kernel`: block-wise FP8 quantization (block_size=128), optional in-place quant-dequant
- `fp4_quant_kernel`: block-wise FP4 quantization (block_size=32), power-of-2 scales
- `fp8_gemm_kernel`: FP8 matmul with per-block A/B scaling, L2 swizzle, 4-stage pipeline
- `fp4_gemm_kernel`: FP8 activation x FP4 weight GEMM — loads FP4, casts to FP8, applies separate act (128) and weight (32) scales
- `sparse_attn_kernel`: FlashAttention-style online softmax with index-gathered top-k KV, learnable attn_sink
- `hc_split_sinkhorn_kernel`: Sinkhorn normalization for HC (Hash Compress) routing — iteratively normalizes row/col of a combination matrix

**generate.py** (6.1K, 155 lines) — entry point:
- `sample()`: Gumbel-max trick (faster than multinomial on GPU, avoids CPU sync)
- `generate()`: batch generation with left-padding, prefill+decode phases
- Interactive mode: chat loop with `/exit` and `/clear` commands
- Batch mode: reads prompts separated by blank lines
- Multi-node via torchrun with NCCL
- Uses `encode_messages` / `parse_message_from_completion_text` from an external `encoding` module (not included — ../encoding/encoding_dsv4.py)

**convert.py** (6.9K, 168 lines) — weight conversion:
- Converts HuggingFace safetensors to model-parallel shards
- Maps HF weight names to internal names (e.g., self_attn -> attn, mlp -> ffn)
- Handles FP4->FP8 lossless conversion (e2m1fn to e4m3fn) with careful scale handling
- Supports expert_dtype fp8 or fp4
- Shards by expert index for MoE, by dimension for embeddings/projections
- Copies tokenizer files alongside weights

**requirements.txt**:
- torch>=2.10.0, transformers>=5.0.0, safetensors>=0.7.0
- fast_hadamard_transform (for rotate_activation in Indexer)
- tilelang==0.1.8 (JIT kernel compiler for quantization + attention kernels)

### What's Missing

The `../encoding/` directory with `encoding_dsv4.py` is not included — it handles chat template encoding/parsing. You'd need that from the full repo for interactive mode to work.

### Hardware Requirements

With FP8+FP4 quantization and 384 experts, this model is enormous. The default config expects 8-way model parallelism (MP=8). Your RTX 4070 (12 GB) won't fit even one shard. The MI300X (192 GB HBM3) on AMD Dev Cloud could handle it — likely needs 1-2 MI300X cards depending on batch size.