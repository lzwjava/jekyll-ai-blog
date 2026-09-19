---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ISTA-DASLab：高效AI研究组
translated: true
type: note
---

**问题：** Hugging Face 上的 ISTA-DASLab 是什么？他们做什么？

**回答：**

**ISTA-DASLab** 代表 **IST奥地利分布式算法与系统实验室**（深度算法与系统实验室），是一个隶属于[奥地利科学技术研究院 (ISTA)](https://ist.ac.at) 的研究小组。

**领导：** 该小组由 **Dan Alistarh** 教授领导，他自2022年起担任ISTA教授。他的背景包括在MIT从事博士后研究、在微软剑桥研究院从事研究工作，以及获得EPFL博士学位。

**使命：** Alistarh 小组致力于通过创建比传统方法显著更高效的训练和推理算法，消除 AI 普及化道路上的障碍。他们的核心关切在于，训练和部署最先进的 AI 模型所需的计算量呈指数级增长，这可能阻碍创新，并导致专业知识和经济收益方面的不平等。

**研究重点：** 他们当前的项目涵盖大规模 AI 模型的高效训练与推理、大规模分布式机器学习、自适应并发数据结构以及分布式计算的基本极限。他们开发新的算法，用于在压缩表示（如稀疏或量化模型）上进行学习，以及能够在实践中利用压缩收益的高效系统实现。

**他们在 Hugging Face 上发布的内容：** 该实验室在 Hugging Face 上托管了164个模型和2个数据集，有19名团队成员参与贡献。他们近期最突出的工作包括：

- **GSQ**（Gumbel-Softmax 量化）—— 用于LLM的高精度低比特标量量化
- **GSQ-RCO-GGUF** —— 使用标准 GGUF 格式中按张量混合精度的非均匀 GGUF 量化
- 流行大模型（如 Qwen3、Kimi-K2 和 Llama 3.1）的量化版本（2比特和3比特精度）

简而言之，DASLab 是一个领先的学术研究小组，致力于推动 **LLM 压缩与高效推理** 的前沿，在不牺牲质量的前提下使大模型更小、更快。

**参考资料：**

- [Hugging Face 上的 ISTA-DASLab](https://huggingface.co/ISTA-DASLab)
- [Alistarh 小组 — ISTA](https://ist.ac.at/en/research/alistarh-group/)
