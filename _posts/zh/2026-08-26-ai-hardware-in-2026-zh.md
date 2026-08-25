---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 2026年AI硬件
translated: true
type: note
---

**问题：** 当前AI硬件领域的热点是什么，包括Plaud及其他值得关注的设备？

**回答：**

## 🔧 数据中心/芯片层面

英伟达凭借Blackwell平台及即将推出的Rubin架构持续领先。B200 GPU实现了巨大的性能飞跃，而AMD则以MI350/MI355系列反击，凭借具有竞争力的内存和推理速度，吸引了注重成本的云服务提供商。

旗舰级英伟达Vera Rubin NVL72机架级解决方案每个机架最多可扩展至72个GPU，AWS、Google Cloud、Microsoft Azure和Oracle Cloud是首批部署者。在AMD方面，其新的Helios机架级解决方案也支持每个机架最多72个MI455X GPU，直接与英伟达的NVL72竞争。

英特尔Gaudi 3 GPU与英伟达H100竞争，训练模型速度提升1.5倍且功耗更低。其后续产品Jaguar Shores仍计划于2026年发布，专注于能效。苹果和博通也在联合开发一款名为Baltra的AI专用服务器芯片，用于内部推理任务。

---

## 💻 消费级/本地AI硬件

2026年的内存短缺极大地重塑了本地AI硬件构建市场——消费级DRAM价格较2024-2025年的低点上涨了约300-600%。目前，二手英伟达RTX 3090（24GB显存）为本地AI GPU构建提供了最佳的每GB性价比。

在2026年，硬件开发不再仅仅追求更高时钟频率或更多核心，而是聚焦于效率、并行性和实时推理，使设备能够在本地运行复杂模型，减少对远程数据中心的依赖。

---

## 🎙️ Plaud — AI笔记硬件

Plaud现有产品线包括**Plaud Note**——可贴在手机背面的口袋大小卡片式录音设备，以及**Plaud NotePin**，可作胸针、项链吊坠或腕带佩戴。设备起售价159美元，每月免费包含最多300分钟的转录时长，无需订阅。

在CES 2026上，Plaud发布了**NotePin S**（179美元），新增物理按钮用于开始/停止录音和轻点标记，并推出了一款新的桌面应用，无需机器人加入通话即可转录数字会议。

Plaud的**即将发布的新款可穿戴设备**（2026年晚些时候）标志着一项战略转变——从被动转录工具转向旨在**将数据直接馈送给自主AI代理**的硬件，目标续航8-12小时，并可能支持蜂窝网络连接。

Plaud预计**2026年销售额将达到5亿美元**，用户超过200万，其中美国、日本和欧洲市场约占其业务的80%。

与Otter或Fireflies等纯软件竞争对手相比，Plaud的关键差异化优势在于捕捉**面对面对话**——医生问诊、现场考察、实地工作等软件会议工具无法触及的场景。

---

**参考资料：**
- [2026年值得关注的AI硬件产品](https://airmore.ai/ai-review/ai-hardware-products)
- [2026年AI芯片硬件加速趋势 – Zylos Research](https://zylos.ai/research/2026-02-01-ai-chip-hardware-acceleration-2026/)
- [Plaud计划推出新款可穿戴设备，目标销售额5亿美元 – Bloomberg](https://www.bloomberg.com/news/articles/2026-06-16/plaud-plans-new-wearable-as-ai-note-taking-startup-eyes-500-million-in-sales)
- [Plaud NotePin S发布 – TechCrunch](https://techcrunch.com/2026/01/04/plaud-launches-a-new-ai-pin-and-a-desktop-meeting-notetaker/)
- [Plaud透露将推出无需手机的穿戴设备 – T3 / Yahoo Tech](https://tech.yahoo.com/wearables/articles/plaud-teases-ai-wearable-one-110000748.html)
- [2026年本地AI硬件指南](https://www.modemguides.com/blogs/ai-infrastructure/best-hardware-running-local-ai-models-2026)