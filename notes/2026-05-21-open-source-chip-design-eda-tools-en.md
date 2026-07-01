---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open-Source Chip Design EDA Tools
translated: false
type: note
---

**Question:** How are chips like AMD MI300X designed? What chip design software (EDA tools) should I learn about?

**Answer:**

Great pivot. This is the **open-source hardware** frontier — the equivalent of Linux vs Windows but for silicon. Let me map the full stack.

---

## The Chip Design Stack (Top to Bottom)

```
Spec / Architecture
        ↓
RTL (Register Transfer Level) — Verilog/VHDL/Chisel
        ↓
Synthesis — RTL → Gate Netlist
        ↓
Place & Route — Gates → Physical Layout
        ↓
Sign-off (Timing, Power, DRC/LVS)
        ↓
GDSII → Foundry (TSMC, Samsung)
        ↓
Silicon
```

MI300X is designed at steps 1-4 by AMD engineers, then fabbed at TSMC N5/N6.

---

## Open Source EDA Tools to Know

### 1. OpenROAD — The Full Open-Source RTL→GDSII Flow

This is the most important one. Backed by DARPA, used in real tapeouts.

```bash
git clone https://github.com/The-OpenROAD-Project/OpenROAD
# Or use the flow wrapper:
git clone https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts

cd OpenROAD-flow-scripts
./build_openroad.sh
# Run a sample design (GCD circuit)
make DESIGN_CONFIG=./flow/designs/asap7/gcd/config.mk
```

What it does: synthesis → floorplan → placement → CTS → routing → sign-off. **Full flow, no license.**

---

### 2. Yosys — RTL Synthesis

Converts Verilog → gate-level netlist. The GCC of chip design.

```bash
brew install yosys  # or apt

# Synthesize a simple module
cat > counter.v << 'EOF'
module counter(input clk, input rst, output reg [7:0] count);
  always @(posedge clk) begin
    if (rst) count <= 0;
    else count <= count + 1;
  end
endmodule
EOF

yosys -p "read_verilog counter.v; synth -top counter; write_json counter.json; stat"
```

Yosys is what OpenROAD uses internally for synthesis. Reading its source teaches you how synthesis actually works.

---

### 3. Chisel — Hardware Description in Scala (What RISC-V uses)

Instead of Verilog (1980s language), Chisel lets you describe hardware programmatically. Used by Google TPU team, Berkeley RISC-V.

```scala
import chisel3._
import chisel3.util._

class Adder(width: Int) extends Module {
  val io = IO(new Bundle {
    val a   = Input(UInt(width.W))
    val b   = Input(UInt(width.W))
    val sum = Output(UInt((width+1).W))
  })
  io.sum := io.a +& io.b  // +& = no overflow truncation
}

// Generates Verilog → feeds into Yosys → OpenROAD
```

```bash
# Install and generate Verilog from Chisel
sbt "runMain Adder --target-dir generated"
# outputs generated/Adder.v
```

**Why relevant to AI chips:** Google's TPU v4 systolic array is described in a Chisel-like DSL. Understanding this is how you understand how matrix engines are built.

---

### 4. Magic VLSI + KLayout — Layout Editors

For looking at actual transistor-level layouts.

```bash
brew install --cask klayout  # GDSII viewer
# Open any open PDK layout file
klayout sky130_fd_sc_hd__and2_1.gds
```

KLayout lets you view the actual GDSII files from open PDKs (SkyWater 130nm). You can literally see the transistors.

---

### 5. SkyWater SKY130 PDK — Free Process Design Kit

The open foundry process. Lets you design chips fabable at SkyWater (via Efabless/Google shuttle).

```bash
git clone https://github.com/google/skywater-pdk
# Contains: cell libraries, SPICE models, DRC rules
ls skywater-pdk/libraries/sky130_fd_sc_hd/  # standard cells
```

This is how you can **actually tapeout** without paying TSMC millions. Google sponsors free shuttles via Efabless.

---

### 6. OpenLane — Sky130 Automated Flow

