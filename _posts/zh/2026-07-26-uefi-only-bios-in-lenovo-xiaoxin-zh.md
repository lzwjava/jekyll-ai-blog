---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 联想小新UEFI专用BIOS
translated: true
type: note
---

问题：在联想小新BIOS（ID字符串LACN36WW）中找不到UEFI/Legacy切换选项——它在哪里，或者它是否存在？

答案：我无法找到关于`LACN36WW`的具体文档，但根据命名模式（`XXCN36WW`），这匹配最近用于2022+小新/IdeaPad/游戏型号的联想消费级BIOS构建（Insyde H2O固件）。**重要：这些较新的小新型号大多根本没有Legacy/CSM切换选项——它们出厂就是纯UEFI。**所以如果你找不到它，很可能是因为它确实不存在，而不是因为你找错了地方。

为了确认，首先进入BIOS：

1. 完全关机。
2. 用回形针按下**Novo按钮**（侧面靠近电源端口的小针孔按钮），或者开机后立即按`Fn+F2`或`F2`。
3. 你将进入Insyde H2O设置——顶部有标签页：**Main / Configuration / Security / Boot / Exit**。
4. 检查**Boot**选项卡——查找“Boot Mode”、“UEFI/Legacy”或“CSM Support”。如果只显示**“Boot Mode: UEFI”**且没有下拉菜单或其他选项，那就确认是纯UEFI固件——这里没有什么可更改的。
5. 检查**Security**选项卡中的**Secure Boot**——这对这些型号更可能相关。如果它开启，尝试将其**关闭**（Windows 11安装无论哪种方式都可以，但有时带有Secure Boot enabled的GPT磁盘和缺失的ESP会出错）。

**鉴于此，我之前关于“CSM/Legacy不匹配”的理论可能对你的硬件是错误的**——既然它无论如何都是纯UEFI，Disk 0上缺失的ESP实际上是由其他原因造成的：可能你运行了`convert gpt`，但Windows安装程序仍然以MBR风格创建分区，因为之前的`clean`导致**分区样式标志过期**——或者安装程序因之前的失败尝试而处于异常状态。

**最简单的修复方式，跳过BIOS寻找：** 重新进行完整的diskpart clean操作：

```
diskpart
list disk
select disk 0
clean
convert gpt
exit
```

然后刷新→选择未分配空间→下一步，并仔细检查这次在设置自动创建分区后（在再次点击下一步之前）是否出现**EFI System Partition**。如果出现，无论BIOS引导模式如何，你都没问题。

参考：

- [Lenovo BIOS builds reference - Wim's BIOS](https://www.wimsbios.com/biosupdates/lenovo.jsp)
- [Insyde H2O UEFI setup navigation](https://neosmart.net/wiki/enable-uefi-boot/)
