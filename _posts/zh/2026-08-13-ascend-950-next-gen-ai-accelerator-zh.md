---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 昇腾950下一代AI加速器
translated: true
type: note
---

问题：**华为昇腾950是什么？**

答案：

![Image](https://images.openai.com/static-rsc-4/ekY9WvsC7aEC_j5uOBe0gcaDjs39bz8g9vLIJIRDRG2V1_LU6PZAPT32P3BbKGvOCsBbfdu0Jin4fUao9mPZ5QocA1DvAshX9AtGHvUrkrUGen_8QZfuEWZ5aOUDhzqo10BY4aZO7PadI8JW9zFfla7G_5lgnGxe_wiPjJw3qBTPz3FEnQb-ocVNhrXu4uBD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/2YLQXg8-UcXqRJAsbCdHZdNkP6jTMH50qpaB_te4xJ6Y4X5nB43_vgn3bgwXscc7S4cyku5X1ZK4q4_oEKV7e_ncb9-BycdwT_1JVKutmn1CT-LkjqBseEpbBKMp0YmbtmRfepXbzUj67hbnPzs-XFbOdMAbU57_E1FfhmcikcRThz5n9qSloAXyAuuMAvNP?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/vofGbdlIv0CK80uTOph4zGPyrgNBtJmMWPmyY0XPmWqP1Iw1dJOTV8KEz4SeqjsxtPKtkxiS7xIaAFgQ1ESzqVocsMlcwF0Hw2gtxhFvPUuDbMWhgqB4b9XHw7dchWt-YCxvvIQ8pAHtO68gzcBVizJ54JfuHmhRRB9-uBel5xuWUc4b9KxcGmqQDb-X2yv5?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/cyirqFu2y0GaHwqwG2JBAve-VsGxEQ1ot20CEt_TC2sWrGO5VYdUY4ylxI90lJtQxAgHl4LMFzk5tSAaakkSMAjG_dEzaLhRMsZik7SUic2ckIBz9kLAwYwkQ2RllvfGrC9PCSWs0BRUy4YdeDdXwJJAZ9i3OoKYd7SMYdJ0s-krC9CzwBv1WNWbm5q9Aatg?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/xnQYVsCAQzDC7_I2vTf9sv7jnjvFgCZTovlTb56m7KZd5zBNBS-xmjswnyhyRGwGbhV1ja5nfStbnjLeR03NwwdhMtwUM_NnGsM3X7TMMTZJX_Vo7Q2MVfuuuBeJH3vNyT_ohUv5j2gASzdrji28kJO2TdAfFU8PQxp41GllyA1i21_lZPfHCp2d_XC3hYE7?purpose=fullsize)

**昇腾950是华为下一代AI加速器系列，直接针对大规模LLM训练和推理。** 重要的是，它不仅仅是“更快的910C”；华为正在围绕**内存带宽+互连+大规模NPU池化**改变架构。

950系列有两款芯片：

* **昇腾950PR** — 更侧重于训练/通用计算。
* **昇腾950DT** — 更侧重于训练+推理 Decode，拥有更大的内存带宽和互连带宽。 ([Huawei][1])

### 1. 关键数字

对于**昇腾950DT**：

|                             |            昇腾950DT |
| --------------------------- | -------------------: |
| 内存                        |           **144 GB** |
| 内存带宽                    |           **4 TB/s** |
| 芯片互连带宽                |           **2 TB/s** |
| FP8                         |         **1 PFLOPS** |
| FP4                         |         **2 PFLOPS** |
| 格式                        | FP8, MXFP8, MXFP4, HiF8 |
| 预期发布                    |          **2026年Q4** |

华为专门针对**LLM Decode和训练**的瓶颈设计了950DT，在这些场景中，内存移动的重要性已不亚于原始矩阵FLOPS。 ([Huawei][2])

因此，真正有趣的部分是：

> **950与其说是一个NPU，不如说是一个互连/内存架构。**

---

## 2. 为什么950对LLM如此重要

想象一下LLM推理步骤。

对于Decode，大致如下：

```text
新token
   │
   ▼
Q/K/V
   │
   ▼
attention
   │
   ▼
MLP
   │
   ▼
下一个token
```

对于单个生成token，模型权重必须反复访问。

因此，最终：

```text
计算 ↑
但
内存带宽 ↑↑
```

成为限制因素。

这就是为什么华为强调：

```text
144 GB HBM
4 TB/s 内存带宽
2 TB/s NPU互连
```

而不是仅仅宣传一个巨大的FLOPS数字。

从LLM训练的角度来看，**4 TB/s可能比1 PFLOPS FP8更值得关注**。

---

# 3. 但真正疯狂的是 Atlas 950

芯片只是第一层。

华为更大的想法是：

```text
昇腾950DT
      ↓
昇腾卡
      ↓
Atlas 950 SuperPoD
      ↓
大规模集群
```

已公布的**Atlas 950 SuperPoD**可扩展至**8,192张昇腾950DT卡**。

华为公布的完整配置：

```text
8192 × 昇腾950DT
        │
        ▼
Atlas 950 SuperPoD
        │
        ├── 128个计算柜
        ├── 32个互连柜
        └── 总共约160个柜
```

华为声称：

```text
FP8:  8 EFLOPS
FP4: 16 EFLOPS
互连: 16 PB/s
```

并计划在**2026年Q4**左右实现商用。 ([Huawei][1])

这是重要的架构方向。

---

# 4. "SuperPoD"是关键概念

通常，如果你有：

```text
GPU  GPU  GPU  GPU
 │    │    │    │
 └────┴────┴────┘
      网络
```

这些GPU是通过网络通信的独立机器。

华为想要的是更接近：

```text
        ┌─────────────────────────────┐
        │       一台巨型机器          │
        │                             │
        │ NPU NPU NPU NPU NPU NPU...  │
        │  ↕   ↕   ↕   ↕   ↕   ↕      │
        │   统一互连                   │
        │                             │
        │   共享/全局资源             │
        └─────────────────────────────┘
```

物理系统可能包含数百/数千个加速器，但软件应越来越多地将其视为**一台巨型计算机**。

华为将底层互连技术称为**UnifiedBus / 灵衢**。

2026年Atlas 950 SuperPoD的发布描述中提到了**统一内存寻址、极高带宽和约3微秒RTT**（针对WAIC上展示的1024卡配置）。 ([Huawei][3])

---

# 5. 软件层面的影响巨大

如果你正在使用PyTorch/LLM训练，这一点就变得相关。

华为不仅仅是在以下层面竞争：

```text
CUDA
   vs
昇腾NPU
```

真正的竞争正变成：

```text
NVIDIA:
GPU
+
HBM
+
NVLink
+
NVSwitch
+
CUDA
+
集合通信
+
DGX / GB系统

vs

华为:
昇腾
+
HBM
+
UnifiedBus
+
SuperPoD
+
CANN
+
Mind
+
Atlas
```

华为表示，它一直在开放CANN和Mind软件栈，截至2026年7月，CANN社区仓库的开源代码已超过1244万行。 ([Huawei][3])

因此，这场战斗越来越是**全栈**的。

---

# 6. 昇腾路线图

华为公布的路线图大致如下：

```text
910B / 910C
      │
      ▼
  昇腾950
      │
      ▼
  昇腾960
      │
      ▼
  昇腾970
```

华为表示：

| 代际 |      FP8 |      FP4 | 互连 |
| ---- | -------: | -------: | ---: |
| 950  | 1 PFLOPS | 2 PFLOPS | 2 TB/s |
| 960  | 2 PFLOPS | 4 PFLOPS |     — |
| 970  | 4 PFLOPS | 8 PFLOPS | 4 TB/s |

960目前计划于**2027年Q4**发布，970计划于**2028年Q4**发布。华为宣称的方向大致是**每代计算能力翻倍**，同时增加内存容量/带宽和互连能力。 ([Huawei][1])

---

## 7. 一个微妙的架构变化

华为明确表示950引入了：

> **SIMD/SIMT新型同构架构**

这对程序员来说相当重要。

目标本质上就是让NPU编程模型不那么特殊，而更接近GPU风格编程的人所熟悉的方式。

概念上：

```text
旧的加速器编程

       框架
           │
       编译器
           │
     专用NPU
           │
      许多约束


950方向

        PyTorch
           │
      算子
           │
      编译器
           │
      SIMD / SIMT
           │
          NPU
```

华为还在扩展支持的数值格式：

```text
FP32
HF32
FP16
BF16
FP8
MXFP8
HiF8
MXFP4
HiF4
```

这对现代LLM至关重要，因为训练/推理正迅速转向**FP8/FP4级计算**。 ([Huawei][1])

---

# 8. 我对950的思维模型

我不会把它记作：

> "华为的新GPU。"

我会把它记作：

```text
                    昇腾950
                        │
        ┌───────────────┼────────────────┐
        │               │                │
      NPU计算         HBM           互连
        │               │                │
     FP8/FP4        144 GB          2 TB/s
        │               │                │
        └───────────────┼────────────────┘
                        ↓
                  SuperPoD
                        ↓
              数千个NPU
                        ↓
              一台逻辑机器
                        ↓
             万亿参数LLM
```

**这才是真正的故事。**

而最有趣的比较并非简单的**950 vs H100/H200/B200**。而是：

**昇腾950 + UnifiedBus + SuperPoD + CANN**

vs.

**NVIDIA Blackwell/Rubin + NVLink/NVSwitch + CUDA**

因为在8K加速器规模下，**互连、内存层次结构、集合通信、编译器和软件栈可能会主导原始NPU规格。**

华为最新的WAIC演示已经是**1024卡昇腾950 SuperPoD**，而公布的完整Atlas 950设计可扩展到8192卡。 ([Huawei][3])

参考文献：

* [Huawei — 昇腾芯片路线图和Atlas 950发布](https://www.huawei.com/cn/news/2025/9/hc-xu-keynote-speech?utm_source=chatgpt.com)
* [Huawei — 2026世界人工智能大会Atlas 950 SuperPoD](https://www.huawei.com/cn/news/2026/7/atlas-950-superpod?utm_source=chatgpt.com)
* [Huawei — Atlas 950全球首秀](https://www.huawei.com/en/news/2026/3/mwc-superpod-ai?utm_source=chatgpt.com)

[1]: https://www.huawei.com/cn/news/2025/9/hc-xu-keynote-speech?utm_source=chatgpt.com "以开创的超节点互联技术，引领AI基础设施新范式"
[2]: https://www.huawei.com/en/news/2025/9/hc-xu-keynote-speech?utm_source=chatgpt.com "Leading a New Paradigm for AI Infrastructure"
[3]: https://www.huawei.com/cn/news/2026/7/atlas-950-superpod?utm_source=chatgpt.com "昇腾950超节点真机亮相2026世界人工智能大会"
