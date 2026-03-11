---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 危险标志忽略目录限制
translated: true
type: note
---

问题：
在 Claude Code 中，使用 `--dangerously-skip-permissions` 时，它是否仅在当前目录生效，并且会避免删除当前目录外的文件？

回答：

否。该标志 `--dangerously-skip-permissions` **不受当前目录限制**。它 **不会将 Claude 沙箱限制在当前工作目录**，并且 **可能修改或删除当前目录外的文件**，具体取决于它运行的命令或工具。

### 1. 该标志实际的作用

当你使用以下命令启动 Claude Code 时：

```
claude --dangerously-skip-permissions
```

你启用了 **bypass permissions mode**（有时称为 *YOLO mode*）。在此模式下：

* 所有工具操作 **自动批准**
* 不会出现确认提示
* Claude 可以运行：

  * file read/write operations
  * shell commands
  * network requests
  * git commands
  * system operations

一切操作 **无需用户确认** 即可执行。([AGCMD][1])

### 2. 作用范围是整个环境，而非仅当前目录

CLI 本身 **不会强制执行目录边界**。如果 Claude 决定运行像这样的 shell 命令：

```
rm -rf ../some_folder
```

或

```
rm -rf ~
```

如果操作系统允许，这些命令将正常运行。

因此有效范围是：

* **当前用户账户有权限访问的一切**
* 不仅仅是项目文件夹

这意味着它理论上可能影响：

* 父目录
* 你的 home directory
* 系统文件（如果以提升权限运行）

### 3. 为什么该标志名为“dangerously”

该标志名称故意明确，因为它移除了所有安全检查。这意味着单个错误的指令或幻觉命令可能导致破坏性操作，例如删除文件或修改系统状态。([ClaudeLog][2])

可能后果的示例：

* 意外的 `rm -rf` 命令
* 破坏性的 git 操作
* 修改配置文件
* 覆盖无关目录

### 4. 开发者通常如何使其安全

经验丰富的用户通常在 **隔离环境** 中运行它，例如：

1. **容器内**

   * Docker devcontainer
   * ephemeral CI runner

2. **项目工作区内**

   * 仅挂载 repo 文件夹

3. **使用 git 保护**

   * 如需回滚更改

示例安全工作流程：

```
docker run -it -v ./project:/workspace dev-env
cd /workspace
claude --dangerously-skip-permissions
```

这样，最坏情况下的损害仅限于 `/workspace`。

### 5. 实用经验法则

将此标志视为：

> “Claude 可以运行你在终端中能运行的任何命令。”

因此它 **不受目录范围限制**，并且 **可以修改当前文件夹外的文件**。

如果想要更安全的行为，请使用：

* `allowedTools` 配置
* 权限提示
* 容器化环境

---

如果你愿意，我也可以解释 **Codex、Claude Code 和 Cursor 如何不同地沙箱文件访问**，因为它们的安全模型实际上大不相同。

[1]: https://agcmd.com/?utm_source=chatgpt.com "claude --dangerously-skip-permissions | Skip Permissions Claude Code CLI"
[2]: https://claudelog.com/faqs/what-is-dangerously-skip-permissions/?utm_source=chatgpt.com "What is Dangerously Skip Permissions in Claude Code | ClaudeLog"