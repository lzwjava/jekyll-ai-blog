---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA DLI 认证考试详解
translated: true
type: note
---

**问题：** NVIDIA DLI 的哪些认证考试是监考的（现场或远程），以及它们如何详细运作？

**答案：**

## NVIDIA DLI 认证考试 — 2026 完整指南

首先，一个许多人忽略的重要澄清：

> **DLI 课程 ≠ 认证。** DLI 课程提供完成证书。NVIDIA 认证是独立的监考考试，用于验证您的应用专业知识——这两者是完全不同的。

---

## 考试交付与监考

所有 NVIDIA 考试均在线上交付，并严格采用远程监考。您需要一个安静的房间、高质量的网络摄像头以及可靠的互联网连接。NVIDIA 目前使用 **Certiverse** 作为考试管理平台。

对于远程测试，监考人员会引导考生完成考试启动、登录程序、多因素身份验证以及 360° 环境安全评估。监考人员可能通过摄像头远程监控您，并查看您的整个测试环境。

**例外 — GTC 会议现场：** 对于 GTC 现场参与者，NVIDIA 提供免费监考认证考试（价值 $135–$500），仅在会议期间独家提供。这包括新的 Associate 级考试，甚至专业认证的动手部分。

---

## 考试结构

Associate (NCA) 考试通常给予您 **60 分钟** 来回答大约 **50 道题**。Professional (NCP) 考试给予您 **120 分钟** 来回答 **60–75 道高度复杂的题目**。

考试主要由多选题和多选响应题组成。目前没有实时的动手实验部分——您必须在概念和架构上理解所测试的确切命令行标志和框架行为。

远程监考考试期间不允许休息。完成考试后立即显示结果，并按领域细分。

---

## 两个级别：Associate (NCA) 与 Professional (NCP)

**Associate (NCA)** 考试测试基础、高层次概念——LLM 是什么、基本 prompting 以及高层次用例。**Professional (NCP)** 考试测试高级、细粒度的工程知识——如何在多个 GPU 上实现分布式训练、如何执行 Parameter-Efficient Fine-Tuning (PEFT)，以及框架的具体细节。

---

## 可用认证完整列表（2026）

### 🔵 Associate 级别 (NCA) — 每场 $125 USD

  
| 考试代码 | 名称 | 时长 | 测试内容 |
|---|---|---|---|
| **NCA-GENL** | Generative AI with LLMs | 60 分钟 / 50 题 | 使用生成式 AI 和 LLMs 结合 NVIDIA 解决方案开发、集成和维护 AI 驱动应用的基礎概念 |
| **NCA-GENM** | Generative AI Multimodal | 60 分钟 / 50 题 | 设计、实施和管理跨文本、图像和音频模态合成及解释数据的 AI 系统的基礎技能 |
| **NCA-AIIO** | AI Infrastructure & Operations | 60 分钟 / 50 题 | 与基础设施和运营相关的 AI 计算基礎概念；需要对数据中心基础设施的基本理解 |
| **NCA-ADS** | Accelerated Data Science | 60 分钟 / 50 题 | 初级分析师的 RAPIDS/GPU 数据科学入门 |

### 🟠 Professional 级别 (NCP) — $200–$400 USD

  
| 考试代码 | 名称 | 费用 | 测试内容 |
|---|---|---|---|
| **NCP-GENL** | Generative AI LLMs Professional | $200 | 分布式训练策略（tensor parallelism 与 pipeline parallelism）、PEFT、复杂 RAG 部署、Triton/TensorRT-LLM 推理 |
| **NCP-AAI** | Agentic AI Professional | $200 | 多代理系统、规划与推理、生产代理式应用的 RAG 设计 |
| **NCP-ADS** | Accelerated Data Science | $200 | RAPIDS 生态系统的深入熟练掌握——cuDF、cuML、cuGraph——使用 Dask 在多个 GPU 上扩展工作流，将加速分析集成到 MLOps 管道中 |
| **NCP-AII** | AI Infrastructure Professional | $400 | Slurm 工作负载管理器、使用 NVIDIA GPU Operator 的 Kubernetes 编排、Base Command Manager、部署企业级 DGX/HGX 系统 |
| **NCP-AIO** | AI Operations Professional | $400 | 大规模监控、优化和故障排除 AI 工作负载 |
| **NCP-AIN** | AI Networking Professional | $400 | 针对 AI 工作负载优化的 Spectrum-X Ethernet 或 InfiniBand 网络结构 |
| **NCP-OUSD** | OpenUSD Professional | $200 | 使用 OpenUSD 构建、维护和优化 3D 内容创建管道；适用于媒体/娱乐、游戏、数字孪生 |

