---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Mini-llama.cpp 里程碑 1 落地
translated: true
type: note
---

一切已完成并推送到 GitHub。下面是完整情况：

## ✅ 里程碑 1 已落地 —— `mini-llama.cpp` 在 M40 机器上跑通了

**仓库 `lzwjava/mini-llama.cpp` 在 `.137` 上** — 已构建、运行、验证、提交、**推送**（`fe030ca` 在 `origin/main` 上）：
- `src/gguf.{h,c}` — 极简 **GGUF v3 reader**（可读取真实的 Qwen2.5 模型）
- `src/gpu_mm.cu` — 面向 M40 的 **sm_52 CUDA kernels + cuBLAS**
- `Makefile` — `make`（CPU stub）+ `make mini-llama-gpu`

```
== GGUF ==  arch=qwen2  name=qwen2.5-0.5b-instruct  v3  tensors=291  kv=26
  vocab = 151936  (token_embd Q5_0, hidden=896)
  real tensor blk.0.attn_norm.weight (F32): GPU y=2x+1  max|err|=0  PASS
  cuBLAS GEMM 512²: 921 GFLOPS  rel err 2.4e-7  PASS
```

**调试之旅（为了学习，这一切都值得）：** value-type 字段是 **u32** 而不是 u8，GGUF v3 **没有 per-tensor KV 存储**，张量偏移量是**相对于对齐后的数据段**（不是绝对位置），而且 cuBLAS 是**列主序（column-major）**（行主序缓冲区需要转置后的参考结果）。已与参考 `gguf` Python 包逐字节比对验证通过。

## Bonus：M40 的故事现在明确了
- ✅ 原生 CUDA `sm_52` + cuBLAS 12.4 跑得很好：**4.3 TFLOPS GEMM @ 4096²**，约 1.4 ms/token 的 row-GEMM
- 之前“GPU 已死”的结论是错的——问题出在 580 驱动上 PyTorch 的 UVM 路径。你自己用 C/CUDA 写的 llama.cpp 才是使用这张卡的正确方式。

## 在 `.137` 上的当前状态

| 项目 | 状态 |
|---|---|
| 500 GB TOSHIBA 磁盘 | ✅ GPT+ext4，挂载在 `/mnt/models`（剩余 435 GB），fstab 持久化，167 MB/s |
| Qwen2.5-0.5B-Instruct q4_K_M GGUF | ✅ `/mnt/models/qwen2.5-0.5b-instruct-q4_k_m.gguf`（491 MB） |
| Git | ✅ 身份已设置，SSH 密钥已生成（你添加后——推送成功了！），仓库已上线 GitHub |

## 下一步（里程碑 2）：在 GPU 上反量化
q4_K/Q5_0/Q8_0 块格式 → 将 fp32 权重上传到 VRAM（24 GB 可以容纳整个 0.5B 模型，fp32 约 2 GB——甚至 7B q4 转成 fp32 约 13 GB）。然后是里程碑 3：真正的前向传播（RMSNorm → RoPE → attention → SiLU MLP）。

要我现在开始 M2（块反量化 + 全量权重上传）吗？