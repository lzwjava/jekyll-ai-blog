---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源Transformer ASIC设计参考
translated: true
type: note
---

问题：**如果我想构建一个在架构上与Etched Sohu（一种专门的AI推理加速器/Transformer ASIC）类似的东西，有哪些好的开源项目值得参考？**

答案：

是的。如果你的目标是**“Etched，但是开源/可研究/可破解”**，我不会寻找一个单一的项目。有用的技术栈是：

```text
                 Transformer / LLM
                       │
                 compiler/runtime
                       │
              ┌────────┴────────┐
              │                 │
           operator          scheduler
              │                 │
              └────────┬────────┘
                       │
                accelerator ISA
                       │
              ┌────────┴────────┐
              │                 │
          systolic/dataflow    SRAM
              │                 │
              └────────┬────────┘
                       │
                    HBM/DDR
                       │
                    NoC/SoC
                       │
                    RTL/ASIC
```

Etched的有趣之处在于，他们基本上是协同设计了这整个技术栈，而不是制造另一个GPU。他们目前的描述明确表示，他们为前沿推理协同设计**芯片、机架、软件和制造**。（[Etched][1]）

### 1. Gemmini——可能是最好的起点

Gemmini

[ucb-bar/gemmini](https://github.com/ucb-bar/gemmini?utm_source=chatgpt.com)

Gemmini是一个**可参数化的脉动阵列加速器生成器**，用Chisel编写，并与Chipyard集成。它为你提供的不仅仅是RTL：加速器架构+ISA接口+编译器/软件+仿真。（[GitHub][2]）

概念上：

```text
RISC-V
  │
  │ custom instructions
  ▼
Gemmini
  │
  ├── DMA
  ├── scratchpad SRAM
  ├── systolic array
  ├── accumulator
  └── memory interface
```

这对于理解基本问题非常有用：

> **硬件到底应该向LLM运行时暴露什么？**

例如，一个简单的加速器可以暴露类似：

```c
matmul(
    A_addr,
    B_addr,
    C_addr,
    M, N, K
);
```

但一个严肃的推理ASIC开始转向：

```text
load weights
load activations
attention(Q,K,V)
KV-cache read/write
GEMM
GEMM
activation
quantize
DMA
```

而不是暴露单个的MAC。

---

### 2. Chipyard——构建整个ASIC原型

[ucb-bar/chipyard](https://github.com/ucb-bar/chipyard?utm_source=chatgpt.com)

如果Gemmini是加速器，那么**Chipyard就是你在其中构建SoC的实验室**。

它提供：

* RISC-V内核
* 加速器
* 存储系统
* NoC/互连
* RTL仿真
* FPGA仿真
* ASIC流程
* 软件生成

Chipyard明确集成了Gemmini和NVDLA，并支持RTL仿真、FPGA加速仿真和VLSI流程。（[GitHub][3]）

对于真正尝试构建类似Etched原型的人来说，我会从以下开始：

```bash
git clone https://github.com/ucb-bar/chipyard
cd chipyard

# 然后添加你自己的加速器
#        ↓
# RISC-V + 你的transformer加速器
#        ↓
# Chipyard
#        ↓
# Verilator / FPGA / ASIC flow
```

---

### 3. NVDLA——研究一个真正的开源加速器

NVIDIA NVDLA

[NVIDIA NVDLA](https://nvdla.org/?utm_source=chatgpt.com)

如果你想了解**一个严肃的神经网络加速器是如何实际分解的**，NVDLA可能是最重要的参考。

与玩具FPGA项目不同，NVDLA包括：

```text
RTL
 ↓
C model
 ↓
compiler
 ↓
runtime
 ↓
Linux driver
 ↓
test infrastructure
```

NVIDIA将其描述为可扩展、可配置的开放架构，包含Verilog RTL、编译器、驱动、测试平台和软件。（[NVIDIA Deep Learning Accelerator][4]）

有趣的是，NVDLA**不是专门针对transformer的**。

这正是我建议将其与Etched一起研究的原因：

```text
NVDLA
general DNN accelerator
        │
        ├── convolution
        ├── GEMM
        ├── activation
        └── pooling

Etched
transformer-specialized accelerator
        │
        ├── QKV
        ├── attention
        ├── KV cache
        ├── FFN
        └── decode/prefill
```

这种差异就是架构上的深坑。

---

### 4. Apache TVM VTA——加速器+编译器协同设计

[apache/tvm-vta](https://github.com/apache/tvm-vta?utm_source=chatgpt.com)

VTA特别有趣，因为它将**编译器和加速器视为一个系统**。

```text
PyTorch / model
       ↓
      TVM
       ↓
VTA compiler
       ↓
accelerator instructions
       ↓
 FPGA hardware
```

它提供开放硬件、模拟器、驱动/运行时和一个端到端的TVM编译器栈。（[GitHub][5]）

这比单纯设计一个矩阵乘法单元更接近实际的Etched问题。

因为关键问题不是：

> “我的硬件能做100 TOPS吗？”

而是：

> **“编译器能把一个实际的自回归解码循环变成一个高效的静态调度吗？”**

---

### 5. Tenstorrent——非常相关的架构参考

Tenstorrent

Tenstorrent值得研究，即使其芯片不像Gemmini/NVDLA那样开源。

有趣的部分是**可编程数据流架构+开放软件栈**。

与Etched的哲学相比：

```text
GPU:
programmable SIMD/SIMT

Tenstorrent:
programmable dataflow

Groq:
highly deterministic dataflow

Etched:
specialized transformer hardware
```

因此，我建议研究Tenstorrent，以理解以下之间的界限：

```text
fixed-function ASIC
        ↕
programmable accelerator
```

`awesome-ai-hardware`项目也是这些架构（包括Tenstorrent、Groq、Cerebras、Maia、TPU和Etched）的一个有用的索引。（[GitHub][6]）

---

### 6. 如果你想要FPGA→ASIC迭代，VTA是不错的选择

如果你的计划是：

```text
Python model
     ↓
compiler
     ↓
FPGA
     ↓
measure
     ↓
change architecture
     ↓
FPGA
     ↓
ASIC
```

那么VTA特别有吸引力，而不是立即尝试完整的ASIC。

对于个人/小团队来说，这要现实得多。

---

### 7. 小型FPGA加速器项目——对学习RTL很有用

还有一些小型项目，比如：

[taitashaw/fpga-ai-accelerator](https://github.com/taitashaw/fpga-ai-accelerator?utm_source=chatgpt.com)

这个项目在SystemVerilog中实现了一个**8×8 INT8脉动阵列**，包括SRAM、分块、重新量化、AXI接口、验证和FPGA部署。（[GitHub][7]）

这很有用，因为你可以一次读完整个设计：

```text
rtl/
  systolic_array
  ├── PE
  ├── SRAM
  ├── DMA
  ├── tiler
  └── quantizer
```

在深入数百万行的加速器代码库之前，这更容易消化。

---

## 我实际会研究的内容

如果你的目标是**“我想理解/构建一个开源的迷你Etched”**，我会使用以下顺序：

| 层                 | 项目                     | 概念上可以借鉴的东西                 |
| ------------------- | ------------------------ | ------------------------------------------ |
| RTL                 | 小型FPGA加速器           | MAC / SRAM / DMA                           |
| 矩阵引擎            | **Gemmini**              | 脉动阵列架构                               |
| SoC                 | **Chipyard**             | RISC-V + 加速器 + 存储                     |
| DNN加速器           | **NVDLA**                | 生产级加速器分解                           |
| 编译器              | **VTA/TVM**              | 编译器 ↔ 硬件契约                          |
| 数据流              | **Tenstorrent**          | 可编程空间执行                             |
| 系统架构            | **Etched**               | 针对transformer的专门化                    |

我**不会**做的是从实现一个巨大的transformer ASIC开始。

从以下开始：

```text
                CPU
                 │
              command
                 │
                 ▼
        ┌─────────────────┐
        │ Transformer ACC │
        │                 │
        │ QKV GEMM        │
        │ Attention       │
        │ FFN GEMM        │
        │ RoPE            │
        │ KV cache        │
        └────────┬────────┘
                 │
              HBM/DDR
```

然后衡量**tokens/sec/W**，而不是TOPS。

对于自回归推理，一个非常有用的第一性原理模型是：

```text
decode one token

        weight bytes
             +
       KV-cache bytes
             +
      activation bytes
             ↓
      memory bandwidth
             ↓
        token latency
```

这就是为什么Etched式架构很有趣：一旦你知道你愿意支持的精确transformer计算，你就可以消除大量的**通用可编程性**。

我个人会用作**基础骨架**的开源项目是**Chipyard + Gemmini**，然后逐步用针对transformer的数据流引擎替换通用的GEMM-centric加速器。

我还可以绘制一个**“迷你Sohu”架构**，你可以在FPGA上实际原型实现——包括KV-cache SRAM布局、注意力数据路径、指令集，以及一个最小的PyTorch→加速器编译器路径。

[1]: https://www.etched.com/?utm_source=chatgpt.com "Etched"
[2]: https://github.com/ucb-bar/gemmini?utm_source=chatgpt.com "GitHub - ucb-bar/gemmini: Berkeley's Spatial Array Generator · GitHub"
[3]: https://github.com/ucb-bar/chipyard/blob/main/README.md?plain=1&utm_source=chatgpt.com "chipyard/README.md at main · ucb-bar/chipyard · GitHub"
[4]: https://nvdla.org/?utm_source=chatgpt.com "NVIDIA Deep Learning Accelerator"
[5]: https://github.com/apache/tvm-vta?utm_source=chatgpt.com "GitHub - apache/tvm-vta: Open, Modular, Deep Learning Accelerator · GitHub"
[6]: https://github.com/ai-hpc/awesome-ai-hardware?utm_source=chatgpt.com "GitHub - ai-hpc/awesome-ai-hardware: AI accelerators, edge inference devices, compilers, runtimes, benchmarks, and research for building and evaluating machine-learning systems. · GitHub"
[7]: https://github.com/taitashaw/fpga-ai-accelerator?utm_source=chatgpt.com "GitHub - taitashaw/fpga-ai-accelerator: Open-source 8×8 INT8 systolic array inference accelerator — from RTL to bitstream · GitHub"