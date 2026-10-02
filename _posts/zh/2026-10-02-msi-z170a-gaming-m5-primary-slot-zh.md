---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI Z170A Gaming M5 主插槽
translated: true
type: note
---

问题：MSI Z170A Gaming M5上的三个PCIe x16长度插槽中，哪个是主GPU插槽？

答案：在**MSI Z170A Gaming M5**上，主GPU插槽是**PCI_E1**——**最靠近CPU插槽的顶部PCIe x16长度插槽**。

典型布局：

```text
CPU
┌─────────────────────────┐
│                         │
└─────────────────────────┘

PCI_E1  █████████████████  ← 主GPU，连接CPU的x16
PCI_E2  █████████████████  ← 次要
PCI_E3  █████████████████  ← 底部插槽
```

针对你的**M40/P100故障排查**，请先将显卡插入**PCI_E1**。

另外，不要仅凭物理长度判断。该主板有三个x16长度插槽，但它们的电气通道配置不同。在Z170上，顶部插槽才是单GPU所需的插槽。

如果即使在PCI_E1中插入M40后仍出现**“检测到PCI资源不足”**的错误，下一步我建议检查**PCI_E1/E2/E3的通道/资源配置 + Above 4G + CSM**。
