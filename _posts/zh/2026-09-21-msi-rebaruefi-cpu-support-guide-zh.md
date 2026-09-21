---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI ReBarUEFI CPU支持指南
translated: true
type: note
---

**问题：** 那些支持 MSI ReBarUEFI 的主板支持哪些 CPU？

**回答：** 关键区别在于 **Z170 = 第六代 Skylake**，而 **Z270 = 第六/七代 Skylake/Kaby Lake**。

### 列表中的 MSI 主板

| 主板                | 插槽    | 官方支持的 CPU 代次       | 推荐的好 CPU                      |
| ------------------- | ------- | ------------------------- | --------------------------------- |
| **Z170-A PRO**      | LGA1151 | 第六代                    | i7-6700K、i7-6700、i5-6600K       |
| **Z170A Gaming M5** | LGA1151 | 第六代                    | i7-6700K、i7-6700、i5-6600K       |
| **Z270-A PRO**      | LGA1151 | 第六代 + 第七代           | **i7-7700K**、i7-6700K、i5-7600K  |
| **Z270 Gaming M5**  | LGA1151 | 第六代 + 第七代           | **i7-7700K**、i7-6700K、i5-7600K  |

MSI 明确列出 Z170-A PRO 支持第六代 Core i3/i5/i7、Pentium 和 Celeron CPU。([MSI][1])

**Z270 主板更有意思**：MSI 官方列出其支持第六代和第七代 Core i3/i5/i7 CPU。

因此，如果你购买旧平台**专门为了 Intel Arc GPU + ReBarUEFI**，我会寻找：

```text
MSI Z270-A PRO
       +
Core i7-7700K
       +
Intel Arc A770 / A750 / B 系列
       +
ReBarUEFI
```

**i7-7700K + Z270** 是该平台最高端的主流 CPU 组合。

一个重要的注意事项：**不要假设所有 LGA1151 CPU 都能在所有 LGA1151 主板上工作**。Z170/Z270 使用相同的物理插槽，但它们官方支持的 CPU 代次不同。

如果你正在考虑购买**二手 MSI 主板 + 廉价 CPU 专门用于运行 Arc B580/B570**，请告诉我你的目标 Arc GPU 和预算——我可以帮你缩小到最便宜的可行 CPU/主板组合。

[1]: https://us.msi.com/Motherboard/Z170-A-PRO/Specification?utm_source=chatgpt.com "Specification Z170-A PRO | MSI USA"
