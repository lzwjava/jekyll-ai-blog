---
audio: false
generated: true
image: false
lang: zh
layout: post
title: EMC编号标识Mac硬件版本
translated: true
type: note
---

**问题：** 在 Apple Mac 型号中，“EMC” 是什么意思？

**答案：**

**EMC = Electro-Magnetic Compatibility** — 但在 Apple 的语境中，它被用作 **内部型号标识编号**，而非电磁特性的描述。

Apple 为其提交 FCC/监管认证的每个产品分配一个 EMC 编号。这本质上是 Apple 的内部修订代码，印在机器底部并用于监管备案。

**实际意义：**

相同的型号名称（例如 "MacBook Pro 13-inch A1708"）可能有 **多个硬件修订版本**，对应不同的 EMC 编号：

| EMC 编号 | 年份 | CPU 代际 |
| --------- | ------ | -------- |
| EMC 2978 | 2016 年末 | Skylake (i5-6360U) |
| EMC 3164 | 2017 年中 | Kaby Lake (i5-7360U) |

两者都是 A1708，但不同的 EMC 编号意味着不同的内部组件。在购买零件（电池、屏幕、键盘）时，EMC 编号可确保您获得 **完全正确的零件**，适用于您的特定修订版本 —— 即使外部型号编号相同也是如此。

**在哪里找到它：**

- 印在 Mac 底部外壳上
- Apple 菜单 → 关于本机 → 系统报告 → 型号标识符区域
- 在原始包装盒上

**TL;DR：** EMC 是 Apple 的监管备案修订编号，被重新用作硬件修订标签。在购买替换零件时，请匹配 EMC 编号以确保兼容性。
