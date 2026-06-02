---
audio: false
generated: true
image: false
lang: en
layout: post
title: "PicoRV32: Compact RISC-V Core"
translated: false
type: note
---

This repo is **PicoRV32** — a size-optimized RISC-V CPU core by **YosysHQ** (the same folks behind Yosys open-source synthesis).

It's a Verilog-based processor that implements the **RISC-V RV32IMC instruction set** (configurable as RV32E, RV32I, RV32IC, RV32IM, or RV32IMC). Key highlights:

- **Tiny footprint**: 750–2000 LUTs on Xilinx 7-Series FPGAs
- **Fast**: 250–450 MHz on 7-Series Xilinx FPGAs
- **Interfaces**: native memory interface, AXI4-Lite master, or Wishbone master
- **Optional features**: built-in interrupt controller, co-processor interface (PCPI) for things like MUL/DIV
- **Typical use**: auxiliary processor in FPGA designs and ASICs — small enough to drop into existing designs without breaking timing closure

The core Verilog module is `picorv32.v`, and there are variants `picorv32_axi` and `picorv32_wb` depending on the bus interface you need.

It's licensed under the ISC license (MIT/BSD-like permissive). Looks like you cloned the upstream repo from `github.com/YosysHQ/picorv32`. Is there something specific you're looking to do with it — synthesize it, run simulations, or modify the core?
