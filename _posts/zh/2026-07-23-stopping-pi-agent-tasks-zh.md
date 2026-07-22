---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 停止pi代理任务
translated: true
type: note
---

问题：当使用 pi agent 进行长时间运行的任务时，如何停止它？

答案：

对于像 **pi agent** 这样的 CLI agent，停止长时间运行的任务通常与停止前台终端进程一样：

```bash
Ctrl + C
```

这会向正在运行的 agent 发送 `SIGINT` 信号。大多数行为良好的 agent 会捕获该信号并优雅地停止。

如果它忽略 `Ctrl+C`：

### 1. 找到进程

```bash
ps aux | grep pi
```

或者：

```bash
pgrep -af pi
```

示例：

```
lzw   12345  ... pi-agent ...
```

### 2. 发送终止信号

```bash
kill 12345
```

如果仍然卡住：

```bash
kill -9 12345
```

`kill -9` 是强制停止（`SIGKILL`），不会进行清理操作。

---

### 如果 pi agent 产生了子进程

有时 agent 会启动：

* `npm install`
* `python`
* `docker`
* 构建任务
* 测试运行器

你可能需要终止进程树：

```bash
pstree -p $(pgrep -f pi)
```

或者：

```bash
pkill -P <父进程ID>
```

---

### 针对 tmux / 远程会话

如果你在 tmux 中运行 agent：

```bash
tmux attach
```

然后：

```
Ctrl+C
```

或者杀死整个会话：

```bash
tmux kill-session -t <会话名称>
```

---

### Agent 原生工作流技巧

对于长时间自主运行的任务，我通常会在单独的会话中运行 agent：

```bash
tmux new -s agent
pi
```

然后你可以分离：

```
Ctrl+B D
```

稍后：

```bash
tmux attach -t agent
```

这样可以避免因关闭终端而意外杀死 agent。

对于 "yolo 模式" agent（跳过确认），tmux + `Ctrl+C` 基本上就是标准的控制循环：让它运行，偶尔检查，在需要时中断。