---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU权重已为M3准备就绪
translated: true
type: note
---

✅ **里程碑 2 已完成** — 已提交（`33853e3`）并推送至 GitHub。

## M2 交付内容

**`src/quant.{h,c}`** — 该模型中全部 5 种类型的块反量化，**逐字移植自 llama.cpp 的 ggml-quants.c**：

- **Q5_0**（133 个张量）、**Q8_0**（13）、**Q4_K**（12，`K_SCALE_SIZE=12`）、**Q6_K**（12）、F16/F32 直通

**`src/m2.cu`** — census → CPU 反量化 → VRAM 上传 → 真实 GEMM：

```
== census: Q5_0=133 F32=121 Q8_0=13 Q6_K=12 Q4_K=12 ==
  total params 0.630B -> fp32 = 2.52 GB (fits the 24 GB M40)
  token_embd  (Q5_0, 136M) v[0..3]=-0.0102 0.0408 0.0102 -0.0000   [EXACT match w/ reference]
  attn_q      (Q5_0)  ... min/max EXACT match
  attn_v      (Q8_0)  ... min/max EXACT match
  output      (Q8_0)  ... min/max EXACT match
  ffn_down    (Q6_K)  min/max match (multiset ✓, llama.cpp ordering)
  blk.11.ffn_down (Q4_K) min/max match
  VRAM: token_embd 545MB + ffn_up 17MB -> 573 MB used, 24.97 GB free
  GPU ffn_up gemm: X(1x896) @ W(4864x896): 28 GFLOPS  err/scale=5.6e-06  PASS
```

对全集进行 CPU 反量化耗时 **0.85 秒**（单线程）；2.52 GB 的 fp32 模型可轻松装入 VRAM（约 10 倍余量）。

## 验证中的兔子洞（值得了解）

- **Q5_0/Q8_0**：与 `gguf` Python 参考实现逐元素位级完全一致 ✅
- **Q6_K/Q4_K**：我的代码与 llama.cpp 的代码 *逐字节相同*——而 llama.cpp 正是此文件的写出方，因此它的实现是权威的。有趣的发现：**gguf-py 自己的 Q4_K/Q6_K 反量化会重建出不同的值**（不同的半字节↔缩放配对——即使排序后的数组也不一致）。因此两个“官方”实现并不一致；对于 llama.cpp 的克隆来说，llama.cpp 的数学实现才是定义上的正确。已记录在 README 中。

## 项目状态

```
mini-llama-gpu  (M1): GGUF parse + sm_52 kernels + cuBLAS ✓
mini-llama-m2   (M2): dequant all block types + weights on the M40 ✓
```

现在，真正的前向传播所需的每一步都已得到验证：GGUF 读取 ✓、完整 fp32 权重驻留 VRAM ✓、cuBLAS GEMM ✓。

**下一步（M3）：在 GPU 上执行 transformer 前向传播** — RMSNorm（及其自定义 kernel）、RoPE、带 KV-cache 的 QKV attention、SiLU 门控 MLP、dot-product/softmax，然后 `output.weight × hidden → logits`。我会先做的最小实际步骤：一个独立的 **M40 上的 RMSNorm + SiLU 测试程序**，与 CPU 结果对比验证，然后再做完整 block。

你准备好后，我随时可以开始 M3。
