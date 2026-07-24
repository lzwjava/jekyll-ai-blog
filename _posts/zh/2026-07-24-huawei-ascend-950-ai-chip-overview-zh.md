---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华为昇腾950 AI芯片概述
translated: true
type: note
---

问题：华为950芯片GPU介绍

回答：

假设您指的是**华为昇腾950**，它是华为昇腾AI处理器系列中的下一代AI加速器/类GPU芯片。它**不是传统的GPU**（如NVIDIA H100/B200），而是主要针对大规模AI训练和推理设计的**AI加速器（NPU）**。

![Image](https://images.openai.com/static-rsc-4/ekY9WvsC7aEC_j5uOBe0gcaDjs39bz8g9vLIJIRDRG2V1_LU6PZAPT32P3BbKGvOCsBbfdu0Jin4fUao9mPZ5QocA1DvAshX9AtGHvUrkrUGen_8QZfuEWZ5aOUDhzqo10BY4aZO7PadI8JW9zFfla7G_5lgnGxe_wiPjJw3qBTPz3FEnQb-ocVNhrXu4uBD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/cyirqFu2y0GaHwqwG2JBAve-VsGxEQ1ot20CEt_TC2sWrGO5VYdUY4ylxI90lJtQxAgHl4LMFzk5tSAaakkSMAjG_dEzaLhRMsZik7SUic2ckIBz9kLAwYwkQ2RllvfGrC9PCSWs0BRUy4YdeDdXwJJAZ9i3OoKYd7SMYdJ0s-krC9CzwBv1WNWbm5q9Aatg?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/tLLhIY0240X3gCkCI3othkoCEpGVp5nyOwAHlVvaWo6TF0egGXuDPFjnaTIES77v6DssHSAUSmiHYOvrvC9S_Xikgkky-T3mvkEhWTpQhwxp7hyED3JPdyp1ndEJWnFg4mrY4ynkbiZyzcjv-CCaHxNPiVwQ074R0kp0q-pMLbDyJ9cy-tIXpNRJNbuH-KWW?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/OHQWQENl_um9yekiH6rK0jQuCtfsUH9kSI9Lrh2lPO8ub14ISxZJf45UNIvuV7lJ9cUs23fITfzI33i5Zya-LJeW3gdwm65702xCCbRfS3N0rdxHpKJ0bR2IGu_9Iwiahep0J5f3IY9G6WOZoTrfH8BAfaJ5aiX5xbxcw9fgHOhqspgfw6hQ_uftVRgO8wbD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ZHd9VcS34VFUP4e_KildWkbz-Z_3ZH61ayjeNpUftoQ3R4x_lV-sKtOuBV64IrDGnsYWn1DjamdhapxE2VbMk2xnNFdr-KfzbKQPyCDwTFizUyOsPqtgzO4mMv9S6n-0FgXH53yLaMGijUNhaT9rF-R2kxupIgRoPfjphYUWmm3UCfcE8R5lm0Nml82A6zBN?purpose=fullsize)

## 1. 昇腾950的定位

华为AI芯片路线图：

```
昇腾310
   |
   | 边缘推理
   |
昇腾910
   |
   | 训练/数据中心AI加速器
   |
昇腾910B / 910C
   |
   | 对标NVIDIA A100/H100级别的国内替代方案
   |
昇腾950
   |
   | 下一代AI加速器
```

昇腾系列是华为以下产品线的一部分：

* **昇腾芯片** → 计算核心
* **CANN（计算架构 for 神经网络）** → 软件栈
* **MindSpore** → AI框架
* **Atlas服务器** → 硬件系统

同类生态系统对比：

| NVIDIA               | 华为                         |
| -------------------- | ---------------------------- |
| GPU                  | 昇腾NPU                      |
| CUDA                 | CANN                         |
| cuDNN                | 昇腾库                       |
| PyTorch CUDA后端     | PyTorch 昇腾NPU后端          |
| TensorRT             | MindSpore / CANN优化         |

---

## 2. GPU与昇腾NPU架构对比

简化版GPU：

```
CPU
 |
PCIe/NVLink
 |
GPU
 |
+----------------+
| CUDA核心       |
| Tensor Core    |
| SRAM/L2        |
| HBM            |
+----------------+
```

昇腾：

```
CPU
 |
PCIe / HCCS
 |
昇腾NPU
 |
+----------------+
| AI Core        |
| Cube Engine    |
| Vector Engine  |
| AI Memory      |
| HBM            |
+----------------+
```

关键区别：

* NVIDIA设计的是**通用并行处理器**
* 华为设计的是**张量计算引擎**

对于LLM工作负载：

```
Transformer：

Q,K,V投影
       |
       v
   矩阵乘法
       |
       v
   Attention
       |
       v
   FFN

```

大部分计算量为：

```
C = A × B
```

因此华为优化了：

```
矩阵乘法
+
内存带宽
+
通信
```

---

## 3. 昇腾950为何重要

AI加速器的竞争已不仅是FLOPS。

瓶颈所在：

```
训练LLM：

40% 计算
60%：

- HBM带宽
- 内存容量
- 互联
- 编译器效率
```

一款芯片需要：

### 计算

示例：

```
BF16 Tensor：

1000 TFLOPS
```

### 内存

```
HBM：

3 TB/s+
```

### 扩展

```
8个GPU/NPU

↓

数百/数千颗芯片
```

真正的竞争：

```
NVIDIA B200
        vs
华为昇腾950
        vs
AMD MI350
        vs
Google TPU
```

---

## 4. 昇腾软件栈

最困难的部分并非芯片本身。

NVIDIA的优势：

```
CUDA
 |
cuBLAS
 |
cuDNN
 |
TensorRT
 |
PyTorch
 |
数百万开发者
```

华为软件栈：

```
MindSpore
 |
PyTorch-NPU
 |
CANN
 |
昇腾硬件
```

编译器至关重要。

例如：

PyTorch：

```python
x = torch.matmul(a, b)
```

CUDA路径：

```
PyTorch
 |
ATen
 |
cuBLAS
 |
Tensor Core
```

昇腾：

```
PyTorch
 |
torch_npu
 |
CANN编译器
 |
Cube Engine
```

---

## 5. 与NVIDIA H100的关系

大致定位：

| 芯片               | 定位                     |
| ------------------ | ------------------------ |
| NVIDIA H100        | 2023年前沿               |
| NVIDIA H200        | HBM容量升级              |
| NVIDIA B200        | 2025年前沿               |
| AMD MI300X         | H100竞争对手             |
| 华为昇腾910C      | 国内AI加速器             |
| 华为昇腾950       | 未来一代                 |

昇腾950的目标并非在软件生态上全球击败NVIDIA。其目标是：

1. 减少对CUDA/NVIDIA的依赖
2. 构建中国AI基础设施栈
3. 提供足够的性能以支持：

   * DeepSeek风格训练
   * 企业级推理
   * 政府/云端AI

---

## 6. 重要的工程启示

对于LLM：

一款芯片不仅仅是：

```
TOPS/FLOPS
```

真正的技术栈是：

```
AI模型
 |
PyTorch/JAX
 |
编译器
 |
内核库
 |
运行时
 |
互联
 |
内存系统
 |
芯片
```

NVIDIA之所以主导市场，是因为CUDA掌控了整个栈。

华为面临的挑战与AMD ROCm类似：

```
硬件只占30%。
软件生态占70%。
```

对于从事LLM训练的人来说，有趣的比较可能是：

```
昇腾950
vs
AMD MI300X / MI350
vs
NVIDIA Blackwell
```

因为三者都在应对同一个瓶颈：**HBM + 分布式Transformer训练效率**。

参考文献：

* 华为昇腾AI计算平台：[https://www.hiascend.com/](https://www.hiascend.com/)
* 华为CANN架构：[https://www.hiascend.com/software/cann](https://www.hiascend.com/software/cann)
* NVIDIA Blackwell架构：[https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/)
* AMD Instinct加速器：[https://www.amd.com/en/products/accelerators/instinct.html](https://www.amd.com/en/products/accelerators/instinct.html)