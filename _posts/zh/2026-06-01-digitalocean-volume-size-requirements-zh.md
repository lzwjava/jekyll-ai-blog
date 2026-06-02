---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DigitalOcean 卷大小要求
translated: true
type: note
---

AMD Dev Cloud 的卷管理界面很可能要求特定的格式或单位。我来确认一下。关键发现：AMD Dev Cloud 实际上底层基于 DigitalOcean——它会重定向到 DigitalOcean 并部署 GPU Droplet。因此卷管理界面就是 DigitalOcean 的。

**问题所在：** DigitalOcean 卷的**最小大小为 1 GiB，且该字段接受以 GiB 为单位的整数**，但同时还存在**最小 1 GiB 和最大 16,384 GiB 的限制**。输入 `200` 时出现“大小无效”最常见的原因是：

1. **你输错了字段**——它可能期望输入 `200 GiB`，但界面上有一个单位下拉菜单（GiB 与 TiB），你可能错误地将单位设置为 TiB，导致系统将 200 解释为 TiB（200 TiB 超过了 16 TB 的最大值）
2. **该字段要求最小值**——DO 卷的最小值是 **1 GiB**，但某些 GPU Droplet 的卷配置有更高的最小值（有时为 10 GiB）
3. **粘贴时混入了尾部空格或非数字字符**

**可以尝试的快速修复方法：**

- 输入 `100` 而不是 `200`——排除上限的限制
- 检查字段旁边是否有单位选择器——确保设置为 **GiB** 而不是 **TiB**
- 尝试输入 `50` 以确认字段是否正常工作
- 完全清空字段并重新输入（不要粘贴）

由于底层是 DO，有效范围是 **1–16384 GiB**，因此理论上 `200` GiB 应该是可以的。很可能是界面下拉菜单中的单位不匹配问题。
