---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 腾讯混元推理引擎概述
translated: true
type: note
---

**问题：** 腾讯混元是什么？请介绍该模型系列，并说明其推理引擎在 NVIDIA H20 和 Blackwell (B200) GPU 上的性能优化情况。

---

## 答案：腾讯混元 — 概述与推理引擎深度解析

---

### 什么是混元？

腾讯开发了混元作为其大型语言模型系列，为旗下产品中的对话式 AI 和内容生成提供支持。它并非单一模型，而是一个完整的技术栈：涵盖大语言模型、图像生成、视频生成、3D、OCR 以及智能体。可以将其视为腾讯对标 OpenAI 和 Google 正在构建的技术体系，但深度集成于微信、QQ 和腾讯云之中。

混元大语言模型覆盖文本到文本、文本到图像、文本到视频以及多模态理解。

---

### 模型系列（当前状态，2025 年中）

**Hunyuan-Large (Hunyuan-MoE)** — 最初的开源旗舰版本。旗舰模型 Hunyuan-Large (Hunyuan-MoE-A52B) 拥有 3890 亿总参数，其中 520 亿参数被激活，是一款领先的开源 Transformer 架构 MoE 模型。

**Hunyuan-TurboS** — 架构上最具创新性的模型。该模型于 2025 年 2 月 27 日发布，采用 Hybrid-Mamba-Transformer 融合模式，有效降低了传统 Transformer 架构的计算复杂度与 KV-Cache 占用，显著减少了训练和推理成本。

架构细节：TurboS 结合了 57 个 Mamba2 层、7 个 Attention 层和 64 个前馈神经网络层，按“AMF”和“MF”区块模式策略性排列。KV cache 和 FFN 采用 MoE 结构。基于 16T 高质量 token 进行预训练，支持 256K 上下文长度，是业界首个大规模部署的 Mamba 模型。

这一点意义重大：Mamba 层的线性复杂度（O(N) vs O(N²)）意味着长上下文推理的计算成本根本性降低。保留了 7 个 Attention 层，用于在 Mamba 递归能力不足时捕获全局上下文。

**Hunyuan-T1** — 推理模型（慢思考）。Hunyuan-T1 正式版基于 TurboS 快思维基础模型，腾讯将其描述为全球首个超大规模 Hybrid-Transformer-Mamba MoE 模型。通过大规模后训练，其推理能力得到显著扩展。

**Hunyuan-A13B** — 高效开源版本。Hunyuan-A13B 模型拥有 800 亿总参数，其中 130 亿参数被激活，支持最大 256K token 的上下文长度。

**Hunyuan 2.0** （2025 年 12 月）：基于 MoE 架构，总参数 4060 亿，激活参数 320 亿，支持 256K 上下文窗口，在预训练数据和数学、科学、编程等领域的 RL 策略上有所改进。

Chatbot Arena 排名：在 Chatbot Arena 上，Hunyuan TurboS 已跻身全球前八，在中国仅次于 DeepSeek。

---

### 推理引擎 — 他们的构建方案

腾讯在 GTC 2025 上介绍了使用 TensorRT-LLM 为混元构建高性能推理引擎的方案。根据 GitHub 和 GTC 资料，关键优化包括：

#### 1. **CLA（跨层注意力）实现 KV-Cache 压缩**
引入新的 CLA 结构显著降低了 GPU 内存使用，KV-Cache 部分节省达 50%，从而确保高效处理长文本场景。这对大规模 MoE 模型至关重要——在高批处理量下，KV cache 往往是内存瓶颈。

#### 2. **FP8 量化**
采用 FP8 量化，相比传统的 FP16/BF16 量化，内存使用减少 50%，同时保持精度，吞吐量提升 70%。

#### 3. **TRT-LLM 对比 vLLM**
通过利用 TRT-LLM 核心的高效算子，TRT-LLM 方案的性能超过 vLLM 30% 以上。TRT-LLM 是他们的生产环境默认方案；他们最初开源了 vLLM 路径。

