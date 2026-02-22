---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Cerebras 巨型芯片重新定义 AI 速度
translated: true
type: note
---

Cerebras Systems 已崭露头角，成为人工智能硬件领域最具特色且强大的竞争者之一，以一种截然不同的方法挑战 Nvidia 的主导地位：wafer-scale engine。与将数千个小型处理器拼凑在一起不同，Cerebras 制造了一块餐盘大小的巨型芯片，专为使 AI inference——即将实时数据通过模型运行的过程——瞬间完成而设计。

这份全面介绍探讨了 Cerebras 的独特之处、其开创性技术、向 inference 的战略转向，以及其在快速演变的 AI 格局中的位置。

### 🚀 什么是 Cerebras？新一代 AI 计算机

Cerebras Systems 由一群开创性的计算机架构师和深度学习研究员于 2016 年创立，旨在解决一个根本问题：现有的计算机芯片并非为现代 AI 的需求而设计。他们的解决方案是构建一种全新的计算机类别，将 AI 工作加速到超越现有技术的数个数量级。

其核心是，Cerebras 是一家 AI 硬件公司，设计并构建全栈计算解决方案。这包括：
*   **Wafer-Scale Engine (WSE)：** 其革命性的巨型芯片。
*   **CS Systems (CS-2, CS-3)：** 配备 WSE 的交钥匙 AI 超级计算机，包含定制冷却、电源和网络。
*   **Cerebras Cloud：** 一项云服务，允许客户远程访问 Cerebras 硬件的强大性能，用于 training 和关键的 inference。

公司于 2019 年达到“unicorn”地位（估值超过 10 亿美元）。截至 2025 年 10 月的最新 Series G 融资轮次，Cerebras 以 **81 亿美元** 的估值融资 11 亿美元。该轮融资由 Fidelity 等主要投资者领投，表明市场对其技术和战略的强烈信心。

### 💡 魔法所在：Wafer-Scale Engine (WSE) 技术

要理解 Cerebras，首先要理解其芯片。传统处理器，包括 Nvidia 的 GPUs，都是通过将大块硅晶圆切割成数百个微小芯片（dies）制成。Cerebras 则反其道而行之：保持晶圆完整，创建单一的巨型处理器。

这种看似简单的颠倒带来了深刻的性能影响，尤其是在 inference 方面。

#### 为什么 GPU Inference 感觉缓慢
大型语言模型 (LLMs) 如 Llama 3.1 70B 需要将整个模型——整整 140GB——从内存移动到计算核心，用于它生成的 *每一个单词*（token）。GPUs 的片上快速内存非常有限（仅约 200MB）。这迫使它们不断从较慢的外部内存获取数据，造成瓶颈从而限制速度。一块 H100 GPU 具有 3.3 TB/s 的内存带宽，足以进行缓慢的 inference，但要实现瞬间速度则需要超过 140 TB/s。

#### Cerebras 解决方案：片上内存
WSE 完全消除了这一瓶颈。
*   **海量片上内存：** 最新的 WSE-3 在芯片上集成了 **44GB 高速度 SRAM**。这足以在几块芯片上容纳整个 Llama 70B 等模型，无需访问缓慢的外部内存。
*   **无与伦比的内存带宽：** 因为内存位于芯片上，通往计算核心的路径极短且宽阔。WSE-3 拥有 **21 PB/s** 的总内存带宽，大约是 H100 GPU 的 7000 倍。
*   **海量计算能力：** WSE-3 基于 5nm 工艺，集成了惊人的 **4 万亿晶体管** 和超过 **90 万个 AI 优化核心**。相比之下，一块 Nvidia H100 约有 800 亿晶体管和 18,688 个核心。

这种设计意味着 LLM 可以完全存储在处理器上，其所有参数都能以闪电般的速度访问，从而实现每秒生成数千个 tokens。

### ⚡ Cerebras Inference：速度即服务

虽然 Cerebras 硬件也用于 training，但公司当前的重点和最近的成功主要集中在 **Inference Cloud** 上。该平台于 2024 年 8 月推出，通过简单 API 向开发者提供其独特硬件。

