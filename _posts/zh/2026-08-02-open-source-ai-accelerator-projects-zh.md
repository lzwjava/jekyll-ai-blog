---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 开源AI加速器项目
translated: true
type: note
---

问题：有哪些与Taalas类似的开源项目？Taalas是一家构建基于ASIC的AI推理硬件的公司。

答案：

Taalas之所以引人注目，是因为它并非又一家GPU公司。其核心理念是：

> 与其用通用GPU运行神经网络，不如构建一款定制ASIC，让芯片本身针对模型架构进行优化。

开源世界中几乎没有完整的“类Taalas”项目（因为流片成本高达数百万美元），但围绕**AI加速器ASIC、开放芯片、ML编译器栈以及硬件/软件协同设计**，确实存在多个相关项目。

![Image](https://images.openai.com/static-rsc-4/r9haLXmV73hun6dfENc11P7E-vv-Vy_wdJujYRE0-uCi-YWFa9RrhIPBpsGwyZxiYMTz8NKXAgbLsxKCzbyELxjUZTV1GeC95C1PAODs5jOYlXvoFf6ME8i0AgimjsZelTRsDwDypUh6p25Fpt48mIm6WuPvXLbjUMM8CiDCljllFrzqaTWsfqCZpY3N9_SF?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/XXgQDJ9uGXZQFlXDFb2n9wNAzMwZArbBxLqnZeRz6aD3BUu3BX-qyIkmWmiT9n8ONk-R_78O4klidT7Mw3rR9er6IESr2pM2PCO2mkuvUopf3FD6iqNkPFHve_Pa-MJ8B3XLtcHJg_m1rlpbU1ZZYGO8_B24vP1Atg4MPHk5o0h3z9IdP3hviSEe_ax4fmQE?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/qqJ4K-cTCuZLqCqjaIQqFWHIzKLUCb8phmMXA26Mb-_PXsjYT6RwK_zsFUemXQhnz7Q1mDlxC0DB16OkCgYv3cCk8jo8VnVlQpJTZhDz_LTL5Gt87ROb2GbMMlM_v_MBKQnM7HEb6gx7dOoXVxZO1VqqYrItZaoIIHDRe94THQlXfz1FWHiwH92LLAMyqMjK?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/fZt2JqIkRS60Z_A1Ofk0FNHEBgwVqDGey2-_OLbFh01lR8em_RghGC43_XULq89g1hkXDU7uvWKMjVyrIS-yQ_XIdQ2FJbn1KXExpJyVaV9EkaJrYnsTPxRevZzigz2NCF69bJNtslAyjFh0gljjZrlZfBL6TjAzIh3TF2zcYhswpUPVYKEZdv_di63jyT5Y?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/s_p_IGPGneX_GNvtgs3BxGwlkoFZZ1cxUdTsgJQuGMkoA9X6nNN1P3lxpwsTQptUruLI8t38S7I2Tfhd_Tx47ZPEv_na5Cwc4_TD3-0xuKyuSgdg5iowFbeCthI_g434hVMTeeRy4KMgn1Ta1TV9mcyB7ufhoLn13HLzo5st2W9omywixM9zH3l81KWCEwN9?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/KYHVp9S1HzeoO6-zSYrlX7mcJk4DN9RKc0P2XWrN_s0sjeZNYChHGjFyHAwXaZkDWq7jZwmVRR6Fn9wvCaTTipK6HFyVwNNI11GUhhkDwysdYHsgnBYmXgWdYevWs92p8wX0c_vfD97dolhJh4MVM1UkmXDVnrSHsXikY12n6D3vZQkyTwgKX8G6EmPEPrao?purpose=fullsize)

## 1. 开放计算项目（Open Compute Project）AI硬件

网站：
[开放计算项目](https://www.opencompute.org?utm_source=chatgpt.com)

OCP并非单一的ASIC项目，但它是超大规模云服务商开源硬件设计的地方。

示例：

* AI服务器设计
* 加速器系统
* 机架架构
* 电源/散热

类Taalas公司最终都需要这个生态系统。

---

## 2. OpenROAD —— 开放ASIC的基础

网站：
[OpenROAD项目](https://theopenroadproject.org?utm_source=chatgpt.com)

这可能是最重要的开源ASIC项目。

传统ASIC流程：

```
RTL代码
   |
   v
综合
   |
   v
布局布线
   |
   v
GDSII
   |
   v
制造
```

OpenROAD实现自动化：

```
Verilog
   |
   v
OpenROAD
   |
   v
芯片布局
```

你实际上可以制造出硅芯片。

示例：

```
my_ai_accelerator.v

        |
        v

OpenROAD

        |
        v

AI加速器芯片
```

---

## 3. Tiny Tapeout

网站：
[Tiny Tapeout](https://tinytapeout.com?utm_source=chatgpt.com)

非常适合学习。

人们提交小型设计：

```
Verilog模块

      |
      v

Tiny Tapeout流片服务

      |
      v

实际制造的芯片
```

你可以将以下模块置于真实的硅片上：

* CPU
* 加速器
* 神经网络模块
* DSP

---

## 4. RISC-V国际AI加速器

网站：
[RISC-V国际](https://riscv.org?utm_source=chatgpt.com)

RISC-V是开放硬件的CPU侧。

许多AI芯片架构如下：

```
        RISC-V CPU
             |
             |
       控制逻辑
             |
   --------------------
   |                  |
张量核心           SRAM
   |
矩阵乘法
```

示例：

* 向量扩展
* AI协处理器
* 边缘推理芯片

---

## 5. CVA6 + 加速器研究

网站：
[CVA6 RISC-V CPU](https://github.com/openhwgroup/cva6?utm_source=chatgpt.com)

一个实际的开放AI芯片栈：

```
CVA6 CPU
   |
   |
定制加速器
   |
   |
SRAM / DRAM
```

---

## 6. Apache TVM

网站：
[Apache TVM](https://tvm.apache.org?utm_source=chatgpt.com)

这更贴近Taalas的软件层面。

未来的AI芯片栈是：

```
PyTorch模型

      |
      v

编译器

      |
      v

硬件特定指令

      |
      v

ASIC
```

TVM的工作流程：

```
模型图
    |
优化
    |
内核生成
    |
加速器后端
```

---

## 7. MLIR

网站：
[MLIR项目](https://mlir.llvm.org?utm_source=chatgpt.com)

现代AI加速器高度依赖编译器基础设施。

示例：

```
PyTorch

 ↓

Torch-MLIR

 ↓

MLIR

 ↓

硬件后端

 ↓

ASIC
```

---

## 8. Cerebras Systems的晶圆级引擎（WSE）理念（非开源）

Cerebras并非开源，但概念上接近：

GPU：

```
许多小芯片
+
通用CUDA
```

Cerebras/Taalas：

```
专用硅片
+
模型特定优化
```

---

## 9. OpenXLA

网站：
[OpenXLA](https://openxla.org?utm_source=chatgpt.com)

Google TPU采用了这一理念：

```
模型

 ↓

XLA编译器

 ↓

TPU硬件
```

这恰恰是AI ASIC的设计理念。

---

# 如果你想自行构建一个“迷你Taalas”

鉴于你拥有vLLM / nanoGPT / CUDA的背景，可行的路径如下：

## 第一阶段：用Verilog构建一个小型加速器

示例：

```
矩阵乘法：

C = A * B
```

硬件：

```
        A
        |
        v
+----------------+
| 脉动阵列      |
+----------------+
        |
        v
        C
```

学习内容：

* 脉动阵列
* SRAM
* MAC单元
* 量化

---

## 第二阶段：先使用FPGA

使用：

* Xilinx FPGA
* AMD Alveo
* Lattice FPGA

实现：

```
INT8 GEMM加速器
```

---

## 第三阶段：编译器

连接：

```
PyTorch

  |
  v

自定义编译器

  |
  v

你的加速器
```

---

## 第四阶段：ASIC

使用：

* OpenROAD
* SkyWater 130nm PDK
* Tiny Tapeout

---

对于具备你这种背景（训练GPT-2、nano-vLLM、CUDA实验）的人来说，最有价值的开源贡献领域**可能不是设计晶体管**，而是模型与硅片之间的这一层：

```
        LLM
         |
         |
   编译器/运行时
         |
         |
  加速器内核
         |
         |
       ASIC
```

像以下项目：

* Apache TVM
* MLIR
* OpenXLA
* OpenROAD
* SGLang/vLLM硬件后端

正是软件工程师能够产生巨大影响的地方。

参考资料：

* [OpenROAD项目](https://theopenroadproject.org?utm_source=chatgpt.com)
* [Tiny Tapeout](https://tinytapeout.com?utm_source=chatgpt.com)
* [Apache TVM](https://tvm.apache.org?utm_source=chatgpt.com)
* [MLIR项目](https://mlir.llvm.org?utm_source=chatgpt.com)
* [OpenXLA](https://openxla.org?utm_source=chatgpt.com)