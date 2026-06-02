---
audio: false
generated: true
image: false
lang: en
layout: post
title: Icarus Verilog Simulation Workflow
translated: false
type: note
---

Good — **Icarus Verilog** is installed (`iverilog` + `vvp`). Here's the full workflow:

---

### 1. Create a testbench

The counter module has no testbench. Write one alongside it:

**`counter_tb.v`**
```verilog
`timescale 1ns / 1ps

module counter_tb;
    reg  clk, rst_n, en;
    wire [3:0] count;

    counter uut (
        .clk  (clk),
        .rst_n(rst_n),
        .en   (en),
        .count(count)
    );

    // 10 MHz clock -> 100 ns period
    always #50 clk = ~clk;

    initial begin
        $dumpfile("counter.vcd");
        $dumpvars(0, counter_tb);

        clk   = 0;
        rst_n = 0;
        en    = 0;

        #200 rst_n = 1;    // release reset
        #100 en    = 1;    // start counting

        #1000 en    = 0;   // pause
        #200  en    = 1;   // resume

        #800  rst_n = 0;   // async reset
        #100  rst_n = 1;   // release
        #200  en    = 1;
        #400;

        $finish;
    end

    initial $monitor("time=%0t  count=%d", $time, count);
endmodule
```

### 2. Compile & simulate

```bash
# Compile
iverilog -o counter.vvp counter.v counter_tb.v

# Run (produces counter.vcd + console output)
vvp counter.vvp
```

Output will look like:
```
time=0     count=0
time=200   count=0
time=300   count=1
time=350   count=2
...
time=1300  count=0
...
```

### 3. View the waveform (optional)

```bash
# Install GTKWave if you haven't
brew install gtkwave

# View
gtkwave counter.vcd
```

---

**One-liner** if you save the testbench as `counter_tb.v` in the same directory:

```bash
iverilog -o counter.vvp counter.v counter_tb.v && vvp counter.vvp
```
