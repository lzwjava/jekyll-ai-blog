---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Mastering Verilog: Thinking in Hardware"
translated: false
type: note
---

**Question:** How to study Verilog? What open-source projects and runnable code examples exist?

**Answer:**

Verilog is learnable in days syntactically — the hard part is **thinking in hardware** (everything is parallel, time is explicit). Here's the fastest path.

---

## Mental Model Shift First

```
Software mindset:          Hardware mindset:
─────────────────          ────────────────
Sequential execution       Everything runs simultaneously
Functions call each other  Modules exist in parallel always
Variables store values     Wires carry signals RIGHT NOW
Time is implicit           Time is clock edges, explicit
```

This is the #1 stumbling block. A Verilog module isn't a function — it's a **physical circuit that is always on.**

---

## Verilog in 50 Lines — Core Syntax

```verilog
// --- WIRES vs REGISTERS ---
wire a;          // combinational — driven by another module/gate
reg  b;          // sequential — holds value across clock edges

// --- MODULES (the basic unit, like a class but hardware) ---
module adder #(parameter WIDTH=8) (
    input  [WIDTH-1:0] a,
    input  [WIDTH-1:0] b,
    output [WIDTH-1:0] sum,
    output             carry
);
    assign {carry, sum} = a + b;  // combinational, always active
endmodule

// --- ALWAYS BLOCKS ---
// Combinational (no clock):
always @(*) begin
    case (sel)
        2'b00: out = a;
        2'b01: out = b;
        default: out = 0;
    endcase
end

// Sequential (clocked flip-flop):
always @(posedge clk or posedge rst) begin
    if (rst)
        count <= 8'h00;    // non-blocking assignment <=
    else
        count <= count + 1;
end

// --- BLOCKING vs NON-BLOCKING (critical distinction) ---
// = blocking:     executes sequentially within always block (use in comb)
// <= non-blocking: all RHS evaluated first, then assigned (use in sequential)

// --- INSTANTIATION ---
adder #(.WIDTH(16)) my_adder (
    .a(x), .b(y), .sum(result), .carry(c_out)
);
```

---

## Simulation Tools — Run Verilog Now

### Option 1: Icarus Verilog + GTKWave (local, free)

```bash
brew install icarus-verilog gtkwave
# or
sudo apt install iverilog gtkwave
```

Write a module + testbench, simulate:

```verilog
// counter.v
module counter(
    input clk, rst,
    output reg [7:0] count
);
    always @(posedge clk or posedge rst)
        if (rst) count <= 0;
        else     count <= count + 1;
endmodule

// counter_tb.v  (testbench)
module counter_tb;
    reg clk, rst;
    wire [7:0] count;

    counter dut(.clk(clk), .rst(rst), .count(count));

    // generate clock
    initial clk = 0;
    always #5 clk = ~clk;  // toggle every 5ns = 100MHz

    initial begin
        $dumpfile("counter.vcd");  // waveform output
        $dumpvars(0, counter_tb);
        rst = 1; #20;
        rst = 0; #200;
        $finish;
    end

    // monitor output
    initial $monitor("t=%0t count=%d", $time, count);
endmodule
```

```bash
iverilog -o sim counter.v counter_tb.v
./sim
gtkwave counter.vcd   # see the waveform
```

### Option 2: EDA Playground — Zero Install, Browser-Based

Go to **edaplayground.com** — paste Verilog, run in browser. Supports Icarus, Synopsys VCS, Cadence Xcelium. Best for quick experiments.

### Option 3: Verilator — Fastest Simulator, C++ Output

```bash
brew install verilator

# Verilator compiles Verilog → C++ → native binary
# 10-100x faster than Icarus for large designs
verilator --cc counter.v --exe counter_tb.cpp --build
./obj_dir/Vcounter
```

Verilator is what serious open-source projects (including RISC-V cores) use for simulation.

---

## Structured Learning Path

### Stage 1: Combinational Logic (Week 1)

Build these in order, simulate each:

```verilog
// 1. Half adder
module half_adder(input a, b, output sum, carry);
    assign sum   = a ^ b;
    assign carry = a & b;
endmodule

// 2. Full adder
module full_adder(input a, b, cin, output sum, cout);
    assign {cout, sum} = a + b + cin;
endmodule

// 3. 4-to-1 MUX
module mux4(input [3:0] d, input [1:0] sel, output reg out);
    always @(*) out = d[sel];
endmodule

// 4. Priority encoder
module priority_enc(input [3:0] in, output reg [1:0] out, output valid);
    assign valid = |in;
    always @(*) casez(in)
        4'b1???: out = 2'd3;
        4'b01??: out = 2'd2;
        4'b001?: out = 2'd1;
        default: out = 2'd0;
    endcase
endmodule
```

### Stage 2: Sequential Logic (Week 2)

```verilog
// 1. D flip-flop (fundamental building block)
module dff(input clk, rst, d, output reg q);
    always @(posedge clk or posedge rst)
        q <= rst ? 0 : d;
endmodule

// 2. Shift register
module shift_reg #(parameter N=8)(
    input clk, rst, sin,
    output reg [N-1:0] q
);
    always @(posedge clk or posedge rst)
        q <= rst ? 0 : {q[N-2:0], sin};
endmodule

// 3. FIFO — critical for GPU memory pipelines
module fifo #(parameter DEPTH=16, WIDTH=8)(
    input clk, rst, wr_en, rd_en,
    input [WIDTH-1:0] din,
    output reg [WIDTH-1:0] dout,
    output full, empty
);
    reg [WIDTH-1:0] mem [0:DEPTH-1];
    reg [$clog2(DEPTH):0] wr_ptr, rd_ptr, count;

    assign full  = (count == DEPTH);
    assign empty = (count == 0);

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            wr_ptr <= 0; rd_ptr <= 0; count <= 0;
        end else begin
            if (wr_en && !full) begin
                mem[wr_ptr] <= din;
                wr_ptr <= wr_ptr + 1;
                count <= count + 1;
            end
            if (rd_en && !empty) begin
                dout <= mem[rd_ptr];
                rd_ptr <= rd_ptr + 1;
                count <= count - 1;
            end
        end
    end
endmodule
```

