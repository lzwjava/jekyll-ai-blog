---
audio: false
generated: true
image: false
lang: zh
layout: post
title: X99-QD4已确认可与ReBAR正常工作
translated: true
type: note
---

问题：**这个中文列表中的华南X99-QD4是否如`ReBarUEFI#11`所示，支持ReBarUEFI / Resizable BAR？**

回答：

**是的——这个确切的主板型号已被明确确认可用。**

在`xCuri0/ReBarUEFI#11`中，测试条目为：

| 主板                  | GPU      |       BAR | UEFIPatch |
| --------------------- | -------- | --------: | --------- |
| **华南X99-QD4**       | RTX 3060 | **16 GB** | **否**    |

所以这不是从“某款X99主板”推断出来的；**X99-QD4本身已通过16 GB BAR测试，且无需UEFIPatch**。([GitHub][1])

[ReBarUEFI #11 — 可用主板列表](https://github.com/xCuri0/ReBarUEFI/issues/11?utm_source=chatgpt.com)

### 这对那个列表意味着什么

卖家的主板：

> 华南 x99-QD4 / Q87 / DDR4 / 双M.2

几乎可以确定就是ReBarUEFI项目所指的**华南X99-QD4系列**。该项目明确提到了**“AliExpress X99教程”**，并说明这些X99主板不需要常规的UEFIPatch流程。([GitHub][2])

此外还有一个**2026年X99-QD4专用修改版BIOS项目**，明确列出了：

* 已注入ReBarDxe
* 已解除超频锁定
* 已解锁内存调校
* 已解锁VRM电流限制
* 已移除BCLK downspread

并报告X99-QD4的BIOS已测试/可用。([GitHub][3])

### 重要的区别

我想把这三件事分开来看：

```text
X99-QD4硬件
       │
       ├── ReBar能力 ─────── 是，有文档记录
       │
       ├── 原版BIOS ───────────── 取决于BIOS版本
       │
       └── 修改版BIOS ──────────── 可注入ReBarDxe + 超频
```

GitHub issue证明了**ReBar在X99-QD4上可用**，但这**并不**意味着每个原版BIOS版本都自动暴露了ReBAR。

对于你正在考虑的那块主板，我建议你特别向卖家询问：

```text
1. 确切的BIOS版本
2. 显示Above 4G Decoding的BIOS截图
3. 是否已注入ReBarDxe
4. 能否禁用CSM
5. 能否提供原始BIOS转储
```

ReBarUEFI的要求基本上是**Above 4G Decoding + 关闭CSM**，并将ReBar DXE模块插入固件中。([GitHub][2])

### 另一个有趣的点：“鸡血BIOS”

卖家的**2690 v3全核3.5 GHz**和**1650 v3 4.4/4.5 GHz**声称是另一个独立的BIOS修改/CPU微码问题，与ReBAR无关。

所以如果你的目标类似于：

```text
X99-QD4
+ E5-1650 v3 @ ~4.4 GHz
+ DDR4
+ RTX 3090 / 4090 / Arc
+ ReBAR
```

那么**X99-QD4是一个特别有趣的平台，因为我们有这块确切主板的直接ReBarUEFI证据。**

一个注意事项：原始#11测试是**RTX 3060 + 16 GB BAR**，所以它确立了固件/平台的能力，而不是说*每款*现代GPU都会有相同表现。该项目当前的wiki显示已有超过200块主板经过测试，并维护着可用主板列表。([GitHub][4])

如果你告诉我**你打算在这块X99-QD4上使用哪款GPU**（尤其是3090/4090/Arc A770/B580），我可以查看该GPU + X99组合的ReBarUEFI报告，并告诉你实际需要哪些BIOS修改。

[1]: https://github.com/xCuri0/ReBarUEFI/issues/11 "可用主板列表 · Issue #11 · xCuri0/ReBarUEFI · GitHub"
[2]: https://github.com/xCuri0/ReBarUEFI?utm_source=chatgpt.com "GitHub - xCuri0/ReBarUEFI：适用于（几乎）任何UEFI系统的Resizable BAR · GitHub"
[3]: https://github.com/avkila-tech/HUANANZHI-X99-QD4-2024/blob/main/README.md?utm_source=chatgpt.com "HUANANZHI-X99-QD4-2024/README.md at main · avkila-tech/HUANANZHI-X99-QD4-2024 · GitHub"
[4]: https://github.com/xCuri0/ReBarUEFI/wiki?utm_source=chatgpt.com "主页 · xCuri0/ReBarUEFI Wiki · GitHub"