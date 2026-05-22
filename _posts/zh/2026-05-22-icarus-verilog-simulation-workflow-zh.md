---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Icarus Verilog 仿真工作流程
translated: true
type: note
---

很好——**Icarus Verilog** 已安装（`iverilog` + `vvp`）。以下是完整的工作流程：

---

### 1. 创建一个 testbench

计数器模块没有 testbench。在它旁边编写一个：

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

    // 10 MHz 时钟 -> 100 ns 周期
    always #50 clk = ~clk;

    initial begin
        $dumpfile("counter.vcd");
        $dumpvars(0, counter_tb);

        clk   = 0;
        rst_n = 0;
        en    = 0;

        #200 rst_n = 1;    // 释放复位
        #100 en    = 1;    // 开始计数

        #1000 en    = 0;   // 暂停
        #200  en    = 1;   // 恢复

        #800  rst_n = 0;   // 异步复位
        #100  rst_n = 1;   // 释放
        #200  en    = 1;
        #400;

        $finish;
    end

    initial $monitor("time=%0t  count=%d", $time, count);
endmodule
```

### 2. 编译与模拟

```bash
# 编译
iverilog -o counter.vvp counter.v counter_tb.v

# 运行（生成 counter.vcd + 控制台输出）
vvp counter.vvp
```

输出将类似于：
```
time=0     count=0
time=200   count=0
time=300   count=1
time=350   count=2
...
time=1300  count=0
...
```

### 3. 查看波形（可选）

```bash
# 如果尚未安装 GTKWave，请安装
brew install gtkwave

# 查看
gtkwave counter.vcd
```

---

**一行命令**，如果你把 testbench 保存为同一目录下的 `counter_tb.v`：

```bash
iverilog -o counter.vvp counter.v counter_tb.v && vvp counter.vvp
```