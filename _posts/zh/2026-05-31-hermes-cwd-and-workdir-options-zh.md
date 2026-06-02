---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes 当前工作目录和工作目录选项
translated: true
type: note
---

现在我已经清楚了。以下是答案：

---

**CWD 对 Hermes 的影响主要体现在两个方面：**

**1. 项目上下文文件（AGENTS.md / CLAUDE.md / .cursorrules）**

当 Hermes 启动时，它会扫描当前工作目录（CWD）以查找这些文件，并将其注入到系统提示中。这是最主要的功能——Hermes 通过这种方式了解项目的结构、约定、构建命令等。来自代码的提示：

> “子目录中的 AGENTS.md 文件会在代理（agent）进入相应文件夹时逐步被发现。”

因此，即使在同一个会话中，如果代理 `cd` 进入一个包含自身 AGENTS.md 的子目录，该文件也会被加载。

**2. 终端工具 CWD（通过 TERMINAL_CWD 环境变量）**

`terminal.cwd` 配置映射到 `TERMINAL_CWD`，该变量决定了 shell 命令的执行位置。这就是 `git status`、`python test.py` 等命令能在正确目录下运行的原因。

---

**你真的需要切换目录吗？**

不需要。在当前会话中，你有三个更好的选择：

1. **终端命令的 `workdir` 参数**——我现在就可以用 `workdir=~/projects/git-credential-manager` 运行任何命令，效果相同。

2. **`--ignore-rules` 标志**——如果你想要一个没有任何 AGENTS.md 的干净会话，可以使用 `hermes --ignore-rules`。

3. **带有 `workdir` 的定时任务**——对于重复性任务，定时任务中的 `workdir` 参数正是用来设置 TERMINAL_CWD 并从该目录加载上下文文件的。

“打开新标签页并 `cd`” 的建议只在以下情况才需要：你希望获得一个永久限定在该项目范围内的完整交互式会话（自动补全、上下文文件、所有终端命令默认在该目录下执行）。对于快速检查或一次性命令，使用终端工具的 `workdir` 参数就能达到同样效果，无需离开当前会话。
