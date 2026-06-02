---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 如何在Hermes中显示当前目录
translated: true
type: note
---

```
问题：如何知道当前工作目录？有没有类似 /working-dir 的命令？

回答：

=== 没有专门的 /cwd 命令 ===

Hermes 中没有 /cwd 或 /working-dir 这样的斜杠命令。

=== 查找方法 ===

1. /status —— 不会显示工作目录。它显示：
   - 会话 ID、路径（= ~/.hermes 主目录）、模型、提供商等。

2. 运行时页脚 —— 在运行时页脚中确实有一个 "cwd" 字段可用，但默认是关闭的。要启用它：

     /footer on

   这会在终端底部显示一个持久页脚，包含模型、上下文百分比和 cwd。字段默认为：
   ["model", "context_pct", "cwd"]

3. 直接询问代理 —— 输入：
     当前工作目录是什么？
   它会通过终端工具运行 `pwd` 并告诉你。

4. TUI 模式（--tui）—— 终端标签页标题包含 cwd：
     "◆ <模型> · ~/projects/hermes-agent"
   因此在 TUI 模式下，cwd 在标签页标题中是可见的。

=== 实际的 cwd 值 ===

Hermes 解析工作目录的方式如下：

  terminal.cwd 配置值（在 config.yaml 中）
    -> 如果设置为 "." 或 "auto" 或 "cwd" -> os.getcwd()
    -> 如果为显式路径 -> 该路径
  TERMINAL_CWD 环境变量会覆盖配置
  os.getcwd() 是后备值

实际使用中：你在运行 `hermes` 之前用 `cd` 进入的目录就是工作目录。它在会话期间不会改变。

=== 建议 ===

如果你同时在 5-6 个窗口中切换，需要知道每个窗口在哪个目录下工作：

  /footer on     —— 在每个提示符中添加一个包含 cwd 的持久页脚

或者在 TUI 模式下，它已经显示在标签页标题中。
```

所以快速回答：运行 `/footer on` 可以持久显示 cwd。没有 `/cwd` 命令，但页脚字段存在，只是默认关闭。
