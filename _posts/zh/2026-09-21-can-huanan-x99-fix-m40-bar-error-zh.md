---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 华南X99能否修复M40 BAR错误
translated: true
type: note
---

**问题：** 华南X99-4 MT Plus + Xeon E5-2673v3的组合能帮助解决M40的PCI/BAR错误吗？

**回答：**

**简短回答：可能可以——比旧联想主板更好——但不能保证。**

详细说明如下：

---

### 为什么这是一个改进

| | 旧联想（i5-4460） | 华南X99-4 MT Plus + 2673v3 |
| --- | --- | --- |
| **平台** | 消费级Haswell，2016年BIOS | LGA2011-3 X99平台 |
| **PCIe通道** | 有限 | 40通道Xeon（E5-2673v3） |
| **BIOS年龄** | 很旧，不支持UEFI Tesla | 国产X99主板通常有修改版/更新版BIOS |
| **Above 4G Decoding** | 几乎肯定没有 | 可能有或可通过修改实现 |

E5-2673v3是一款**40通道Xeon**——拥有完整的PCIe 3.0 x16带宽以及CPU端足够的地质空间来支持大型BAR分配，这正是M40所需要的。

---

### 真正的风险：华南X99-4 MT芯片组

X99-4 MT Plus通常使用**消费级芯片组（H81或B85）**伪装成X99风格主板，**并非真正的Intel C612/X99服务器芯片组**。这在便宜的国产X99主板中很常见。确实有报告称M40 24GB在启用Above 4G解码后仍在某些主板上因BAR1无法分配而失败。

需要检查的关键项：

- **你的BIOS是否有“Above 4G Decoding”？** 进入BIOS，在高级/PCIe设置下查找。这是最重要的开关。
- **CSM（兼容支持模块）是否已禁用？** Tesla显卡在纯UEFI模式下工作更好。

---

### 如果缺少Above 4G Decoding

一些修改版的国产X99 BIOS包含Above 4G Decoding和Resizable BAR支持——像Win-Raid这样的社区专门为国产X99主板提供BIOS修改版本。ReBarUEFI项目还提供了一个UEFI DXE驱动，可以在不支持官方Resizable BAR的系统上启用该功能。如果没有4G Decoding，你将被限制在1GB的BAR。

---

### 总结

```
华南X99-4 MT Plus + 2673v3 + M40
        ↓
步骤1：检查BIOS中的“Above 4G Decoding”
        ↓
找到 → 启用它，禁用CSM → 可能可行
        ↓
未找到 → 刷入修改版BIOS或使用ReBarUEFI
```

这是一个**比旧联想主板好得多的候选方案**，但结果取决于那个BIOS里实际有什么。

**参考资料：**

- [ReBarUEFI - 在不支持的平台上启用Resizable BAR](https://github.com/xCuri0/ReBarUEFI)
- [Win-Raid：国产X99主板的超频BIOS修改](https://winraid.level1techs.com/t/guide-overclock-bios-mods-for-chinese-x99-mbs/104683)
- [Tesla M40 + Above 4G Decoding讨论（Tom's Hardware）](https://forums.tomshardware.com/threads/tesla-m40-and-dell-oem-board.3600010/)
