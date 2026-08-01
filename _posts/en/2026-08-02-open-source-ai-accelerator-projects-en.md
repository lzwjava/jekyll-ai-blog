---
audio: false
generated: true
image: false
lang: en
layout: post
title: Open Source AI Accelerator Projects
translated: false
type: note
---

Question: What open source projects are similar to Taalas, which builds ASIC-based AI inference hardware?

Answer:

Taalas is interesting because it is not just another GPU company. The idea is:

> Instead of a general-purpose GPU running a neural network, build a custom ASIC where the silicon itself is optimized around the model architecture.

The open-source world does not have many full "Taalas-like" projects (because tape-out costs millions), but there are several projects around **AI accelerator ASICs, open silicon, ML compiler stacks, and hardware/software co-design**.

![Image](https://images.openai.com/static-rsc-4/r9haLXmV73hun6dfENc11P7E-vv-Vy_wdJujYRE0-uCi-YWFa9RrhIPBpsGwyZxiYMTz8NKXAgbLsxKCzbyELxjUZTV1GeC95C1PAODs5jOYlXvoFf6ME8i0AgimjsZelTRsDwDypUh6p25Fpt48mIm6WuPvXLbjUMM8CiDCljllFrzqaTWsfqCZpY3N9_SF?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/XXgQDJ9uGXZQFlXDFb2n9wNAzMwZArbBxLqnZeRz6aD3BUu3BX-qyIkmWmiT9n8ONk-R_78O4klidT7Mw3rR9er6IESr2pM2PCO2mkuvUopf3FD6iqNkPFHve_Pa-MJ8B3XLtcHJg_m1rlpbU1ZZYGO8_B24vP1Atg4MPHk5o0h3z9IdP3hviSEe_ax4fmQE?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/qqJ4K-cTCuZLqCqjaIQqFWHIzKLUCb8phmMXA26Mb-_PXsjYT6RwK_zsFUemXQhnz7Q1mDlxC0DB16OkCgYv3cCk8jo8VnVlQpJTZhDz_LTL5Gt87ROb2GbMMlM_v_MBKQnM7HEb6gx7dOoXVxZO1VqqYrItZaoIIHDRe94THQlXfz1FWHiwH92LLAMyqMjK?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/fZt2JqIkRS60Z_A1Ofk0FNHEBgwVqDGey2-_OLbFh01lR8em_RghGC43_XULq89g1hkXDU7uvWKMjVyrIS-yQ_XIdQ2FJbn1KXExpJyVaV9EkaJrYnsTPxRevZzigz2NCF69bJNtslAyjFh0gljjZrlZfBL6TjAzIh3TF2zcYhswpUPVYKEZdv_di63jyT5Y?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/s_p_IGPGneX_GNvtgs3BxGwlkoFZZ1cxUdTsgJQuGMkoA9X6nNN1P3lxpwsTQptUruLI8t38S7I2Tfhd_Tx47ZPEv_na5Cwc4_TD3-0xuKyuSgdg5iowFbeCthI_g434hVMTeeRy4KMgn1Ta1TV9mcyB7ufhoLn13HLzo5st2W9omywixM9zH3l81KWCEwN9?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/KYHVp9S1HzeoO6-zSYrlX7mcJk4DN9RKc0P2XWrN_s0sjeZNYChHGjFyHAwXaZkDWq7jZwmVRR6Fn9wvCaTTipK6HFyVwNNI11GUhhkDwysdYHsgnBYmXgWdYevWs92p8wX0c_vfD97dolhJh4MVM1UkmXDVnrSHsXikY12n6D3vZQkyTwgKX8G6EmPEPrao?purpose=fullsize)

## 1. Open Compute Project AI Hardware

Website:
[Open Compute Project](https://www.opencompute.org?utm_source=chatgpt.com)

OCP is not a single ASIC project, but it is where hyperscalers open-source hardware designs.

Examples:

* AI server designs
* accelerator systems
* rack architecture
* power/cooling

Taalas-like companies ultimately need this ecosystem.

---

## 2. OpenROAD — the foundation for open ASIC

Website:
[OpenROAD Project](https://theopenroadproject.org?utm_source=chatgpt.com)

This is probably the most important open-source ASIC project.

Traditional ASIC flow:

```
RTL code
   |
   v
Synthesis
   |
   v
Place & Route
   |
   v
GDSII
   |
   v
Manufacturing
```

OpenROAD automates:

```
Verilog
   |
   v
OpenROAD
   |
   v
chip layout
```

You can actually build silicon.

Example:

```
my_ai_accelerator.v

        |
        v

OpenROAD

        |
        v

AI accelerator chip
```

---

## 3. Tiny Tapeout

Website:
[Tiny Tapeout](https://tinytapeout.com?utm_source=chatgpt.com)

Very cool for learning.

People submit small designs:

```
Verilog module

      |
      v

Tiny Tapeout shuttle

      |
      v

real manufactured chip
```

You can put:

* CPU
* accelerator
* neural network block
* DSP

onto real silicon.

---

## 4. RISC-V International AI accelerators

Website:
[RISC-V International](https://riscv.org?utm_source=chatgpt.com)

RISC-V is the CPU side of open hardware.

Many AI chips look like:

```
        RISC-V CPU
             |
             |
       control logic
             |
   --------------------
   |                  |
Tensor Core       SRAM
   |
Matrix Multiply
```

Examples:

* vector extensions
* AI coprocessors
* edge inference chips

---

## 5. CVA6 + accelerator research

Website:
[CVA6 RISC-V CPU](https://github.com/openhwgroup/cva6?utm_source=chatgpt.com)

A realistic open AI chip stack:

```
CVA6 CPU
   |
   |
Custom accelerator
   |
   |
SRAM / DRAM
```

---

## 6. Apache TVM

Website:
[Apache TVM](https://tvm.apache.org?utm_source=chatgpt.com)

This is closer to the software side of Taalas.

The future AI chip stack is:

```
PyTorch model

      |
      v

Compiler

      |
      v

Hardware-specific instructions

      |
      v

ASIC
```

TVM does:

```
model graph
    |
optimization
    |
kernel generation
    |
accelerator backend
```

---

## 7. MLIR

Website:
[MLIR Project](https://mlir.llvm.org?utm_source=chatgpt.com)

Modern AI accelerators depend heavily on compiler infrastructure.

Example:

```
PyTorch

 ↓

Torch-MLIR

 ↓

MLIR

 ↓

hardware backend

 ↓

ASIC
```

---

## 8. Cerebras Systems WSE ideas (not open source)

Cerebras is not open source, but conceptually close:

GPU:

```
many small chips
+
general CUDA
```

Cerebras/Taalas:

```
specialized silicon
+
model-specific optimization
```

---

## 9. OpenXLA

Website:
[OpenXLA](https://openxla.org?utm_source=chatgpt.com)

Google TPU uses this philosophy:

```
Model

 ↓

XLA compiler

 ↓

TPU hardware
```

This is exactly the AI ASIC philosophy.

---

# If you want to build a "mini Taalas" yourself

Given your vLLM / nanoGPT / CUDA background, the realistic path:

## Stage 1: Build a tiny accelerator in Verilog

Example:

```
matrix multiplication:

C = A * B
```

Hardware:

```
        A
        |
        v
+----------------+
| systolic array |
+----------------+
        |
        v
        C
```

Study:

* systolic arrays
* SRAM
* MAC units
* quantization

---

## Stage 2: FPGA first

Use:

* Xilinx FPGA
* AMD Alveo
* Lattice FPGA

Implement:

```
INT8 GEMM accelerator
```

---

## Stage 3: Compiler

Connect:

```
PyTorch

  |
  v

custom compiler

  |
  v

your accelerator
```

---

## Stage 4: ASIC

Use:

* OpenROAD
* SkyWater 130nm PDK
* Tiny Tapeout

---

For someone with your background (training GPT-2, nano-vLLM, CUDA experiments), the highest-value open-source contribution area is probably **not designing transistors**. It is the layer between models and silicon:

```
        LLM
         |
         |
   compiler/runtime
         |
         |
  accelerator kernels
         |
         |
       ASIC
```

Projects like:

* Apache TVM
* MLIR
* OpenXLA
* OpenROAD
* SGLang/vLLM hardware backends

are where software engineers can have outsized impact.

References:

* [OpenROAD Project](https://theopenroadproject.org?utm_source=chatgpt.com)
* [Tiny Tapeout](https://tinytapeout.com?utm_source=chatgpt.com)
* [Apache TVM](https://tvm.apache.org?utm_source=chatgpt.com)
* [MLIR Project](https://mlir.llvm.org?utm_source=chatgpt.com)
* [OpenXLA](https://openxla.org?utm_source=chatgpt.com)
