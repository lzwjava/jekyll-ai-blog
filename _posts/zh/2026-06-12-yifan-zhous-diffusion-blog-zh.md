---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 周逸凡的扩散博客
translated: true
type: note
---

**问题：** 介绍博客 <https://zhouyifan.net> 及其作者。

**回答：**

## 作者：周弈帆 (Yifan Zhou)

周弈帆是新加坡南洋理工大学计算机科学与工程学院博士生，NTU MMLab成员（隶属于NTU S-Lab），师从潘新钢教授。读博前，他曾在NTU S-Lab和上海人工智能实验室担任研究工程师，本科毕业于北京理工大学计算机科学专业。研究方向是图像和视频生成——扩散模型、DiT架构和注意力效率。

值得关注的职业亮点：

- 在上海人工智能实验室（2021–2022），他是 OpenMMLab 生态中开源模型部署库 MMDeploy 的核心开发者和维护者。
- 竞赛编程背景：1 块 ACM-ICPC 金牌、5 块银牌，以及 2 块 CCPC 银牌。GitHub 账号：SingleZombie。
- 发表论文包括 Rerender A Video (SIGGRAPH Asia 2023)、FRESCO 和 DiffMorpher (均为 CVPR 2024)、Alias-free Latent Diffusion Models (CVPR 2025 Oral)，以及他最新的第一作者工作 Trainable Log-linear Sparse Attention for Efficient Diffusion Transformers——被接收为 CVPR 2026 Highlight。
- 他公开声明的长期目标在 ML 研究者中不常见：他坦言游戏设计才是他真正的梦想，现在追求 AI 研究成功是为了最终资助“AI + 游戏设计”的事业。他计划在完成学术生涯后，以单人创始人的工作模式，围绕 AI 驱动的游戏玩法设计，开展研究、开发工具和游戏产品。

## 博客（周弈帆的博客）

基于 Hexo，自 2019 年左右运行，共 158 篇文章，涵盖 21 个分类，以中文为主（英文镜像见 /blog-en）。这是关于扩散模型和注意力机制最好的中文深度解读博客之一，与你的 nanoGPT/MoE/sparse-attention 方向直接相关。标志性风格：从基本原理开始的论文讲解，包含数学、复杂度分析和诚实批评部分（他公开批评自己论文的弱点，这很少见）。

近期代表性内容：

- **LLSA（他自己的论文）**——对 Log-linear Sparse Attention 的第一人称解释，该工作通过层级 Top-K 选择、KV 丰富化和 KV 重加权，将稀疏注意力从 O(N²) 降低到 O(N log N)，并附有开源的高性能 Triton 实现（github.com/SingleZombie/LLSA）——在无 VAE、无 patchify 的像素 DiT 上验证，序列长度可达 512×512 像素。这与 MoBA (Kimi) 和 NSA (DeepSeek) 形成竞争，后两者并未真正降低渐近复杂度——其运行时仍按 O(N²) 增长。
- **Pixel DiT 系列**——对 JiT（何恺明团队）、DiP、DeCo 和 PixelDiT 的比较分析，深入剖析为什么大 patch 的 DiT 难以训练，以及像素级解码器如何替代 unpatchify。
- **FlashAttention 教程**——“无需 CUDA 知识也能理解 FlashAttention”，以及他的 Triton GPU 编程笔记（高效反向传播的稀疏索引转置、Q-major → K-major 索引转换）。

他本人也很有个性：在丹佛举行的 CVPR 2026 上，他在自己的海报环节之余，还 cosplay 了 BanG Dream! 中的户山香澄——他承认这是为了吸引关注，灵感来源于 CVPR 2024 上 cos 芙莉莲的参会者。他的自我介绍半开玩笑地说，自己的编程能力是“人类中的王者级别”。

**为什么与你的方向相关：**他的 LLSA Triton 内核正是你正在构建的那种注意力内部 + GPU 编程素材（与 NSA/MoBA 类似，开源，可即插即用替代注意力）。FlashAttention 和稀疏注意力文章与你对 nanoGPT/DeepSeek-v4 MoE 的研究非常契合——而且他的代码在单块 H200 级别的预算下就能运行，也就是你已经租用的 MI300X 的领域。

**参考链接：**

- [周弈帆的博客 (主页)](https://zhouyifan.net)
- [关于 / CV 页面](https://zhouyifan.net/about/)
- [LLSA 论文讲解](https://zhouyifan.net/2025/12/18/20251211-llsa-1/)
- [arXiv 上的 LLSA](https://arxiv.org/abs/2512.16615)
- [LLSA GitHub](https://github.com/SingleZombie/LLSA)