> ⚠️ **NCP-GENL 和 NCP-AAI** 已公布，并于 2026 年初新发布或即将推出——请检查 NVIDIA Certification Portal 以获取当前可用性。

---

## 定价总结

Associate 级别 (NCA) 考试每次尝试 $125 USD。Professional 级别开发者和数据科学考试 (NCP-GENL、NCP-AAI、NCP-ADS) 费用 $200 USD。Professional 级别基础设施和网络考试 (NCP-AII、NCP-AIO、NCP-AIN) 费用 $400 USD。

---

## 有效期与续期

所有 NVIDIA 认证自颁发之日起有效期恰好为 **两年**。由于 AI 技术发展迅速，您必须通过重考当前版本的考试来重新认证，以保持活跃状态和数字徽章。

---

## 重考与调度政策

全球指南规定尝试之间需等待 **14 天**，每年最多 **五次尝试**。  
您可以在考试开始前 **24 小时** 内取消或重新调度考试。考试在会话开始前 24 小时内不可退款，NVIDIA 不会为错过、通过或失败的考试退款。

---

## 通过后获得什么

通过后，您将收到通过 **Credly** 颁发的 **数字徽章**，可添加到简历、LinkedIn 和作品集。您还可以选择加入 NVIDIA 的公共认证目录，以便雇主找到您。

---

## 谁应该获得哪些认证？

  
| 您的背景 | 推荐路径 |
|---|---|
| AI 开发人员 / 软件工程师 | NCA-GENL → NCP-GENL 或 NCP-AAI |
| 数据科学家 / ML 工程师 | NCA-ADS → NCP-ADS |
| IT / 系统管理员 / 基础设施 | NCA-AIIO → NCP-AII |
| SRE / AI 运维工程师 | NCA-AIIO → NCP-AIO |
| AI 数据中心网络工程师 | NCA-AIIO → NCP-AIN |
| 3D / VFX / 数字孪生开发人员 | NCP-OUSD |

---

## 它们值得吗？

以 $125–$400 的价格，NVIDIA 认证价格实惠且全球认可。雇主视其为实用、可部署技能的证明。NVIDIA 认证专业人士在 AI Infrastructure Specialist、Data Engineer 和 Machine Learning Engineer 等角色中需求旺盛，年薪通常在 $100K–$150K 之间，高级职位超过 $200K。

无需学位——NVIDIA 认证验证技能而非文凭，非常适合职业转型者或自学者。

---

**参考资料：**

- [NVIDIA Certification Portal (Official)](https://www.nvidia.com/en-us/learn/certification/)
- [NVIDIA DLI Training Home](https://www.nvidia.com/en-us/training/)
- [NCA-GENL Exam Page](https://www.nvidia.com/en-us/learn/certification/generative-ai-llm-associate/)
- [NCA-AIIO Exam Page](https://www.nvidia.com/en-us/learn/certification/ai-infrastructure-operations-associate/)
- [NVIDIA GTC 2026 Training & Exams](https://www.nvidia.com/gtc/training/)
- [FlashGenius: Ultimate NVIDIA Certification Guide 2026](https://flashgenius.net/blog-article/the-ultimate-guide-to-nvidia-certifications)
- [PassItExams: NVIDIA Certification Path 2026](https://passitexams.com/articles/nvidia-certification-path/)