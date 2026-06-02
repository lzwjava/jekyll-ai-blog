---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: G++ 编译器选项指南
translated: true
type: note
---

G++ 是 GNU 的 C++ compiler，它是 GCC (GNU Compiler Collection) 套件的一部分。它通过 compilation 和 linking 将 C++ 源代码转换为可执行程序。了解其 options 对于高效的 C++ 开发至关重要。

## Basic Usage

最简单的 g++ 调用是在一个步骤中完成编译和链接：

```bash
g++ program.cpp -o program
```

这将从 `program.cpp` 创建一个名为 `program` 的可执行文件。

## Essential Options

**Output Control**

- `-o <filename>` — 指定输出文件名（如果不指定，默认为 `a.out`）
- `-c` — 仅编译为 object file，不进行 link（生成 `.o` 文件）
- `-S` — 仅生成 assembly code（`.s` 文件）
- `-E` — 仅进行 preprocess，输出到 stdout

**Language Standards**

- `-std=c++11`, `-std=c++14`, `-std=c++17`, `-std=c++20`, `-std=c++23` — 选择 C++ standard 版本
- `-std=gnu++17` — 使用带有 GNU 扩展的 C++17

**Warning Options**

- `-Wall` — 启用大多数常见的 warnings（实际上并不意味着 "all"）
- `-Wextra` — 除 `-Wall` 之外的额外 warnings
- `-Wpedantic` — 严格的 ISO C++ warnings
- `-Werror` — 将 warnings 视为 errors
- `-Wconversion` — 针对可能改变值的隐式转换发出警告
- `-Wshadow` — 当变量遮蔽（shadow）其他变量时发出警告

**Optimization Levels**

- `-O0` — 不进行优化（默认，编译速度最快）
- `-O1` 或 `-O` — 基础优化
- `-O2` — 推荐用于 release builds 的优化
- `-O3` — 激进优化，可能会增加 binary 大小
- `-Os` — 针对大小进行优化
- `-Ofast` — `-O3` 加上不符合标准限制的优化
- `-Og` — 优化但保留可调试性

**Debugging**

- `-g` — 包含 debugging information（用于 gdb, lldb）
- `-g3` — 包含宏定义在内的最大调试信息
- `-ggdb` — 专门为 GDB 准备的调试信息

## Include Paths and Libraries

**Headers**

- `-I<directory>` — 将目录添加到 include 搜索路径
- `-isystem <directory>` — 添加系统 header 目录（抑制来自这些 headers 的警告）

**Libraries**

- `-L<directory>` — 将目录添加到 library 搜索路径
- `-l<library>` — 链接库文件（例如，`-lm` 用于数学库）
- `-static` — 静态链接库，而不是动态链接
- `-shared` — 创建一个 shared library

**Example:**

```bash
g++ app.cpp -I./include -L./lib -lmylib -o app
```

## Preprocessor Options

- `-D<macro>` — 定义预处理器 macro（例如 `-DDEBUG`）
- `-D<macro>=<value>` — 定义带有值的宏
- `-U<macro>` — 取消宏定义
- `-include <file>` — 在处理源码之前包含文件

## Code Generation

- `-fPIC` — 生成 position-independent code（shared libraries 所需）
- `-march=<arch>` — 为特定架构生成代码（例如 `-march=native`）
- `-mtune=<cpu>` — 为特定 CPU 优化而不限制兼容性
- `-m32` / `-m64` — 生成 32-bit 或 64-bit 代码
- `-pthread` — 启用 POSIX thread 支持

## Analysis and Safety

- `-fsanitize=address` — 启用 AddressSanitizer（检测内存错误）
- `-fsanitize=undefined` — 启用 UndefinedBehaviorSanitizer
- `-fsanitize=thread` — 启用 ThreadSanitizer（竞态条件检测）
- `-fstack-protector-strong` — 栈缓冲区溢出保护
- `-D_FORTIFY_SOURCE=2` — 运行时缓冲区溢出保护

## Practical Compilation Patterns

**Debug Build:**

```bash
g++ -std=c++17 -Wall -Wextra -g -Og program.cpp -o program_debug
```

**Release Build:**

```bash
g++ -std=c++17 -Wall -Wextra -O2 -DNDEBUG program.cpp -o program
```

**Multiple Files:**

```bash
# 分别编译
g++ -c -std=c++17 -Wall file1.cpp -o file1.o
g++ -c -std=c++17 -Wall file2.cpp -o file2.o

# 链接在一起
g++ file1.o file2.o -o program
```

**With Sanitizers (开发期间):**

```bash
g++ -std=c++17 -g -fsanitize=address,undefined program.cpp -o program
```

## Advanced Options

- `-v` — 显示所有编译步骤的详细输出
- `-save-temps` — 保留中间文件（preprocessed, assembly）
- `-pipe` — 使用 pipes 代替临时文件（加快编译速度）
- `-fno-exceptions` — 禁用 C++ exception handling
- `-fno-rtti` — 禁用 runtime type information
- `-flto` — 启用 link-time optimization

## Getting Help

- `g++ --help` — 显示简短帮助
- `g++ --help=warnings` — 显示警告选项
- `man g++` — 完整的 manual 页面

日常开发中最常见的组合是：release builds 使用 `-std=c++17 -Wall -Wextra -O2`，debug builds 使用 `-std=c++17 -Wall -Wextra -g -Og`。
