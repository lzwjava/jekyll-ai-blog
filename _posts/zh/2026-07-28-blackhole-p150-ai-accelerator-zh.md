---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Blackhole P150 AI加速器
translated: true
type: note
---

问题：**Blackhole@ P150 系列是什么？**

答案：

**Blackhole P150 系列**是 Tenstorrent 推出的一款 AI 加速卡。它是 NVIDIA GPU 在 AI 训练/推理领域的竞争对手，但采用了截然不同的架构：**RISC-V + Tensix AI 核心**，而非 CUDA GPU。([Tenstorrent][1])

![Image](https://images.openai.com/static-rsc-4/nFFF1ELWmmr4deT2uoEeQDXIOtY7SRQvfuFh5kUfJOI5reSgJuoWP1lgNDdINviWHfLvBqr5Gk6Y_7cOToNmr4rzQ3XVefRetheuCIjdR0tFuZi7_Wxu3TdmZ6Yxe9-VHvXuzgT77ojvx_rFf1_l8efTcsnap6V7aTimXlPMb3HITU8T3RNS-6VlQZcxA4H1?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/pKnUVcMCqocr9IrnJfub8597Z3DRqEQ-qKnlsbtNgE7orowe79kk-dkXD4xMbSJLB946zAfhPhf_fLLhrKctt-XqmPMz-xR4BB_iTRzXbTowNAzelGov6ywDZrE2nnk4E8WX_lMU5XgJFt5fuiAwIpltkhbjGXeoZDaR1ENog6Fp3aKwNkEIsDZdB4RF_Elx?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/CFQ9kGiDO_JOMq6i4pRbSnGmkETufczyd-rsXBXl6_GCyokw4ZuA6tw0DUOY1NeWLNge4CNhhRwsp7_Eu1_KGUyRxvR4QcmqVTdt4YjEGI8MSdpARPLsyLs5x6TzDzbwcIjvlNfCGQEv5hOpXSFkPAsrTZVwYQRn4OwRFqbMKmr-WQtau4yM0PWCe8N242LM?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/YkwD56dSz4eOAkD5OzFAJ3h7rfZrobL5JGUsGbwEFNSkkU92R92W5nqVzrltL6NNTQLwLoPt9Nmc2AuBf5SM0eK8VBw3nS6DAnkAUYH-O8as3aCMQW3FWqSVZ3-JHDUFO4sBmc1Eer1o4Qh2fKCCE94NhGefPIH9NgxhTPEDMuztBPH6TeZfKdNPGG2Cd4qy?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/z0dsUw_ZOO43tYA6W-5W0TMHzV6rKpE2bILgVoVr7Mesq9NWsYLk9c2KvCWSLMFxSkdCfHS7qjymLqin1cot2FVXXUMewQga2xcsDVXoNS6z9gidBsDancUBCD2JFVFbWZocNlQRDG_IGcnlUs8RzeH6O4dqRIvjp_B9RsL7uGye5Tjb2fTnNZyC-9CizJfo?purpose=fullsize)

## 硬件概览

**Blackhole P150**：

* PCIe Gen 5 AI 加速卡
* 单个 Blackhole 处理器
* 功耗最高约 300W
* 4 个 QSFP-DD 高速链路，用于多卡扩展
* 专为 AI 工作负载（训练/推理）设计 ([Tenstorrent][1])

P150 本质上是一个**大型 AI ASIC 加上许多小型 RISC-V 核心**：

```
Blackhole 芯片

        RISC-V CPU
            |
            |
   +----------------+
   | Tensix 核心    |
   | AI 计算        |
   +----------------+
            |
     SRAM / 内存
            |
       PCIe / 以太网
```

Tenstorrent 的设计理念：

* NVIDIA：

```
CUDA 生态系统
    |
GPU SM
    |
Tensor Core
```

* Tenstorrent：

```
RISC-V 控制核心
    |
Tensix AI 处理器
    |
数据流执行
```

([Spinics][2])

---

## 为什么对 AI 工程师有吸引力？

有趣之处在于**软件开放性**。

Blackhole 卡实际上可以在内部运行 Linux，因为它包含 RISC-V 核心。Linux 内核社区已添加对 Blackhole P100/P150 PCIe 卡的支持。([Spinics][2])

因此从概念上看：

```
普通 GPU：

CPU
 |
PCIe
 |
NVIDIA GPU
 |
CUDA 内核


Blackhole：

主机 CPU
 |
PCIe
 |
Blackhole
 |
  +-- Linux
  +-- RISC-V 核心
  +-- AI 加速核心
```

这更接近于一台**分布式 AI 计算机**，而非纯粹的 GPU。

---

## 性能对比（粗略）

粗略对比：

| 卡                     | 架构              | 主要生态系统       |
| ---------------------- | ----------------- | ---------------- |
| NVIDIA H100            | GPU + CUDA        | 主导地位         |
| AMD MI300X             | GPU + ROCm        | 开放替代方案     |
| Tenstorrent Blackhole P150 | RISC-V + Tensix  | 新兴生态系统     |

Blackhole P150 的目标：

* LLM 推理
* AI 训练实验
* 大规模 AI 集群

P150 并非试图在软件成熟度上立刻击败 H100。它的赌注是：

> “CUDA 今天是护城河，但未来的 AI 硬件应该是可编程且开放的。”

这与 RISC-V 背后的理念相似。

---

## 针对你的配置（RTX 4070 + LLM 训练）

P150 之所以值得关注，是因为：

你当前的架构：

```
PyTorch
 |
CUDA
 |
RTX 4070
```

将变为：

```
PyTorch
 |
TT-Metal / Tenstorrent 栈
 |
Blackhole
```

生态系统差距是主要问题。

对于在本地训练 GPT-2/nanoGPT 的人来说，目前：

* RTX 4090 / 5090 → 最简单
* MI300X → 严肃训练
* Blackhole → 对未来 AI 架构的研究

---

## 为什么人们谈论它

Tenstorrent 由 Jim Keller 领导，他因 CPU 架构工作（AMD Zen、Apple A 系列参与）而闻名。该公司正试图构建一个后 CUDA 时代的 AI 计算平台。([Tenstorrent][1])

对于 AI 基础设施构建者来说，Blackhole 有趣之处在于它结合了：

* 开放指令集（RISC-V）
* AI 加速器
* 可扩展互连
* 支持 Linux 的计算节点

基本上：**“如果 AI 集群更像计算机而非 GPU 农场来构建，会怎样？”**

参考文献：

* ([Tenstorrent][1])
* ([Spinics][2])

[1]: https://tenstorrent.com/en/support?utm_source=chatgpt.com "Support | Tenstorrent"
[2]: https://www.spinics.net/lists/kernel/msg5869923.html?utm_source=chatgpt.com "[PATCH v2 0/8] RISC-V: Add support for Tenstorrent Blackhole SoC — Linux Kernel"