---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 影驰 GAMER II DDR4-2666 推荐
translated: true
type: note
---

问题：**Galaxy GAMER II DDR4-2666 8GB** 是否适合你的 B150M + i5-6500 GPU 测试工作站？

答案：**是的。只要价格合理，我会买。**

### 兼容性

你的配置：

```text
MSI B150M
    +
i5-6500
    +
Galaxy GAMER II DDR4-2666 8GB
```

**兼容。** 需要注意的是，DDR4-2666 会**自动降频到平台支持的内存速度**（i5-6500/B150 平台为 DDR4-2133）。

所以：

```text
内存条：       DDR4-2666
       ↓
B150 + i5-6500
       ↓
运行在 ~DDR4-2133
```

你无法获得 2666 MHz 的频率，但对于 GPU 测试来说完全没问题。

### 1×8GB 正是我会使用的配置

对于你的工作站：

| 配置       | 结论        |
| ---------- | ----------- |
| 1×4GB      | ❌ 我会避免  |
| 2×4GB      | 👍 可以      |
| **1×8GB**  | ⭐ **最佳**  |
| 2×8GB      | 没必要      |

GPU 诊断不需要双通道性能。你的工作流程更像是：

```text
启动 Linux
→ NVIDIA 驱动
→ nvidia-smi
→ GPU-Z / lspci
→ CUDA 测试
→ VRAM 测试
→ 压力测试
→ 基准测试
```

8 GB 系统内存绰绰有余。

### 有一点我需要检查

“双面颗粒”不是问题。**不要把双面内存与 ECC/registered 内存混淆。**

向卖家索取一张 CPU-Z 截图，显示以下内容：

```text
类型：       DDR4
容量：       8 GB
DRAM：       ...
模块：       UDIMM
```

如果是普通的台式机 **DDR4 UDIMM**，那就没问题。

**我现在的评价：**

> **B150M + i5-6500 ¥219 + 这根 8GB DDR4-2666 → 非常合理的廉价 GPU 测试平台。**

2666 的标称频率并没有浪费——它只是让你拥有一根可以后续在新款 DDR4 系统中继续使用的内存条。
