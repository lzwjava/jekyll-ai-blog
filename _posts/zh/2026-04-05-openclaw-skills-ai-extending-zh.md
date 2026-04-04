---
audio: false
generated: true
image: false
lang: zh
layout: post
title: OpenClaw技能：拓展AI能力
translated: true
type: note
---

**问题：** OpenClaw（AI代理）中的“技能”指什么？

**回答：**

## OpenClaw中的技能是什么？

在OpenClaw中，**技能**是模块化、可安装的能力包，用于告知AI代理*如何*执行特定任务。它们本质上是OpenClaw的插件系统——这是代理获得除基础对话之外新能力的机制。

---

### 核心定义

技能是扩展代理能力的模块化功能，涵盖诸如CRM更新、邮件自动化、支付处理、日历管理、文档生成等任务。

从技术上讲，一个技能是一个包含`SKILL.md`文件（内含元数据和执行脚本）的目录。本质上，这些以Markdown编写的指令教导代理如何执行特定功能。

---

### 技能在代理循环中如何工作

当您输入命令时，模型会解读指令并决定所需行动。随后，OpenClaw使用其“技能”（如shell命令、浏览器或API）执行任务。结果将返回给代理，代理会持续工作直至任务完成。

更具体地说，当代理运行时在调用AI模型前组装上下文时，它会包含一个“技能提示”——一个符合条件的技能（名称、描述、路径）的紧凑列表，用于告知模型当前有哪些可用技能。接着，模型决定调用哪个（哪些）技能。

---

### 技能生态系统（ClawHub）

OpenClaw拥有一个名为ClawHub的公共注册中心，托管超过13,000个可安装技能。这些技能充当AI代理的“操作手册”。开发者和用户无需硬编码集成，而是可以通过安装技能来教导代理新能力。

一个完整的技能大约只需20行代码即可实现，这也是该生态系统得以迅速发展的原因。

---

### 技能能做什么

技能的范围从与API交互到控制智能设备或总结文档。主要类别包括：

- **编程与DevOps**（最大的类别，约占总技能的45%）
- **生产力**工具（邮件、日历、任务管理）
- **网络搜索/研究**
- **家庭自动化**（智能灯光、物联网设备）
- **媒体与创意任务**（图像生成、音频处理）

---

### 自创技能

如果现有技能无法满足您的需求，您可以向代理描述任务，并让它草拟一个新技能。OpenClaw被描述为“自我改进”，因为它能够自主编写代码以创建相关的新技能来执行所需任务。

---

### 安全警告

技能可从ClawHub安装或从头编写。思科研究人员曾警告，社区技能可能实现静默数据窃取和类似提示注入的滥用行为。Snyk安全审计扫描了数千个社区技能，发现相当一部分存在严重问题，包括提示注入、恶意软件和凭证窃取。在安装技能前，请务必仔细审查，尤其是那些与电子邮件或浏览器自动化等敏感工具交互的技能。

---

### 总结

| 方面 | 细节 |
|---|---|
| **格式** | Markdown文件（`SKILL.md`）+ 执行脚本 |
| **注册中心** | ClawHub（13,000+个技能） |
| **目的** | 模块化扩展代理能力 |
| **示例** | 浏览器自动化、邮件、API、智能家居、编程 |
| **自创功能** | 代理可按需编写新技能 |
| **风险** | 社区技能可能包含恶意软件或安全漏洞 |

**参考资料：**

- [OpenClaw - 维基百科](https://en.wikipedia.org/wiki/OpenClaw)
- [什么是OpenClaw？完整指南 - Milvus博客](https://milvus.io/blog/openclaw-formerly-clawdbot-moltbot-explained-a-complete-guide-to-the-autonomous-ai-agent.md)
- [OpenClaw详解 - KDnuggets](https://www.kdnuggets.com/openclaw-explained-the-free-ai-agent-tool-going-viral-already-in-2026)
- [什么是OpenClaw？ - DigitalOcean](https://www.digitalocean.com/resources/articles/what-is-openclaw)
- [OpenClaw技能列表指南 - Skywork AI](https://skywork.ai/skypage/en/openclaw-skill-list-ai-agents/2038602600443363328)
- [OpenClaw工作原理 - Medium](https://bibek-poudel.medium.com/how-openclaw-works-understanding-ai-agents-through-a-real-architecture-5d59cc7a4764)
- [什么是OpenClaw - Vida AI](https://vida.io/blog/what-is-openclaw)