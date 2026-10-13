---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 适用于ROCm的廉价AMD GPU
translated: true
type: note
---

## 问题：哪些便宜的二手 AMD GPU 支持 ROCm？

**答案：** 对于你的 AI 实验室，我会重点关注较旧的 AMD Instinct 加速卡，而不是消费级 Radeon 显卡。但有一个问题：**最便宜的、显存够用的 AMD GPU，并不一定是能可靠运行 PyTorch + ROCm 的最便宜 GPU。**

我准备调研的候选清单：

| GPU | VRAM | 架构 | 评估 |
| --- | ---: | --- | --- |
| Radeon RX 6600 | 8GB | RDNA 2 | 廉价消费级显卡；需确认具体的 ROCm 支持情况 |
| Radeon RX 6700 XT | 12GB | RDNA 2 | 显存更大，但软件支持需要验证 |
| Radeon RX 6800 | 16GB | RDNA 2 | 对预算有限的 AI 项目可能有吸引力 |
| Instinct MI50 | 16GB 或 32GB | CDNA 1 | 较老的计算加速卡；现代 ROCm 支持令人担忧 |
| Instinct MI100 | 32GB | CDNA 1 | 计算方面更有前景，但需检查当前支持和二手价格 |
| Instinct MI210 | 64GB | CDNA 2 | 更好的现代计算选项，通常更贵 |

这些只是待调研的候选，并非声称每张卡都受最新 ROCm 版本支持。

## 1. 我的首选

### 选项 A：Instinct MI100 32GB —— 面向计算

如果你想要以低价获得大容量显存，MI100 是最值得调研的老一代工作站/服务器加速卡。

- 32GB HBM2
- 1 TB/s 内存带宽
- CDNA 架构，目标为 `gfx908`
- 出现在 AMD 当前的 ROCm 硬件支持文档中。[AMD ROCm](https://rocm.docs.amd.com/en/latest/about/release-notes.html?utm_source=chatgpt.com)

它的主要缺点是 300W 功耗、服务器取向的硬件，以及可能较难安装。购买前请确认具体的 ROCm/PyTorch 组合兼容性。

### 选项 B：Radeon RX 7900 XT 20GB —— 面向消费级 PC

如果你更想用普通游戏 GPU，RX 7900 XT 值得调研。

- 20GB GDDR6
- RDNA 3 架构
- 受当前 ROCm 文档支持。[AMD ROCm](https://rocm.docs.amd.com/en/latest/about/release-notes.html?utm_source=chatgpt.com)

与 MI100 相比，它在传统台式机上更新、更实用，尽管二手价格可能更高。

### 选项 C：Radeon Pro W6800 32GB —— 面向大显存需求

W6800 提供 32GB 显存，并且出现在 AMD 当前的 ROCm 支持文档中。[AMD ROCm](https://rocm.docs.amd.com/en/latest/about/release-notes.html?utm_source=chatgpt.com)

如果你能找到便宜的 W6800，值得与 MI100 做比较，尤其是当你想要工作站显卡而非服务器加速卡时。

## 2. 那特别便宜的 MI50 和 RX 6800 呢？

这两张卡要小心。

- **MI50 32GB：** 显存容量很诱人，但社区报告显示 ROCm 6.3.3 是最后一个兼容版本。把它当作一个遗留软件项目，而不是当前的 ROCm 解决方案。[Reddit](https://www.reddit.com/r/ROCm/comments/1ominy2?utm_source=chatgpt.com)
- **RX 6800 16GB：** 它出现在较早的 ROCm 硬件文档中，但不在当前 ROCm 10.1 官方支持的 Radeon GPU 列表中。我不会为了当前的官方 ROCm 支持而专门购买它。[AMD ROCm](https://rocm.docs.amd.com/en/latest/about/release-notes.html?utm_source=chatgpt.com)

## 3. 如果我是你，我会怎么做

既然你已经有一块 RTX 4070 12GB，并且正在为 LLM 实验寻找廉价 GPU，我会比较这三张卡：

| GPU | 主要优势 | 建议 |
| --- | --- | --- |
| MI100 32GB | 大容量 HBM | 廉价计算加速卡的最佳候选 |
| Radeon Pro W6800 32GB | 工作站显卡的大显存 | 值得调研 |
| RX 7900 XT 20GB | 现代消费级 GPU | 更适合桌面使用的选项 |

**一个问题：你是在中国的二手市场（比如闲鱼）买，还是在美国买？** 这会影响我推荐哪款卡，因为当地的二手价格会完全改变性价比排名。
