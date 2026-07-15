---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA NCP-AAI 认证概览
translated: true
type: note
---

问题：什么是 NVIDIA 的 NCP-AAI 认证？

答案：NCP-AAI = **NVIDIA 认证专业人士：自主式 AI（大语言模型）**。这是 NVIDIA 最新的专业认证，区别于早些的 NCA-GENL（助理级 GenAI/LLM 认证）和 NCP-AII（基础设施运维认证）。

考试机制：
- **60–70 道题，90–120 分钟**（资料说法不一——NVIDIA 官方页面称 60-70 题/120 分钟，第三方指南称 90 分钟——注册时请在 Certiverse 确认）
- **200 美元**，在线考试，通过 Certiverse 远程监考
- 有效期 2 年，续证需重考

先决条件（软性要求，非强制）：1–2 年 AI/ML 生产环境经验，具备智能体编排、多智能体框架、工具/模型集成的实践经验。

五大考试领域：智能体设计与认知（架构、推理/规划、记忆、多智能体协调）；知识集成与智能体开发（RAG 流水线、数据处理、提示工程、多模态智能体）；NVIDIA 平台实现与部署（推理优化、规模部署、生产工作流）；评估、监控与维护（基准测试、调优、实时监控、故障排除）；人类、伦理与合规考量（人机协同设计、安全/合规护栏）。

鉴于您已在使用 MI300X 训练模型并自行构建智能体 CLI（ww/iclaw/zz），该认证对您而言更多是信号传递/人力资源筛选需求，而非知识补充——考试领域涵盖的内容您已实际交付过。仅在客户或合同明确要求该资质时值得投入。

付费前需核实：截至 2026 年 3 月 GTC 主题演讲，NVIDIA 参考模型系列已切换至 Nemotron 3（Super 120B/12B-active 正式发布，Ultra 预览版，Nano 4B 及 Nano Omni 面向边缘/多模态）——若参考 2026 年 4 月前的资料备考，考试中会遇到过时的模型引用。

参考资料：
- [NVIDIA 自主式 AI 大语言模型专业人士认证](https://www.nvidia.com/en-us/learn/certification/agentic-ai-professional/)
- [NVIDIA 认证项目](https://www.nvidia.com/en-us/learn/certification/)
- [NCP-AAI 2026 完全指南 | Preporato](https://preporato.com/blog/nvidia-ncp-aai-certification-complete-guide-2025)