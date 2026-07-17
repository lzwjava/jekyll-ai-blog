---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么SXM在GPU上优于PCIe
translated: true
type: note
---

**问题：** 为什么 PCIe 形态在 GPU（例如 H100/H200/MI300X）上不如 SXM？

**答案：**

按实际影响排序的核心原因：

**1. 互连带宽（主要因素）**

- SXM 通过插槽将 NVLink（或 MI300X 的 Infinity Fabric）直接暴露给 NVSwitch 背板。
- H100 SXM：每 GPU 双向 NVLink 带宽 900 GB/s，通过 NVSwitch 实现全互联。
- H100 PCIe：NVLink 桥接（如果存在）仅提供约 600 GB/s，且只能配对相邻 GPU（2-GPU 桥接，非全网状）。无 NVSwitch 结构。
- 没有 NVLink 桥接时，PCIe 卡回退到 PCIe Gen5 x16，GPU 间通信双向带宽为 64 GB/s——通过 CPU 根复合体/PLX 交换机路由，增加延迟并与主机流量竞争。
- 对于张量并行或流水线并行训练（你的 GPT-2 760M 运行以及更大规模任务），all-reduce / all-gather 开销占主导。14 倍的带宽差异（900 vs 64 GB/s）直接限制了 2-4 个 GPU 以上的扩展效率。

**2. 供电**

- SXM 插槽直接从主板供电（H100 SXM 最高 700W，B200 SXM 最高 1000W）。
- PCIe 形态受插槽 + 电源接口限制，通常为 300-350W（H100 PCIe 为 350W，而 SXM 为 700W）——意味着更低的主频持续时间和更少的算力。

**3. 散热**

- SXM 模块专为 HGX 基板设计，配备按系统定制的直接液冷/均热板冷却方案。
- PCIe 卡在标准机箱插槽中使用涡轮式风冷——在持续全核负载下常见热节流。

**4. 拓扑结构 / 全互联**

- SXM + NVSwitch = 完全无阻塞的全互联拓扑，每个 GPU 都能以全 NVLink 速度与任意其他 GPU 通信。
- PCIe 多 GPU = 通过 PCIe 交换机和 CPU 形成的树形/星形拓扑，根据通信的 GPU 对产生不对称带宽。

**对你而言的实际数值：** 在 8 块 H100 SXM 上，针对 7B 参数梯度同步的 all-reduce 耗时约个位数毫秒。同样的操作在 8 块 H100 PCIe（无 NVLink 桥接）上可能慢 5-10 倍，直接降低 MFU（模型 FLOPs 利用率）——这就是为什么进行严肃预训练的云服务商（以及为什么你的 MI300X 设备很重要）默认采用 SXM/OAM 基板，而 PCIe 卡则定位于推理或单/双 GPU 推理工作负载（此时互连不是瓶颈）。

具体到 MI300X，它采用 OAM（开放加速器模块，AMD 的 SXM 等效方案）并配备 Infinity Fabric——同样的情况：每 GPU 聚合带宽 896 GB/s，相比之下，假设中的 PCIe 版 MI300X（AMD 实际上并未推出）将被 Gen5 x16 限制。

参考文献：

- [NVIDIA H100 数据手册](https://www.nvidia.com/en-us/data-center/h100/)
- [NVIDIA NVLink 和 NVSwitch](https://www.nvidia.com/en-us/data-center/nvlink/)
- [AMD Instinct MI300X 数据手册](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html)
