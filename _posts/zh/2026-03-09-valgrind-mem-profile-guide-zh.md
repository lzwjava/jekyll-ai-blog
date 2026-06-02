---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Valgrind 内存剖析指南
translated: true
type: note
---

**问题：** 如何使用 Valgrind 进行内存分析，它在 macOS 上能用吗？

---

**回答：**

## 什么是 Valgrind？

Valgrind 是一套用于调试和分析的工具。它能自动检测内存管理和线程错误，并进行详细的性能分析。当前稳定版本是 3.26.0。

Valgrind 的架构是模块化的，因此可以轻松创建新工具。包含的主要工具有：**Memcheck**（内存错误检测器）、**Cachegrind**（缓存和分支预测分析器）、**Callgrind**（调用图生成缓存分析器）、**Helgrind**（线程错误检测器）和 **DHAT**（堆分析器）。

---

## 安装

**在 Linux (Ubuntu/Debian) 上：**
```bash
sudo apt-get install valgrind
```

**在 macOS 上** — 请参阅下面的 macOS 部分。

---

## 如何使用 Valgrind

### 步骤 1：使用调试符号编译

使用 `-g` 编译程序以包含调试信息，这样 Memcheck 的错误消息就能显示确切的行号。如果可以容忍性能下降，使用 `-O0` 也是个好主意。

```bash
gcc -g -O0 -Wall myprogram.c -o myprogram
```

### 步骤 2：使用 Valgrind 运行

基本语法是：
```bash
valgrind --tool=<toolname> <valgrind-options> ./myprogram [program-args]
```

Memcheck 是默认的 Valgrind 工具，可以使用 `valgrind program` 运行，而无需指定 `--tool=memcheck`。

---

## Memcheck — 内存错误检测

Memcheck 是一个内存错误检测器。它能检测：访问不应访问的内存（例如，堆块溢出、释放内存后访问）、使用未定义/未初始化的值，以及内存泄漏。

**基本命令：**
```bash
valgrind ./myprogram
```

**完整泄漏检查命令：**
```bash
valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all -v ./myprogram
```

**Memcheck 的关键标志：**

| Flag | 描述 |
|---|---|
| `--leak-check=full` | 显示每个独立内存泄漏的详细信息 |
| `--show-leak-kinds=all` | 显示所有类型的泄漏 |
| `--track-origins=yes` | 报告未定义值的来源 |
| `-v` | 详细输出 |

**内存泄漏示例输出：**
```
==17624== HEAP SUMMARY:
==17624==     in use at exit: 40 bytes in 1 blocks
==17624==   total heap usage: 1 allocs, 0 frees, 40 bytes allocated
==17624== LEAK SUMMARY:
==17624==    definitely lost: 40 bytes in 1 blocks
```

使用 Memcheck 时，程序运行速度会比正常运行慢 10 到 30 倍。

---

## Massif — 堆内存分析器

Massif 是一个堆分析器 — 它测量程序使用了多少堆内存。它可以提供堆使用量、堆管理字节和栈大小的信息。堆分析有助于减少程序使用的内存量。

**运行 Massif：**
```bash
valgrind --tool=massif ./myprogram
```

程序结束后，Massif 会打印摘要空间统计信息，并在名为 `massif.<pid>.ps` 的文件中生成表示程序堆使用情况的图表，该文件可由任何 PostScript 查看器读取。

**可视化结果：**
```bash
ms_print massif.out.<pid>
```

---

## Callgrind — 调用图和缓存分析器

使用 Callgrind，只需传递程序可执行文件及其参数：
```bash
valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes --collect-jumps=yes ./myprogram
```

Callgrind 会生成大量关于程序执行的数据。最容易理解的方法是使用 **kcachegrind** GUI 工具，它会创建函数调用列表并附带计时信息。

---

## Valgrind 在 macOS 上能用吗？

**简短回答：原生支持不佳，但有变通方法。**

官方 Valgrind **不支持** 现代 macOS 版本（尤其是 Apple Silicon / M1/M2 芯片）。但是：

1. **社区 macOS 分支**：有一个社区维护的仓库（`LouisBrunner/valgrind-macos`），包含针对 macOS 平台的改进补丁。它可以通过 Homebrew 安装，首先 tap 该仓库。

   ```bash
   export HOMEBREW_NO_INSTALL_FROM_API=1
   brew tap Homebrew/core
   brew tap LouisBrunner/valgrind
   brew install --HEAD LouisBrunner/valgrind/valgrind
   ```

2. **macOS 原生替代 — `leaks`**：`leaks` 是 Mac 电脑上可用的工具，能执行类似于 Valgrind 的内存检查。在运行前，在终端设置 `MallocStackLogging=1` 以保留内存分配信息。

   ```bash
   MallocStackLogging=1 ./myprogram &
   leaks myprogram
   ```

3. **Xcode Instruments**：Apple 的 Xcode 包含 Instruments，提供内存分析功能，是官方推荐的 macOS 替代方案。

4. **AddressSanitizer (ASan)**：一种基于编译器的替代方案，支持 Linux 和 macOS：
   ```bash
   clang -fsanitize=address -g ./myprogram.c -o myprogram
   ./myprogram
   ```

5. **Heapusage**：Heapusage 是一个轻量级工具，用于在 Linux 和 macOS 应用程序中查找堆内存错误。它提供 Valgrind memcheck 功能的一个小子集，适用于无法承受 Valgrind 性能下降的大型/复杂应用程序。

---

## 总结表格

| Tool | Platform | Use Case |
|---|---|---|
| Valgrind Memcheck | Linux (最佳) | 内存泄漏、非法访问 |
| Valgrind Massif | Linux | 堆使用分析 |
| Valgrind Callgrind | Linux | CPU/调用图分析 |
| `leaks` | macOS | 基本内存泄漏检测 |
| Xcode Instruments | macOS | 完整内存/CPU 分析 |
| AddressSanitizer | Linux & macOS | 快速内存错误检测 |

---

**参考资料：**

- [Valgrind Quick Start](https://valgrind.org/docs/manual/quick-start.html)
- [Red Hat: Using Valgrind to Profile Memory](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/performance_tuning_guide/s-memory-valgrind)
- [Valgrind macOS Community Fork](https://github.com/LouisBrunner/valgrind-macos)
- [Mac leaks tool guide](https://computerscience.chemeketa.edu/guides/valgrind/leaks/)
- [Heapusage for macOS](https://github.com/d99kris/heapusage)
- [NERSC Valgrind Guide](https://docs.nersc.gov/tools/debug/valgrind/)
