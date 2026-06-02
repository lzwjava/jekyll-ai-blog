---
audio: false
generated: true
image: false
lang: en
layout: post
title: Exploring the PicoRV32 CPU Core
translated: false
type: note
---

Here's the full picture on PicoRV32 and what you can do with it.

---

## What This Project Is

PicoRV32 is a **RISC-V RV32IMC CPU core written in Verilog** — not software you "run" on your Mac, but **hardware you simulate or synthesize onto an FPGA**. Think of it as the blueprint for a tiny processor. It's from the YosysHQ (open-source EDA) ecosystem, ~750–2000 LUTs on Xilinx 7-series, can hit 250–450 MHz.

## Platform: Does It Need Linux or macOS?

**Either works.** The core development flow uses:

| Tool | Role | macOS (Homebrew) | Ubuntu/Linux |
|------|------|------------------|--------------|
| **Icarus Verilog** (`iverilog`/`vvp`) | Simulate the CPU in software | `brew install icarus-verilog` | `apt install iverilog` |
| **Verilator** | Faster cycle-accurate C++ simulation | `brew install verilator` | `apt install verilator` |
| **RISC-V GNU Toolchain** (`riscv32-unknown-elf-gcc`) | Compile C/asm → RISC-V binaries | Build from source or cross-compile | Same; some distros have packages |
| **Yosys** | Synthesis (Verilog → gate netlist) | `brew install yosys` | `apt install yosys` |
| **FPGA tools** (Vivado, Quartus, IceStorm) | Actually put it on hardware | Mostly x86/Linux/Windows only | Yes |

**The short answer:** For simulation and learning — macOS is fine with Icarus Verilog installed. For actual FPGA synthesis — you'll want your Ubuntu workstation (192.168.1.36).

## What You Can Actually Do Here

### Level 1: Run the simplest test (no toolchain needed)

```bash
brew install icarus-verilog   # one-time
cd /Users/lzwjava/projects/picorv32
make test_ez
```

This runs `testbench_ez.v` — a minimal testbench that instantiates the CPU with a hardcoded tiny program. It prints instruction fetches, reads, and writes. No RISC-V compiler needed. Runs in seconds on your Air.

What you'll see: the CPU fetching fake instructions from a hardcoded ROM, executing them cycle by cycle, with `$display` output showing every memory access.

### Level 2: Full test suite (needs RISC-V toolchain)

```bash
make test          # standard tests
make test_vcd      # generates VCD waveform you can view in GTKWave
make test_axi      # tests the AXI4-Lite interface variant
make test_verilator  # faster C++ simulation
```

This compiles the ~50 assembly test files in `tests/` (add.S, mul.S, div.S, etc.) into a firmware hex file, loads it into the simulated CPU, and runs them all. Each test exercises one RISC-V instruction.

### Level 3: Read and understand the CPU implementation

The entire CPU is **one file**: `picorv32.v`. It's ~3600 lines of well-commented Verilog. You can trace:

- The **fetch/decode/execute pipeline** (it's multi-cycle, not pipelined — simpler to understand)
- How **compressed ISA (RV32C)** instructions get expanded
- The **PCPI co-processor interface** — how MUL/DIV get offloaded to `picorv32_pcpi_mul` and `picorv32_pcpi_div`
- The **native memory interface** vs AXI4-Lite vs Wishbone

This is actually an interesting project for someone with your AI/GPU background because:

1. It's a **real hardware design** — you're looking at the gates-and-flip-flops level that ultimately executes the ML models you work with
2. The PCPI (co-processor) pattern is conceptually similar to how GPUs offload compute — a minimalist host CPU + specialized accelerators
3. Understanding RISC-V at this level gives you deep intuition for what happens when your Triton/CUDA code eventually becomes instructions

### Level 4: FPGA synthesis (on your Ubuntu workstation)

The `scripts/` directory has Makefiles for:
- **IceStorm** (open-source Lattice iCE40 FPGA flow) — `scripts/icestorm/Makefile`
- **Vivado** (Xilinx) — `scripts/vivado/Makefile`
- **Quartus** (Intel/Altera) — `scripts/quartus/Makefile`

If you have an FPGA board (e.g., iCEBreaker, TinyFPGA), you can actually run your compiled RISC-V code on real hardware.

### Level 5: Formal verification with Yosys-SMTBMC

```bash
make check-yices   # proves properties about the CPU using SMT solvers
```

This formally verifies properties of the design — not just testing a few inputs, but proving certain behaviors hold for all possible inputs. Heavy math, very cool.

## What's Most Relevant to Your AI Path

This project is more "systems curiosity" than direct AI work, but it connects in two ways:

1. **Hardware intuition for GPU/accelerator architecture.** The PCPI interface in `picorv32.v` is a simplified version of how modern AI accelerators couple compute units to a control processor. Understanding how a CPU dispatches to a co-processor, manages memory-mapped IO, and handles traps/interrupts gives you mental models for how NVIDIA's CUDA cores relate to the warp scheduler, or how Apple's ANE sits alongside the CPU.

2. **Verilog as a target for ML-driven hardware generation.** There's active research in using LLMs for HDL generation. If you ever go in the direction of "use AI to design hardware" (which Wenfeng Liang / DeepSeek folks care about), understanding a real, clean Verilog CPU is essential context.

## Quick Start Right Now

```bash
brew install icarus-verilog
cd /Users/lzwjava/projects/picorv32
make test_ez
```

If iverilog is already installed (I can check), you're 10 seconds from seeing a RISC-V CPU execute instructions in simulation on your MacBook Air.

Want me to check what's already installed and try running it?
