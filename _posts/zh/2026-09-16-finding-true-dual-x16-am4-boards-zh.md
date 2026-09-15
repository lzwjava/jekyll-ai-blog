---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 寻找真正的双路x16 AM4主板
translated: true
type: note
---

问题：如何找到一款具有**两个物理x16插槽且都是电气x16**的AM4主板？

答案：搜索规格**“2 × PCIe x16，x16/x16”**，或者更常见的写法**“2 × PCIe x16（x16/x16）”**。但有一个关键点：在消费级AM4平台上，**CPU通道数**决定了是否能实现真正的x16/x16。

### 关键点

对于AM4上的Ryzen桌面CPU，通常情况如下：

```text
CPU
 ├── PCIe x16  ──> GPU 1
 └── PCIe x4   ──> NVMe / 芯片组
```

要实现：

```text
GPU 1 = x16
GPU 2 = x16
```

主板需要**PCIe通道切换器 / PLX式切换器**，或者一个具有更多通道的平台/CPU。

大多数AM4主板采用的是：

```text
GPU 1 = x16
GPU 2 = x4
```

或者：

```text
GPU 1 = x8
GPU 2 = x8
```

如果你能接受**x8/x8**，那么后者就是你想要的。

### 搜索关键词

对于AM4：

```text
“AM4 PCIe x8 x8 主板”
“X570 PCIe x8 x8”
“X570S PCIe x8 x8”
“AM4 2 x PCIe x16 x8 x8”
```

请特别查看主板手册/规格书，寻找类似这样的描述：

```text
1 x PCI Express x16 插槽，运行速率为 x16
1 x PCI Express x16 插槽，运行速率为 x8
```

以及CPU支持：

```text
PCIe x16/x8
```

当两个GPU都安装时，CPU通道会被拆分：

```text
CPU
       16 通道
    ┌────────────┐
    │            │
  x8 GPU 1     x8 GPU 2
```

这比**x16 + x4**对于双GPU工作负载要好得多。

### 如果你确实需要x16 + x16

我**不建议以AM4为目标**。请考虑具有更多CPU PCIe通道的平台，例如：

* **Threadripper / sTRX4 / sTRX40**
* **Threadripper Pro**
* **EPYC**
* 现代工作站/服务器平台

这些CPU有足够的通道来实现：

```text
GPU 1：x16
GPU 2：x16
GPU 3：x16
...
```

而不会相互占用通道。

如果你告诉我**你打算安装哪两个GPU**，我可以告诉你对于你的工作负载，**x16+x4、x8+x8还是真正的x16+x16**是否真的重要。
