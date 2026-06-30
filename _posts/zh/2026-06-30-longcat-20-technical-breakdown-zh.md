---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LongCat 2.0 技术解析
translated: true
type: note
---

你说得对——我之前把两件事混淆了。

你粘贴的那份文档是美团官方发布的 LongCat-2.0 上线公告，其中明确提到在 OpenRouter 上运行的是 **预览** 版本，并未直接说明它使用了"Owl Alpha"这个内部代号。公告指出，LongCat-2.0 预览版本通过 OpenRouter 和 longcat.ai 向全球开发者开放，并取得了调用量前三的成绩（#1 Hermes、#2 Claude Code、#3 OpenClaw）。

因此，准确的关系链是：

- **美团（该文档）确认的信息：** LongCat-2.0 的 *预览版* 通过 OpenRouter 提供服务，并登顶了 Hermes 排行榜。
- **媒体归因（非美团宣称）：** 记者们基于 4 月 24 日发布 / 4 月 28 日 OpenRouter 上线的重合时间点、1M 上下文以及代理编码特性，将那个具体的匿名列表"Owl Alpha"与 LongCat 预览版关联了起来。

"Owl Alpha = LongCat"这个等号是推断得出的，并非美团自己在 Owl Alpha 列表上留下的标记。如果你说"不"意味着认为这个代号映射关系有误——那是合理的，因为预览版完全可能以其他名称或直接路由的方式发布。官方文档中并未出现"Owl Alpha"字样。

而文档真正明确下来的、对你而言更有价值的部分是：

- **1.6T 总参数量，约 48B 激活参数（33B–56B 动态范围）**——基于零计算专家的 token 级动态激活 MoE 架构。
- **在约 5 万张国产（非 NVIDIA）计算卡集群上端到端训练**，预训练数据量超过 30T tokens，稳定状态下每天吞吐量超过 1T tokens，MFU 提升 1.5 倍。
- **LongCat Sparse Attention（LSA）**——将 1M 上下文的注意力从平方复杂度降至线性复杂度，这是实现"Agent 能看见整个代码库"的关键技巧。
- **MOPD 架构**——融合三组专家（Agent / 推理 / 交互），通过选通网络按任务类型进行分发，而非简单的参数合并。
- 宣称的基准测试成绩：**SWE-bench Pro 59.5**（领先于 GPT-5.5 的 58.6 和 Claude Opus 4.6 的 57.3）、**SWE-bench Multilingual 77.3**、**Terminal-Bench 2.1 70.8**。

他们在国产芯片稳定性方面的工作才是真正新颖的工程成果：HCCL 异常处理 + 弹性缩放 + 自动恢复，将每日故障率降低超过 70%；确定性算子配合逐位一致性验证确保正确性。这正是万亿参数模型在非 CUDA 硬件上训练时艰难而不起眼的部分，也是任何关注中国国产计算能否实现前沿运行的人需要盯住的真正信号。

需要我深入讲解 LSA 机制或零计算专家路由的实现细节吗？
