---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD MI300X 在 llama.cpp 中的支持
translated: true
type: note
---

**问题：** llama.cpp 对 AMD MI300X 的支持好吗？

**回答：**

是的——截至 2025 年底，支持已经相当好，从平庸走向了有竞争力。以下是技术细节：

---

## 后端：HIP (ROCm)，而非 CUDA

llama.cpp 通过其 HIP 后端来调用 MI300X——HIP 是 AMD 的 CUDA 兼容层，可编译到 GCN/CDNA 指令集架构。该框架通过 HIP（异构计算接口，用于可移植性）扩展至 AMD Instinct GPU，例如 MI300X。运行时的关键设备标识符是 `gfx942`（CDNA3 架构）。

---

## 波前大小 bug（现已修复）

这是过去 llama.cpp 在 AMD 上性能不佳的根本原因。早期版本的 llama.cpp 未能在 AMD Instinct GPU 上取得良好性能，主要原因之一是未能利用 AMD GPU 更大的波前大小。具体来说，NVIDIA GPU 的波前大小仅为 32，而 AMD Instinct GPU 的波前大小为 64。早期实现将波前大小硬编码为 32，导致无法充分利用 AMD Instinct GPU 的计算能力。

该修复已于 2025 年 7 月合并到上游。仅此一项，就带来了重大突破。

---

## 2025 年 10 月：为 MoE 添加分组 GEMM

AMD 在 2025 年 10 月的版本中为 llama.cpp 的 hipBLASLt 添加了分组 GEMM API 支持。分组 GEMM 内核允许推理引擎将不同大小、转置和缩放因子的矩阵乘法捆绑到单个内核启动中，相比朴素的批处理 GEMM 循环可带来显著加速，尤其适用于混合专家（MoE）模型这类工作负载。

这直接惠及 DeepSeek-V3、Mixtral、Kimi-K2 等模型。

---

## 基准测试数据（2025 年 12 月，AMD 内部测试）

借助 ROCm 7，AMD Instinct MI300X 系统提供行业领先的吞吐量，在多个模型和配置下超越 NVIDIA H100。AMD Instinct MI300X 8 卡 GPU 在 DeepSeek-V3-671B-Q4_K_M 上，提示长度为 4096 时，推理吞吐量相比 NVIDIA H100 最高提升 76%；在启用闪存注意力（flash attention）的情况下，Meta-Llama-3.1-70B-Instruct-Q4_K_M 的推理吞吐量相比 NVIDIA H100 最高提升 213%。

213% 这个数字在物理上是合理的——MI300X 拥有 192GB HBM3（H100 为 80GB）和约 5.3 TB/s 的峰值带宽，因此在内存带宽受限的推理场景（令牌生成始终如此）中，它应当碾压 H100。

社区实测定点单卡 MI300X（Qwen3-8B Q4_K_M）：

```
pp512  → 5839 t/s
tg128  → 161 t/s
```

单张 MI300X 卡的性能介于 RTX 4090 和 RTX 5090 之间——对于 8 卡配置，由于每卡拥有统一的 192GB HBM3，差距会急剧拉大。

---

## 构建指南

```bash
# 先安装 ROCm 7.x，然后：
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build \
  -DGGML_HIP=ON \
  -DAMDGPU_TARGETS=gfx942 \  # MI300X 目标
  -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j$(nproc)

# 启用闪存注意力运行（对性能至关重要）
./build/bin/llama-bench -m model.gguf -ngl 999 -fa 1
```

AMD 还提供了经过 AMD 验证的 llama.cpp 预编译二进制文件——预先编译好的稳定可执行文件（如 server 和 llama-bench），无需任何编译即可在 Linux 系统上直接运行。

---

## 汇总表

| 特性 | 状态 |
| --- | --- |
| HIP/ROCm 后端 | ✅ 一流支持 |
| 闪存注意力 | ✅ 已支持，推荐启用 |
| 多 GPU（8× MI300X） | ✅ 正常工作 |
| MoE / 分组 GEMM | ✅ 2025 年 10 月及之后 |
| DeepSeek-V3 671B Q4 | ✅ 已基准测试 |
| 预编译 ROCm 二进制文件 | ✅ AMD 提供 |
| 相比 H100 的吞吐量 | ✅ 在大上下文/批量场景下胜出 |

---

**结论：** 如果你能使用 MI300X（例如通过 AMD 开发者云），llama.cpp 是它上面真正的顶级推理栈——不再是二等公民。每卡 192GB HBM 意味着你可以将 70B 以上的模型完全放入显存，并留有长上下文的空间；波前大小和分组 GEMM 的修复确保了计算能力现在得到充分利用。对于大规模生产环境，vLLM+ROCm 是值得比较的替代方案。

**参考文献：**

- [在 AMD Instinct MI300X 上加速 llama.cpp（2025 年 12 月）](https://rocm.blogs.amd.com/ecosystems-and-partners/llama-cpp-oct2025/README.html)
- [Llama.cpp 遇见 Instinct：开源 AI 加速的新时代](https://rocm.blogs.amd.com/ecosystems-and-partners/llama-cpp/README.html)
- [llama.cpp 在 AMD GPU（MI300X）上的性能——GitHub 讨论](https://github.com/ggml-org/llama.cpp/discussions/14640)
- [llama.cpp 预编译二进制文件——ROCm 文档](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/advanced/advancedrad/windows/llm/llamacpp.html)
