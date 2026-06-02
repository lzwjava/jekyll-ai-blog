---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: vLLM：高效大语言模型服务引擎
translated: true
type: note
---

### vLLM 的诞生

vLLM（"virtual LLM"的简称）是一个专为大语言模型推理与服务打造的高吞吐、内存高效开源库。该项目由加州大学伯克利分校RISELab的Sky Computing实验室研究人员于2023年初创立，最初是专为英伟达A100 GPU和有限模型集优化的推理引擎，致力于解决LLM服务中的内存碎片化和低吞吐量等核心难题。

重要早期里程碑：
- **2023年4月中旬**：首次与FastChat完成公开集成，为LMSYS的Vicuna和Chatbot Arena演示提供支持
- **2023年6月**：正式发布并公开GitHub代码库
- **2023年9月12日**：在arXiv发表奠基性研究论文《基于PagedAttention的大语言模型服务高效内存管理》，提出实现连续批处理和近零KV缓存浪费的核心PagedAttention机制

GitHub代码库（vllm-project/vllm）创建于2023年5-6月，与项目初期开发阶段同步。

### 知名度攀升

vLLM于2024年开始获得显著关注，从小众研究工具演进为开源LLM服务的事实标准。其爆发式增长得益于快速的功能迭代（如量化、推测解码、多模态支持）、硬件平台扩展（英伟达、AMD、谷歌TPU等）以及被亚马逊（2024年会员日期间支持Rufus）、LinkedIn等企业的生产环境采用。

2024年关键增长指标：
- **GitHub星标数**：从1.4万（2024年初）增长2.3倍至3.26万（2024年底）
- **月下载量**：从6000次猛增4.5倍至2.7万次
- **GPU使用量**：2024下半年增长约10倍
- **社区规模**：贡献者数量增长3.9倍达740人，设立双周办公时间并建立合作伙伴关系（如英伟达、IBM、AWS）

截至2024年中，项目已收获约2万星标，并因在吞吐量方面超越同类方案而频繁获得AI社区讨论。这一增长势头持续至2025年：
- 2024年12月加入PyTorch生态系统
- 2024年10月进入LF AI & Data孵化计划
- 2025年6月达成5万星标里程碑

目前（2025年10月），项目已获得超5.5万星标，支持近100种模型架构，成为可扩展AI部署的基石技术。

[PagedAttention arXiv论文](https://arxiv.org/abs/2309.06180)
[vLLM GitHub代码库](https://github.com/vllm-project/vllm)
[vLLM 2024回顾博客](https://blog.vllm.ai/2025/01/10/vllm-2024-wrapped-2025-vision.html)
[PyTorch集成公告](https://pytorch.org/blog/vllm-joins-pytorch/)
