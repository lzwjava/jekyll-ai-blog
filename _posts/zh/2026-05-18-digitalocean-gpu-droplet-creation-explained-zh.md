---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DigitalOcean GPU Droplet创建详解
translated: true
type: note
---

问题: DigitalOcean 的 GPU Droplet 创建界面中包含 AMD MI300X 和 ROCm 选项，这代表什么含义？每个部分如何运作？

回答:

这是 **DigitalOcean GPU Droplet 创建界面**，专门用于配置基于 AMD 硬件的云端 GPU 虚拟机。以下是每个部分的详细说明：

---

## 1. 什么是 GPU Droplet？

DigitalOcean GPU Droplet 是配备高性能 AMD GPU 的虚拟化服务器，提供单 GPU 和多 GPU 配置。这些实例包含本地 NVMe 存储和 AI/ML 就绪镜像，用户只需点击几下即可启动预装驱动和框架的计算环境。

---

## 2. GPU 方案 — MI300X 选项

您可以在两种硬件配置中选择，两者均采用 **AMD Instinct MI300X** GPU：

### MI300X x8（8-GPU 方案）

- 8 个 GPU，总显存 1.5 TB，160 vCPU，1920 GB
- 启动磁盘：2 TB NVMe | 临时磁盘：40 TB NVMe
- **$1.99/GPU/小时**（= 8 个 GPU 总计约 $15.92/小时）

### MI300X x1（单 GPU 方案）

- 1 个 GPU，192 GB 显存，20 vCPU
- 启动磁盘：720 GB NVMe | 临时磁盘：5 TB NVMe
- **$1.99/GPU/小时**

AMD Instinct MI300X 的大容量显存可容纳数千亿参数的模型，减少模型跨 GPU 拆分的需求。

MI300X 基于下一代 AMD CDNA 3 架构，为最严苛的 AI 和 HPC 应用提供高效能与高性能，并针对 LLM 技术的训练与推理进行了特别优化。

---

## 3. 选择镜像

此部分可让您选择 Droplet 上预装的操作系统和预装软件栈。

### 裸操作系统

- **ROCm 软件** — 预装 AMD ROCm 驱动栈的纯净操作系统。您可自行手动安装任何 AI 工具。适合希望完全控制环境的用户。

### 快速启动包

这些是基于 Docker 的预配置环境，内含可直接使用的 JupyterLab 笔记本，可通过 SSH 或浏览器访问。每个包将 ROCm 与特定 AI 框架集成：

| 包名称 | 版本 | 用途 |
| --- | --- | --- |
| **vLLM** | 0.17.1 + ROCm 7.2.0 | 优化的 LLM 推理与服务 |
| **SGLang** | 0.5.9 + ROCm 7.0.0 | LLM 推理与服务 |
| **PyTorch** | 2.6.0 + ROCm 7.0.0 | 通用深度学习 / 模型训练 |
| **Megatron-LM** | 0.10.0 + ROCm 7.0 | 大规模分布式 LLM 训练 |
| **JAX** | 0.4.35 + ROCm 6.4.2 | 大规模机器学习训练（Google 框架） |
| **ROCm-enabled GPT-OSS** | 120B + ROCm 7 | 运行 OpenAI 开源权重的 120B 推理模型 |

ROCm 相当于 NVIDIA 的 CUDA，包含驱动、开发工具和 API，支持从底层内核到最终用户应用的 AMD GPU 编程。随着 AMD GPU 在开发领域（尤其是大语言模型方面）的普及，ROCm 软件包生态系统正在蓬勃发展。

---

## 4. SSH 密钥认证

创建 GPU Droplet **必须** 添加 SSH 密钥。这是一项安全要求——GPU Droplet 不支持密码登录。SSH 密钥对（公钥 + 私钥）可让您在实例创建后通过终端安全连接。

如果您没有 SSH 密钥，DigitalOcean 会引导您生成一个。

---

## 5. 定价摘要

使用这些 GPU Droplet 提供具有竞争力的定价：$1.99/GPU/小时，设置过程简单，并附带企业级 SLA。其他云提供商需要多个步骤和深厚技术知识来配置安全、存储和网络需求，而 DigitalOcean 的 GPU Droplet 只需点击几下即可完成设置。

计费按秒计算，最低取整 5 分钟。即使 Droplet 处于关闭状态，由于资源仍被保留，仍会产生费用，因此请在不使用时始终销毁 Droplet。

---

## 何时选择何种方案

| 使用场景 | 推荐选项 |
| --- | --- |
| 通过 API 提供大型 LLM 服务 | vLLM 快速启动包 |
| 微调或训练模型 | PyTorch 或 Megatron |
| 运行 GPT-OSS 120B 模型 | ROCm-enabled GPT-OSS |
| 自定义设置，完全控制 | 裸操作系统 + ROCm |
| 研究 / 实验 | JAX 或 SGLang |

参考来源：

- [Introducing AMD Instinct MI300X GPU Droplets – DigitalOcean 博客](https://www.digitalocean.com/blog/now-available-amd-instinct-mi300x-gpus)
- [使用 AMD MI300X 进行新一代 AI 开发 – DigitalOcean 社区](https://www.digitalocean.com/community/tutorials/amd-gpu-droplets-mi300x)
- [DigitalOcean GPU Droplets 产品页面](https://www.digitalocean.com/products/gradient/gpu-droplets)
- [DigitalOcean 与 AMD 合作 – 新闻稿](https://investors.digitalocean.com/news/news-details/2025/DigitalOcean-and-AMD-Collaborate-to-Advance-AI-Using-Cloud-Based-GPUs/default.aspx)
