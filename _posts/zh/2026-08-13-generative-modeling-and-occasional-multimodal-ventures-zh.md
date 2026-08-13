---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 生成式建模与偶发的多模态探索
translated: true
type: note
---

问：何恺明（MIT/DeepMind）最近在研究什么，尤其是多模态相关的内容？

答：他的实验室自2025年中以来一直专注于生成式建模——主要是扩散/流匹配理论和图像生成，而非经典的多模态（视觉-语言）工作。近期的研究方向如下：

**生成式建模核心（他的主要关注点）**
- "Mean Flows for One-step Generative Modeling"（NeurIPS 2025 口头报告，2025年5月）——通过"平均速度"替代流匹配中的瞬时速度实现单步生成模型。这是后续一系列研究的奠基性论文。
- "Improved Mean Flows: On the Challenges of Fastforward Generative Models"（CVPR 2026 亮点论文）和"One-step Latent-free Image Generation with Pixel Mean Flows"（2026年1月）——将平均流推向像素空间，消除VAE潜在变量依赖。
- "Bidirectional Normalizing Flow: From Data to Noise and Back"（CVPR 2026 亮点论文）
- "Back to Basics: Let Denoising Generative Models Denoise"（CVPR 2026）——与Tianhong Li合作，重新审视扩散模型中花哨技巧的必要性。
- "Is Noise Conditioning Necessary for Denoising Generative Models?"（ICML 2025）
- "Diffuse and Disperse: Image Generation with Representation Regularization"（2025年6月）
- "Fractal Generative Models"（TMLR 2025）、"Autoregressive Image Generation without Vector Quantization"（NeurIPS 2024 亮点论文）——他的MAR系列，连续token自回归图像生成，无需VQ码本。

**最接近"多模态"的工作**
- "Fluid: Scaling Autoregressive Text-to-image Generative Models with Continuous Tokens"（ICLR 2025）——与Yonglong Tian合作的文本到图像自回归缩放。
- "Image Generators are Generalist Vision Learners"（Google DeepMind合作，2026年4月）——这是真正接近多模态的工作。作者名单庞大（Barron、Saining Xie、Soricut等），论证图像生成器本身能学习通用视觉表征。项目页面：vision-banana.github.io。
- "ARC Is a Vision Problem!"（CVPR 2026）——与Jacob Andreas/Yoon Kim（语言领域）合作，将ARC-AGI重新定义为视觉任务——推理基准与视觉之间的有趣桥梁。
- "ELF: Embedded Language Flows"（2026年5月）——与Yoon Kim和Jacob Andreas（MIT NLP）合作的最新成果。这可能是最接近语言+生成融合的工作——将流匹配应用于嵌入式语言场景。

**非生成式相关工作**
- "GeoPT: Scaling Physics Simulation via Lifted Geometric Pre-Training"（2026年2月）——物理模拟预训练，与视觉-语言无关。
- "Transformers without Normalization"（CVPR 2025，与Yann LeCun合作）——用动态tanh替代归一化层。
- "Scaling Proprioceptive-Visual Learning with Heterogeneous Pre-trained Transformers"（NeurIPS 2024）——机器人/视觉领域，若你将其视为多模态亦无不可。

总结：他并未追逐CLIP/LLaVA风格的VLM工作。他在MIT的后续轨迹（2024-2026年）几乎完全聚焦于简化和统一生成式建模理论——平均流、无技巧去噪、无VQ的自回归——其中DeepMind的"通用视觉学习者"论文和新ELF论文才是真正涉及语言/多模态领域的工作。

参考文献：
- [何恺明 — 出版物](https://people.csail.mit.edu/kaiming/publications.html)
- [Mean Flows for One-step Generative Modeling](https://arxiv.org/abs/2505.13447)
- [Image Generators are Generalist Vision Learners](https://arxiv.org/abs/2604.20329)
- [ELF: Embedded Language Flows](https://arxiv.org/abs/2605.10938)
- [ARC Is a Vision Problem!](https://arxiv.org/abs/2511.14761)