---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD GPU用于AI：硬件领先，软件滞后
translated: true
type: note
---

**问题：** AMD GPU 与 NVIDIA GPU 在 AI/ML 工作负载上的对比——AMD GPU 的性能大约是 NVIDIA 的 70%70 吗？通过 DigitalOcean 使用的 AMD 开发者云是否是一个好选择？

**回答：**

“答案：**

“70%”这个数字是一个粗略的估算，但实际效果高度取决于你所衡量的指标。以下是详细分析：

## AMD MI300X vs NVIDIA H100 —— 实际数据

| 指标 | AMD MI300X | NVIDIA H100 SXM | AMD 占 NVIDIA 百分比 |
|---|---|---|---|
| FP16 TFLOPS | 1307 | 989 | **132%** ✅ |
| BF16 TFLOPS | 1307 | 989 | **132%** ✅ |
| HBM 内存 | **192 GB** | 80 GB | **240%** ✅ |
| 内存带宽 | 5.3 TB/s | 3.35 TB/s | **158%** ✅ |
| FP8 TFLOPS | 2614 | 1979 | **132%** ✅ |

**从纸面参数看，MI300X 在原始规格上超越了 H100。** 那么，“70%”的感觉从何而来？

## 真正的差距：软件栈

瓶颈在于 **ROCm vs CUDA**：

- **CUDA 生态系统**：超过 15 年的优化积累，cuDNN、cuBLAS、FlashAttention、Triton 等均已经过充分实战考验
- **ROCm**：追赶速度很快，但在内核级优化方面仍落后约 1-2 年
- **PyTorch on ROCm**：可以运行，但自定义 CUDA 内核无法自动移植
- **FlashAttention**：已有 ROCm 移植版本，但历史上性能较慢
- **Triton**：2024 年 AMD 支持显著改善

所以“70%”实际上指的是**软件效率**，而非硬件规格。在原始 FLOPS 上 AMD 获胜或持平。但在实际工作负载的实际训练吞吐量——根据模型不同，大约为 H100 的 70-85%。

## AMD 开发者云（通过 DigitalOcean）

这是 **Instinct MI300X** 的云服务方案。关键事实：

- MI300X 拥有 **192GB HBM3** —— 这对于大型模型推理是一个巨大优势（单卡可容纳全精度的 70B 模型）
- 适合：推理、微调、内存受限的模型
- 注意：代码中的自定义 CUDA 内核需要寻找 ROCm 移植版本
- `torch.compile()` + ROCm 在 PyTorch 2.x 中已有大幅改进

## 针对你的使用场景（训练、微调、智能体）

```bash
# 检查你的技术栈是否兼容 ROCm
pip install torch --index-url https://download.pytorch.org/whl/rocm6.0

# 大多数功能可以直接使用：
# ✅ PyTorch 训练循环
# ✅ HuggingFace Transformers
# ✅ LoRA / PEFT
# ✅ vLLM（已支持 ROCm）
# ⚠️ 自定义 CUDA 内核 → 需要 HIP 移植
# ⚠️ Flash Attention → 使用 `flash-attn` 的 ROCm 分支或 `xformers`
```

## 结论

- **针对 nanoGPT 级别的模型训练**：AMD 完全适用，ROCm + PyTorch 已相当成熟
- **针对 LoRA 微调**：效果良好，HuggingFace 技术栈兼容
- **针对大型模型推理**：MI300X 的 192GB 显存实际上是 **杀手级优势**，超越 H100
- **成本**：通常比 H100 同类产品便宜 30-50%
- **陷阱**：如果遇到与 ROCm 不兼容的操作，调试难度比 CUDA 更高

你提到的渠道听起来是合法的——AMD + DigitalOcean 的合作确实存在。值得针对你的工作负载进行测试。单凭 192GB 显存这一点，就足以让它在本地运行 70B 模型时极具吸引力。