---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解码MODS记忆训练状态
translated: true
type: note
---

问题：**在 MODS 日志中，`NV_PFB_FBPA_*_TRAINING_STATUS = 0x00`、`0x02` 等值代表什么？**

答案：

是的——这些是**显存 PHY 训练结果**。它们对于诊断 VRAM 故障非常有用。

典型的 MODS 片段如下：

```text
NV_PFB_FBPA_0_TRAINING_STATUS = 0x00000000
NV_PFB_FBPA_1_TRAINING_STATUS = 0x00000002
NV_PFB_FBPA_2_TRAINING_STATUS = 0x00000000
NV_PFB_FBPA_3_TRAINING_STATUS = 0x00000008
```

可以将其理解为：

```text
GPU
 └── FBPA
      ├── FBPA 0 → 显存通道 A
      ├── FBPA 1 → 显存通道 B
      ├── FBPA 2 → 显存通道 C
      ...
```

训练本质上是 GPU 试图在 GPU 显存控制器与 GDDR 显存之间建立可靠的电信号时序。MODS 通过 `NV_PFB_FBPA_*_TRAINING_STATUS` 暴露结果。一个公开的 MODS 示例显示 `FBPA_3 = 0x08` 后跟 `Memory DQ write training failed`。（[VLab][1]）

### 有用的值

对于常见的 GDDR MODS 日志：

| 训练状态     | 含义                     |
| ------------ | ------------------------ |
| `0x00`       | **通过 / 训练完成**      |
| `0x02`       | **Bank 0 故障**          |
| `0x08`       | **Bank 1 故障**          |
| `0x0A`       | **Bank 0 和 Bank 1 均故障** |

因此：

```text
FBPA_0 = 0x00
```

表示该通道训练成功。

而：

```text
FBPA_0 = 0x02
```

大致表示：

```text
通道 A
└── Bank 0  ← 故障
```

并且：

```text
FBPA_0 = 0x08
```

表示：

```text
通道 A
└── Bank 1  ← 故障
```

以及：

```text
FBPA_0 = 0x0A
```

表示两者均故障：

```text
通道 A
├── Bank 0  ← 故障
└── Bank 1  ← 故障
```

这种映射关系在实用的 MODS/MATS 维修工作中也有记载。（[GPU Solutions][2]）

### 重要：`FBPA_0` 不一定等于“VRAM 芯片 0”

这是人们经常感到困惑的地方。

`FBPA_0` 是一个**内存控制器/通道拓扑标识符**，而不仅仅是“第一个物理 VRAM 芯片”。

例如，对于具有通道 A–H 的显卡：

```text
FBPA_0 → A
FBPA_1 → B
FBPA_2 → C
FBPA_3 → D
...
```

那么：

```text
FBPA_3 = 0x08
```

在常见映射下将指示：

```text
D1
```

但是**哪个物理内存封装是 PCB 上的 D1，取决于 GPU/显卡的内存拓扑**。训练状态告诉你失败的逻辑内存位置；它本身并不能告诉你物理问题是 DRAM 封装、焊点/焊盘、走线还是 GPU 端连接。（[GPU Solutions][2]）

### 这与你之前的 `Error 220` 不同

这个区别对你的显卡很重要。

你的截图显示：

```text
Error 220
Gpu.Initialize pci device not found
```

这意味着 MODS **还没进展到足以初始化 GPU**。

而像这样的日志：

```text
NV_PFB_FBPA_0_TRAINING_STATUS = 0x00000000
...
NV_PFB_FBPA_3_TRAINING_STATUS = 0x00000008

Error 00000507:
Memory DQ write training failed
```

则是一种完全不同的情况：**GPU 已被找到并初始化到足以执行显存训练的程度，但某个显存通道失败了。** 公开的 MODS 示例正好展示了这一序列。（[VLab][1]）

因此，如果你正在维修 GPU，**完整的 `NV_PFB_FBPA_*_TRAINING_STATUS` 块比单独的错误代码要有用得多。**

如果你粘贴你的实际代码块，例如：

```text
NV_PFB_FBPA_0_TRAINING_STATUS = ...
NV_PFB_FBPA_1_TRAINING_STATUS = ...
...
```

我可以将其解码为 **A0/A1/B0/B1 等，并告诉你哪些 VRAM 通道可能存在问题**。

参考文献：

* [MODS/MATS 显存训练示例](https://vlab.su/viewtopic.php?f=48&p=1010828&t=124090)（[VLab][1]）
* [MODS FBPA 训练状态解码](https://gpusolutions.net/tag/memory-testing/)（[GPU Solutions][2]）

[1]: https://vlab.su/viewtopic.php?f=48&p=1010828&t=124090&utm_source=chatgpt.com "MATS/MODS 400/455/520/570 Тест видеопамяти nVidia для флешки • VLab"
[2]: https://gpusolutions.net/tag/memory-testing/?utm_source=chatgpt.com "Memory Testing Archives - GPU Solutions"