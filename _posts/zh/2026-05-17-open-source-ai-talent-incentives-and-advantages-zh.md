---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源人工智能人才的激励与优势
translated: true
type: note
---

问题：开源AI领域顶尖人才的激励挑战是什么？开源为何仍能胜出？此外，CUDA与AMD的ROCm相比如何？

回答：

## 第一部分：开源人才激励问题——以及它为何仍能胜出

### 核心问题

开源AI中经典的张力是真实存在的：顶尖工程师——那些能编写优化CUDA内核、设计推理调度器或架构分布式系统的人——可以进入NVIDIA、AMD或任何超大规模公司，并获得50万美元以上的总薪酬包。那么，是什么驱使他们去构建或维护开源项目呢？

有多个相互关联的原因使得开源仍能吸引并留住强大的贡献者：

---

### 1. 资助与风险投资成为新薪酬

开源AI基础设施的资助模式已经显著成熟。2023年8月，a16z推出了开源AI资助计划，资助了vLLM核心开发者Woosuk Kwon和Zhuohan Li。在后续批次中，SGLang核心开发者Ying Sheng和Lianmin Zheng也获得了资助。

这随后升级为完整的公司组建。vLLM的创建者筹集了1.5亿美元的种子轮资金，估值为8亿美元，通过一家名为Inferact的新初创公司将该技术商业化。该轮融资由Andreessen Horowitz和Lightspeed Venture Partners联合领投，Sequoia Capital、Altimeter Capital、Redpoint Ventures和ZhenFund参投。

与此同时，Inferact的推出紧随SGLang作为RadixArk的商业化进程，后者在由Accel领投的融资中获得了4亿美元的估值。

这种模式——开源项目 → 风投资助 → 衍生出初创公司——现在是一条经过验证的路径。维护一个开源项目成为你的公开作品集，从而引发投资兴趣。

---

### 2. 面向中级贡献者的AI工具与工具赞助

并非每个人都需要是天才的内核编写者。开源项目已开始有意识地降低中级工程师的贡献门槛。长期活跃的SGLang贡献者可以申请编码代理赞助，例如Cursor、Claude Code或OpenAI Codex。

这是一个巧妙的飞轮：AI辅助开发（Copilot、Claude Code等）让“基础设施初学者”或中级CUDA工程师能够为复杂系统做出有意义的贡献。贡献门槛降低，贡献者基础扩大，核心团队在分布式劳动力上获得更多杠杆。

---

### 3. 企业赞助商派遣其工程师参与开源

vLLM和SGLang都已成为全球首选的推理解决方案，来自Google、Meta、Microsoft、字节跳动、阿里巴巴、腾讯等公司的工程师积极参与其中。

大型科技公司有战略动机进行贡献：他们希望塑造自己依赖的推理基础设施的发展方向。这意味着开源核心维护者实际上获得了一支来自大科技公司的带薪工程师大军——无需支付工资。

---

### 4. 声誉、论文与职业发展轨迹

开源AI基础设施拥有声望飞轮。成为vLLM或SGLang的核心维护者现在比在大公司担任匿名L6级别更能促进职业发展。会议、论文和演讲邀请随之而来。同时孕育了vLLM和SGLang的伯克利天空计算实验室也孕育了Apache Spark和Ray——这些技术如今支撑着全球现代数据基础设施。

---

### 5. “基础设施初学者”民主化效应

一个被低估的动态是：AI辅助编码意味着一位不深入了解CUDA的工程师现在也可以贡献集成、测试、文档、基准测试，甚至中等程度的内核工作。这极大地扩展了开源项目的劳动力池，让5-10人的精英核心团队可以专注于最难的20%问题，而社区处理其余部分。

---

## 第二部分：CUDA 与 AMD ROCm 对比

### CUDA——根深蒂固的霸主

CUDA近二十年的先发优势带来了一个极其成熟的生态系统。数千个库、框架和工具专门为CUDA构建，包括用于深度学习的cuDNN、用于线性代数的cuBLAS以及用于并行算法的Thrust。主要的机器学习框架如TensorFlow、PyTorch和JAX为CUDA提供一流的支持并带有广泛优化。

CUDA拥有超过400万开发者、3000多个优化应用程序，并深度集成到所有主要AI框架中。大学讲授CUDA，研究论文基于CUDA。

