---
audio: false
generated: true
image: false
lang: zh
layout: post
title: B760M主板并不完全相同
translated: true
type: note
---

问题：**技嘉 B760M 和微星 B760M 是相同的东西吗？谁制造了 B760M？**

答案：

不是。**技嘉 B760M 和微星 B760M 不是同一款主板。** 它们是不同制造商基于**相同英特尔 B760 芯片组**设计的板子。

可以这样理解：

```text
英特尔
  │
  └── B760 芯片组
       │
       ├── 微星 → MAG B760M MORTAR WIFI
       ├── 技嘉 → B760M DS3H / AORUS ELITE
       ├── 华硕 → TUF GAMING B760M / PRIME B760M
       ├── 华擎 → B760M Pro RS
       └── 映泰 → B760M series
```

### “B760M” 是什么意思？

拆解名称：

```text
B760
│
└── 英特尔芯片组

M
│
└── Micro-ATX 板型
```

**B760 由英特尔设计并制造，作为芯片组/平台。**

主板制造商随后基于该芯片组设计实际的主板。

因此：

> **B760M 并非工厂或品牌。**

它本质上是：

**英特尔 B760 芯片组 + mATX 主板设计。**

### 示例

以下都是不同的主板：

| 主板                   | 制造商     | 芯片组       | 尺寸 |
| ---------------------- | ---------- | ------------ | ---- |
| MAG B760M MORTAR WIFI  | 微星       | Intel B760   | mATX |
| B760M DS3H             | 技嘉       | Intel B760   | mATX |
| TUF GAMING B760M-PLUS  | 华硕       | Intel B760   | mATX |
| B760M Pro RS           | 华擎       | Intel B760   | mATX |

它们都能支持相同的通用 CPU 系列，例如：

```text
LGA1700
    ↓
第12代英特尔酷睿
第13代英特尔酷睿
第14代英特尔酷睿
```

但 **VRM、PCIe 布局、M.2 数量、BIOS、网卡芯片、Wi-Fi、音频、USB、散热以及做工用料可能有很大差异。**

### 针对你的 GPU 测试需求

这个区别很重要。

如果有人说：

> “我有一块 B760M。”

这**几乎无法告诉你实际主板的具体信息**。

你需要完整的型号：

```text
微星 MAG B760M MORTAR WIFI
技嘉 B760M DS3H
技嘉 B760M AORUS ELITE
华硕 TUF GAMING B760M-PLUS
……
```

然后我们才能检查它的 **PCIe 拓扑结构**。

例如，两块“B760M”主板可能拥有：

```text
主板 A：
GPU #1 → PCIe x16
GPU #2 → PCIe x4

主板 B：
GPU #1 → PCIe x16
GPU #2 → PCIe x1
```

对于你的**双 GPU 维修/测试平台**，这个差异远比“B760M”这个词本身更重要。