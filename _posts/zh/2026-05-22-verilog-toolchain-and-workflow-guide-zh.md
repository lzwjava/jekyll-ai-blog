---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Verilog 工具链与工作流程指南
translated: true
type: note
---

**问题：** 如何编译Verilog？是否有VSCode插件、类似GCC的编译器或集成开发环境？

**回答：** 三者都有。以下是完整的工具链概览。

---

## Verilog的“编译”流程

与C/Java不同，Verilog有两种不同的最终目标：

```
Verilog source
      │
      ├─── Simulation  →  iverilog / verilator  →  runs on your CPU
      │                   (like "gcc + ./a.out" but for hardware behavior)
      │
      └─── Synthesis   →  yosys  →  actual gates  →  FPGA bitstream / GDSII
           (like compiling to a specific CPU architecture, but for silicon)
```

学习建议：**先仿真，后综合**。

---

## 1. Icarus Verilog — Verilog界的GCC

```bash
# 安装
brew install icarus-verilog      # macOS
sudo apt install iverilog        # Ubuntu

# 编译+运行（和gcc完全一样）
iverilog -o sim counter.v counter_tb.v
./sim

# 类比：
# iverilog  =  gcc
# ./sim      =  ./a.out
```

输出是仿真结果——它会告诉你每个纳秒时刻信号的状态，就像真实硬件一样。

---

## 2. Verilator — 高速编译器（LLVM级别速度）

将Verilog转化为C++再编译为本地二进制。对于大型设计比Icarus快10-100倍。

```bash
brew install verilator

verilator --binary -j 0 --trace counter.v --top-module counter
./obj_dir/Vcounter
```

使用者：picorv32、RISC-V内核、严肃的开源芯片项目。

---

## 3. Yosys — 综合（Verilog → 逻辑门）

```bash
brew install yosys

yosys -p "read_verilog counter.v; synth -top counter; stat"
# 告诉你：你的设计使用了多少触发器、查找表、加法器
```

---

## VSCode配置——最佳轻量级IDE

安装以下扩展：

```
1. "Verilog-HDL/SystemVerilog/Bluespec SystemVerilog"
   发布者: mshr-h
   → 语法高亮、语法检查、ctags导航

2. "TerosHDL"
   发布者: teros-technology
   → 原理图查看器、测试激励生成器、文档

3. "WaveTrace"
   → 在VSCode内部查看.vcd波形文件（无需GTKWave）
```

从终端安装：

```bash
code --install-extension mshr-h.veriloghdl
code --install-extension teros-technology.teroshdl
code --install-extension wavetrace.wavetrace
```

在`settings.json`中配置linting：

```json
{
  "verilog.linting.linter": "iverilog",
  "verilog.linting.iverilog.arguments": "-Wall",
  "verilog.ctags.path": "ctags"
}
```

现在你就能看到错误时的红色波浪线、转到定义和悬停文档了。

---

## 在VSCode中的完整工作流程

```bash
mkdir myproject && cd myproject
code .
```

创建`counter.v`：

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

创建`counter_tb.v`：

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

在VSCode终端中：

```bash
iverilog -o sim counter.v counter_tb.v && ./sim
# WaveTrace扩展会自动检测wave.vcd — 点击即可打开波形
```

---

## 其他集成开发环境

| 工具 | 类型 | 最适合 |
|---|---|---|
| **EDA Playground** | 浏览器 | 零安装，共享代码片段 |
| **Vivado** | 完整IDE | Xilinx FPGA，有免费版 |
| **Quartus Prime** | 完整IDE | Intel FPGA，免费精简版 |
| **GTKWave** | 波形查看器 | 查看`.vcd`仿真输出 |
| **HDLBits** | 浏览器练习 | 互动学习 |

对于你目前阶段——**VSCode + iverilog + WaveTrace** 就是全部所需。5分钟安装完成，覆盖90%的学习工作流程。

---

## 快速参考——每日常用命令

```bash
# 编译并仿真
iverilog -o sim design.v testbench.v && ./sim

# 查看波形
gtkwave wave.vcd

# 仅检查语法（类似于gcc -fsyntax-only）
iverilog -tnull design.v

# 综合并查看门级统计
yosys -p "read_verilog design.v; synth -top mymodule; stat"

# 使用Verilator进行快速仿真
verilator --binary --trace design.v -top-module mymodule
```

---

## 参考资料

- [Icarus Verilog](https://github.com/steveicarus/iverilog)
- [Verilator](https://github.com/verilator/verilator)
- [mshr-h VSCode extension](https://github.com/mshr-h/vscode-verilog-hdl-support)
- [TerosHDL](https://terostechnology.github.io/terosHDLdoc/)
- [HDLBits interactive exercises](https://hdlbits.01xz.net)
- [EDA Playground](https://edaplayground.com)
