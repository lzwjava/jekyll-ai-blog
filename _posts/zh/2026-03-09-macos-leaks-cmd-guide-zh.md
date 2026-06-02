---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS 泄漏命令指南
translated: true
type: note
---

**问题：** 如何在 macOS 中使用 `leaks` 命令搜索进程中的内存泄漏？

**答案：**

## 概述

`leaks` 命令用于识别内存泄漏 — 即应用程序已分配但丢失且无法释放的内存。它检查指定进程的内存，寻找可能指向 `malloc` 分配缓冲区的值。从可写全局内存、寄存器或栈中无法到达的任何缓冲区都被视为泄漏。

该工具位于 `/usr/bin/leaks`，并内置于 macOS — 无需安装。

---

## 基本用法语法

```
leaks [options] pid | partial-process-name | memory-graph-file
leaks [options] --atExit -- <command-and-arguments>
```

---

## 方法 1：通过 PID 检查运行中进程

首先使用 `ps` 或 `pgrep` 查找 PID，然后运行：

```bash
# 获取 PID
ps aux | grep MyApp

# 对其运行 leaks
leaks 12345
```

或者直接使用部分进程名：

```bash
leaks MyApp
```

---

## 方法 2：在退出时启动并检查 (`--atExit`)

这是命令行程序最常用且最方便的方法。

```bash
leaks --atExit -- ./my_program
leaks --atExit -- ./my_program arg1 arg2
```

使用 `-atExit` 会自动为指定命令设置 `MallocStackLogging=lite`，以便显示泄漏分配的栈回溯。

要获取完整的栈跟踪细节，手动设置：

```bash
MallocStackLogging=YES leaks -quiet -atExit -- ./my_program
```

---

## 方法 3：在运行前启用栈日志记录

为了获得更丰富的输出，包括分配栈跟踪：

```bash
# 在一个终端中：使用栈日志启动程序
MallocStackLogging=1 ./my_program &

# 在另一个终端中：对其运行 leaks
leaks <PID>
```

---

## 常用选项

##

| Option | Description |
|---|---|
| `-quiet` | 抑制信息输出，仅显示泄漏 |
| `-nocontext` | 不打印泄漏内存的十六进制/字符串内容 |
| `-nostacks` | 跳过打印泄漏块的回溯 |
| `-exclude <symbol>` | 排除回溯中包含给定符号的泄漏（可重复使用） |
| `-trace <address>` | 打印从根到特定块的引用链 |
| `-outputGraph <path>` | 保存 `.memgraph` 文件以供后续分析 |
| `-fullContent` | 在内存图文件中包含完整对象内容 |
| `-list` | 列出所有泄漏块 |
| `-groupByType` | 按类型分组泄漏块 |

`-exclude` 选项允许忽略在您没有源代码的库中分配的泄漏。

---

## 实际示例

**对运行中 app 进行基本检查：**
```bash
leaks Safari
```

**安静模式 — 仅显示泄漏：**
```bash
leaks -quiet --atExit -- ./myapp
```

**带栈跟踪日志：**
```bash
MallocStackLogging=1 leaks -quiet -atExit -- ./myapp
```

**过滤仅显示泄漏行 (grep)：**
```bash
leaks --atExit -- ./myapp | grep LEAK:
```

**排除已知系统泄漏：**
```bash
leaks --atExit -exclude CFRunLoopRun -- ./myapp
```

**保存内存图以供后续分析：**
```bash
leaks --outputGraph /tmp/myapp.memgraph --atExit -- ./myapp
```

**分析保存的内存图：**
```bash
leaks /tmp/myapp.memgraph
```

---

## 环境变量

##

| Variable | Effect |
|---|---|
| `MallocStackLogging=1` | 为所有分配记录栈跟踪 |
| `MallocStackLogging=lite` | 更轻量级的栈日志记录（`-atExit` 会自动使用） |
| `MallocScribble=1` | 用 `0x55` 填充已释放块，减少虚假指针匹配 |

如果目标进程使用 `MallocScribble` 环境变量运行，`leaks` 命令可能会检测到更多泄漏。设置后，已释放的 malloc 块将被 `0x55` 字节填充，覆盖过时指针数据并减少误报。

---

## 退出状态

`leaks` 命令的退出码为：未检测到泄漏时为 `0`，检测到一个或多个泄漏时为 `1`，发生错误时为 `>1`。

这便于在脚本中使用：

```bash
leaks -quiet --atExit -- ./myapp
if [ $? -eq 1 ]; then
    echo "Memory leaks found!"
fi
```

---

## 获得更好结果的提示

- 在单元测试期间运行 `leaks`，因为单元测试会以可重复的方式执行所有代码路径，比生产环境更容易发现泄漏。
- 如果 `leaks` 间歇性地报告泄漏，请在目标代码路径周围设置循环，并运行数百或数千次代码，以增加泄漏一致出现的机会。
- 对于 GUI 替代方案，Xcode 的 **Instruments** 应用包含 Leaks 工具，具有相同的检测功能加上可视化调用树分析。

**参考资料：**

- [leaks man page (unix.com)](https://www.unix.com/man-page/osx/1/leaks/)
- [leaks man page (keith.github.io)](https://keith.github.io/xcode-man-pages/leaks.1.html)
- [Apple Developer: Finding Memory Leaks](https://developer.apple.com/library/archive/documentation/Performance/Conceptual/ManagingMemory/Articles/FindingLeaks.html)
- [EECS 280 Leak Checking Tutorial](https://eecs280staff.github.io/tutorials/setup_leakcheck.html)
- [Detect memory leaks on macOS (Medium)](https://dr-rost.medium.com/detect-memory-leaks-on-macos-4cf257529aa)
