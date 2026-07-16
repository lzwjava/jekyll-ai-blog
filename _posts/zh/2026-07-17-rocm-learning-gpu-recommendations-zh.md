---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ROCm学习GPU推荐
translated: true
type: note
---

问题：推荐用于学习 ROCm / PyTorch / LLM 的 AMD GPU。

回答：

针对你的情况（**已有 RTX 4070 + MI50 16GB 即将到手 + 对 ROCm 感兴趣**），我对 ROCm 学习显卡的排名如下：

## 1. AMD Instinct MI50 16GB — 最便宜的 ROCm 学习卡 ⭐⭐⭐⭐⭐

[AMD Radeon Pro VII 16GB HBM2](https://www.newegg.com/amd-100-506163-radeon-pro-vii-16gb-graphics-card/p/N82E16814105105?item=9SIB1PGGS91889&negg_topt=22&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com) 属于同一家族；MI50 是 Instinct 版本。

原因：

```
MI50
-------------
16GB HBM2 ECC
4096-bit 内存总线
~1 TB/s 带宽
gfx906
CDNA 前身
```

价格：

```
二手 ¥600-1000
```

你花 ¥630 买 MI50 其实非常划算。

适合：

* 学习 ROCm 安装
* HIP 编程
* PyTorch ROCm
* 内核实验
* LLM 推理

缺点：

* 架构老旧
* 与较新 GPU 相比，ROCm 支持正逐渐老化/弃用（[AMD ROCm][1]）

示例：

```bash
pip install torch --index-url https://download.pytorch.org/whl/rocm6.3
```

---

## 2. Radeon Pro VII 16GB — 带显示输出的 MI50 ⭐⭐⭐⭐

[AMD Radeon Pro VII 16GB HBM2](https://www.newegg.com/amd-100-506163-radeon-pro-vii-16gb-graphics-card/p/N82E16814105105?item=9SIB1PGGS91889&negg_topt=22&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

基本上：

```
Radeon Pro VII
=
Radeon VII 工作站版
=
MI50 硅片家族
```

规格：

```
16GB HBM2
4096-bit
1TB/s 带宽
gfx906
```

非常有趣的原因：

* 二手便宜
* 工作站驱动
* ECC
* HBM

但同样的问题：

```
gfx906 已老旧
```

ROCm 的未来支持较弱。（[AMD ROCm][1]）

---

## 3. RX 7900 XT 20GB — 最佳现代 ROCm 性价比 ⭐⭐⭐⭐⭐

如果你想要一张能用多年的卡：

```
RX 7900 XT
----------------
RDNA3
20GB GDDR6
gfx1100
```

ROCm 官方支持 RX 7900 XT/XTX/GRE 级别显卡。（[AMD ROCm][2]）

优势：

* 现代 ROCm
* 20GB 显存
* 速度快
* 支持更新的 PyTorch wheels

对于 LLM：

```
7B FP16
14GB

13B Q4
~10GB

30B Q4
~18GB
```

20GB 比 12GB 实用得多。

---

## 4. RX 7900 XTX 24GB — 消费级“穷人的 MI300” ⭐⭐⭐⭐⭐

```
RX 7900 XTX
----------------
24GB 显存
384-bit
960GB/s 带宽
```

非常适合：

* llama.cpp
* vLLM 实验
* 微调小模型

缺点：

* 价格贵
* 游戏卡散热

---

## 5. Radeon RX 7800 XT 16GB ⭐⭐⭐

更便宜的现代选择：

```
7800 XT
-------------
16GB
RDNA3
gfx1101
```

但不如 7900 XT 有吸引力。

---

# 学习 ROCm 时应避免的显卡

## RX 6700 XT 12GB

我不建议购买。

原因：

```
12GB 显存
RDNA2
gfx1031
```

ROCm 支持远不如人意。目前官方支持主要聚焦于较新的 Radeon 系列，如 RX 7900 系列。（[AMD ROCm][2]）

---

## Radeon VII

除非非常便宜，否则不要买。

```
16GB HBM2
```

看起来不错，但：

```
老旧 gfx906
```

与 MI50 相同的问题。

---

# 针对你的具体推荐

你目前的配置：

```
RTX 4070 12GB
+
MI50 16GB
```

已经是一个非常棒的学习组合。

我会建议：

### 低成本路线

```
保留 MI50
↓
学习 ROCm/HIP
↓
运行 PyTorch ROCm
↓
进行实验
```

成本：

~¥630

非常棒。

---

### 升级路线

以后购买：

```
RX 7900 XT 20GB
```

或

```
RX 7900 XTX 24GB
```

然后：

```
RTX 4070
    CUDA 生态

RX 7900 XT/XTX
    ROCm 生态

MI50
    老旧 Instinct/HBM 实验
```

你覆盖了三个世界。

对于学习 GPU 系统的 AI 工程师来说，这实际上比再买一张 NVIDIA 卡更有价值。

参考资料：

* AMD ROCm 支持 GPU 矩阵（[AMD ROCm][2]）
* AMD ROCm 6.x 兼容性列表（MI50 / Radeon Pro VII / RX 7900 系列）（[AMD ROCm][1]）
* Radeon Pro VII 16GB HBM2 产品列表

[1]: https://rocm.docs.amd.com/projects/install-on-linux/en/docs-6.1.5/reference/system-requirements.html?utm_source=chatgpt.com "系统要求（Linux）— ROCm 安装（Linux）"
[2]: https://rocm.docs.amd.com/projects/install-on-linux/en/docs-7.1.0/reference/system-requirements.html?utm_source=chatgpt.com "系统要求（Linux）— ROCm 安装（Linux）"