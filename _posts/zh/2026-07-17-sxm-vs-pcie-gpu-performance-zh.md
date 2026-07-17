---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SXM与PCIe GPU性能对比
translated: true
type: note
---

问题：为什么SXM外形的GPU（H100/H200/MI300X SXM）比PCIe版本更好？

答案：

**1. 互联带宽 —— 关键因素**

- PCIe显卡：GPU间的流量通过NVLink Bridge（有限，仅成对）或回退到PCIe本身。
  - H100 PCIe：NVLink bridge仅能绑定2个GPU，双向约600 GB/s，其余流量通过PCIe Gen5 x16（每个方向约64 GB/s，与主机共享）。
- SXM显卡：插入专有插座，直连基板上的完整NVSwitch交换结构。
  - H100 SXM：18条NVLink 4.0链路 = 每GPU **900 GB/s** 双向，全互联、无阻塞，通过NVSwitch实现。
  - MI300X OAM（类似概念，AMD的SXM等效方案）：Infinity Fabric聚合带宽约896 GB/s。

对于采用张量/流水线并行的训练，all-reduce和all-to-all操作主导了步进时间。900 GB/s的全互联与约64 GB/s的PCIe路由相比，差距巨大——这决定了GPU是真正作为一个大型加速器工作，还是8个独立岛屿被一条同时服务主机DMA的总线所瓶颈。

**2. 供电能力**

- PCIe外形受限于插槽功耗规格：H100 PCIe = 300-350W。
- SXM基板直接供电：H100 SXM = 700W，MI300X SXM(OAM) = 750W。
- 更高的功耗余量 → 更高的持续时钟频率 → 在仅考虑芯片本身的情况下，H100 PCIe的FP16/BF16吞吐量比H100 SXM低约15-20%，尚未计入互联影响。

**3. 拓扑 / 扩展性**

- SXM主板（HGX/UBB）设计为4或8 GPU单元，NVSwitch已预接线，无需桥接电缆，对等流量无需经过主机CPU热路径。
- PCIe显卡需要交换拓扑、NVLink桥接器（H100 PCIe上仅成对），且跨插槽传输需经主机CPU/根复合体中介，增加延迟并占用本应给网卡/NVMe的PCIe通道。

**4. 对您工作负载的实际影响**

对于您在MI300X上进行的GPT-2 760M训练——如果使用OAM/SXM MI300X（8 GPU UBB），梯度同步的all-reduce开销扩展性远优于PCIe MI300X。在小模型规模（760M）下影响较小，因为计算/通信比有利；但一旦扩展到您每月训练20亿 token、更大架构的模型时，互联将首先成为瓶颈，而非FLOPs。

**经验法则：** PCIe适用于推理/单GPU/小型微调。一旦进行多GPU预训练且使用张量并行，SXM就是必须的，因为通信密集型操作（all-reduce、all-to-all）正是PCIe显卡性能急剧下降的地方。

参考资料：

- [NVIDIA H100 数据手册](https://www.nvidia.com/en-us/data-center/h100/)
- [NVLink 和 NVSwitch 概述](https://www.nvidia.com/en-us/data-center/nvlink/)
- [AMD Instinct MI300X 数据手册](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html)