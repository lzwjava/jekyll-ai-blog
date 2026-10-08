---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 即使有硬盘，BOOT LED仍为红色
translated: true
type: note
---

问题：**即使你连接了硬盘，BOOT_DEVICE LED 仍然显示红色——这是为什么？**

回答：是的——在第二张照片中我可以看到**硬盘已通过 SATA 电源线和 SATA 数据线连接**，但关键问题是主板能否真正检测到它。

这个红色 LED 在你的 Z170-A 上明确标记为 **`BOOT_DEVICE_LED`**。华硕表示，这个 LED 亮起意味着主板无法找到可用的启动设备。([@ROG][1])

### 请按以下步骤精确测试

**1. 完全断开硬盘。**

仅保留：

```text
Z170-A
├── CPU + 散热器
├── 1 根内存条
├── 电源 24 针主供电
├── 电源 8 针 CPU 供电
└── 显示器
```

不接硬盘、U 盘或其他 PCIe 卡。

然后开机并反复按：

```text
DEL DEL DEL DEL ...
```

正常情况下，即使没有任何存储设备，你也应该能进入 **UEFI/BIOS**。

此时 BOOT LED 可能仍亮着（因为没有启动设备），但**你应该能进入 BIOS**。

---

### 如果能进入 BIOS

那么主板很可能没有问题。

连接硬盘：

```text
硬盘
 ├── SATA 电源线
 └── SATA 数据线 → SATA6G_1
```

然后在 BIOS 中检查：

```text
高级模式
    ↓
高级
    ↓
SATA 配置
```

查看硬盘是否出现。

如果**没有出现**，怀疑：

1. SATA 数据线故障
2. SATA 接口故障
3. 硬盘故障
4. SATA 电源问题
5. BIOS SATA 配置问题

尝试：

```text
SATA6G_1 → SATA6G_2
```

并换一根 SATA 数据线。

华硕特别建议，当 BOOT LED 一直亮着时，重新连接 SATA 数据线和存储设备。([@ROG][1])

### 但还有一项更重要的测试

你的照片似乎显示**主板上没有连接显示器线缆**，而且我看不到独立显卡。

如果你的 CPU 是类似：

```text
i5-6500
i5-6600
i7-6700
i7-6700K
```

这类 CPU 带有 Intel 核显，因此请将显示器连接到**主板的 HDMI/DVI/DisplayPort 输出接口**。

如果你的 CPU 是 **F 系列** 或不带核显，则需要安装独立显卡。

---

### 关键区别

如果出现以下情况：

```text
BOOT_DEVICE_LED = 红色
+
BIOS 能显示
```

→ 这是**存储/启动问题**，而非主板 POST 失败。

如果出现以下情况：

```text
BOOT_DEVICE_LED = 红色
+
无 BIOS / 无显示
```

→ 需要进一步排查。此时 BOOT LED 可能是 POST 流程中*最后*一个亮起的 LED，而非实际根本原因。

Z170-A 的 POST LED 设计顺序为 CPU → 内存 → 显卡 → 启动设备检查，问题对应的 LED 会保持常亮。([motherboarddb.com][2])

**请告诉我这台 Z170-A 上安装的精确 CPU 型号**（例如 `i7-6700K`），以及你的显示器目前是否**有任何显示**。这样我就能大幅缩小排查范围。

[1]: https://rog.asus.com/us/support/faq/1042678/?utm_source=chatgpt.com "[主板] 华硕主板通过 Q-LED 指示灯进行故障排除 | 官方支持 | ROG 美国"
[2]: https://motherboarddb.com/media/manuals/Asus/Z170-A/Z170-A.pdf?utm_source=chatgpt.com "1.8 板载 LED"