价值主张很简单：无与伦比的速度和准确性。
*   **行业领先性能：** Cerebras 声称其 inference 是世界上最快的，对于较小模型可达 **2000+ tokens/秒**，对于 Llama 3.1 70B 等巨型模型达 450 tokens/秒——比基于 GPU 的超大规模云快 **高达 20 倍**。
*   **全精度准确性：** 与一些竞争对手使用低精度 8-bit 权重来提升速度不同，Cerebras 使用模型创建者（如 Meta）发布的原始 **16-bit 权重**。这确保了最高可能的准确性，对于 reasoning 和多轮对话等复杂任务至关重要。
*   **实时推理：** 这种速度开启了新一代应用。像 Alibaba 的 Qwen3-32B 等高级“reasoning models” 以前需要 30-90 秒“思考”，现在在 Cerebras 硬件上只需 **1.2 秒** 即可返回答案。这首次使复杂的 AI agents 和 copilots 真正实现交互。

对于开发者，Cerebras Inference API 使用熟悉的 **OpenAI-compatible 格式**，只需更改几行代码即可切换到更快的服务。该平台支持不断增长的热门开源模型，包括各种 Llama、Qwen 和 Mistral 模型。

### 🏢 商业策略与市场定位

Cerebras 正积极定位自己为高速 inference 的首选提供商，直接挑战 Nvidia 和主要云提供商的 GPU 中心基础设施。

#### 商业模式
Cerebras 通过两大主要渠道产生收入：
1.  **系统销售：** 直接向政府、国家实验室（如 Argonne）、研究机构以及大型企业（如 GSK 和 Mayo Clinic）销售 CS-3 系统，用于本地部署。
2.  **云服务：** 通过 Cerebras Inference Cloud 提供硬件访问，为希望按需付费的开发者和企业创造 recurring revenue。

#### 关键合作伙伴和客户
公司策略正获得有影响力的合作伙伴认可：
*   **OpenAI (2026 年 1 月)：** 在一项里程碑式交易中，OpenAI 宣布与 Cerebras 合作，在未来几年将其平台整合 **750 兆瓦低延迟 AI 计算**。这是全球领先 AI 公司对 Cerebras 技术的巨大认可，旨在使 OpenAI 的模型响应更快。
*   **Hugging Face：** 与 Hugging Face 的交易使 Cerebras inference 可一键访问该平台的数百万开发者，这是一次重要的营销胜利。
*   **Perplexity AI 和 Mistral：** 这些领先 AI 公司也在使用 Cerebras 满足其 inference 需求。
*   **Sovereign AI：** Cerebras 推出专属“Cerebras for Nations”计划，为寻求 sovereign compute 能力的国家提供交钥匙 AI 基础设施，据报道计划在阿联酋的 Stargate AI 中心进行大规模部署。

#### 竞争格局
Cerebras 的主要竞争对手是 **Nvidia**，其 GPUs 和 CUDA 软件生态是行业标准。其他竞争对手包括 **AMD** 以及拥有定制硅的云提供商，如 **AWS (Trainium/Inferentia)** 和 **Google (TPU)**。然而，Cerebras 的 wafer-scale 架构使其在超低延迟 inference 的特定高价值细分市场中具有独特优势。

### 📈 最近发展与未来展望

Cerebras 正处于快速扩张和战略演变的阶段。
*   **巨额融资：** 2025 年 10 月的 11 亿美元 Series G 轮融资用于扩展制造并通过新数据中心规模化其 inference 云。
*   **数据中心扩张：** 公司计划在北美和欧洲运营多达 15 个 AI 数据中心，专攻高速 inference。
*   **IPO 暂缓：** 尽管 2024 年提交 IPO 文件，但 Series G 融资后 Cerebras 撤回了计划，表明在回归公开市场前专注于长期私人增长。
*   **收入增长：** 公司处于快速规模化阶段，收入从 2023 年的 7870 万美元增长到 2024 年中期的超过 2 亿美元年化收入。

### 🏁 结论

Cerebras 不仅仅是另一家 AI 芯片初创公司。通过大胆重新思考处理器的基本设计，它构建了一台专为 AI 未来而生的机器——一个模型不仅仅生成文本，而是实时 reasoning、规划并与用户互动的未来。其与 OpenAI 的开创性合作巩固了其地位，不再是遥远的挑战者，而是下一代 AI 的关键基础设施提供商。对于寻求市场上最快 inference 的开发者和企业，Cerebras 已让自己不可忽视。

您是感兴趣尝试其 API 的开发者，还是更好奇 WSE-3 芯片的技术规格？