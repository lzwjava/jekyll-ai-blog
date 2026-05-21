---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'PicoRV32: 紧凑型RISC-V核心'
translated: true
type: note
---

本仓库是 **PicoRV32** — 由 **YosysHQ**（Yosys 开源综合工具背后的同一团队）开发的尺寸优化的 RISC-V CPU 核心。

它是一个基于 Verilog 的处理器，实现了 **RISC-V RV32IMC 指令集**（可配置为 RV32E、RV32I、RV32IC、RV32IM 或 RV32IMC）。主要亮点：

- **极小的面积**：在 Xilinx 7 系列 FPGA 上仅需 750–2000 个 LUT
- **高速**：在 7 系列 Xilinx FPGA 上可达 250–450 MHz
- **接口**：原生内存接口、AXI4-Lite 主设备或 Wishbone 主设备
- **可选特性**：内置中断控制器、协处理器接口（PCPI）用于 MUL/DIV 等操作
- **典型用途**：FPGA 设计和 ASIC 中的辅助处理器 — 足够小巧，可嵌入现有设计而不破坏时序收敛

核心 Verilog 模块为 `picorv32.v`，根据所需的总线接口还有变体 `picorv32_axi` 和 `picorv32_wb`。

它采用 ISC 许可证（类似 MIT/BSD 的宽松许可证）。看起来您是从 `github.com/YosysHQ/picorv32` 克隆了上游仓库。您是否有特定的目标 — 综合、仿真或者修改核心？