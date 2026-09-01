---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 联想L-IG41M3 PCIe插槽
translated: true
type: note
---

问题：联想 L-IG41M3 主板配备的是哪种 PCIe 插槽——PCIe 3.0 还是 4.0，以及是否为 x16 规格？

答案：很可能是 **PCIe 2.0 x16**。

区别如下：

```text
PCIe 2.0 = 代际/速度
x16       = PCIe 通道数量/物理插槽
```

因此，G41 平台上的显卡插槽为：

```text
PCIe 2.0
└── x16 物理插槽
```

### 这对显卡维修意味着什么

现代显卡（如 RTX 4070）可以物理插入该插槽：

```text
RTX 4070
   │
   ▼
PCIe x16 插槽
   │
   ▼
G41 / L-IG41M3
PCIe 2.0 x16
```

但链接带宽会降级为 **PCIe 2.0**。

近似单向带宽如下：

| PCIe       | x16 带宽 |
| ---------- | --------:|
| PCIe 1.0   | 约 4 GB/s |
| **PCIe 2.0** | **约 8 GB/s** |
| PCIe 3.0   | 约 16 GB/s |
| PCIe 4.0   | 约 32 GB/s |

不过，对于**显卡维修**而言，这不一定是问题。你通常关心的是：

```bash
lspci
lspci -vv
dmesg
```

以及显卡是否：

```text
检测到 PCIe 设备？
       ↓
GPU 初始化完成？
       ↓
显存被识别？
       ↓
驱动加载成功？
       ↓
GPU 正常工作？
```

而非游戏下的最大带宽。

**购买前建议核实一点：** 联想有时会在相似主板名称下使用不同配置。如果你能发一张 **L-IG41M3 主板的照片**，尤其是 PCIe 区域，我可以直接识别出插槽类型。
