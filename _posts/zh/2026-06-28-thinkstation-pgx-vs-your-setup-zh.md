---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ThinkStation PGX 对比您的配置
translated: true
type: note
---

让我看看那个页面。这是联想的 ThinkStation PGX —— 他们基于 NVIDIA DGX Spark（原名 "Project DIGITS"）打造的版本。它是一款紧凑型桌面 AI 开发设备，搭载 NVIDIA GB10 Grace Blackwell Superchip。

页面中的相关规格：

- **SoC：** NVIDIA GB10 Grace Blackwell Superchip —— 一颗 20 核 Arm Grace CPU 通过 NVLink-C2C 与 Blackwell GPU 融合
- **内存：** 128GB LPDDR5x 统一内存（CPU 和 GPU 共享，一致性访问）
- **存储：** 最高 4TB NVMe M.2
- **操作系统：** NVIDIA DGX OS（基于 Ubuntu）
- **价格：** 约 $5,079（显示促销价 $4,825），SFF 小外形规格

宣传卖点是“你自己的小型 DGX”。GB10 提供约 **1 petaflop FP4（稀疏）** AI 算力，而 128GB 一致性内存池是真正的亮点——它可以让您加载那些无法装入单块独立 GPU VRAM 的模型。两台设备可以通过 NVLink 桥接，用于运行约 405B 参数级别的模型进行推理。

具体应用到您的情况：

**相比您的 RTX 4070（12GB）的优势：** 4070 在 VRAM 上对您限制很大。PGX 的 128GB 统一内存意味着您可以运行/微调 70B 参数级别的量化模型，或者在更大的基座模型上进行 LoRA 训练，而不会遇到 OOM 问题。对于您的 DeepSeek-v4 MoE 探索和 nanochat 规模的工作，内存上限才是真正释放您潜力的关键。

**劣势：** FP4 petaflop 的宣传 ≠ 训练吞吐量。LPDDR5x 的带宽（约 273 GB/s）远低于 MI300X 的 HBM3（约 5.3 TB/s），甚至低于 RTX 4090 的 GDDR6X。对于原始训练速度——您的从头训练 GPT-2 760M 项目——它会比 MI300X **慢得多**。这是一款“能装大模型，但跑得慢”的设备，针对推理、原型设计和微调优化，而不是从头预训练。

**对您来说诚实的比较：** 大约 $5K 的价格，相当于在 MI300X 开发云上使用约 2,500 小时（按 $2/小时计算）。考虑到您已经有 MI300X 用于重度训练，以及 RTX 4070 用于本地迭代，PGX 的定位是“一个可以装下 70B 模型用于 agent/推理工作而无需租用云的本地盒子”。这确实是您现有设置中的空白，但这是一个便利性/延迟购买，并不是您缺乏的能力。如果目标是不断积累训练能力，MI300X 的云时数在每美元的学习收益上更高。如果目标是静音、始终在线的本地推理/agent 主机，同时拥有大内存，那么 PGX 很合适。

参考链接：

- [联想 ThinkStation PGX 产品页面](https://www.lenovo.com/us/en/p/workstations/thinkstation-p-series/lenovo-thinkstation-pgx-sff/len102s0023)
- [NVIDIA DGX Spark](https://www.nvidia.com/en-us/products/workstations/dgx-spark/)
