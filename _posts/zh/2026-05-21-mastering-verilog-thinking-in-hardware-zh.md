---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 精通Verilog：硬件思维
translated: true
type: note
---

**问题：** 如何学习 Verilog？有哪些开源项目和可运行的代码示例？

**回答：**

Verilog 的语法可以在几天内学会——难点在于**用硬件思维思考**（一切都是并行的，时间是显式的）。下面是最高效的学习路径。

---

## 首先转换思维模型

```
软件思维模式：                硬件思维模式：
─────────────────            ────────────────
顺序执行                     所有操作同时运行
函数相互调用                 模块始终并行存在
变量存储值                   导线立即传输信号
时间隐含                     时间是时钟边沿，显式
```

这是最大的绊脚石。Verilog 模块不是函数——它是一个**始终通电的物理电路**。

---

## 50 行理解 Verilog —— 核心语法

```verilog
// --- 导线 vs 寄存器 ---
wire a;          // 组合逻辑——由其他模块/门驱动
reg  b;          // 时序逻辑——在时钟边沿保持值

// --- 模块（基本单元，类似类但用于硬件） ---
module adder #(parameter WIDTH=8) (
    input  [WIDTH-1:0] a,
    input  [WIDTH-1:0] b,
    output [WIDTH-1:0] sum,
    output             carry
);
    assign {carry, sum} = a + b;  // 组合逻辑，始终有效
endmodule

// --- always 块 ---
// 组合逻辑（无时钟）：
always @(*) begin
    case (sel)
        2'b00: out = a;
        2'b01: out = b;
        default: out = 0;
    endcase
end

// 时序逻辑（带时钟的触发器）：
always @(posedge clk or posedge rst) begin
    if (rst)
        count <= 8'h00;    // 非阻塞赋值 <=
    else
        count <= count + 1;
end

// --- 阻塞赋值 vs 非阻塞赋值（关键区别） ---
// = 阻塞赋值：在 always 块内顺序执行（用于组合逻辑）
// <= 非阻塞赋值：先计算所有右值，再统一赋值（用于时序逻辑）

// --- 实例化 ---
adder #(.WIDTH(16)) my_adder (
    .a(x), .b(y), .sum(result), .carry(c_out)
);
```

---

## 仿真工具 —— 立即运行 Verilog

### 选项 1：Icarus Verilog + GTKWave（本地，免费）

```bash
brew install icarus-verilog gtkwave
# 或
sudo apt install iverilog gtkwave
```

编写模块 + 测试平台，仿真：

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

// counter_tb.v  (测试平台)
module counter_tb;
    reg clk, rst;
    wire [7:0] count;

    counter dut(.clk(clk), .rst(rst), .count(count));

    // 生成时钟
    initial clk = 0;
    always #5 clk = ~clk;  // 每 5ns 翻转一次 = 100MHz

    initial begin
        $dumpfile("counter.vcd");  // 波形输出
        $dumpvars(0, counter_tb);
        rst = 1; #20;
        rst = 0; #200;
        $finish;
    end

    // 监视输出
    initial $monitor("t=%0t count=%d", $time, count);
endmodule
```

```bash
iverilog -o sim counter.v counter_tb.v
./sim
gtkwave counter.vcd   # 查看波形
```

### 选项 2：EDA Playground —— 零安装，基于浏览器

访问 **edaplayground.com** —— 粘贴 Verilog，在浏览器中运行。支持 Icarus、Synopsys VCS、Cadence Xcelium。适合快速实验。

### 选项 3：Verilator —— 最快的仿真器，生成 C++ 输出

```bash
brew install verilator

# Verilator 将 Verilog 编译为 C++ → 原生可执行文件
# 对于大型设计，比 Icarus 快 10-100 倍
verilator --cc counter.v --exe counter_tb.cpp --build
./obj_dir/Vcounter
```

Verilator 是严肃的开源项目（包括 RISC-V 核心）用于仿真的工具。

---

## 结构化学习路径

### 阶段 1：组合逻辑（第 1 周）

按顺序构建以下模块，每个都进行仿真：

```verilog
// 1. 半加器
module half_adder(input a, b, output sum, carry);
    assign sum   = a ^ b;
    assign carry = a & b;
endmodule

// 2. 全加器
module full_adder(input a, b, cin, output sum, cout);
    assign {cout, sum} = a + b + cin;
endmodule

// 3. 4 选 1 多路选择器
module mux4(input [3:0] d, input [1:0] sel, output reg out);
    always @(*) out = d[sel];
endmodule

// 4. 优先编码器
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

### 阶段 2：时序逻辑（第 2 周）

```verilog
// 1. D 触发器（基本构建块）
module dff(input clk, rst, d, output reg q);
    always @(posedge clk or posedge rst)
        q <= rst ? 0 : d;
endmodule

// 2. 移位寄存器
module shift_reg #(parameter N=8)(
    input clk, rst, sin,
    output reg [N-1:0] q
);
    always @(posedge clk or posedge rst)
        q <= rst ? 0 : {q[N-2:0], sin};
endmodule

// 3. FIFO —— 对 GPU 内存流水线至关重要
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

### 阶段 3：有限状态机（第 3 周）—— 控制逻辑如何工作

```verilog
// 简单的 FSM：检测序列 "1011"
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

