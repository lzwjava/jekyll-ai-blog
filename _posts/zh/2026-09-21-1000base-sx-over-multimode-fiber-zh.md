---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 1000BASE-SX多模光纤
translated: true
type: note
---

问题：**1000BASE-SX** 在多模光纤上使用什么？

答案：

**1000BASE-SX = 通过多模光纤（MMF）运行的千兆以太网，使用 850 nm VCSEL 激光器。**

典型配置：

```text
1000BASE-SX
     │
     ├── 波长：850 nm
     ├── 光源：VCSEL 激光器
     ├── 光纤：多模光纤（MMF）
     ├── 速率：1 Gbit/s
     └── 双工：2 芯光纤
             ├── TX
             └── RX
```

常见光纤类型：

| 光纤                | 1000BASE-SX 典型最大距离 |
| ------------------- | -----------------------: |
| OM1（62.5/125 µm）  |                   ~275 m |
| OM2（50/125 µm）    |                   ~550 m |
| OM3（50/125 µm）    |                   ~550 m |
| OM4（50/125 µm）    |                   ~550 m |
| OM5                  |                   ~550 m |

重要区别在于：

* **1000BASE-SX** → **850 nm + 多模**
* **1000BASE-LX** → **1310 nm**，主要针对单模，但通过适当的模式调节配置也可在多模光纤上运行
* **1000BASE-T** → 铜缆双绞线

对于 SFP 模块，你通常会看到类似这样的规格：

```text
1000BASE-SX SFP
LC 双工
850 nm
MMF
```

所以，如果你正在查看现有的**多模 LC 光纤链路**，我也可以帮你整理 **OM1/OM2/OM3/OM4 → 可以使用的 1G/10G SFP 及其对应传输距离**。