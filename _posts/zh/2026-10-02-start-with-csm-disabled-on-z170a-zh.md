---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Z170A上禁用CSM启动
translated: true
type: note
---

问题：对于你的 **Z170A Gaming M5 + M40**，应该启用还是禁用 CSM？

回答：**先禁用 CSM。**

针对你的 PCI 资源故障排查，请使用以下设置：

```text
CSM / Legacy        = 禁用
Above 4G Decoding   = 启用
PCI_E1              = M40
PCIe Link Speed     = Gen2
```

原因：**Above 4G Decoding + 纯 UEFI** 能为固件提供最干净的环境，用于分配大型 PCIe MMIO 区域。

如果仍然出现以下错误：

```text
PCI 资源不足
检测到 PCI 资源不足
```

那么，请进行第二次测试，**启用 CSM**。如果结果发生变化，说明 M40 的 Legacy/UEFI 初始化过程涉及其中。

因此，我建议按以下顺序测试：

```text
1. CSM 关闭 + Above 4G 开启 + Gen2
2. CSM 开启 + Above 4G 开启 + Gen2
3. CSM 关闭 + Above 4G 开启 + Gen1
```

**不要同时更改多个变量**，仅限于这些受控组合；否则很难确定是什么解决了资源错误。