FSM 是**每个** GPU 控制单元、内存控制器和缓存仲裁器的实现方式。这不是学术内容。

---

## 值得阅读的真实开源项目

### 1. picorv32 —— 极简 RISC-V CPU（约 2000 行）

最适合初次阅读的实际 CPU。代码整洁、注释完善、单个文件。

```bash
git clone https://github.com/YosysHQ/picorv32
wc -l picorv32.v   # 约 3000 行——全部阅读
```

内部关键内容：

- 取指/译码/执行 FSM
- 寄存器文件（32 x 32 位寄存器）
- 内存事务如何工作
- 乘法/除法单元

```bash
# 仿真运行实际的 RISC-V 代码
cd picorv32
make test   # 运行 Icarus 仿真
```

### 2. VexRiscv —— 基于 SpinalHDL 的流水线 RISC-V

更接近真实，流水线架构，插件化设计：

```bash
git clone https://github.com/SpinalHDL/VexRiscv
# 用 SpinalHDL（基于 Scala，类似 Chisel）编写
# 生成干净的 Verilog
sbt "runMain vexriscv.demo.GenFull"
# 输出 VexRiscv.v —— 阅读生成的 Verilog
```

### 3. MIAOW —— 开源 AMD GCN GPU

与你对 MI300X 的兴趣直接相关：

```bash
git clone https://github.com/VerticalResearchGroup/miaow
ls miaow/src/gpu/
# fetch_decode/   — 指令取指和译码
# execute/        — ALU、浮点单元
# mem/            — 内存流水线
# simfiles/       — 仿真基础设施
```

首先阅读 `miaow/src/gpu/fetch_decode/fetch.v` —— 这里是指令输入的地方。

### 4. Gemmini —— 脉动阵列（直接与 AI 芯片相关）

```bash
git clone https://github.com/ucb-bar/gemmini
# 用 Chisel 编写，生成 Verilog
# 在概念上这就是 MI300X 矩阵核心所做的
ls generators/gemmini/src/main/scala/gemmini/
# 脉动阵列 PE、网格、控制器
```

### 5. OpenTitan —— 生产级 SystemVerilog

Google 的开源芯片项目。真实世界的代码质量：

```bash
git clone https://github.com/lowRISC/opentitan
# 超过 50 万行 SystemVerilog
# AES、SHA、RISC-V 核心、USB、I2C —— 全部开源
ls hw/ip/aes/rtl/   # AES 硬件加速器
```

---

## 你的具体第一周计划

```bash
# 第 1 天：安装工具
brew install icarus-verilog gtkwave verilator

# 第 2 天：编写并仿真计数器、加法器、多路选择器
# （使用上面的代码，添加测试平台，查看波形）

# 第 3 天：构建 FIFO，使用随机读写进行仿真

# 第 4 天：从头到尾阅读 picorv32.v
git clone https://github.com/YosysHQ/picorv32
cat picorv32.v | grep -A 20 "always @"  # 找到所有 FSM

# 第 5 天：运行 picorv32 仿真
cd picorv32 && make test

# 第 6 天：使用 Yosys 综合某个模块
yosys -p "read_verilog counter.v; synth -top counter; stat"
# 查看你的 RTL 变成了多少门电路

# 第 7 天：浏览 MIAOW GPU 源码
git clone https://github.com/VerticalResearchGroup/miaow
```

---

## 需要牢记的关键思维模型

| 概念 | 在软件中对应什么 |
| --- | --- |
| `wire` | 一个实时值，类似始终在计算的返回值 |
| `reg` | 一个变量，仅在时钟边沿更新 |
| `always @(*)` | 一个纯函数，当输入变化时重新计算 |
| `always @(posedge clk)` | 一个事件循环节拍 |
| 模块实例化 | 启动一个永远运行的 goroutine |
| 测试平台 | 你的 `main()` / 测试框架 |
| `$display` | `printf` |
| `$finish` | `exit(0)` |

最难的概念：**没有调度器。** 每个 `always` 块都并行、永远、同时运行。综合工具会计算出如何连接晶体管来实现该行为。

---

## 参考资料

- [picorv32 —— 极简 RISC-V Verilog 实现](https://github.com/YosysHQ/picorv32)
- [MIAOW 开源 GPU](https://github.com/VerticalResearchGroup/miaow)
- [Gemmini 脉动阵列](https://github.com/ucb-bar/gemmini)
- [EDA Playground —— 浏览器仿真器](https://edaplayground.com)
- [OpenTitan 生产级 SystemVerilog](https://github.com/lowRISC/opentitan)
- [nandland —— 最佳 Verilog 入门教程](https://nandland.com)
- [HDLBits —— 交互式 Verilog 练习](https://hdlbits.01xz.net/wiki/Main_Page)

HDLBits 尤其好——它是 Verilog 的 LeetCode，浏览器内即时仿真反馈。
