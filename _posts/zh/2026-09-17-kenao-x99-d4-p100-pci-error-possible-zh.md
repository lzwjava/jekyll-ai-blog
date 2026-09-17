---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Kenao X99-D4 P100 PCI 错误可能
translated: true
type: note
---

问题：**Kenao X99-D4 + NVIDIA Tesla P100** 组合是否会遇到 **“PCI OUT OF RESOURCES CONDITION”** 错误？

答案：**可能会，但单张 P100 通常没问题。** 如果使用多张 GPU 或多个 PCIe 设备，风险会显著增加。

以典型配置为例：

```text
Kenao X99-D4
Xeon E5 v3/v4
DDR4
1× Tesla P100 PCIe 16GB
1× NVMe
```

仅添加一张 P100，我**预计不会触发 PCI 资源耗尽**。

关键 BIOS 设置是：

```text
Above 4G Decoding = Enabled
```

特别是如果你最终想要：

```text
2× P100
4× P100
+ NVMe
+ 10/25/40GbE NIC
```

### 为什么 P100 可能触发该问题

P100 需要大量的 PCIe BAR/MMIO 空间。在较老的 X99 固件上，问题不一定在于 CPU 缺少 PCIe 通道，而在于 **BIOS 可能无法分配足够的 PCI 地址空间**。

可以把这两个限制分开理解：

```text
PCIe 通道                         PCI 资源地址空间
───────────                        ───────────────────────────
Xeon 提供大量通道                  BIOS 必须映射设备 BAR
        │                                    │
        ▼                                    ▼
设备能否电气连接？                 固件能否分配地址？
```

因此，即便 E5 Xeon 可能有 **40 条 PCIe 3.0 通道**，仍然可能出现资源分配错误。

### 针对你提出的廉价 P100 机器方案

我会将 BIOS 大致配置为：

```text
Above 4G Decoding     Enabled
CSM                   Disabled*
UEFI Boot             Enabled
Resizable BAR         Disabled
```

`CSM` 取决于具体的 Kenao BIOS 与 GPU 组合，如果当前系统能正常启动，不要盲目修改。

然后验证：

```bash
lspci -nn
nvidia-smi
```

确保 P100 在两个命令中都能显示。

**这块 Kenao 主板更大的问题不在于 P100 本身，而在于廉价 X99 主板的品质/固件一致性。** 如果你考虑购买整批 200 块主板，建议先购买并测试**一块主板与你的具体 P100 搭配**，再批量升级。

如果你告诉我**你的是哪款 P100（PCIe 12GB/16GB 还是 SXM2）**以及**具体的 X99-D4 链接/照片**，我可以检查插槽布局并告诉你 1/2/4 张 P100 是否可行。
