---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源芯片设计EDA工具
translated: true
type: note
---

**问题：** AMD MI300X 这类芯片是如何设计的？我应该了解哪些芯片设计软件（EDA 工具）？

**回答：**

很好的转向。这是**开源硬件**的前沿领域——相当于硅片界的 Linux 与 Windows 之争。让我为你梳理整个技术栈。

---

## 芯片设计栈（从顶层到底层）

```
规格 / 架构
        ↓
RTL（寄存器传输级）—— Verilog/VHDL/Chisel
        ↓
综合（Synthesis）—— RTL → 门级网表
        ↓
布局布线（Place & Route）—— 门级 → 物理版图
        ↓
签核（Sign-off，时序、功耗、DRC/LVS）
        ↓
GDSII → 晶圆厂（台积电、三星）
        ↓
硅片
```

MI300X 由 AMD 工程师在步骤 1-4 设计，然后在台积电 N5/N6 工艺上制造。

---

## 需要了解的开源 EDA 工具

### 1. OpenROAD —— 完整的开源 RTL→GDSII 流程

这是最重要的一个。由 DARPA 资助，在真实流片中投入使用。

```bash
git clone https://github.com/The-OpenROAD-Project/OpenROAD
# 或者使用流程封装工具：
git clone https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts

cd OpenROAD-flow-scripts
./build_openroad.sh
# 运行一个示例设计（GCD 电路）
make DESIGN_CONFIG=./flow/designs/asap7/gcd/config.mk
```

它能做什么：综合 → 布局规划 → 布局 → 时钟树综合 → 布线 → 签核。**完整流程，无需许可证。**

---

### 2. Yosys —— RTL 综合

将 Verilog 转换为门级网表。相当于芯片设计中的 GCC。

```bash
brew install yosys  # 或 apt

# 综合一个简单的模块
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

Yosys 是 OpenROAD 内部用于综合的工具。阅读它的源码能让你了解综合的实际工作原理。

---

### 3. Chisel —— 基于 Scala 的硬件描述语言（RISC-V 使用）

与 Verilog（1980 年代的语言）不同，Chisel 允许你用编程方式描述硬件。被 Google TPU 团队、伯克利 RISC-V 项目使用。

```scala
import chisel3._
import chisel3.util._

class Adder(width: Int) extends Module {
  val io = IO(new Bundle {
    val a   = Input(UInt(width.W))
    val b   = Input(UInt(width.W))
    val sum = Output(UInt((width+1).W))
  })
  io.sum := io.a +& io.b  // +& = 不截断溢出
}

// 生成 Verilog → 输入到 Yosys → OpenROAD
```

```bash
# 安装并从 Chisel 生成 Verilog
sbt "runMain Adder --target-dir generated"
# 输出 generated/Adder.v
```

**与 AI 芯片的相关性：** Google TPU v4 的脉动阵列是用类似 Chisel 的 DSL 描述的。理解这一点就能理解矩阵引擎是如何构建的。

---

### 4. Magic VLSI + KLayout —— 版图编辑器

用于查看实际的晶体管级版图。

```bash
brew install --cask klayout  # GDSII 查看器
# 打开任意开源 PDK 版图文件
klayout sky130_fd_sc_hd__and2_1.gds
```

KLayout 允许你查看开源 PDK（SkyWater 130nm）中的实际 GDSII 文件。你可以直接看到晶体管。

---

### 5. SkyWater SKY130 PDK —— 免费工艺设计套件

开放的晶圆厂工艺。让你设计可在 SkyWater 制造的芯片（通过 Efabless/Google  shuttle）。

```bash
git clone https://github.com/google/skywater-pdk
# 包含：单元库、SPICE 模型、DRC 规则
ls skywater-pdk/libraries/sky130_fd_sc_hd/  # 标准单元
```

通过这种方式，你可以**实际流片**而无需向台积电支付数百万美元。Google 通过 Efabless 赞助免费 shuttle。

---

### 6. OpenLane —— Sky130 自动化流程

封装了 Yosys + OpenROAD + Magic，适用于 SKY130：

```bash
git clone https://github.com/The-OpenROAD-Project/OpenLane
cd OpenLane
make
make mount
# 在容器内：
./flow.tcl -design spm  # 在示例设计上运行完整 RTL→GDSII
```

这是人们用来提交到 Google 免费芯片 shuttle 的工具。真实的芯片已经通过这种方式制造出来。

---

## MI300X 的实际设计方式（高层视角）

```
1. 架构规格
   - 计算单元数量、缓存层次结构、HBM 接口
   - 以文档形式编写，非代码

