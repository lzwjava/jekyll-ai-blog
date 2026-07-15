---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA NCP-AII 认证概述
translated: true
type: note
---

问题：请介绍 NVIDIA 的 NCP-AII（AI 基础设施）认证。

回答：**NCP-AII = NVIDIA 认证专家：AI 基础设施。** 这是一项侧重于运维的认证，而非模型或智能体相关——它验证的是你能否搭建并运行 GPU 数据中心，而非编写机器学习代码的能力。

**考试机制：**
- 70–75 道题，**120 分钟**（美国页面显示；部分地区页面显示 90 分钟/60–70 题——请查看你所在地区的页面）
- 费用 200 美元，在线考试，通过 **Certiverse** 远程监考，考试后约 24 小时通过 Credly 获取徽章
- 有效期 2 年，仅显示通过/未通过（不显示分数）
- 先决条件：具备 2–3 年使用 NVIDIA 硬件的实际操作数据中心运维经验（软性要求，注册时不强制检查）

**实际涵盖内容**——指模型/智能体工作底层的实际基础设施层面：
- 部署 DGX/HGX 服务器、安装 GPU 驱动、固件更新
- 为多租户环境配置 MIG
- BlueField DPU 配置
- 容器栈 + 集群调度器（NVIDIA 使用的参考栈为 Slurm 配合 Enroot/Pyxis）
- AI 集群的存储和网络基础
- 实时 GPU 集群的监控与故障排除

**在 NVIDIA 认证体系中的位置：**
| 认证 | 级别 | 重点 |
|---|---|---|
| NCA-AIIO | 助理级 | AI 基础设施/运维基础概念 |
| **NCP-AII** | 专业级 | AI 基础设施的部署/配置/故障排除 |
| NCP-AI Networking | 专业级 | 专攻 InfiniBand/网络 |
| NCP-AAI | 专业级 | Agentic AI/大语言模型系统（你之前问过的那个） |

**对你而言：** 鉴于你已经在运行 MI300X 集群，并且每月在多款模型上处理约 20 亿 Token 的推理任务，你已经完成了该认证所考核的实际工作（驱动/固件、容器编排、集群调度）——如果有差距，也仅在于 NVIDIA 特有工具的名称（如 BlueField、MIG、NIM），而非概念本身。与 NCP-AAI 的结论相同：只有客户合同或工作职位明确要求该徽章时，才值得投入 200 美元及备考时间。

参考链接：
- [AI 基础设施 (AII) 专业认证 | NVIDIA](https://www.nvidia.com/en-us/learn/certification/ai-infrastructure-professional/)
- [NCP-AII 认证：2026 年完全指南 | FlashGenius](https://flashgenius.net/blog-article/ncp-aii-certification-the-complete-2025-nvidia-ai-infrastructure-guide-to-get-certified)