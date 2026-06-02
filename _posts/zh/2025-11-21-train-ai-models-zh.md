---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在12GB显存上训练AI模型
translated: true
type: note
---

以下是一些真正"硬核"的开源项目，你可以在单张RTX 4070（12GB显存）上完整训练（或微调大部分内容）。这些项目非常适合深入理解底层工作原理——远不止运行演示那么简单。

| 项目 | 类型 | 教育意义与硬核特性 | 训练所需显存 | 4070训练耗时 | 链接 |
|------|------|-------------------|----------------|--------------|------|
| Karpathy的**nanoGPT**（经典之作）| LLM（GPT-2风格从零实现）| "极简代码"的黄金标准GPT | 124M模型约10GB | 数小时 | https://github.com/karpathy/nanoGPT |
| Karpathy的**minGPT** | LLM | 更轻量，适合逐行调试 | <6GB | 数分钟至数小时 | https://github.com/karpathy/minGPT |
| Karpathy的**llm.c** | 纯CUDA GPT-2 | 完全用原生CUDA训练GPT-2（无需PyTorch），底层GPU编程的绝佳教材 | 124M模型8-10GB | 莎士比亚数据集1-3天 | https://github.com/karpathy/llm.c |
| OpenLLaMA / LLaMA-Adapter / Lit-GPT（微调）| LLM微调 | 单卡4070使用LoRA/QLoRA微调3B-7B模型 | 7B QLoRA约8-10GB | Alpaca/ShareGPT数小时 | https://github.com/Lightning-AI/lit-gpt |
| Hiero **OpenDiT** / **PixArt-alpha** | 基于DiT的文生图（替代Stable Diffusion的从零训练）| 训练Diffusion Transformer替代U-Net，现代SOTA架构 | 24M DiT梯度检查点约10-11GB | LAION美学子集1-2周 | https://github.com/NVIDIA/OpenDiT |
| **从零实现Stable Diffusion**（轻量版）| U-Net扩散模型 | 多个代码库支持训练轻量版SD（非仅微调）| 64×64轻量SD约6-9GB | 数天 | https://github.com/tea-mang/nano-diffusion, https://github.com/huggingface/diffussions（参考训练示例） |
| **BitNet**（1-bit Transformer）| 1-bit大语言模型 | 微软的1-bit权重模型，可训练BitNet b1.58（类似LLaMA的三元权重）| 3B模型<6GB | 数小时至数天 | https://github.com/microsoft/BitNet |
| **Mamba**（状态空间模型）| Transformer后新一代架构 | 热门的Transformer替代方案，支持从零训练 | 130M-2.8B模型轻松适配 | 数小时 | https://github.com/state-spaces/mamba（含训练脚本） |
| **RWKV**（RNN架构，Transformer级扩展）| Raven / Eagle / Finch模型 | 训练表现如Transformer但显存恒定的循环模型 | 12GB可训练3B-7B分块版本 | 数天 | https://github.com/BlinkDL/RWKV-LM |
| **Grok-1**开源权重复现尝试（340B混合专家）| 从零理解MoE架构 | 虽无法训练完整314B模型，但可训练微型MoE理解路由机制 | 8专家微型MoE约10GB | 数小时 | https://github.com/cg123/mergekit（构建自定义MoE）+ https://github.com/EleutherAI/gpt-neox（MoE代码） |
| **RetNet**（微软Transformer替代方案）| 保留网络 | 另一强效Transformer替代架构 | 与Mamba相近 | | https://github.com/microsoft/torchscale（含RetNet训练） |

### 个人推荐的"最具教育意义且4070可实践"Top 5

1. **llm.c**——用纯C+CUDA训练GPT-2。这是学习反向传播、内核实现、FlashAttention的最佳途径
2. **Mamba**——状态空间模型可能是未来趋势，且代码清晰易懂
3. **BitNet b1.58**——训练1-bit大语言模型令人惊叹，且显存效率极高
4. **OpenDiT / PixArt-alpha**——想要扩散模型但追求现代Transformer骨干网络而非2015版U-Net的最佳选择
5. **RWKV**——击败同规模Transformer的循环架构，训练复杂度线性增长

所有项目均可在单张RTX 4070上流畅运行（部分需配合FlashAttention、bitsandbytes/QLoRA、梯度检查点或RWKV分块技巧）。

选择其中一个深入钻研——你将对模型的理解达到大多数研究者未曾触及的层次。祝探索愉快！
