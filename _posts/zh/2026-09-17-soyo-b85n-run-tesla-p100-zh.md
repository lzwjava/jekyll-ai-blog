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

问题：**SOYO SY-B85N + i5-4460 + 4GB DDR3** 能否运行 Tesla P100？

答案：**可以，这也是个不错的选择。** 该基础平台与 PCIe Tesla P100 兼容。

```text
SOYO SY-B85N
├── i5-4460
├── DDR3 4GB
└── PCIe x16
      └── Tesla P100
```

关键点：

| 组件                    | 兼容性                         |
| ----------------------- | ------------------------------ |
| i5-4460                 | ✅ LGA1150                     |
| DDR3                    | ✅                             |
| Tesla P100 PCIe         | ✅ PCIe x16                    |
| UEFI/PCI 资源分配       | ⚠️ 需要测试                    |
| P100 显示输出           | ❌ P100 是计算卡/无显示输出    |
| 供电                    | ⚠️ P100 需要约250W + 辅助供电 |
| 散热                    | ⚠️ 必须提供强劲气流            |

### 与 ASUS B85M-F 对比

针对你具体的 **P100 测试**，我的大致评价如下：

**ASUS B85M-F + i3-4170**

* ASUS BIOS 更成熟稳定
* 可支持 8–16 GB DDR3
* 价格便宜：基于列表约 ¥67
* **我倾向于用它排查 PCIe/BIOS 问题**

**SOYO SY-B85N + i5-4460 + 4GB**

* CPU 性能更高
* 自带内存
* B85 + Haswell 是恰好合适的世代
* 4GB 足够基本 P100 检测/测试，但最终建议用 8–16 GB
* **同样完全合理**

重要的是，**i5 与 i3 对 P100 是否能工作影响不大**。关键因素在于：

```text
PCIe x16 插槽
       ↓
BIOS 能识别 P100
       ↓
足够 PCIe MMIO 资源
       ↓
电源为 P100 供电
       ↓
良好气流
       ↓
nvidia-smi / CUDA 能检测到 P100
```

鉴于你正试图解决在 A68HM-E 上遇到的 **`PCI OUT OF RESOURCES CONDITION`** 问题，如果价格相近，我会优先选择 **ASUS B85M-F**，主要是因为 ASUS 的 BIOS/UEFI 是更稳妥的可排除变量。

如果 SOYO **价格明显更低，并且你可以在广州用你的 P100 进行测试**，那也值得一试。