#### 4. **CUDA Graph 优化**
从部署配置来看：
```yaml
use_cuda_graph: true
cuda_graph_padding_enabled: true
cuda_graph_batch_sizes: [1, 2, 4, 8, 16, 32]
```
这消除了 CPU-GPU 启动开销——对于小批处理量下的延迟至关重要。

#### 5. **训练并行技术栈（AngelPTM / AngelRL）**
在训练方面，他们全面集成了所有模型并行技术，包括张量并行（TP）、流水线并行（PP）、专家并行（EP）、上下文并行（CP）以及序列拼接优化，以提升效率。推理框架称为 **AngelHCF**。

---

### H20 对比 B200 — GPU 平台背景

**H20** 是 NVIDIA 符合中国出口规定的芯片（阉割版 Hopper）。Hunyuan-Large 明确在 H20 上进行了测试——在 H20 上，LoRA 微调需要至少 8 张 GPU。它是目前中国数据中心内主流的推理 GPU。

对于更广泛的 **Blackwell B200**：NVIDIA Blackwell B200 每百万 token 的成本从发布时的 0.11 美元降至两个月后 GPT-OSS-120B 上的 0.02 美元——仅凭软件优化就实现了 5 倍提升。

在分离式服务（预填充/解码分离）方面，腾讯的大规模部署受益于此：NVIDIA 的分离式服务相比在 DGX B200 系统上使用动态批处理的传统聚合服务，每 GPU 吞吐量提升近 1.5 倍——相比在 DGX H200 系统上使用动态批处理，累计提升超过 5 倍。

Blackwell FP4 支持是下一个前沿。Blackwell 架构支持高级精度模式（FP8、FP4），B200 和 B300 在 TF32、FP16 和 FP8 下的吞吐量相比上一代 H200 提升超过 2 倍。它还配备了一个支持 FP4 的新型 Transformer 引擎。

---

### “Hunyuan 3.0”的定位

注意：根据我的搜索，“Hunyuan 3.0”这一术语未出现在公开文档中——它可能指代 **Hunyuan 2.0**（2025 年 12 月）作为当前版本，或者是尚未公开的内部版本号。推理引擎的工作主要围绕 **TensorRT-LLM + AngelHCF**，上述优化技术栈是生产环境基线。

---

### 给你的总结

腾讯做出的有趣工程选择：
- **Mamba + MoE 混合**是真正的架构押注——大规模下的线性复杂度，Mamba 在 100B+ MoE 中的首次实际部署。值得研读 TurboS 论文：[arxiv 2505.15431](https://arxiv.org/abs/2505.15431)
- **CLA（跨层注意力）**用于 KV cache 缩减——与 GQA/MQA 方向相同但结构不同
- **FP8 量化**作为标准基线，Blackwell 上即将推出 FP4
- **分离式服务**（预填充/解码分离）是大规模吞吐量提升的真正来源
- **AngelHCF** 是腾讯在 TRT-LLM 之上构建的内部推理框架——尚未完全开源，但 GTC 2025 的演示文稿涵盖了其架构

参考文献：
- [Tencent-Hunyuan-Large GitHub](https://github.com/Tencent-Hunyuan/Tencent-Hunyuan-Large)
- [Hunyuan-TurboS 论文 (arxiv 2505.15431)](https://arxiv.org/abs/2505.15431)
- [Hunyuan-TurboS GitHub](https://github.com/Tencent-Hunyuan/Hunyuan-TurboS)
- [GTC 2025 会议：腾讯混元推理引擎](https://www.nvidia.com/en-us/on-demand/session/gtc25-S71563/)
- [NVIDIA Blackwell 推理记录 (MLPerf)](https://developer.nvidia.com/blog/nvidia-blackwell-ultra-sets-new-inference-records-in-mlperf-debut/)
- [HuggingFace 上的 Hunyuan-A13B](https://huggingface.co/tencent/Hunyuan-A13B-Instruct)