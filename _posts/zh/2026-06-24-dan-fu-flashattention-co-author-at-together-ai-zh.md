---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'Dan Fu: Together AI的FlashAttention合著者'
translated: true
type: note
---

**问题：** 谁是 Together AI 内核副总裁 Dan Fu？

**答案：**

Dan Fu 本质上是 Tri Dao 的密切合作伙伴，负责运营 Together AI 的底层 GPU 工程。以下是详细介绍：

**他是谁：**

加州大学圣地亚哥分校（CSE 系）助理教授，领导 SandyResearch 实验室，同时担任 Together AI 内核副总裁——正在组建一支专注于底层性能工程和 GPU 内核的世界级团队。

他的研究方向是为机器学习开发高效算法，重点关注那些在理论上高效且在现代硬件上实际运行快速的解决方案。

**他的主要工作：**

- 与 Tri Dao（斯坦福博士，同为 Chris Ré 指导）合著 **FlashAttention**
- **H3** — 一种混合 SSM/注意力架构（仅含 2 个注意力层，ICLR 2023 亮点论文，与 Tri Dao 合著）
- **ThunderKittens** — 一个用于快速 GPU 内核开发的库。在获得 NVIDIA Blackwell GPU 访问权限后的一周内，他的团队就发布了当时最快的 FP4 和 FP8 GEMM 内核之一，在 H100 上相比 cuBLAS 实现了高达 2 倍的加速。

**他的运作模式：**

Dan Fu 在 UCSD 运营一个专注于高风险基础研究的实验室，包括他个人热衷的 FFT 算法项目。Together AI 联合创始人 Tri Dao 则在普林斯顿大学。这种模式是共生关系：在学术界降低想法风险，在 Together AI 将其产品化。博士生加入公司，Together AI 的实习生则在学术实验室从事更长期的研究。

因此，Together AI 的内核团队本质上是一个斯坦福/普林斯顿系统领域的“黑手党”，将他们自己的研究成果产品化——FlashAttention、Mamba、H3、ThunderKittens——全部直接从学术界流入推理栈。这与 DeepSeek 的运作方式非常相似：研究优先，实现深度作为护城河。

**参考资料：**

- [Dan Fu 的个人主页 - danfu.org](https://danfu.org/)
- [Inside the Together AI kernels team](https://www.together.ai/blog/inside-the-together-ai-kernels-team)