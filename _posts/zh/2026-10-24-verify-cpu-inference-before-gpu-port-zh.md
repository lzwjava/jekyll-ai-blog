---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 GPU 移植前验证 CPU 推理
translated: true
type: note
---

以下是当前进展和推荐的推进路径：

## 当前状态

- ✅ M1–M3 全部已提交：GGUF 读取器 → GPU GEMM/dequant (M2) → **CPU Qwen2 推理** (M3，刚刚推送)
- ⚠️ M3 代码是全新的，**从未实际构建/运行** —— 已提交但未经验证
- 机器情况：**Tesla M40 24GB**（sm_52，cuBLAS 已在 M2 中验证），GitHub ✅，`hf-mirror.com` ✅，`huggingface.co` ❌（被屏蔽）

## 推荐下一步：**在真实模型上端到端构建并验证 M3**

其他所有工作（GPU 移植、优化）都取决于确认 CPU 路径确实能生成合理的 token。具体计划：

1. **配置构建** —— 在 Makefile 中添加 `mini-llama-m3` 目标（`cc … m3_cpu.c gguf.c quant.c qwen2.c tokenizer.c -lm`）。仅 CPU，避免慢速的 `nvcc` M2 构建。同时清理两个警告（`quant.c:105` 缩进、未使用的 `buf` 参数）。
2. **获取一个小模型** —— 从 `hf-mirror.com` 获取 `Qwen/Qwen2.5-0.5B-Instruct-GGUF` **Q8_0**（约 530MB）（HF 直连被屏蔽；你有 17G 可用空间）。
3. **运行并验证** —— `./mini-llama-m3 model.gguf "The capital of France is" 32`。检查：tokenizer id 是否正确、top-5 logits 是否为有限值、tok/s 是否合理、输出是否可读。机器上已有 `~/llama.cpp` → 以参考 llama.cpp 的 logits/tokens 作为 ground truth 进行对比。
4. **修复出现的问题** —— 可能的候选点：tokenizer merge-rank 处理、RMSNorm dtype 边界情况、或 KV-cache 索引。

## 然后 M4（这之后真正的里程碑）

将经过验证的 CPU 前向传播移植到 M40 上的 CUDA —— M2 中的 dequant/GEMM 工作已经证明了内核的正确性（误差 5.6e-6），因此 M4 就是将 `qwen2_forward_token` 接入 `m2.cu` 并添加 GPU KV cache。

**要我现在执行第 1–3 步吗？** 我会配置 Makefile，通过 hf-mirror 拉取 Q8_0 模型，构建并运行首次推理测试。
