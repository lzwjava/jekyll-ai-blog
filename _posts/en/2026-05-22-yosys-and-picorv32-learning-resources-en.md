---
audio: false
generated: true
image: false
lang: en
layout: post
title: Yosys and PicoRV32 Learning Resources
translated: false
type: note
---

**Question:** What is Yosys, what company/org is behind it, and is the PicoRV32 repo a good resource for learning Verilog/GPU/hardware design?

**Answer:**

## What is Yosys?

Yosys is an open-source **RTL synthesis framework** — it takes Verilog hardware description code and converts it into a gate-level netlist. Think of it as the "compiler" for hardware, analogous to how GCC compiles C to machine code, except Yosys compiles Verilog to logic gates.

The pipeline:
```
Verilog HDL → [Yosys] → Gate-level netlist → [nextpnr/place-and-route] → FPGA bitstream / ASIC layout
```

What that `stat` command shows you:
```
Number of wires:                 23
Number of cells:                 14
  $_DFF_P_                        4   ← flip-flops (registers, state)
  $_NOT_                          2   ← inverters
  $_MUX_                          3   ← multiplexers
  $_ADD_                          2   ← adders
  LUT4                            3   ← look-up tables
```

This tells you the **resource cost** of your RTL design — directly analogous to counting FLOPs in a neural network. For a 4-bit counter you'd expect exactly 4 flip-flops (one per bit).

---

## Who is Behind Yosys?

**Not a Fortune 500, not a typical startup.** It's a different category entirely:

| | |
|---|---|
| **Author** | Claire Xenia Wolf (formerly Clifford Wolf) — independent hacker/researcher |
| **Organization** | [YosysHQ](https://github.com/YosysHQ) — a tiny open-source focused company |
| **Model** | Open-core: Yosys itself is MIT licensed; YosysHQ sells commercial support and proprietary add-ons (Tabby CAD Suite) |
| **Founded** | Yosys started ~2012 as a research project |
| **Team size** | ~10-20 people range |
| **Funding** | Bootstrapped / consulting / commercial licenses — not VC-backed |

It's the **LLVM/GCC of hardware synthesis** — widely used in academia and increasingly in industry, with massive community contribution. Companies like Google, efabless, and others use it in production chip flows (e.g., Google's OpenMPW shuttle program).

---

## PicoRV32 — Is It Good Learning Material?

Yes, **extremely good**, and specifically for you as someone moving toward AI hardware/GPU internals.

[picorv32](https://github.com/YosysHQ/picorv32) is a **compact, clean RISC-V CPU implementation in ~3000 lines of Verilog**, also by Claire Wolf. It's:

- Synthesizable on real FPGAs
- Used in production silicon (Google's Skywater PDK tapeouts)
- Designed to be readable — not optimized for obfuscation

**Why it matters for your AI engineering trajectory:**

```
GPU = thousands of shader cores, each is basically a simplified CPU
↓
Understanding a simple CPU in RTL (PicoRV32)
↓
Understanding how compute pipelines work at the gate level
↓
Understanding why memory bandwidth >> compute is the GPU bottleneck
↓
Understanding KV cache, CUDA warp scheduling, tensor core layout
```

Reading PicoRV32 will teach you:

- **Register file** — how weights/activations live in hardware registers
- **ALU pipeline** — how matrix ops decompose to add/multiply at gate level  
- **Memory interface (AXI/Wishbone)** — foundation for understanding HBM, GDDR, memory coalescing
- **Stall/hazard logic** — directly analogous to GPU warp stalls on memory latency

---

## Practical Yosys Workflow for Learning

```bash
# Install
brew install yosys

# Write a simple module
cat > counter.v << 'EOF'
module counter (
  input clk, rst,
  output reg [3:0] count
);
  always @(posedge clk) begin
    if (rst) count <= 0;
    else     count <= count + 1;
  end
endmodule
EOF

# Synthesize and inspect
yosys -p "
  read_verilog counter.v;
  synth -top counter;
  stat;
  show;          # generates graphviz of gate netlist
"

# For PicoRV32
git clone https://github.com/YosysHQ/picorv32
cd picorv32
# Synthesize the whole CPU, see how many flip-flops a CPU takes
yosys -p "read_verilog picorv32.v; synth -top picorv32; stat"
```

Running `stat` on PicoRV32 will show you ~2000-4000 cells — that's a real CPU in gate count. Grounding intuition for "how complex is this?" at the hardware level is invaluable when you're thinking about GPU die area, power budgets, and why tensor cores are shaped the way they are.

---

## Learning Path Recommendation for You

Given your trajectory toward GPU/AI hardware understanding:

```
PicoRV32 (read the Verilog) 
  → nanoGPT (which you've already done)
  → understand why matmul maps so well to GPU tensor cores
  → read "Why is GPU programming so hard?" by Tim Dettmers
  → CUDA kernel writing (you can map back to RTL mental model)
```

The hardware → software stack becomes much less magical once you've read a CPU in Verilog. It's the same skill that makes Karpathy's "building GPT from scratch" valuable — you stop treating the hardware as a black box.

**References:**

- [YosysHQ/yosys](https://github.com/YosysHQ/yosys)
- [YosysHQ/picorv32](https://github.com/YosysHQ/picorv32)
- [YosysHQ company site](https://www.yosyshq.com/)
- [OpenMPW / Google + Yosys in production](https://efabless.com/open_shuttle_program)