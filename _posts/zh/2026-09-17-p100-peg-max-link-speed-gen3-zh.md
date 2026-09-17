---
audio: false
generated: true
image: false
lang: zh
layout: post
title: P100 PEG最大链路速度Gen3
translated: true
type: note
---

问题：对于华硕A68HM-E主板上的NVIDIA Tesla P100，**PEG Max Link Speed** 和 **PCI Latency Timer** 应如何设置？

答案：

对于您的 **Tesla P100 PCIe + 华硕A68HM-E**，我建议使用以下设置：

| BIOS 选项                | 设置值                                                          |
| ------------------------ | --------------------------------------------------------------- |
| **PEG Max Link Speed**   | **Gen3**                                                        |
| **PCI Latency Timer**    | **64 PCI Bus Clocks**                                           |
| PCIe Link Width          | **Auto / x16**                                                  |
| Above 4G Decoding        | **Enabled**（如果可用）                                         |
| CSM                      | 如果您的操作系统/GPU启动配置支持纯UEFI，建议 **Disabled**       |

其中关键的一项是 **PEG Max Link Speed = Gen3**。P100 PCIe 是一款 **PCIe 3.0 ×16** 的GPU，因此Gen3是其原生接口。NVIDIA 规定 PCIe Gen3 ×16，双向带宽最高可达32 GB/s。（[NVIDIA][1]）

### PCI Latency Timer

设置为 **64**。

但在现代PCIe GPU上，此设置远不如链路代际设置重要。PCI Latency Timer 主要是一个传统的PCI总线仲裁参数，它 **并不** 意味着“GPU延迟 = 64个周期”。您不应认为32与64之间会产生有意义的CUDA性能差异。

如果您的BIOS提供以下选项：

```text
PCI Latency Timer
    32 PCI Bus Clocks
    64 PCI Bus Clocks
    96 PCI Bus Clocks
    128 PCI Bus Clocks
```

我建议直接选择：

```text
64 PCI Bus Clocks
```

### A68HM-E 的一个关键问题

华硕A68HM-E 是一款老旧的 AMD A68H/FM2+ 平台，华硕为其提供了该代产品的手册和支持文档。（[ASUS Global][2]）

因此，如果您的P100当前显示类似：

```text
PCIe x16  @ x8 1.1
```

或

```text
PCIe x16  @ x16 2.0
```

**请勿立即归咎于 PCI Latency Timer。** 我们首先应确定主板/CPU实际协商的结果。

启动Linux后，运行：

```bash
lspci -vv -s $(lspci | awk '/NVIDIA/{print $1; exit}')
```

以及：

```bash
nvidia-smi -q | grep -i -A5 "PCI"
```

对于P100，理想结果大致为：

```text
LnkCap: Speed 8GT/s, Width x16
LnkSta: Speed 8GT/s, Width x16
```

`8 GT/s` 对应 **PCIe Gen3**。

因此，我的BIOS起点仅为：

```text
PEG Max Link Speed  -> Gen3
PCI Latency Timer   -> 64
```

[华硕A68HM-E 支持/手册](https://www.asus.com/us/supportonly/a68hm-e/helpdesk_manual/?utm_source=chatgpt.com)
[NVIDIA Tesla P100 PCIe 规格](https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com)

如果您能贴出 **完整的BIOS高级 → PCI/PCIe设置画面**（照片亦可），我可以针对P100具体映射每个设置。

[1]: https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/solutions/resources/documents1/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com "SPECIFICATIONS"
[2]: https://www.asus.com/us/supportonly/a68hm-e/helpdesk_manual/?utm_source=chatgpt.com "A68HM-E - Support"
