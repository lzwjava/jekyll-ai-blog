---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为tmux会话命名
translated: true
type: note
---

问题：如何创建带有名称的tmux会话？

答案：

要创建带有自定义名称的tmux会话，请使用`tmux new-session`命令（或其简写形式`tmux new`）的`-s`标志。

### 基本命令

```bash
tmux new-session -s 会话名称
```

**示例：**

```bash
tmux new-session -s myproject
```

这将创建一个名为“myproject”的新tmux会话并立即附加到该会话。

### 简写版本

```bash
tmux new -s myproject
```

### 其他实用选项

- **在分离状态下启动**（在后台创建会话而不附加）：

  ```bash
  tmux new -s myproject -d
  ```

- **指定工作目录**：

  ```bash
  tmux new -s myproject -c ~/projects/myapp -d
  ```

- **在会话启动时运行命令**：

  ```bash
  tmux new -s myserver -c ~/projects -d "python run_server.py"
  ```

### 常见工作流程示例

1. **创建并附加会话**：

   ```bash
   tmux new -s dev
   ```

2. **创建分离会话**（适用于脚本或希望先设置多个会话的场景）：

   ```bash
   tmux new -s frontend -d
   tmux new -s backend -d
   tmux new -s database -d
   ```

3. **附加到现有命名会话**：

   ```bash
   tmux attach -t myproject
   ```

4. **列出所有会话**（查看会话名称）：

   ```bash
   tmux list-sessions
   ```

   或更简短的命令：

   ```bash
   tmux ls
   ```

### 在现有tmux会话内部操作

如果你已处于tmux会话内部，并想创建新的命名会话：

- 按`Ctrl+b`（默认前缀键），然后输入`:new -s 新名称`并按Enter键。

### 重命名现有会话

```bash
tmux rename-session -t 旧名称 新名称
```

或在tmux内部操作：`Ctrl+b`后输入`:rename-session 新名称`

### 专业建议

- 会话名称应具描述性且简洁（例如`web`、`api`、`logs`、`project-v2`）。
- 名称中可使用下划线`_`或连字符`-`。
- 终止会话的方法：`tmux kill-session -t 会话名称`

此方法适用于Linux、macOS以及任何安装了tmux的系统。

参考文献：

- [tmux手册页](https://man7.org/linux/man-pages/man1/tmux.1.html)
