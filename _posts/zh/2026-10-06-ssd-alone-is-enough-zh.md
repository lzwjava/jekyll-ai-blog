---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSD单独就够了
translated: true
type: note
---

问题：如果我只将SSD连接到Motherboard，还需要Hard Disk Drive (HDD)吗？

答案：**不。仅SSD就足够了。** 你**不**需要HDD。

对于普通PC：

```text
Motherboard
   │
   ├── SSD ──→ OS + applications + files
   │
   └── HDD ──→ optional extra storage
```

例如：

* **500 GB / 1 TB SSD** → 完全足够安装Windows/Linux并运行计算机。
* **SSD + HDD** → 如果你想要**廉价、大容量存储**（例如4–12 TB），则有用。
* **NVMe SSD** → 直接插入Motherboard的M.2插槽。
* **SATA SSD/HDD** → 通过SATA数据和电源线连接。

因此，如果你正在构建你的GPU/LLM测试机器，你可以简单地：

```text
CPU + motherboard + RAM + GPU + PSU + SSD
```

这样就可以了。HDD是可选的。