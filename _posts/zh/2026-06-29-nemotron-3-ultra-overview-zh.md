---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Nemotron 3 Ultra 概述
translated: true
type: note
---

让我核实一下——"Nemotron 3 Ultra" 的具体规格（550B总参数量/55B活跃参数，混合Transformer-Mamba MoE架构，100万上下文窗口）与我训练数据中的任何信息都不匹配，而且这些数字具体到足以进行核查。  
问：给我介绍一下 NVIDIA Nemotron 3 Ultra。  
答：  

已确认——这是真实的。NVIDIA 于 2026 年 6 月 4 日开源了 **Nemotron 3 Ultra**。以下是技术层面的介绍，比您粘贴的 OpenRouter 简介更深入一层。  

## 它究竟是什么  

一个 **550B 总参数量 / 55B 活跃参数的 MoE**，是 NVIDIA 迄今为止最大的开源模型，专为长时运行智能体（规划、工具调用、多轮推理、深度研究）构建。目前在 Artificial Analysis 智能指数上，它是西方最强的开源权重模型——得分 48，与顶级开源模型的准确率相当，但运行成本低得多。以 NVIDIA 新的开放模型、权重与数据许可证发布，权重、训练配方、代码及大部分数据均已公开。  

## 架构才是亮点  

这 **并非纯 Transformer**。它是一个 **混合 Mamba-Attention MoE**，这也是其吞吐量优势的根源。根据技术报告和模型卡，其模式如下：  

- **Mamba-2 层** 负责大部分序列混合。状态空间模型（SSM）在序列长度上呈 **次二次方** 扩展，并携带固定大小的循环状态，而非不断增长的 KV 缓存。对于百万 token 的智能体上下文，这意味着有界状态与 O(n) 大小、消耗显存的 KV 缓存之间的巨大差异。  
- **稀疏的 Attention 层** 交错分布，用于 **精确召回**——Mamba 的压缩状态在精确检索上是有损的（例如“40万 token 之前的变量名是什么”），因此保留少量 attention 层以恢复“大海捞针”式的精确度。Mamba 以次二次方扩展处理长序列；保留少量 attention 层以在大上下文上实现精确召回。  
- **LatentMoE**——MoE 层在压缩潜在空间中运行（Nemotron 的变体），与 Mamba-2 块交错。  
- **多 token 预测（MTP）层** 用于加速解码并提升质量，与 DeepSeek 风格的 MTP 相同。  

理解模型：Mamba = 廉价的大批量上下文处理，Attention = 昂贵的精确查找，MoE = 稀疏容量，MTP = 解码加速。它与 Jamba/Zamba 属于同一家族思路，但规模达到了前沿级别。  

## 为何快速（对您的智能体管线至关重要）  

在 8K 输入 / 64K 输出的设置下，与 GLM-5.1-754B-A40B、Kimi-K2.6-1T-A32B 和 Qwen-3.5-397B 相比，它的推理吞吐量分别高出 5.9 倍、4.8 倍和 1.6 倍，且准确率相当。正是在长输出场景下，attention KV 缓存成本占据主导——因此 Mamba 层在生成大量内容（推理轨迹、工具调用链）的智能体循环中回报最大。它在对比集中还报告了最高的非幻觉得分，即 AA-Omniscience 上的 78.7 分。  

## 量化 / 部署  

它 **原生以 NVFP4（4 位）进行预训练**，而非事后量化——约 20 万亿 token 的 NVFP4 预训练。发布的检查点混合了 NVFP4 路由专家、FP8 共享专家和 Mamba 线性层，以及 BF16 attention 层——NVIDIA 发现精度在此精度预算以下趋于饱和。实际收益：W4A16 路径可适配单个 8-GPU H100 节点，且有余量容纳 MTP 权重，而 FP8 检查点则需要两个节点。一个 NVFP4 检查点可在 Ampere/Hopper/Blackwell 架构上运行。  

## 后训练  

核心是 **多教师同策略蒸馏（MOPD）**，将 10 余个特化教师蒸馏到一个模型中——然后对合成代码、数学、科学、工具调用、结构化输出和指令数据进行 SFT。  

## 对您的配置而言  

您无法在 4070 或 MI300X 上以全精度（550B）舒适地运行完整模型，但它在两个方面对您有意义：  

1. **通过 GGUF 本地运行**——Unsloth 已将动态量化降至 1 位，磁盘占用 189GB，而 3 位 UD-IQ3_XXS 可适配 256GB 设备。您的 MI300X（192GB HBM3）在激进低比特量化的范围内——这是您唯一可以实际部署它的机器。  
2. **如果您关注 DeepSeek-v4 之后 MoE 的发展方向，这一架构值得研究**。混合 Mamba-Attention + LatentMoE + MTP 堆栈是不同于 DeepSeek 纯 Attention MLA 路线的另一种选择。值得将两份技术报告并排阅读。  

如果需要，我可以从技术报告中提取实际的层模式（Mamba:Attention:MoE 比例）以及头/专家维度，并用约 50 行代码勾勒前向传播，或者设置一次针对免费端点的 OpenRouter 调用，将其与您的 deepseek-v4-flash 基线进行基准测试。  

参考文献：  

- [Nemotron 3 Ultra Technical Report (NVIDIA Research)](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Ultra-Technical-Report.pdf)  
- [NVIDIA Technical Blog — Nemotron 3 Ultra](https://developer.nvidia.com/blog/nvidia-nemotron-3-ultra-powers-faster-more-efficient-reasoning-for-long-running-agents/)  
- [MarkTechPost coverage](https://www.marktechpost.com/2026/06/04/nvidia-ai-releases-nemotron-3-ultra-an-open-550b-mixture-of-experts-hybrid-mamba-transformer-for-long-running-agents/)  
- [NVIDIA build.nvidia.com model card (NVFP4)](https://build.nvidia.com/nvidia/nemotron-3-ultra-550b-a55b/modelcard)  
- [Unsloth — run Nemotron 3 Ultra locally (GGUFs)](https://unsloth.ai/docs/models/nemotron-3-ultra)
