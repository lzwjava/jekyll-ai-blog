---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华为AI芯片架构师廖恒
translated: true
type: note
---

问题：华为科学家廖恒（Liao Heng）是谁？

答案：

廖恒是华为/海思（HiSilicon）的一位资深科学家，主要以其在**AI加速器架构、芯片设计和计算系统**方面的成就而闻名。他并非像任正非或何庭波那样面对公众的名人，但被认为是华为在半导体研究领域的重要技术领军人物之一。（[清华大学][1]）

关键职业经历：

* **华为Fellow**
* 前**华为2012实验室首席科学家**
* 前**海思图灵架构与设计部部长**
* 参与华为**昇腾AI芯片架构**相关工作（昇腾 / Ascend）

他的背景异常偏向硬件：

* 曾在**清华大学计算机系**学习，包括清华“少年班”路径。
* 在**普林斯顿大学电子工程系**从事博士后研究。
* 在美国半导体行业**PMC-Sierra**工作，担任架构和研发领导职务，之后加入华为。

他的技术领域：

```
AI workload
     |
     v
Algorithm / Model
     |
     v
Compiler + Runtime
     |
     v
AI Accelerator Architecture
     |
     v
NPU / ASIC / Memory / Interconnect
```

廖恒主要关注下半部分：

* AI加速器架构
* NPU设计
* 芯片/系统架构
* 高性能计算基础设施

这是公司与NVIDIA竞争的层面。像DeepSeek或Qwen这样的模型不仅需要GPU/NPU，还需要：

* 张量计算单元
* HBM/内存带宽
* 芯片间通信
* 编译器栈
* 分布式推理/训练系统

华为近期在AI基础设施方面的工作还涉及大规模昇腾集群和LLM服务架构。一篇关于华为CloudMatrix384的2025年论文将Heng Liao列为从事大规模LLM推理架构的作者之一。（[arXiv][2]）

粗略对比：

| 人物 | 主要领域 |
| --- | --- |
| 任正非 | 公司战略 |
| 何庭波 | 半导体领导力 |
| 廖恒 | 芯片架构/AI计算系统 |
| 徐直军 | 企业与产品战略 |
| 王成录 | 软件生态 |

从AI工程师的角度来看，廖恒代表了AI的**“硬件+系统”方面**。未来的竞争不仅仅是训练更大的模型，而是整个栈：

```
Model
 ↓
Framework (PyTorch / MindSpore)
 ↓
Compiler (CUDA / Ascend CANN)
 ↓
Runtime (vLLM / SGLang style serving)
 ↓
Accelerator (GPU / NPU / ASIC)
 ↓
Silicon
```

像廖恒这样的人在硅边界附近工作。对于从事SGLang/vLLM、分布式推理、ROCm/CUDA或定制加速器的人来说，这是相同的战略层面：通过系统工程让AI更便宜、更快。（[career.huawei.com][3]）

参考文献：

* （[清华大学][1]）
*
* （[复旦新闻][4]）
* （[arXiv][2]）

[1]: https://www.tsinghua.edu.cn/info/1181/35825.htm?utm_source=chatgpt.com "华为2012实验室总裁何庭波访问清华 探讨基础学科人才培养合作-清华大学"
[2]: https://arxiv.org/abs/2506.12708?utm_source=chatgpt.com "Serving Large Language Models on Huawei CloudMatrix384"
[3]: https://career.huawei.com/cn/young-genius?utm_source=chatgpt.com "挑战课题专项招聘"
[4]: https://news.fudan.edu.cn/2022/0924/c5a132488/page.htm?utm_source=chatgpt.com "复旦-华为微电子联合实验室2022年度研讨会圆满召开"
