---
audio: false
generated: true
image: false
lang: en
layout: post
title: Verilog Toolchain and Workflow Guide
translated: false
type: note
---

**Question:** How do you compile Verilog? Are there VSCode plugins, GCC-like compilers, or IDEs for it?

**Answer:**

Yes to all three. Here's the full toolchain map.

---

## The Verilog "Compilation" Pipeline

Unlike C/Java, Verilog has two different end goals:

```
Verilog source
      │
      ├─── Simulation  →  iverilog / verilator  →  runs on your CPU
      │                   (like "gcc + ./a.out" but for hardware behavior)
      │
      └─── Synthesis   →  yosys  →  actual gates  →  FPGA bitstream / GDSII
           (like compiling to a specific CPU architecture, but for silicon)
```

For learning: **simulation first, synthesis later.**

---

## 1. Icarus Verilog — The GCC of Verilog

```bash
# Install
brew install icarus-verilog      # macOS
sudo apt install iverilog        # Ubuntu

# Compile + run (exactly like gcc)
iverilog -o sim counter.v counter_tb.v
./sim

# Analogy:
# iverilog  =  gcc
# ./sim      =  ./a.out
```

Output is a simulation — it tells you what signals would be at each nanosecond if this were real hardware.

---

## 2. Verilator — The Fast Compiler (LLVM-level speed)

Converts Verilog → C++ → native binary. 10-100x faster than Icarus for large designs.

```bash
brew install verilator

verilator --binary -j 0 --trace counter.v --top-module counter
./obj_dir/Vcounter
```

Used by: picorv32, RISC-V cores, serious open-source chip projects.

---

## 3. Yosys — Synthesis (Verilog → Gates)

```bash
brew install yosys

yosys -p "read_verilog counter.v; synth -top counter; stat"
# tells you: how many flip-flops, LUTs, adders your design uses
```

---

## VSCode Setup — Best Lightweight IDE

Install these extensions:

```
1. "Verilog-HDL/SystemVerilog/Bluespec SystemVerilog"
   publisher: mshr-h
   → syntax highlight, lint, ctags navigation

2. "TerosHDL"
   publisher: teros-technology  
   → schematic viewer, testbench generator, documentation

3. "WaveTrace"
   → view .vcd waveform files INSIDE vscode (no GTKWave needed)
```

Install from terminal:

```bash
code --install-extension mshr-h.veriloghdl
code --install-extension teros-technology.teroshdl
code --install-extension wavetrace.wavetrace
```

Configure linting in `settings.json`:

```json
{
  "verilog.linting.linter": "iverilog",
  "verilog.linting.iverilog.arguments": "-Wall",
  "verilog.ctags.path": "ctags"
}
```

Now you get red squiggles on errors, go-to-definition, hover docs.

---

## Full Workflow in VSCode

```bash
mkdir myproject && cd myproject
code .
```

Create `counter.v`:
```verilog
module counter(
    input clk, rst,
    output reg [7:0] count
);
    always @(posedge clk or posedge rst)
        if (rst) count <= 0;
        else     count <= count + 1;
endmodule
```

Create `counter_tb.v`:
```verilog
module counter_tb;
    reg clk = 0, rst = 1;
    wire [7:0] count;
    
    counter dut(.clk(clk), .rst(rst), .count(count));
    
    always #5 clk = ~clk;
    
    initial begin
        $dumpfile("wave.vcd");
        $dumpvars(0, counter_tb);
        #20 rst = 0;
        #200 $finish;
    end
endmodule
```

Terminal inside VSCode:
```bash
iverilog -o sim counter.v counter_tb.v && ./sim
# WaveTrace extension auto-detects wave.vcd — click to open waveform
```

---

## Other IDEs

| Tool | Type | Best for |
|---|---|---|
| **EDA Playground** | Browser | Zero install, share snippets |
| **Vivado** | Full IDE | Xilinx FPGAs, free version exists |
| **Quartus Prime** | Full IDE | Intel FPGAs, free lite version |
| **GTKWave** | Waveform viewer | Viewing `.vcd` simulation output |
| **HDLBits** | Browser exercises | Learning interactively |

For your stage — **VSCode + iverilog + WaveTrace** is all you need. Install in 5 minutes, covers 90% of learning workflow.

---

## Quick Reference — Commands You'll Use Daily

```bash
# Compile and simulate
iverilog -o sim design.v testbench.v && ./sim

# View waveform
gtkwave wave.vcd

# Check syntax only (like gcc -fsyntax-only)
iverilog -tnull design.v

# Synthesize and see gate count
yosys -p "read_verilog design.v; synth -top mymodule; stat"

# Fast simulation with Verilator
verilator --binary --trace design.v -top-module mymodule
```

---

## References

- [Icarus Verilog](https://github.com/steveicarus/iverilog)
- [Verilator](https://github.com/verilator/verilator)
- [mshr-h VSCode extension](https://github.com/mshr-h/vscode-verilog-hdl-support)
- [TerosHDL](https://terostechnology.github.io/terosHDLdoc/)
- [HDLBits interactive exercises](https://hdlbits.01xz.net)
- [EDA Playground](https://edaplayground.com)