---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Yosys 和 PicoRV32 学习资源
translated: true
type: note
---

**问题：** 什么是 Yosys，它背后是哪个公司/组织，以及 PicoRV32 仓库是否是学习 Verilog/GPU/硬件设计的良好资源？

**回答：**

## 什么是 Yosys？

Yosys 是一个开源的 **RTL 综合框架**——它接收 Verilog 硬件描述代码，并将其转换为门级网表。可以把它想象成硬件的“编译器”，类似于 GCC 将 C 编译为机器码，只是 Yosys 将 Verilog 编译为逻辑门。

流程如下：

```
Verilog HDL → [Yosys] → 门级网表 → [nextpnr/布局布线] → FPGA 比特流 / ASIC 版图
```

`stat` 命令向你展示的内容：

```
Number of wires:                 23
Number of cells:                 14
  $_DFF_P_                        4   ← 触发器（寄存器，状态）
  $_NOT_                          2   ← 反相器
  $_MUX_                          3   ← 多路选择器
  $_ADD_                          2   ← 加法器
  LUT4                            3   ← 查找表
```

这告诉你 **RTL 设计的资源开销** —— 直接类比于神经网络中的 FLOPs 计数。对于一个 4 位计数器，你预期正好有 4 个触发器（每 bit 一个）。

---

## Yosys 背后是谁？

**不是财富 500 强，也不是典型初创公司。** 这是一个完全不同的类别：

| | |
|---|---|
| **作者** | Claire Xenia Wolf（原名 Clifford Wolf）——独立黑客/研究员 |
| **组织** | [YosysHQ](https://github.com/YosysHQ) —— 一家小型开源专注公司 |
| **模式** | 开放核心：Yosys 本身采用 MIT 许可；YosysHQ 销售商业支持和专有插件（Tabby CAD Suite） |
| **成立时间** | Yosys 始于约 2012 年，作为一个研究项目 |
| **团队规模** | 约 10–20 人 |
| **资金** | 自筹资金/咨询/商业许可——非风投支持 |

它是硬件综合领域的 **LLVM/GCC** —— 在学术界广泛应用，并在工业界日益普及，拥有庞大的社区贡献。Google、efabless 等公司在生产级芯片流程中使用它（例如 Google 的 OpenMPW 穿梭项目）。

---

## PicoRV32——它是好的学习材料吗？

是的，**非常好**，而且特别适合你——因为你正在向 AI 硬件/GPU 内部机制方向前进。

[picorv32](https://github.com/YosysHQ/picorv32) 是一个 **紧凑、干净的 RISC-V CPU 实现，约 3000 行 Verilog**，同样由 Claire Wolf 编写。它的特点是：

- 可在真实 FPGA 上综合
- 用于生产级硅芯片（Google 的 Skywater PDK 流片）
- 设计为可读——未特意为混淆而优化

**为什么它对你的人工智能工程发展路线很重要：**

```
GPU = 数千个着色器核心，每个本质上是一个简化的 CPU
↓
理解一个简单的 RTL 级 CPU（PicoRV32）
↓
理解计算流水线在门级如何工作
↓
理解为什么内存带宽 >> 计算是 GPU 的瓶颈
↓
理解 KV cache、CUDA warp 调度、张量核心布局
```

阅读 PicoRV32 将教你：

- **寄存器文件** —— 权重/激活值如何在硬件寄存器中存储
- **ALU 流水线** —— 矩阵运算如何在门级分解为加法和乘法
- **内存接口（AXI/Wishbone）** —— 理解 HBM、GDDR、内存合并的基础
- **停顿/冒险逻辑** —— 直接类比于 GPU warp 因内存延迟而停顿

---

## 用于学习的实用 Yosys 工作流

```bash
# 安装
brew install yosys

# 编写一个简单模块
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

# 综合并检查
yosys -p "
  read_verilog counter.v;
  synth -top counter;
  stat;
  show;          # 生成门级网表的 graphviz 图
"

# 对于 PicoRV32
git clone https://github.com/YosysHQ/picorv32
cd picorv32
# 综合整个 CPU，看看一个 CPU 需要多少个触发器
yosys -p "read_verilog picorv32.v; synth -top picorv32; stat"
```

对 PicoRV32 运行 `stat` 将显示大约 2000–4000 个单元 —— 这是一个真实 CPU 的门数。在硬件层面建立起“这东西有多复杂？”的直觉，对于你思考 GPU 芯片面积、功耗预算以及为什么张量核心是现在这样的形状，是极其宝贵的。

---

## 为你推荐的学习路径

鉴于你向 GPU/AI 硬件理解方向发展的轨迹：

```
PicoRV32（阅读 Verilog）
  → nanoGPT（你已经做过）
  → 理解为什么 matmul 与 GPU 张量核心如此匹配
  → 阅读 Tim Dettmers 的 "Why is GPU programming so hard?"
  → 编写 CUDA 内核（你可以映射回 RTL 心智模型）
```

一旦你读过用 Verilog 实现的 CPU，硬件→软件栈就不再那么神奇了。这与 Karpathy 的“从零构建 GPT”价值相同——你不再把硬件当作黑盒。

**参考资料：**

- [YosysHQ/yosys](https://github.com/YosysHQ/yosys)
- [YosysHQ/picorv32](https://github.com/YosysHQ/picorv32)
- [YosysHQ 公司网站](https://www.yosyshq.com/)
- [OpenMPW / Google + Yosys 生产应用](https://efabless.com/open_shuttle_program)
