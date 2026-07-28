---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'GTX 580: 用于AlexNet的GPU'
translated: true
type: note
---

问题：NVIDIA RTX 580 介绍，以及伊利亚·苏茨克维（Ilya Sutskever）和辛顿（Hinton）是否在 AlexNet 中使用过它？

答案：

没有 **NVIDIA RTX 580** 这款产品，你指的应该是 **NVIDIA GeForce GTX 580**（2010 年发布）。它是让 AlexNet 取得突破的关键 GPU 之一。

![Image](https://images.openai.com/static-rsc-4/7kCeJNL-l4Rk80tBXjG8Rce7M_EtJYvsz6Qbn-AXxG0VAL23mKi7oMycJ44QtUjtULEDmdSlrV-OBPDMcYbWVlupUPdONIZDWyVo_qN3v-MnTUZSnF1ypNPb7el6I_DHoq2ZYgmCyYV3Jx8OOqKdxz_1Oqqy9Lq0RjMXnL3BuYAJvHg6JXKp8YMZPD08bKA4?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Tnq9y-bzdeo_XmDERupKdqMobrjVlSD8ofFyAVxV_Zjp2iWcV8UFeBbcc6VWvR-2jk5MSsLQ0-d88HS5dqg9N2yG5Frt4-9mqaZ7Lcc0jJDbk9yd_T7RSNWPjOCpxh7-jSu1qwVBmTOPvHGrdlTVNXKUHuS82_sapb1N_Rj2SpaQ-rFVUOhArUb3sJMG2Qcb?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/6E3X1mijYM1CfmhLDH0kcJ_KIW7rtECq0CMsYKyOBU2wIx8X7XAr4OA1TOLRbAoGxjr5t2CBk8uimFOpV4p4Fx0AdfqyfIuP8a3n1srG-FKcMjsBjy_JAvYD27wlwEhAnc9VIiQ-9WpJQKzSvuymre2UADX7djyKOdj_u-bpOX9zBh8qO00-jOlOqGvown8O?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/zwGFLcMtny7ZQvQS9MuJ9tJYhBdL8j6t559675XQ7XZA2sk8qN4hD-W63DxVyRz2JOorPR1Szj7zlpEYi5yr0A7GCLQFJGxOPti6KTFImv0s_958NaM5wuID3rvH9wdy4ab3QqAV4Z41rWLk57Ip7v95F6Ja6Bflwgoai5GdInPZ3InT2Dk6SxRn6mrx2Pde?purpose=fullsize)

**GeForce GTX 580**：

* 架构：**Fermi**
* 发布日期：2010 年 11 月
* CUDA 核心：**512**
* 显存：通常为 **1.5 GB GDDR5**
* 内存带宽：约 192 GB/s
* FP32 算力：约 1.5 TFLOPS
* 功耗：约 244W TDP

按现代标准来看，它的规格很小：

* RTX 4070：约 29 TFLOPS FP32，12GB 显存
* RTX 4090：约 83 TFLOPS FP32，24GB 显存

但在 2012 年，它对于深度学习来说堪称怪兽。

---

### 伊利亚·苏茨克维和杰弗里·辛顿是否在 AlexNet 中使用了 GTX 580？

是的，但具体的 GPU **并非 RTX 580**。AlexNet 是在 **两块 NVIDIA GTX 580 GPU** 上训练的。

那篇著名的 2012 年论文：

> "ImageNet Classification with Deep Convolutional Neural Networks"

作者：

* Alex Krizhevsky
* Ilya Sutskever
* Geoffrey Hinton

使用了：

* 2 × GTX 580
* 总共 3GB GPU 显存（每块 1.5GB）
* CUDA
* 自定义 GPU 并行化

该模型具有：

* 6000 万个参数
* 65 万个神经元
* 5 个卷积层
* 3 个全连接层

巧妙之处在于将网络拆分到两块 GPU 上。

---

### 为什么 GTX 580 足够用？

因为按今天的标准，AlexNet 规模很小。

简化对比：

| 模型          | 参数数量 | 所需 GPU 显存 |
| -------------- | ---------: | ----------------: |
| AlexNet (2012) |        60M |              ~3GB |
| GPT-2 124M     |       124M |              ~GB 级 |
| Llama 7B       |         7B |       ~14GB+ FP16 |
| GPT-4 级别     |    未知 |              巨大 |

真正的突破不在于 GPU 的原始算力，而在于认识到：

```
CNN + ReLU + dropout + GPU CUDA
        ↓
训练更大的网络
        ↓
超越传统计算机视觉
```

---

### 有趣的历史联系

在 AlexNet 之前，GPU 主要用于图形处理。AlexNet 展示了：

```
GPU
 |
 +-- 图形处理
 |
 +-- 科学计算
 |
 +-- 神经网络训练
```

这直接催生了现代 NVIDIA AI 业务。

黄仁勋的名言：

> "你卖出的 GPU 越多，创造出的 AI 就越多。"

正是源于这一转型。

RTX 系列是在很久之后才出现的：

* GTX 580 → Fermi (2010)
* GTX 680 → Kepler (2012)
* GTX 980 → Maxwell (2014)
* GTX 1080 → Pascal (2016)
* RTX 2080 → Turing (2018)
* RTX 4090 → Ada Lovelace (2022)

如今你的 RTX 4070 大约拥有相当于驱动 AlexNet 革命的那两块 GTX 580 **20 倍的算力** 和 **8 倍的显存**。