---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GLM-5.2 GGUF 发布日期
translated: true
type: note
---

**问题：** `unsloth/GLM-5.2-GGUF` 是什么时候发布的？

**回答：**

GLM-5.2 由 Z.ai 于 **2026 年 6 月 13 日** 发布，采用 MIT 许可证的开源权重和按量计费 API 在接下来的一周内逐步推出。Unsloth GGUF 量化仓库会在基础权重发布后不久跟进。

关于模型本身的关键事实：

- 744B 参数（每个 token 约 40B 活跃），MoE 架构，1M token 上下文窗口，MIT 许可证。
- 引入 IndexShare —— 在每四个稀疏注意力层之间复用同一个索引器，在 1M 上下文下将每个 token 的 FLOPs 降低 2.9 倍。MTP 层改进将推测解码的接受长度最多提升 20%。
- 基准测试：Terminal-Bench 2.1 上 81.0 分，SWE-bench Pro 上 62.1 分，使其成为长期编码基准测试（FrontierSWE、PostTrainBench、SWE-Marathon）中排名最高的开源模型。

鉴于你已经大量使用 deepseek-v4-pro/flash —— 采用 MIT 许可证且拥有 1M 上下文的 GLM-5.2，值得通过 AMD MI300X（192GB HBM3 可轻松处理量化版本）上的 Unsloth GGUF 启动运行。