---
audio: false
generated: true
image: false
lang: zh
layout: post
title: P100错误时BIOS设置
translated: true
type: note
---

**问题：我在华硕 A68HM-E 上找不到 CSM。这对 P100 PCI 资源错误有影响吗？**

**答案：不——暂时先别找 CSM 了。** 我查阅了 A68HM-E 的文档，这是一款老旧的 FM2+ BIOS。华硕当前的支持页面只提供了这款主板 2014 年时期的 A68HM 系列手册。（[华硕全球站][1]）

更重要的是，**CSM 并不是我希望你针对这个问题去调整的设置**。

### 我希望你改查的内容

进入 BIOS，查看：

```text
高级（Advanced）
  ├─ 北桥（North Bridge）
  ├─ PCI 配置（PCI Configuration）
  ├─ PCI Express 配置（PCI Express Configuration）
  └─ 芯片组配置（Chipset Configuration）
```

查找以下名称的选项：

```text
Above 4G Decode
Above 4G Decoding
64-bit PCI
Memory Remap
MMIO
PCI MMIO
```

关键在于这个选项：

```text
Above 4G Decoding = 已启用（Enabled）
```

如果支持，此选项允许 64 位 PCI 设备映射到 4GB 地址空间之上。华硕官方将该功能明确描述为“将 64 位 PCI 设备解码到 4G 地址空间之上”。（[华硕下载中心][2]）

### 如果 A68HM-E 没有“Above 4G Decoding”选项

那么这将是一个更为重要的发现。

P100 正在向固件请求一个**非常大的 PCI BAR/MMIO 区域**，而老旧的 FM2+ BIOS 很可能根本无法为其分配。在这种情况下：

```text
Gen1 ❌
Gen2 ❌
Gen3 ❌
延迟 32 ❌
延迟 64 ❌
延迟 128 ❌
```

这些设置不太可能修复资源分配失败的问题。

### 现在请这样做

进入 BIOS，**拍摄整个“高级”（Advanced）选项卡的照片**。

同时拍摄：

```text
高级（Advanced）→ 北桥（North Bridge）
高级（Advanced）→ PCI*
高级（Advanced）→ 芯片组（Chipset*）
启动（Boot）
```

先不要更改其他任何设置。

我会查看 A68HM-E 的实际 BIOS 选项，然后告诉您是否存在让 P100 的 BAR 分配正常工作的办法，或者我们是否正在遭遇**主板固件限制**。

[华硕 A68HM-E 支持/手册页面](https://www.asus.com/us/supportonly/a68hm-e/helpdesk_manual/?utm_source=chatgpt.com) 

[1]: https://www.asus.com/us/supportonly/a68hm-e/helpdesk_manual/?utm_source=chatgpt.com "A68HM-E - 支持"
[2]: https://dlcdnet.asus.com/pub/ASUS/mb/LGA1151/MAXIMUS_VIII_HERO/E10343_MAXIMUS_VIII_HERO_UM_WEB.pdf?utm_source=chatgpt.com "Above 4G 解码 [已禁用]"