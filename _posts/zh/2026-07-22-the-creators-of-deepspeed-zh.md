---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSpeed的创建者
translated: true
type: note
---

问题：DeepSpeed 是谁发明的？

答案：

DeepSpeed **由微软研究院 AI at Scale 团队创建**，并非个人发明。它于 **2020 年 5 月** 作为 PyTorch 优化库开源，用于训练和服务超大型神经网络。（[维基百科][1]）

DeepSpeed 原始项目背后的关键人物包括：

* Jeff Rasley
* Samyam Rajbhandari
* Olatunji Ruwase
* Yuxiong He

这四位作者撰写了最初的 **ZeRO（零冗余优化器）** 论文，这是使 DeepSpeed 闻名的核心创新。ZeRO 将优化器状态、梯度和参数跨 GPU 分区，大幅减少内存使用，同时保持相同的模型语义。DeepSpeed 后续的大多数功能（ZeRO-Offload、ZeRO-Infinity、Ulysses、MoE 支持等）都建立在此基础之上。（[微软][2]）

### 领导力

与 DeepSpeed 整体愿景最密切关联的研究者是 **Yuxiong He**。他领导微软研究院 AI at Scale 工作，并是许多 DeepSpeed 重要论文的高级作者，包括：

* ZeRO
* ZeRO-Offload
* ZeRO-Infinity
* DeepSpeed-MoE
* DeepSpeed Inference
* ZeRO++

### 时间线

| 年份      | 里程碑                                                                 |
| --------- | ---------------------------------------------------------------------- |
| 2020      | 微软研究院开源 DeepSpeed                                              |
| 2020      | 引入 ZeRO 优化器                                                      |
| 2021      | ZeRO-Offload 和 ZeRO-Infinity                                         |
| 2022      | DeepSpeed Inference 和 DeepSpeed-MoE                                  |
| 2023–2024 | Ulysses、ZeRO++、Universal Checkpointing、Domino 及其他扩展优化       |

如今，DeepSpeed 仍然是 PyTorch 三大主流分布式训练框架之一，另外两个是：

* PyTorch Distributed
* NVIDIA Megatron-LM
* DeepSpeed

参考资料：

* [DeepSpeed GitHub](https://github.com/microsoft/DeepSpeed?utm_source=chatgpt.com)
* [微软研究院 DeepSpeed 项目](https://www.microsoft.com/en-us/research/project/deepspeed/people/?utm_source=chatgpt.com)
* （[微软][3]）

[1]: https://en.wikipedia.org/wiki/DeepSpeed?utm_source=chatgpt.com "DeepSpeed"
[2]: https://www.microsoft.com/en-us/research/project/deepspeed/publications/?utm_source=chatgpt.com "DeepSpeed - 微软研究院：出版物"
[3]: https://www.microsoft.com/en-us/research/project/deepspeed/people/?utm_source=chatgpt.com "DeepSpeed - 微软研究院：团队成员"
