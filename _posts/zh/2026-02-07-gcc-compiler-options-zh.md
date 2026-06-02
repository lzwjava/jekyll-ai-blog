---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: GCC 编译器选项指南
translated: true
type: note
---

我将为您详细介绍 GCC (GNU Compiler Collection) 选项，按类别进行组织。

## Basic Usage

基本的 GCC 语法是：
```bash
gcc [options] file...
```

## Essential Compilation Options

**-c** — 将源文件编译为对象文件 (.o) 而不进行 linking
```bash
gcc -c main.c  # 生成 main.o
```

**-o** — 指定输出文件名
```bash
gcc main.c -o myprogram
```

**-E** — 仅进行 preprocess（输出到 stdout）
**-S** — 编译为 assembly (.s) 而不进行 assembling
**-save-temps** — 保留中间文件（preprocessed、assembly、object）

## Optimization Levels

**-O0** — 无优化（默认值，编译速度最快）
**-O1** 或 **-O** — 基础优化
**-O2** — 中度优化（推荐用于生产环境）
**-O3** — 激进优化（可能会增加代码体积）
**-Os** — 针对体积进行优化
**-Ofast** — -O3 加上快速的非标准 math 优化
**-Og** — 针对 debugging 体验进行优化

## Warning Options

**-Wall** — 启用常见警告（大多数项目必备）
**-Wextra** — 除 -Wall 之外的额外警告
**-Werror** — 将警告视为错误
**-pedantic** — 严格的 ISO C/C++ 合规性警告
**-Wno-unused-variable** — 禁用特定警告
**-w** — 抑制所有警告（不推荐）

特定的有用警告：**-Wformat**、**-Wuninitialized**、**-Wshadow**、**-Wconversion**

## Debugging Options

**-g** — 包含 debugging 信息（用于 gdb）
**-ggdb** — 专门为 gdb 生成 debugging 信息
**-g3** — 最大程度的 debug 信息（包含宏定义）
**-p** — 为 prof 生成 profiling 信息
**-pg** — 为 gprof 生成 profiling 信息

## Language Standards

**-std=c89** / **-std=c90** — ANSI C / C90
**-std=c99** — C99 标准
**-std=c11** — C11 标准（近期 GCC 的默认值）
**-std=c17** / **-std=c18** — C17 标准
**-std=gnu11** — 带有扩展的 GNU C11（通常为默认值）

对于 C++：**-std=c++11**、**-std=c++14**、**-std=c++17**、**-std=c++20**、**-std=c++23**

## Include and Library Options

**-I/path/to/headers** — 将目录添加到 include 搜索路径
**-L/path/to/libs** — 将目录添加到 library 搜索路径
**-l<library>** — 链接库（例如 -lm 表示 math library）
**-static** — 进行静态链接而非动态链接
**-shared** — 创建一个 shared library
**-fPIC** — 生成 position-independent code（shared libraries 需要）

示例：
```bash
gcc main.c -I./include -L./lib -lmylib -o program
```

## Preprocessor Options

**-D<macro>=<value>** — 定义 preprocessor 宏
```bash
gcc -DDEBUG=1 -DVERSION=\"1.0\" main.c
```
**-U<macro>** — 取消定义 preprocessor 宏
**-include <file>** — 在处理源文件之前包含文件

## Architecture and Machine Options

**-m32** — 生成 32-bit 代码
**-m64** — 生成 64-bit 代码
**-march=native** — 针对当前 CPU 架构进行优化
**-mtune=<cpu>** — 为特定 CPU 进行调优而不限制指令集
**-msse**、**-msse2**、**-mavx** — 启用特定的 CPU 指令集

## Code Generation Options

**-fno-strict-aliasing** — 禁用严格的别名规则
**-fstack-protector** — 启用 stack 保护
**-fstack-protector-all** — 保护所有函数
**-fomit-frame-pointer** — 不在寄存器中保留 frame pointer
**-fpic** / **-fPIC** — Position-independent code（小/大模型）
**-pie** — 创建 position-independent executable

## Linker Options

**-Wl,<options>** — 将选项传递给 linker
```bash
gcc main.c -Wl,-rpath,/custom/path
```
**-rdynamic** — 导出所有符号用于动态符号解析
**-nostdlib** — 不使用标准系统库
**-nodefaultlibs** — 不使用标准系统库默认值

## Analysis and Sanitizers

**-fanalyzer** — 静态分析（GCC 10+）
**-fsanitize=address** — AddressSanitizer（内存错误）
**-fsanitize=thread** — ThreadSanitizer（数据竞争）
**-fsanitize=undefined** — UndefinedBehaviorSanitizer
**-fsanitize=leak** — LeakSanitizer（内存泄漏）

## Common Combinations

**开发构建：**
```bash
gcc -Wall -Wextra -g -O0 main.c -o program
```

**生产构建：**
```bash
gcc -Wall -O2 -DNDEBUG main.c -o program
```

**最大化警告和调试：**
```bash
gcc -Wall -Wextra -Wpedantic -g3 -Og main.c -o program
```

**带有 sanitizers 的优化构建：**
```bash
gcc -Wall -O2 -g -fsanitize=address,undefined main.c -o program
```

## Verbose and Diagnostic Options

**-v** — 详细输出（显示编译步骤）
**-Q** — 在编译时打印函数名称
**--help** — 显示 GCC 帮助
**-dumpversion** — 打印 GCC 版本
**-print-search-dirs** — 显示库的搜索路径

## Dependency Generation

**-M** — 为 make 生成依赖规则
**-MM** — 类似 -M 但忽略系统头文件
**-MD** — 生成依赖并编译
**-MF <file>** — 指定依赖输出文件

GCC 总共有数百个选项。您可以通过 `man gcc` 或 `gcc --help=<class>` 探索更多，其中 class 可以是 optimizers、warnings、target 等。