### Stage 3: FSM (Week 3) — How Control Logic Works

```verilog
// Simple FSM: detect sequence "1011"
module seq_detector(input clk, rst, in, output reg detected);
    typedef enum reg [1:0] {S0, S1, S2, S3} state_t;
    state_t state, next;

    always @(posedge clk or posedge rst)
        state <= rst ? S0 : next;

    always @(*) begin
        next = S0; detected = 0;
        case (state)
            S0: next = in ? S1 : S0;
            S1: next = in ? S1 : S2;
            S2: next = in ? S3 : S0;
            S3: begin detected = 1; next = in ? S1 : S2; end
        endcase
    end
endmodule
```

FSMs are how **every** GPU control unit, memory controller, and cache arbiter is implemented. This is not academic.

---

## Real Open-Source Projects to Read

### 1. picorv32 — Minimal RISC-V CPU (~2000 lines)

The best first real CPU to read. Clean, well-commented, single file.

```bash
git clone https://github.com/YosysHQ/picorv32
wc -l picorv32.v   # ~3000 lines — read all of it
```

Key things to find inside:
- The fetch/decode/execute FSM
- The register file (32 x 32-bit registers)
- How memory transactions work
- The multiply/divide unit

```bash
# Simulate it running actual RISC-V code
cd picorv32
make test   # runs Icarus simulation
```

### 2. VexRiscv — Pipelined RISC-V in SpinalHDL

More realistic, pipelined, plugin-based architecture:

```bash
git clone https://github.com/SpinalHDL/VexRiscv
# Written in SpinalHDL (Scala-based like Chisel)
# Generates clean Verilog
sbt "runMain vexriscv.demo.GenFull"
# outputs VexRiscv.v — read the generated Verilog
```

### 3. MIAOW — Open-Source AMD GCN GPU

Directly relevant to your MI300X interest:

```bash
git clone https://github.com/VerticalResearchGroup/miaow
ls miaow/src/gpu/
# fetch_decode/   — instruction fetch and decode
# execute/        — ALU, float units
# mem/            — memory pipeline
# simfiles/       — simulation infrastructure
```

Read `miaow/src/gpu/fetch_decode/fetch.v` first — it's where instructions come in.

### 4. Gemmini — Systolic Array (Direct AI Chip Relevance)

```bash
git clone https://github.com/ucb-bar/gemmini
# Written in Chisel, generates Verilog
# This is conceptually what MI300X matrix cores do
ls generators/gemmini/src/main/scala/gemmini/
# Systolic array PE, mesh, controller
```

### 5. OpenTitan — Production-Quality SystemVerilog

Google's open-source silicon project. Real-world code quality:

```bash
git clone https://github.com/lowRISC/opentitan
# 500k+ lines of SystemVerilog
# AES, SHA, RISC-V core, USB, I2C — all open
ls hw/ip/aes/rtl/   # AES hardware accelerator
```

---

## Your Concrete First Week

```bash
# Day 1: Install tools
brew install icarus-verilog gtkwave verilator

# Day 2: Write + simulate counter, adder, mux
# (use the code above, add testbenches, view waveforms)

# Day 3: Build a FIFO, simulate with random write/read

# Day 4: Read picorv32.v top to bottom
git clone https://github.com/YosysHQ/picorv32
cat picorv32.v | grep -A 20 "always @"  # find all FSMs

# Day 5: Run picorv32 simulation
cd picorv32 && make test

# Day 6: Synthesize something with Yosys
yosys -p "read_verilog counter.v; synth -top counter; stat"
# See how many gates your RTL becomes

# Day 7: Browse MIAOW GPU source
git clone https://github.com/VerticalResearchGroup/miaow
```

---

## Key Mental Models to Lock In

| Concept | What it maps to in software |
|---|---|
| `wire` | A live value, like a return value always being computed |
| `reg` | A variable that only updates on clock edge |
| `always @(*)` | A pure function, recomputed when inputs change |
| `always @(posedge clk)` | An event loop tick |
| Module instantiation | Spawning a goroutine that runs forever |
| Testbench | Your `main()` / test harness |
| `$display` | `printf` |
| `$finish` | `exit(0)` |

The hardest concept: **there is no scheduler.** Every `always` block runs in parallel, forever, simultaneously. Synthesis figures out how to wire transistors to implement that behavior.

---

## References

- [picorv32 — minimal RISC-V in Verilog](https://github.com/YosysHQ/picorv32)
- [MIAOW open-source GPU](https://github.com/VerticalResearchGroup/miaow)
- [Gemmini systolic array](https://github.com/ucb-bar/gemmini)
- [EDA Playground — browser simulator](https://edaplayground.com)
- [OpenTitan production SystemVerilog](https://github.com/lowRISC/opentitan)
- [nandland — best beginner Verilog tutorials](https://nandland.com)
- [HDLBits — interactive Verilog exercises](https://hdlbits.01xz.net/wiki/Main_Page)

HDLBits is especially good — it's LeetCode for Verilog, with instant simulation feedback in the browser.