2. RTL（Verilog/SystemVerilog）—— 数百万行
   - 每个功能模块：着色器核心、内存控制器、
     Infinity Fabric 链路、显示引擎
   - AMD 使用内部专有工具（Synopsys DC、Cadence Genus）

3. 验证（最困难的部分——占 60-70% 的工作量）
   - SystemVerilog 断言
   - UVM 测试平台
   - 形式验证（sby / Cadence JasperGold）

4. 综合 → Cadence Genus 或 Synopsys DC
   （相当于 Yosys，但许可证费用为 100 万美元/年）

5. 布局布线 → Cadence Innovus 或 Synopsys ICC2
   （相当于 OpenROAD，但许可证费用为 500 万美元/年）

6. 签核 → Synopsys PrimeTime（时序）、Mentor Calibre（DRC/LVS）

7. GDSII → 台积电 N5 晶圆厂
```

开源工具涵盖的概念与商业工具**完全一致**——只是速度较慢、成熟度较低。学习 OpenROAD 可以让你了解 Cadence Innovus 的功能。

---

## AI 芯片特有部分 —— 脉动阵列

MI300X 矩阵引擎（以及任何 AI 加速器）的核心是用于 GEMM 的**脉动阵列**。以下是一个最小的 Chisel 实现，帮助你理解概念：

```scala
// 脉动阵列的最小 PE（处理单元）
class PE extends Module {
  val io = IO(new Bundle {
    val a_in  = Input(SInt(8.W))   // 向右流动的权重
    val b_in  = Input(SInt(8.W))   // 向下流动的激活值
    val c_in  = Input(SInt(32.W))  // 向下流动的部分和
    val a_out = Output(SInt(8.W))
    val b_out = Output(SInt(8.W))
    val c_out = Output(SInt(32.W))
  })
  // 寄存输入（流水线阶段）
  val a_reg = RegNext(io.a_in)
  val b_reg = RegNext(io.b_in)
  
  io.a_out := a_reg
  io.b_out := b_reg
  io.c_out := RegNext(io.c_in + (a_reg * b_reg))
}
```

这些 PE 组成的阵列 = 矩阵乘法引擎。MI300X 的 CDNA3 拥有 228 个计算单元，每个单元包含进行 4x4 或 16x16 块运算的矩阵核心。

---

## 适合你的学习路径

鉴于你的背景（系统、GPU 计算、LLM 训练）：

```
第 1-2 周：Verilog 基础 → 编写简单的 ALU、FIFO、计数器
第 3-4 周：Yosys 综合 → 了解你的 RTL 变成了什么门电路
第 5-6 周：OpenLane/OpenROAD → 在 SKY130 上运行完整流程
第 7-8 周：Chisel → 用 Chisel 重写你的 RTL，理解抽象层
第 9 周+：阅读实际 GPU RTL —— MIAOW（开源 AMD GCN 克隆）
```

**MIAOW** 是 AMD GCN 指令集架构的开源 Verilog 实现——根本就是一个开源 GPU：
```bash
git clone https://github.com/VerticalResearchGroup/miaow
# AMD GCN 着色器核心的真实 Verilog 实现
```

---

## 现在就该 Star 的关键仓库

| 仓库 | 教授内容 |
|---|---|
| `The-OpenROAD-Project/OpenROAD` | 完整 RTL→GDSII 流程 |
| `YosysHQ/yosys` | 综合内部机制 |
| `chipsalliance/chisel` | 基于 Scala 的硬件描述 |
| `google/skywater-pdk` | 真实工艺节点数据 |
| `VerticalResearchGroup/miaow` | 开源 GPU RTL |
| `ucb-bar/gemmini` | 开源脉动阵列（RISC-V） |
| `efabless/caravel` | 用于流片的开源芯片框架 |

`gemmini` 尤其相关——它是伯克利开发的可配置脉动阵列生成器，用于研究领域。在概念上直接类比 TPU/MI300X 的矩阵引擎。