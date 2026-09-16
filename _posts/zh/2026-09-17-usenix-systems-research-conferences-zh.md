---
audio: false
generated: true
image: false
lang: zh
layout: post
title: USENIX：系统研究会议
translated: true
type: note
---

**问题：USENIX 是什么？它是一个什么样的会议？**

**回答：**

[USENIX](https://www.usenix.org?utm_source=chatgpt.com) **并非单一的会议**。它是一个非营利的计算研究组织，主办了一系列高度技术性的系统会议。其关注点大致可以概括为：

> **"我们如何构建真正能工作的计算机系统？"**

它在 **系统/基础设施/安全/网络/存储/操作系统/分布式系统** 等领域尤为强势。USENIX 将其会议描述为：为具有开创性的计算系统研究提供中立的厂商无关平台，并免费/开放地提供会议论文和视频。（[USENIX][1]）

重要的会议包括：

| 会议                  | 领域                                 | 典型内容                                     |
| ------------------- | ---------------------------------- | ---------------------------------------- |
| **OSDI**            | 操作系统、分布式系统                       | Linux / 数据库 / 运行时 / 基础设施             |
| **NSDI**            | 网络 + 分布式系统                        | 数据中心网络、云、边缘计算                       |
| **USENIX Security** | 安全                                 | 系统安全、密码学、攻击/防御                      |
| **FAST**            | 存储                                 | SSD、文件系统、存储系统                       |
| **ATC**             | 广义系统                              | 实用系统工程                                |
| **SREcon**          | 生产环境/SRE                          | 可靠性、大规模运维                            |
| **SAIS**            | 安全的具身智能AI                        | 更新的AI Agent系统/安全                      |

USENIX 目前列出的会议包括 **OSDI、NSDI、FAST、Security、SREcon**，以及较新的领域如 **SAIS（Secure Agentic-AI Systems）**。（[USENIX][2]）

### 工程师为何关注

USENIX 的一个有趣之处在于，其论文往往 **侧重于实现**。

典型的系统论文不是：

```text
我们提出了一种令人兴奋的架构。
```

而是更像：

```text
我们构建了 X
→ 这是架构
→ 这是实现
→ 这是工作负载
→ 这是基准
→ 这是性能测试
→ 这是它失败的地方
→ 这是它更快/更便宜/更可靠的原因
```

对于从事 **LLM 训练/推理基础设施、分布式系统、GPU 集群、存储、网络或 Agent** 的人来说，我会特别关注 **OSDI + NSDI + FAST + SREcon**。

还有一个巨大的实际优势：**USENIX 的会议论文可免费阅读**，因此你可以将会议论文集视为一个高质量的开源研究资源。（[USENIX][1]）

一个有用的思维模型：

```text
机器学习会议
  NeurIPS / ICML / ICLR
       ↓
  模型 + 算法

系统会议
  OSDI / NSDI / FAST / ATC
       ↓
  机器 + 网络 + 存储 + 分布式软件
```

对于你的工作类型而言，**OSDI/NSDI 的论文很可能比一般的 ML 论文更贴近 LLM 公司面临的工程问题**。

我也可以梳理一下 **过去 2-3 年 OSDI/NSDI/FAST 的论文**，提取出与 LLM 推理/训练基础设施最相关的那些。

[1]: https://www.usenix.org/ "USENIX Home | USENIX"
[2]: https://www.usenix.org/conferences/all?order=field_conference_date&sort=desc&utm_source=chatgpt.com "All Conferences | USENIX"