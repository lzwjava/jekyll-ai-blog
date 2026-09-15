---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 1000W电源适用于双RTX 4070s
translated: true
type: note
---

问题：对于 **两块 RTX 4070** 在 X370 Gaming K3 上，我应该使用什么电源？

回答：**我会买一个优质的 1000W 电源。**

粗略计算如下：

```text
RTX 4070 #1       ~200 W
RTX 4070 #2       ~200 W
CPU               ~65–150 W
主板/内存         ~50–80 W
SSD/风扇等        ~30–50 W
--------------------------------
典型总功耗        ~545–680 W
```

NVIDIA 将 RTX 4070 的功耗标为 **200 W TGP**，并推荐单块 4070 使用 **650 W 电源**。（[NVIDIA][1]）

对于 **2 × 4070**，我的选择是：

| 电源        | 结论                     |
| ---------- | --------------------------- |
| 650 W      | ❌ 不行                    |
| 750 W      | ⚠️ 余量太小              |
| 850 W      | ✅ 可以用                  |
| **1000 W** | **✅ 我的选择**             |
| 1200 W     | 除非未来升级显卡，否则过剩 |

### 更重要的是：电源接口

不要只看功率。对于两块 4070，请选择有 **足够独立 PCIe GPU 供电线** 的电源。

例如：

```text
电源
 ├── PCIe 线 #1 → RTX 4070 #1
 ├── PCIe 线 #2 → RTX 4070 #2
 └── CPU EPS 8-pin → X370 主板
```

最好使用带有原生 GPU 接口的现代 **ATX 3.x / PCIe 5.x 1000W 电源**，而不是依赖一堆转接器。

### 但这个主板还有一个更大的问题

X370 Gaming K3 有以下插槽：

```text
PCIEX16 → PCIe 3.0 x16
PCIEX4  → PCIe 2.0 x4
```

并且第二个插槽可能会根据其他 PCIe 插槽的使用情况降到 **x2**。（[GIGABYTE][2]）

因此：

```text
RTX 4070 #1 → PCIe 3.0 x16
RTX 4070 #2 → PCIe 2.0 x4   ← 非常受限
```

这 **并不是一个理想的双 4070 AI 机器**。电源不是瓶颈；**主板 的 PCIe 拓扑结构才是**。

如果你的目标是专门 **用两块 4070 进行 LLM 推理/训练**，我实际上会建议在购买电源之前重新考虑主板。

[1]: https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4070-family/?utm_source=chatgpt.com "GeForce RTX 4070 Family Graphics Cards | NVIDIA"
[2]: https://www.gigabyte.com/Motherboard/GA-AX370-Gaming-K3-rev-10/sp?utm_source=chatgpt.com "GA-AX370-Gaming K3 (Rev. 1.0) Motherboard - GIGABYTE Global"