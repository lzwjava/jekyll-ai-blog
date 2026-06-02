---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI研究员张吕敏简介
translated: true
type: note
---

**问题：** 张吕敏（lllyasviel）是谁？

**回答：**

张吕敏是当前生成式图像/视频领域最具影响力的应用型AI研究者之一。以下是他的简要介绍：

**身份：**

- 斯坦福大学计算机科学博士生，导师为Maneesh Agrawala。此前在香港中文大学担任研究助理，师从黄田津（Tien-Tsin Wong）。2021年获得苏州大学工学学士学位。

**你一定用过他的成果：**

- **ControlNet** — ICCV 2023最佳论文（Marr奖）。该架构通过可训练副本+零卷积为冻结的文生图扩散模型添加空间控制（边缘、深度、姿态）。这篇论文让Stable Diffusion变得可控，如今几乎所有图像生成流程都在使用它。

- **FramePack** — NeurIPS 2025 Spotlight（前3%）。一种逐帧视频预测架构，通过按重要性压缩输入帧，将更长的上下文打包到固定长度，并采用漂移抑制机制减少误差累积。

- **IC-Light** — ICLR 2025 Oral（前1%）。基于扩散模型的重光照技术，通过施加一致的光传输原理实现可扩展的野外训练。

- **LayerDiffuse** — SIGGRAPH 2024。利用潜空间扩散生成透明图像，将alpha通道编码为潜偏移量（"潜透明度"）。

**使其与众不同的背景：**
他曾与数字绘画艺术家合作多年，并资助了Style2Paints Research项目。大学前他是游戏开发者和职业游戏王玩家，曾开发YGOPro2。此外，他还有匿名参与破解社区活动的经历（主要为Denuvo和虚拟机）。

**模式：** 他总能提出优雅的架构思路——ControlNet的零卷积、FramePack的基于重要性的压缩——来解决生成模型中的棘手实际问题。他发布真实可用的代码，在社区中活跃运营（其GitHub账号`lllyasviel`极其活跃），同时发表顶会论文。他是典型的Karpathy式构建者-研究者复合体，但专注于可控扩散模型和视频生成。

他2026年近期产出（2篇ICML、1篇SIGGRAPH、1篇CVPR）表明他并未放慢脚步。

**参考资料：**

- [张吕敏的个人主页](https://lllyasviel.github.io/lvmin_zhang/)
- [ControlNet论文](https://arxiv.org/abs/2302.05543)
- [FramePack](https://lllyasviel.github.io/frame_pack_gitpage/)
- [IC-Light代码](https://github.com/lllyasviel/IC-Light)
