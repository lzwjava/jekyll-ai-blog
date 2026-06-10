---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude Cowork 与 Claude Code 的差异
translated: true
type: note
---

**问题：** Claude桌面应用中，Claude Cowork 与 Claude Code 有何区别？

**回答：**

相同的代理循环，不同的界面，不同的沙箱模型。两者基于相同的模型和相同的代理基础——Code 面向软件开发者，运行于终端/IDE；Cowork 面向知识工作者，运行于桌面应用，无需命令行。对你而言，关键差异在于执行环境与控制方式：

**执行环境（技术层面的关键差异）**

- Cowork 运行在隔离的虚拟机中，与外部网络隔离；Claude Code 更开放地运行在你的系统上。Code 运行在裸机上意味着可访问完整文件系统、真实 shell、真实的 `~/.ssh` 以及真实的环境变量。
- Code 使用操作系统级别的沙箱——Linux 上用 bubblewrap，macOS 上用 seatbelt。Cowork 的代码执行在虚拟机中进行，但其“计算机使用”路径在 Claude 与你的屏幕之间没有沙箱隔离。
- Code 有文档化的企业控制功能：managed-mcp.json、allowedMcpServers/deniedMcpServers 策略文件、HTTP_PROXY/NODE_EXTRA_CA_CERTS、ConfigChange 钩子、OpenTelemetry、审计日志。Cowork 的活动不会被审计日志或合规 API 捕获——鉴于你在银行的背景，这一点很重要。

**运行位置**

- Cowork 仅在 Claude 桌面应用内运行。Claude Code 也可以在桌面应用中运行，此外还能在终端、VS Code 及其他地方运行。因此，即使在同一个桌面应用内，你也可以启动任意一种——桌面应用中的 Code 本质上是同一本地代理的 GUI 包装器，而 Cowork 则是一个独立的基于虚拟机的工作空间。

**能力范围**

- Cowork 的能力范围设计上更广：可访问授权文件夹内的本地文件、通过 Claude in Chrome 进行浏览、在主机应用上使用计算机功能、可捆绑技能+连接器+子代理的插件、计划任务以及移动端派发。
- Code 为你提供完全控制——你可以看到每一步，随时干预，并拥有操作系统提供的一切权限，此外还有 IDE 集成和通过钩子可配置的权限。
- 可靠性方面，Cowork 在处理复杂的多步骤工作流时可能中途停滞；Code 通常能坚持更久。

**针对你的工作流：** 你是一个以终端为先、拥有自定义 CLI 代理（ww、iclaw、zz）的构建者——Claude Code 是你的工具。钩子、MCP 配置文件以及脚本化能力与你现有的自动化流程直接契合。Cowork 主要作为“面向非开发者的代理式 Claude”模式值得了解：通过授权文件夹的虚拟机进行聊天驱动的委派，没有钩子，没有终端。Cowork 可能对你有用的一个场景：文件密集型的非编码杂务（如批量 PDF 提取、文档整理），你不想自己写脚本——不过以你的风格，你可能还是会自己写脚本。

**参考资料：**

- [Claude Cowork vs Claude Code: Enterprise Security Comparison — General Analysis](https://generalanalysis.com/guides/claude-cowork-vs-claude-code)
- [The Difference Between Claude Code and Cowork — Forte Labs](https://fortelabs.com/blog/the-difference-between-claude-code-and-cowork/)
- [Claude Code vs. Claude Cowork — gradually.ai](https://www.gradually.ai/en/claude-code-vs-claude-cowork/)
- [Claude Code vs Cowork — AI blew my mind](https://aiblewmymind.substack.com/p/claude-code-vs-cowork)