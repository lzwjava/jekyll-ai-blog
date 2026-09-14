---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tesla P100 需要强制风冷
translated: true
type: note
---

问题：Tesla P100 有散热风扇吗？它能用在 B150M Pro + i5-6500 上吗？

答案：**电气上可以，但散热是最大的问题。**

### 1. P100 PCIe 通常**没有风扇**

NVIDIA **Tesla P100 PCIe 是被动散热的**。它有一个大型散热片，但**没有板载鼓风机/风扇**。NVIDIA 明确将散热方案定义为*被动式*，并表示需要系统气流。 ([NVIDIA 图片][1])

它的功耗高达 **250 W**，需要大量气流穿过散热片。 ([NVIDIA][2])

所以：

```text
P100
 ┌─────────────────┐
 │   大型散热片    │
 │ ███████████████ │
 │     GP100       │
 └─────────────────┘
        ↑
   无板载风扇
```

普通的台式机机箱仅靠一个弱排风扇是**不行的**。你需要强劲的气流直接吹过 P100 散热片，或者使用后装导流罩/风扇套件。

### 2. B150M + i5-6500：**可以**

假设你的主板是微星 **B150M PRO** 系列中带有 PCIe x16 插槽的型号，P100 在硬件/PCIe 层面可以正常工作。

例如，B150M PRO-VHL 具有：

```text
PCIe 3.0 x16
```

而 P100 是：

```text
PCIe Gen3 x16
```

两者完全匹配。 ([微星][3])

你的 **i5-6500 也是第六代 LGA1151 CPU**，正是这些 B150 主板支持的代数。 ([华硕全球][4])

CPU 本身不是兼容性问题。

### 3. 真正的问题：电源

这是我最关注的部分。

P100：

```text
GPU 功耗：      250 W
PCIe 接口：     x16
外部供电：     通过 8-pin 最高约 240 W
```

NVIDIA 的规格显示 P100 最高可消耗 **250 W**，其中辅助 12 V 输入占大部分。 ([NVIDIA][2])

我建议至少使用：

```text
额定 650 W 的优质电源
        +
正确的 8-pin PCIe GPU 供电线
```

如果是廉价/老旧的电源，我**不会**在上面接一块 250 W 的 P100。

### 4. 另一个重要事项：P100 是计算卡

P100 不像 GTX 1080。它是 **Tesla 计算加速器**。

对于你的配置：

```text
B150M
  │
  ├── i5-6500
  │
  ├── P100 12/16 GB
  │      └── PCIe 3.0 x16
  │
  └── 电源 ── 8-pin ── P100
```

用于 **CUDA / PyTorch / 模型推理 / 训练**，这正是它的设计用途。

但不要指望 P100 像普通游戏显卡一样带有显示输出。PCIe P100 主要是一个**无头计算加速器**。

### 我的建议

如果你想买一块便宜的二手 P100 用于老台式机，我的看法是：

**B150M + i5-6500 + P100 = 可行**，前提是你满足：

* ✅ PCIe x16 插槽
* ✅ 优质的 **650 W 以上电源**
* ✅ 正确的 **8-pin PCIe 供电**
* ✅ 全高/双槽位空间
* ⚠️ **强劲的机箱气流**
* ⚠️ Linux 更适合 CUDA 计算主机

**被动散热是我会优先解决的问题**。P100 在 250 W 下持续运行，如果没有足够的气流，会严重降频或达到热极限。NVIDIA 规定的运行上限约为 80°C，在 82°C 左右会降速。 ([Scribd][5])

如果你是为了**LLM 推理/训练**而购买，请告诉我**确切的 P100 型号（12GB/16GB，PCIe/SXM2）**以及你的**电源型号**，我就能判断是否值得购买。

[1]: https://images.nvidia.com/content/tesla/pdf/nvidia-tesla-p100-PCIe-datasheet.pdf?utm_source=chatgpt.com "数据表：Tesla P100"
[2]: https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/NV-tesla-p100-pcie-PB-08248-001-v01.pdf?utm_source=chatgpt.com "规格"
[3]: https://www.msi.com/Motherboard/B150M-PRO-VHL/Specification?utm_source=chatgpt.com "B150M PRO-VHL 规格 | 微星全球 - 高端游戏与专业创作的领先品牌"
[4]: https://www.asus.com/us/supportonly/b150m-et-v5/helpdesk_cpu/?utm_source=chatgpt.com "B150M-ET/V5 - 支持"
[5]: https://www.scribd.com/document/738724628/NV-tesla-p100-pcie-PB-08248-001-v01?utm_source=chatgpt.com "NV Tesla p100 Pcie PB 08248 001 v01 | PDF | 图形处理器 | 计算"