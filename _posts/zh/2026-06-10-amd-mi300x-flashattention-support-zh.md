---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD MI300X FlashAttention 支持
translated: true
type: note
---

问题：AMD MI300X 能否使用 FlashAttention 1 或 2？

答案：可以。AMD Instinct MI300X 通过 AMD 的 ROCm 生态系统同时支持 FlashAttention-1 和 FlashAttention-2。但对于你的 FP8/BF16 训练负载，应明确选择 **FlashAttention-2**。

### 支持概览

* **FlashAttention-2（推荐）：** 在使用 ROCm 6.0 及以上版本的 MI300X 上完全支持。它通过两个后端提供优化实现：默认的 Composable Kernel (CK) 后端和替代的 OpenAI Triton 后端。原生支持 `fp16` 和 `bf16` 数据类型。
* **FlashAttention-1：** 历史版本通过早期 ROCm 移植在 MI200 和 MI300 系列上得到支持，但被视为遗留版本，缺乏新实现的性能增强和扩展的 token head 维度。

---

### 你的运行实现细节

由于你通过 `nanochat` 运行训练，可以通过官方仓库安装和配置 FlashAttention-2。

#### 1. 安装

你可以在环境内直接构建与 ROCm 兼容的 FlashAttention-2 版本：

```bash
pip install ninja packaging
git clone --recursive https://github.com/dao-ailab/flash-attention.git
cd flash-attention
# 在 ROCm 上构建将自动检测你的 MI300X 目标
pip install .

```

#### 2. 切换后端

根据你的框架设置，你可以通过切换环境变量来实验哪个后端在 MI300X 上能实现最高的模型 FLOPs 利用率 (MFU)：

* **使用 Composable Kernel 后端（默认）：**
```bash
export FLASH_ATTENTION_TRITON_AMD_ENABLE="FALSE"

```


* **使用 OpenAI Triton 后端：**
```bash
export FLASH_ATTENTION_TRITON_AMD_ENABLE="TRUE"

```



参考文献：

* [Dao-AILab/flash-attention GitHub Repository](https://github.com/dao-ailab/flash-attention)
* [ROCm Model Acceleration Libraries Documentation](https://rocm.docs.amd.com/en/latest/how-to/rocm-for-ai/inference-optimization/model-acceleration-libraries.html)