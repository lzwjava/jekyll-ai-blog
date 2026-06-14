---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在SSH和tmux之间恢复Hermes
translated: true
type: note
---

问题：假设我们在服务器的SSH会话中运行Hermes Agent，然后取消它并退出。我们能在一个tmux会话中恢复它吗，或者反过来？

答案：

### 核心概念

是的，完全可以。你可以毫无障碍地在原始SSH会话和`tmux`会话之间切换你的Hermes Agent工作区。然而，理解这种切换在框架架构中的**确切**工作方式非常重要，因为根据你是想恢复**进程**还是恢复**状态**，有两种完全不同的实现方法。

---

### 方法一：通过Hermes原生会话管理恢复（推荐）

Hermes Agent原生将会话管理抽象为一个持久化的SQLite状态数据库（`state.db`）。每一个对话、记忆上下文和工具状态都由唯一的会话ID或可读的标题自动追踪。

如果你在Agent运行时突然终止或断开SSH终端：

1. 操作系统可能通过挂断信号（`SIGHUP`）终止物理OS进程。
2. Agent的进度和对话上下文安全地存储在数据库中。

要在`tmux`会话（或反过来）中恢复工作：

* 重新登录到服务器，并附加/打开你的`tmux`会话。
* 运行以下命令，从你中断的地方继续：

```bash
hermes --continue
# 或者使用简写标志：
hermes -c

```

> **注意：** `--continue`或`-c`标志会自动将你重新附加到最近的会话。如果你想要一个特定的过去会话，可以使用`hermes sessions list`列出它们，并通过`hermes --resume <会话ID或标题>`恢复。
> 你也可以在TUI中选择自动恢复行为，方法是在shell配置中设置环境变量`export HERMES_TUI_RESUME=1`。

---

### 方法二：通过Linux进程持久化（`tmux`）恢复

如果你真正的目标是在SSH断开时不让Agent的运行终端进程被中断，你应该从一开始就在`tmux`**内部**启动Hermes。

* **标准的SSH陷阱：** 如果你直接在原始SSH会话中启动`hermes`并关闭终端窗口，操作系统会杀死你的终端shell及其内部运行的所有内容。你仍然可以使用方法一（`hermes -c`）将状态历史加载到新进程中，但在断开瞬间正在积极处理的任何长时间运行的工具或生成循环都将被中止。
* **多路复用器的优势：** 如果你登录SSH，启动一个`tmux`多路复用器（`tmux new -s hermes_session`），并在其中运行`hermes`，则该进程属于持久的`tmux`服务器。如果你的SSH连接断开，Agent会在后台继续执行。稍后你可以通过SSH重新连接，并运行`tmux a -t hermes_session`来查看与你离开时完全一致的实时终端输出。
