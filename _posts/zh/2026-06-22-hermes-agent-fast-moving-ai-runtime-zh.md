---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 赫尔墨斯代理：快速移动的AI运行时
translated: true
type: note
---

**问题：** hermes-agent是什么？为什么它是我关注的160多个仓库中更新最频繁的项目？它是否成为了AI编码代理的新标准？

**回答：**

这个项目选得很巧妙。让我为你清晰解析hermes-agent到底是什么、它为何更新如此频繁，以及"新标准"这个说法是否恰当。

## hermes-agent是什么

它**并非**像Claude Code或Aider那样的编码代理，而是更接近一个**个人AI运行时环境**——一个可自托管、持久运行的代理，具备以下特性：

- 可运行在任何LLM上（OpenRouter、Nous Portal、MiMo或你自己的端点）——无供应商锁定
- 通过单一网关进程同时存在于你的终端、Telegram、Discord、Slack和WhatsApp中
- 拥有**闭环学习机制**：能从经验中自主创建并改进"技能"（可重复使用的程序化记忆）
- 支持**子代理并行**——为并行工作流生成独立代理
- 内置计划任务调度——"每天凌晨1点运行夜间备份"，无需配置文件
- 轨迹压缩功能，可为工具调用模型生成训练数据

它本质上是重命名后的**OpenClaw**（注意`hermes claw migrate`命令）——NousResearch将OpenClaw进行了企业级改造，并为其建立了正式的公司背书。

## 为何更新如此频繁（12,076次提交，19.7万星标）

几个结构性原因：

**1. 分叉优先的社区。** 34.9k个分叉意味着成千上万人提交PR。OpenClaw本就拥有庞大的社区；Hermes一夜之间继承了这一切。PR队列已超过5000个。

**2. 广泛的功能覆盖面。** 它并非单一工具——包含：TUI、网关、MCP集成、计划任务、技能系统、轨迹压缩、6种终端后端（本地、Docker、SSH、Singularity、Modal、Daytona），支持Windows/macOS/Linux/Termux。每个模块都是PR的潜在提交点。

**3. 快速发布节奏。** v0.16.0于6月5日发布——这是过去17天内的一次`.0`次版本更新。他们有意识地在快速迭代。

**4. 商业支持+开源。** NousResearch目前正在资助该项目，并利用Nous Portal作为变现层。这是加速开发节奏的常见模式（参考Cursor、Zed等）。

## 它是否是"AI编码的新标准"？

部分正确，但表述不够精确：

| 擅长领域 | 不擅长的领域 |
| --- | --- |
| 持久的个人代理运行时 | 并非专用代码编辑器集成（无LSP支持） |
| 多平台消息代理 | 不直接与Claude Code/Cursor竞争 |
| 通过技能实现自我改进 | 未针对大型代码库导航进行优化 |
| 供应商无关 | 并非微调框架 |
| 轨迹数据生成 | 本身并非模型训练管线 |

对于**AI编码**而言，Claude Code和Cursor在IDE级上下文（文件树、多文件编辑、LSP）方面仍然领先。而Hermes的优势在于**环境性、持久性、多模态代理**的使用场景——即"在你的VPS上常驻并在你睡觉时执行任务的代理"这一类。

## 对你而言真正值得研究的部分

鉴于你的技术方向（CLI代理、ww/iclaw/zz、多模型管线），最值得深入研究的模块包括：

**1. 技能系统（`/skills`、`optional-skills/`）**——如何表示、存储、检索并自动改进程序化知识。这正是你希望在ww中实现的"记忆+学习"模式。

**2. `trajectory_compressor.py`** ——压缩代理交互轨迹用于训练。与你基于MI300X的模型训练工作直接相关。

**3. `acp_adapter/` + `acp_registry/`** ——代理通信协议集成。这正逐渐成为多代理协调的标准。

**4. 网关架构（`gateway/`）** ——如何通过单一代理复用Telegram/Discord/Slack等多个平台。这种干净的设计模式可供你自己的代理借鉴。

**5. `toolset_distributions.py`** ——如何定义和分发工具集。比临时拼凑的工具列表更优。

## 快速上手指引

```bash
# 先安装并探索技能和轨迹系统
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes model  # 指向你的OpenRouter/MiMo端点
hermes tools  # 查看40多个工具

# 研究内部实现：
cd ~/.hermes/hermes-agent
cat trajectory_compressor.py   # 与你的训练工作最相关
ls optional-skills/            # 社区技能示例
cat agent/                     # 核心循环
```

总结：它更新快是因为NousResearch拥有社区动力、广泛的功能范围和商业激励机制。值得特别关注其技能/记忆/轨迹系统。对于你的`ww`代理工作而言，技能系统和轨迹压缩器是迁移性最强的设计理念。

参考资料：

- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
- [hermes-agent文档](https://hermes-agent.nousresearch.com/docs/)
