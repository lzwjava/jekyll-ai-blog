---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CSM在Z170A Gaming M5 BIOS中
translated: true
type: note
---

问题：Z170A Gaming M5 BIOS中的**CSM**是什么？

答案：**CSM = Compatibility Support Module**。它是一个UEFI固件组件，允许现代UEFI主板像旧的legacy BIOS一样运行。

可以这样理解：

```text
UEFI BIOS
   │
   ├── CSM Disabled
   │      └── 纯UEFI启动
   │
   └── CSM Enabled
          └── UEFI + legacy BIOS兼容
```

对于你的**M40 / PCI资源问题**，CSM很重要，因为它可以改变固件初始化PCIe设备和分配资源的方式。

### 在MSI Z170A Gaming M5上

你通常可以在以下位置找到它：

```text
Settings
  └── Advanced
       └── Windows OS Configuration
            └── Windows 10 WHQL Support
```

根据BIOS版本，CSM可能显示为：

```text
Boot
 └── Boot Mode Select
```

或间接通过**Windows 10 WHQL Support**。

典型组合如下：

```text
Windows 10 WHQL Support = Enabled
    → UEFI导向配置
    → CSM有效禁用

Windows 10 WHQL Support = Disabled
    → Legacy/UEFI兼容可用
    → CSM可用
```

### 对于你的M40实验

我建议**首先测试CSM disabled**：

```text
CSM             = Disabled
Above 4G Decode = Enabled
PCI_E1          = 你的M40
PCIe Speed      = Gen2
```

然后启动。

如果不起作用，测试相反的情况：

```text
CSM             = Enabled
Above 4G Decode = Enabled
PCI_E1          = M40
PCIe Speed      = Gen2
```

关键是**CSM本身并不是一个PCIe资源设置**。它改变了固件的启动/设备初始化环境。对于你的**“Insufficient PCI Resources”**错误，我认为更直接相关的设置是**Above 4G Decoding**。

如果你告诉我你的**确切M5 BIOS版本**，我可以映射出实际的MSI BIOS菜单路径，并准确告诉你该设置什么。
