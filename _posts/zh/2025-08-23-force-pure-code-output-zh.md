---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 强制纯代码输出方法
translated: true
type: note
---

明白了——你希望 Claude Code（以及调用它的“路由”工作流）仅输出**代码**，**不包含行内注释/文档字符串/解释性文字**。以下是三种可靠的方法来强制执行这一点，从温和到严格。不使用表格——直接列出步骤。

---

# 1) 将规则放入 `CLAUDE.md`（全局或按项目）

Claude Code 会自动加载“记忆”文件并在不同会话中遵循它们。添加一条简短明确的规则：

**全局（所有项目）：** `~/.claude/CLAUDE.md`
**按项目（纳入版本控制）：** `./CLAUDE.md`

```md
# 输出规则
- 生成代码时，仅输出代码。
- 除非我明确要求，否则不要包含行内注释、块注释、文档字符串或解释性文字。
- 保持信息简洁；如果需要解释，请将其放在代码块之后，并且仅在我要求时这样做。
```

提示：你可以使用 `/memory` 管理这些记忆，并通过在 Claude Code 中以 `#` 开头消息来快速添加新记忆。([Anthropic][1])

---

# 2) 创建一个**自定义输出样式**以禁止注释（更强力）

输出样式会修改 Claude Code 的**系统提示**。创建一个并切换到它：

**创建：**

```
/output-style:new 我想要一个输出样式，总是输出没有任何注释或文档字符串的代码，没有解释。
```

这会在 `~/.claude/output-styles/…` 下创建一个文件。你可以编辑它以确保规则明确无误：

```md
---
name: 仅代码（无注释）
description: 总是发出没有注释/文档字符串的代码；除非被要求，否则不提供解释。
---
# 指令
- 你正处于“仅代码”模式。
- 绝不包含行内注释、块注释或文档字符串。
- 除非明确要求，否则不要在代码前后添加解释性文字。

## 具体行为
- 如果任务暗示需要测试，仅输出测试文件的代码。
- 如果需要澄清，请简要询问，不要解释。
```

**激活：**

```
/output-style "仅代码（无注释）"
```

（输出样式直接更改系统提示；你可以随时使用 `/output-style` 切换。）([Anthropic][2])

---

# 3) 在运行时附加额外的系统提示（最强力 / 每次会话）

如果你从 CLI 或脚本启动 Claude Code，请添加：

```bash
claude --append-system-prompt "总是仅输出代码。没有行内注释，没有块注释，没有文档字符串，除非明确要求，否则没有解释。"
```

你也可以通过 `/config` 设置此项，如果你更喜欢持久的项目设置。（Anthropic 指出你可以使用 `--append-system-prompt` 来修改 Claude Code 的行为。）([Anthropic][3])

---

## 在哪里放置“路由”范围的规则

* 如果你的“Claude Code 路由”只是你在不同代码库中的常规 Claude Code 会话，那么首选**全局记忆** (`~/.claude/CLAUDE.md`) 或**自定义输出样式**，这样规则就能在任何地方生效。([Anthropic][1])
* 如果你通过脚本启动，请将 `--append-system-prompt` 标志嵌入其中，以便每次运行都继承该规则。([Anthropic][3])

---

## 额外防护措施（可选但有用）

* 在项目记忆中，添加一个**“违规”**行，以便模型进行自我检查：“如果你即将输出注释/文档字符串，请停止并移除它们。”
* 如果你有时*需要*注释，可以在提示中添加一次性覆盖：“这次，请包含简要注释。”

就是这样。如果你告诉我你如何启动 Claude Code（桌面版、VS Code、JetBrains 或终端），我可以为你提供一个适用于该设置的即用代码片段。

[1]: https://docs.anthropic.com/en/docs/claude-code/memory "管理 Claude 的记忆 - Anthropic"
[2]: https://docs.anthropic.com/en/docs/claude-code/output-styles "输出样式 - Anthropic"
[3]: https://docs.anthropic.com/en/docs/claude-code/settings "Claude Code 设置 - Anthropic"
