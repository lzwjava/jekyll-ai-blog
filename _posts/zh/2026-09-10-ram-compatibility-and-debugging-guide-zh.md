---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RAM兼容性及调试指南
translated: true
type: note
---

问题：**你正在使用一条 Galaxy GAMER II DDR4-2666 8GB C19 内存条，搭配 i5-6500 + MSI B150M PRO 主板。**

回答：**这条内存应该是兼容的。** DDR4-2666 本身不是问题。

i5-6500 官方支持 **DDR4-2133**，因此在普通的 B150 平台上，你的 DDR4-2666 内存条会以较低的速度运行（通常是 **2133 MT/s**），而不会导致无法开机自检。

所以如果调试 LED 灯一直循环闪烁：

```text
CPU → DRAM → CPU → DRAM ...
```

我建议按以下顺序测试：

```text
1. 单独插一条 GAMER II 8GB 内存条
2. 尝试每个内存插槽
3. 清除 CMOS
4. 重新安装 CPU
5. 检查 LGA1151 插座针脚
6. 尝试另一条已知正常的内存条
```

**暂时不用担心 C19 时序的问题。** 这不太可能是导致完全无法开机的根本原因。

如果你能上传一张 **内存安装后 + 主板调试 LED 灯** 的照片，我可以检查实际安装情况，并告诉你下一步该检查什么。