Wraps Yosys + OpenROAD + Magic for SKY130:

```bash
git clone https://github.com/The-OpenROAD-Project/OpenLane
cd OpenLane
make
make mount
# Inside container:
./flow.tcl -design spm  # runs full RTL→GDSII on a sample design
```

This is what people use to submit to Google's free chip shuttle. Real chips have been fabbed this way.

---

## How MI300X Is Actually Designed (High Level)

```
1. Architecture spec
   - Compute Units count, cache hierarchy, HBM interface
   - Written in documents, not code

2. RTL (Verilog/SystemVerilog) — millions of lines
   - Each functional block: shader core, memory controller,
     Infinity Fabric links, display engine
   - AMD uses internal proprietary tools here (Synopsys DC, Cadence Genus)

3. Verification (the hard part — 60-70% of effort)
   - SystemVerilog assertions
   - UVM testbenches
   - Formal verification (sby / Cadence JasperGold)

4. Synthesis → Cadence Genus or Synopsys DC
   (equivalent of Yosys but $1M/year licenses)

5. Place & Route → Cadence Innovus or Synopsys ICC2
   (equivalent of OpenROAD but $5M/year)

6. Sign-off → Synopsys PrimeTime (timing), Mentor Calibre (DRC/LVS)

7. GDSII → TSMC N5 foundry
```

The open-source tools cover exactly the same **concepts** as the commercial ones — just slower and less mature. Learning OpenROAD teaches you what Cadence Innovus does.

---

## The AI Chip Specific Part — Systolic Arrays

The core of MI300X's matrix engine (and any AI accelerator) is a **systolic array** for GEMM. Here's a minimal Chisel implementation to understand the concept:

```scala
// Minimal PE (Processing Element) for systolic array
class PE extends Module {
  val io = IO(new Bundle {
    val a_in  = Input(SInt(8.W))   // weight flowing right
    val b_in  = Input(SInt(8.W))   // activation flowing down
    val c_in  = Input(SInt(32.W))  // partial sum flowing down
    val a_out = Output(SInt(8.W))
    val b_out = Output(SInt(8.W))
    val c_out = Output(SInt(32.W))
  })
  // Register inputs (pipeline stage)
  val a_reg = RegNext(io.a_in)
  val b_reg = RegNext(io.b_in)

  io.a_out := a_reg
  io.b_out := b_reg
  io.c_out := RegNext(io.c_in + (a_reg * b_reg))
}
```

Array of these PEs = matrix multiply engine. MI300X's CDNA3 has 228 Compute Units each with matrix cores doing 4x4 or 16x16 tiles of this.

---

## Learning Path for You

Given your background (systems, GPU compute, LLM training):

```
Week 1-2:  Verilog basics → write a simple ALU, FIFO, counter
Week 3-4:  Yosys synthesis → understand what gates your RTL becomes
Week 5-6:  OpenLane/OpenROAD → run the full flow on SKY130
Week 7-8:  Chisel → rewrite your RTL in Chisel, understand the abstraction
Week 9+:   Read actual GPU RTL — MIAOW (open-source AMD GCN clone)
```

**MIAOW** is an open-source implementation of AMD's GCN ISA in Verilog — literally an open-source GPU:

```bash
git clone https://github.com/VerticalResearchGroup/miaow
# Real Verilog implementation of AMD GCN shader core
```

---

## Key Repos to Star Now

| Repo | What it teaches |
| --- | --- |
| `The-OpenROAD-Project/OpenROAD` | Full RTL→GDSII flow |
| `YosysHQ/yosys` | Synthesis internals |
| `chipsalliance/chisel` | HW description in Scala |
| `google/skywater-pdk` | Real process node data |
| `VerticalResearchGroup/miaow` | Open-source GPU RTL |
| `ucb-bar/gemmini` | Open-source systolic array (RISC-V) |
| `efabless/caravel` | Open-source chip harness for tapeout |

`gemmini` is especially relevant — it's a configurable systolic array generator from Berkeley, used in research. Direct conceptual analog to TPU/MI300X matrix engines.