转换成本极高。如果每位AI研究人员和工程师都在NVIDIA的堆栈上学习、使用NVIDIA的框架训练模型、针对NVIDIA的架构优化代码，即使竞争对手推出更快的芯片，转换成本也极其高昂。

**关键弱点：** CUDA是专有技术，仅限NVIDIA硬件使用，社区贡献和透明度有限，市场主导地位使其定价较高。

---

### ROCm——AMD的开源反击

最新版本的AMD开源AI软件栈AMD ROCm 7旨在满足生成式AI和高性能计算工作负载日益增长的需求，同时全面改善开发者体验。

ROCm的关键优势在于开放性和可移植性。ROCm由社区驱动且透明，设计为跨AMD GPU架构工作，通常更实惠。

AMD大力确保与流行框架的兼容性。PyTorch官方支持ROCm，TensorFlow可通过ROCm在AMD GPU上运行。HIP（异构计算接口可移植性）工具允许开发者将CUDA代码转换为在AMD硬件上运行，只需极少的更改。

---

### 差距在缩小——但尚未完全消失

在原始硬件方面，AMD现已具备竞争力甚至更优。根据基准测试，AMD的MI355X推理速度比NVIDIA的B200快30%，每美元获得的token数高出约40%。

但软件仍是瓶颈。ROCm与CUDA的生态系统差距是真实存在的，但在堆栈的不同层面上已不再均一。2026年的真实情况是，某些层已基本达到同等水平——对PyTorch、llama.cpp和vLLM的框架支持是最明显的例子。

NVIDIA在2026年占据数据中心GPU收入的86%——较2024年的90%有所下降，因为AMD在推理领域正在取得进展。

---

### 总结表格

| 维度 | CUDA (NVIDIA) | ROCm (AMD) |
|---|---|---|
| 年龄/成熟度 | 约20年 | 约8年 |
| 开发者基础 | 400万+开发者 | 在增长，但规模小得多 |
| 库深度 | cuDNN、TensorRT、NCCL等 | 在改进，仍有差距 |
| 是否开源？ | 否（专有） | 是 |
| 框架支持 | 原生（PyTorch、TF、JAX） | 良好（PyTorch，持续改进） |
| 硬件成本 | 溢价定价 | 每美元产出约多40% token |
| 最适合 | 训练、前沿研发 | 成本优化的推理 |
| 转换成本 | 非常高 | 如果从头开始则较低 |

---

### 战略讽刺

开源AI推理热潮（vLLM、SGLang）讽刺地正在帮助AMD竞争。因为这些框架越来越同时支持CUDA和ROCm，CUDA花了20年建立的生态系统锁定正在被逐步抽象掉。这正是为什么NVIDIA现在投资260亿美元用于开源权重模型——NVIDIA的开源转向与其说是出于利他主义，不如说是生存本能，它认识到仅靠芯片领导地位无法维持一个万亿美元帝国，因为每家主要科技公司都在设计定制芯片。

参考文献：

- [vLLM和SGLang社区故事（Inclusion AI）](https://www.inclusion-ai.org/blog/llm-landscape-vllm-sgl/)
- [Inferact为vLLM商业化筹集1.5亿美元（Fintool）](https://fintool.com/news/inferact-vllm-150m-seed-ai-inference)
- [SGLang GitHub——贡献者赞助](https://github.com/sgl-project/sglang)
- [NVIDIA押注260亿美元押注开源AI（Trending Topics）](https://www.trendingtopics.eu/nvidia-bets-26-billion-on-open-source-ai-to-build-a-new-moat-next-to-cuda/)
- [NVIDIA的开源赌博（TechBuzz AI）](https://www.techbuzz.ai/articles/nvidia-s-open-source-gambit-reveals-cracks-in-chip-dominance)
- [CUDA vs ROCm 2026（GPUnex）](https://www.gpunex.com/blog/nvidia-vs-amd-gpus-2026/)
- [AMD ROCm vs CUDA本地AI 2026（Kunal Ganglani）](https://www.kunalganglani.com/blog/amd-rocm-vs-cuda-local-ai-open-source-guide)
- [AMD推进AI 2025公告](https://www.amd.com/en/newsroom/press-releases/2025-6-12-amd-unveils-vision-for-an-open-ai-ecosystem-detai.html)
