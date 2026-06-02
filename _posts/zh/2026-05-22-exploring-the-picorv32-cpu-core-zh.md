---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 探索PicoRV32 CPU核心
translated: true
type: note
---

以下是关于 PicoRV32 及其用途的完整说明。

---

## 这个项目是什么

PicoRV32 是一个**用 Verilog 编写的 RISC-V RV32IMC CPU 核心**——它不是在你的 Mac 上“运行”的软件，而是**你可以在 FPGA 上仿真或综合的硬件**。你可以把它看作是一个微型处理器的蓝图。它来自 YosysHQ（开源 EDA）生态系统，在 Xilinx 7 系列上约占用 750–2000 LUT，频率可达 250–450 MHz。

## 平台：需要 Linux 还是 macOS？

**两者都可以。**核心开发流程使用以下工具：

| 工具 | 作用 | macOS (Homebrew) | Ubuntu/Linux |
|------|------|------------------|--------------|
| **Icarus Verilog** (`iverilog`/`vvp`) | 在软件中仿真 CPU | `brew install icarus-verilog` | `apt install iverilog` |
| **Verilator** | 更快的周期精确 C++ 仿真 | `brew install verilator` | `apt install verilator` |
| **RISC-V GNU Toolchain** (`riscv32-unknown-elf-gcc`) | 将 C/汇编编译为 RISC-V 二进制文件 | 从源码构建或交叉编译 | 同上；某些发行版有包 |
| **Yosys** | 综合（Verilog → 门级网表） | `brew install yosys` | `apt install yosys` |
| **FPGA 工具**（Vivado、Quartus、IceStorm） | 实际部署到硬件上 | 主要仅支持 x86/Linux/Windows | 是 |

**简答：**对于仿真和学习——macOS 安装 Icarus Verilog 即可。对于实际的 FPGA 综合——你需要你的 Ubuntu 工作站（192.168.1.36）。

## 你在这里实际能做什么

### 第 1 级：运行最简单的测试（无需工具链）

```bash
brew install icarus-verilog   # 一次性安装
cd /Users/lzwjava/projects/picorv32
make test_ez
```

这会运行 `testbench_ez.v` —— 一个最小化的测试平台，实例化了 CPU 并硬编码了一个微型程序。它会打印指令获取、读取和写入。不需要 RISC-V 编译器。在你的 Air 上几秒钟就能运行完毕。

你会看到：CPU 从硬编码的 ROM 中获取伪指令，逐周期执行，`$display` 输出显示每次内存访问。

### 第 2 级：完整测试套件（需要 RISC-V 工具链）

```bash
make test          # 标准测试
make test_vcd      # 生成 VCD 波形，可在 GTKWave 中查看
make test_axi      # 测试 AXI4-Lite 接口变体
make test_verilator  # 更快的 C++ 仿真
```

这会编译 `tests/` 中约 50 个汇编测试文件（add.S、mul.S、div.S 等）为固件 hex 文件，加载到模拟的 CPU 中并全部运行。每个测试测试一条 RISC-V 指令。

### 第 3 级：阅读并理解 CPU 实现

整个 CPU 位于**一个文件**：`picorv32.v`。它大约有 3600 行注释良好的 Verilog。你可以跟踪：

- **取指/译码/执行流水线**（它是多周期而非流水线——更容易理解）
- **压缩 ISA (RV32C)** 指令如何被展开
- **PCPI 协处理器接口** —— MUL/DIV 如何被卸载到 `picorv32_pcpi_mul` 和 `picorv32_pcpi_div`
- **原生内存接口** vs AXI4-Lite vs Wishbone

对于拥有你这种 AI/GPU 背景的人来说，这实际上是一个有趣的项目，因为：

1. 这是一个**真正的硬件设计** —— 你在看门级和触发器级别，最终执行你处理的 ML 模型
2. PCPI（协处理器）模式在概念上类似于 GPU 卸载计算的方式——一个最小化的主机 CPU 加上专用加速器
3. 在这一层级理解 RISC-V 能让你对 Triton/CUDA 代码最终变成指令时发生什么有深刻直觉

### 第 4 级：FPGA 综合（在你的 Ubuntu 工作站上）

`scripts/` 目录包含以下工具的 Makefile：

- **IceStorm**（开源 Lattice iCE40 FPGA 流程）—— `scripts/icestorm/Makefile`
- **Vivado**（Xilinx）—— `scripts/vivado/Makefile`
- **Quartus**（Intel/Altera）—— `scripts/quartus/Makefile`

如果你有一块 FPGA 板（例如 iCEBreaker、TinyFPGA），你可以在真实硬件上运行你编译的 RISC-V 代码。

### 第 5 级：使用 Yosys-SMTBMC 进行形式化验证

```bash
make check-yices   # 使用 SMT 求解器证明 CPU 的属性
```

这会对设计进行形式化属性验证——不仅仅是测试少数输入，而是证明某些行为对所有可能的输入都成立。涉及大量数学，非常酷。

## 对你的 AI 路径最相关的是什么

这个项目更多是“系统好奇心”而非直接与 AI 相关，但它在两个方面有联系：

1. **对 GPU/加速器架构的硬件直觉。** `picorv32.v` 中的 PCPI 接口是现代 AI 加速器将计算单元与控制器耦合的简化版本。理解 CPU 如何将任务分发给协处理器、管理内存映射 IO 以及处理陷阱/中断，能为你提供 NVIDIA CUDA 核心与 warp 调度器之间的关系、Apple ANE 如何与 CPU 并存的思维模型。

2. **Verilog 作为 ML 驱动硬件生成的目标。** 目前有活跃的研究使用 LLM 进行 HDL 生成。如果你未来走向“使用 AI 设计硬件”的方向（这是 Wenfeng Liang / DeepSeek 团队关心的事情），理解一个真实、简洁的 Verilog CPU 是必不可少的背景知识。

## 现在就开始快速上手

```bash
brew install icarus-verilog
cd /Users/lzwjava/projects/picorv32
make test_ez
```

如果 iverilog 已经安装（我可以检查），你只需 10 秒就能在你的 MacBook Air 上看到 RISC-V CPU 在仿真中执行指令。

需要我检查一下已经安装了哪些工具并尝试运行吗？
