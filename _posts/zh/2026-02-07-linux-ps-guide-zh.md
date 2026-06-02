---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Linux ps 命令深度指南
translated: true
type: note
---

我将为您详细介绍 `ps` 命令及其用于列出 process 的选项。

## What is ps?

`ps` 命令用于显示 Unix/Linux 系统中活动 process 的信息。它是 process management 和 system monitoring 最基础的工具之一。

## Basic Usage

最简单的形式是显示当前用户在当前 terminal 中的 process：

```bash
ps
```

## Common Option Styles

`ps` 命令有三种可以混用的选项风格：

1. **Unix options** - 前面带连字符（例如 `-e`）
2. **BSD options** - 不带连字符（例如 `aux`）
3. **GNU long options** - 两个连字符（例如 `--forest`）

## Most Useful Commands

**查看所有用户的所有 process：**

```bash
ps aux          # BSD style
ps -ef          # Unix style
```

**以树状/层级结构查看 process：**

```bash
ps auxf         # BSD style 带有 forest 视图
ps -ef --forest # Unix style 带有 tree 视图
```

**查看特定用户的 process：**

```bash
ps -u username
ps aux | grep username
```

**通过 PID 查看 process：**

```bash
ps -p 1234
ps -p 1234,5678,9101  # 多个 PID
```

## Key Options Explained

### BSD Style (no dash)

- `a` - 显示所有用户的 process
- `u` - 显示面向用户的格式（显示 owner, CPU%, memory% 等）
- `x` - 包含没有控制 terminal 的 process
- `f` - ASCII 艺术风格的 process 层级/forest
- `w` - 宽输出（不要截断 command lines）
- `ww` - 无限制宽度

### Unix Style (with dash)

- `-e` - 选择所有 process
- `-f` - 全格式列出
- `-l` - 长格式
- `-u user` - 特定用户的 process
- `-p pid` - 特定 process ID
- `-C command` - 按 command name 查找 process
- `-o format` - 自定义输出格式
- `--forest` - ASCII 艺术风格的 process 树

## Understanding the Output

当你运行 `ps aux` 时，你会看到如下列：

```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
```

- **USER** - process 所有者
- **PID** - process ID
- **%CPU** - CPU 使用率百分比
- **%MEM** - memory 使用率百分比
- **VSZ** - 虚拟内存大小 (KB)
- **RSS** - 常驻集大小（物理内存，单位 KB）
- **TTY** - 控制 terminal（`?` 表示没有 terminal）
- **STAT** - process 状态：
  - `R` - running
  - `S` - sleeping (interruptible)
  - `D` - sleeping (uninterruptible, 通常是 I/O)
  - `T` - stopped
  - `Z` - zombie
  - `<` - 高优先级
  - `N` - 低优先级
  - `s` - session leader
  - `+` - 前台 process 组
- **START** - process 启动时间
- **TIME** - 累计 CPU 时间
- **COMMAND** - 带有参数的命令

## Custom Output Formats

你可以自定义显示哪些列：

```bash
ps -eo pid,user,%cpu,%mem,command
ps aux --sort=-%cpu | head    # CPU 使用率最高的 process
ps aux --sort=-%mem | head    # 内存使用率最高的 process
```

## Practical Examples

**查找特定 process：**

```bash
ps aux | grep firefox
```

**显示 threads：**

```bash
ps -eLf          # 所有 threads
ps -T -p 1234    # 特定 PID 的 threads
```

**实时监控 process：**

```bash
watch -n 1 'ps aux --sort=-%cpu | head -20'
```

**查看带有完整 command line 的 process：**

```bash
ps auxww | grep process_name
```

**统计 process 数量：**

```bash
ps aux | wc -l
```

**从特定 process 查看 process 树：**

```bash
ps -ef --forest | grep -A 5 process_name
```

## Commonly Used Combinations

```bash
ps aux              # 所有信息，详细
ps -ef              # 所有信息，不同格式
ps auxf             # 带有层级结构的所有信息
ps -u $(whoami)     # 仅显示你的 process
ps -C httpd         # 所有 httpd process
ps -p $$            # 当前 shell process
```

## Tips

- 对于实时监控，请考虑使用 `top` 或 `htop`
- 结合 `grep`、`sort`、`head` 和 `tail` 进行过滤
- 使用 `pgrep` 可以更简单地按名称搜索 process
- 输出可以 pipe 给 `awk` 或 `cut` 以获取特定字段

`ps` 命令非常多才多艺。从 `ps aux` 或 `ps -ef` 开始进行常规概览，然后根据需要添加选项以获取更具体的信息。
