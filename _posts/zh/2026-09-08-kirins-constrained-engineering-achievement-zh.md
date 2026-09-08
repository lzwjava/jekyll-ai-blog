---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 麒麟的受限工程成就
translated: true
type: note
---

问题：**如今华为麒麟芯片的水平如何？**

答案：**麒麟在技术上令人印象深刻，但在绝对能效比上尚未达到苹果/高通的领先水平。它真正的成就在于，华为在严苛的制造限制下重建了一套现代智能手机SoC（系统级芯片）堆栈。**

有趣的地方在于它们*如何*做到的。

### 1. 麒麟9000S是转折点

Mate 60 Pro中的**麒麟9000S**由中芯国际采用其**7nm级N+2工艺**制造，使用DUV（深紫外光刻）而非EUV（极紫外光刻）。TechInsights通过物理分析证实了这一点。（[TechInsights][1]）

这意义重大，因为通常你会期待：

```text
台积电/三星
    ↓
EUV
    ↓
5nm / 4nm / 3nm
    ↓
高晶体管密度 + 高效率
```

而华为/中芯国际的路径大致是：

```text
DUV
 ↓
多重图案化
 ↓
中芯国际 N+2 7nm
 ↓
麒麟9000S
```

这要困难得多且成本更高，因为DUV需要更多的图案化步骤。

所以**“麒麟是7nm”并不意味着“华为只是拥有一个普通的7nm工艺”。** 制造路径从根本上受到更多限制。

---

### 2. 但原始CPU性能并非最强部分

例如，麒麟9020的性能仍大致相当于较旧的高通骁龙旗舰系列，而不是当今最好的苹果/高通芯片。（[Notebookcheck][2]）

概念上：

```text
                    CPU性能
苹果A系列              ██████████
高通骁龙旗舰           █████████
联发科旗舰             █████████
麒麟9020               ██████
```

而且问题不仅在于CPU架构。

还在于：

```text
架构
     ×
工艺节点
     ×
频率
     ×
能效
     ×
内存子系统
     ×
GPU
```

华为在多个方面同时受到制约。

---

### 3. 更有趣的芯片是麒麟9030

对于关注硬件/大语言模型系统的人来说，这里的情况变得有趣得多。

最近的拆解工作发现，**麒麟9030采用中芯国际的N+3工艺**，从根本上仍源自7nm家族。TechInsights表示，N+3的密度已接近5nm级。（[TechInsights][3]）

更令人惊讶的是：

* 局部金属间距：**32.5 nm**
* 晶体管密度：**约113.4 MTr/mm²**
* 无EUV
* 大量使用多重图案化/设计-工艺协同优化

在某些测量中，其密度甚至可以超过台积电N6。（[Tom's Hardware][4]）

但有一个重要的区别：

> **晶体管密度 ≠ 芯片性能**

麒麟9030在CPU性能和能效方面仍大幅落后于当前的苹果/高通芯片。（[Tom's Hardware][4]）

这正是作为工程师应该关注的地方：**仅凭节点名称所能告诉你的信息少得惊人。**

---

### 4. 华为真正的优势在于系统级工程

这可能是麒麟最有趣的地方。

华为并未掌控整个半导体堆栈：

```text
ASML EUV       ❌
台积电           ❌
NVIDIA GPU     ❌
ARM最新IP      受限
        ↓
华为/海思
        ↓
架构 + SoC + 固件
        ↓
中芯国际
        ↓
DUV多重图案化
```

因此，他们通过以下方式进行补偿：

* 自研CPU核心
* 自研GPU架构
* 激进的物理设计
* 更大的芯片面积
* 封装技术
* 内存优化
* 软件优化
* 针对特定工作负载的工程优化

例如，麒麟9020进一步转向华为自研的CPU核心，而非简单使用标准Cortex核心。（[Notebookcheck][2]）

这就是为什么我不会这样评估麒麟：

> “它像骁龙一样快吗？”

我会这样评估：

> **“华为能从受限的制造技术中提取出多少性能？”**

这是一个更有趣的问题。

---

### 5. 如今华为正以不同方式攻克缩放问题

华为在2026年宣布了其**τ（陶）缩放定律**，提出了诸如**LogicFolding**等技术，旨在不单纯依赖晶体管缩小的情况下提升系统效率。路透社报道称，华为正通过这种方法瞄准远超当前的有效能力。（[Reuters][5]）

这在概念上很重要：

```text
传统缩放

更小的晶体管
       ↓
更多晶体管
       ↓
更高性能
       ↓
更低能耗


华为的替代方向

相近工艺
       ↓
更好的物理组织
       ↓
更短的数据移动
       ↓
更好的利用率
       ↓
更高的系统效率
```

对于AI硬件来说，**数据移动通常比算术运算本身更重要**，因此这个方向绝非疯狂。

---

## 我的评估

我大致会这样评价麒麟：

| 领域                           | 麒麟  |
| ------------------------------ | ------ |
| CPU峰值性能                    | 🟡     |
| CPU能效                        | 🟡     |
| GPU                            | 🟡     |
| 调制解调器/连接集成            | 🟢     |
| SoC集成                        | 🟢     |
| 半导体工程能力                 | 🟢🟢   |
| 制造效率                       | 🔴     |
| 绝对领先的工艺节点             | 🔴     |
| 在制裁下生存的能力             | 🟢🟢🟢 |
| 战略重要性                     | 🟢🟢🟢 |

关键点在于：

**麒麟目前并非全球最快的移动SoC。**

但**麒麟是全球最有趣的半导体工程项目之一**，因为华为证明了可以用架构 + 物理设计 + 封装 + 软件 + 巨大的工程投入来弥补制造劣势。

这与你在**华为昇腾 vs NVIDIA**中看到的情况非常相似：有趣的问题未必是“华为能否在FLOPS上击败NVIDIA的H100/B200？”，而是 **“尽管无法获得相同的半导体供应链，华为能构建出多少系统级能力？”**

我还可以进一步拆解 **麒麟 → 昇腾 → 中芯国际 → EUV/DUV → 华为策略为何与大语言模型GPU相关**，这直接联系到你一直在做的GPU/大语言模型工作。

[1]: https://www.techinsights.com/blog/hisilicon-kirin-9000s-smic-7nm-n2-process-flow-full-analysis?utm_source=chatgpt.com "HiSilicon Kirin 9000s (SMIC 7nm, N+2) Process Flow (Full) Analysis | TechInsights"
[2]: https://www.notebookcheck.net/HiSilicon-Kirin-9020-Processor-Benchmarks-and-Specs.953640.0.html?utm_source=chatgpt.com "HiSilicon Kirin 9020 Processor - Benchmarks and Specs - Notebookcheck Tech"
[3]: https://www.techinsights.com/blog/smic-n3-confirmed-kirin-9030-analysis-reveals-how-close-smic-5nm?utm_source=chatgpt.com "Kirin 9030 Analysis Reveals How Close SMIC Is to 5nm"
[4]: https://www.tomshardware.com/tech-industry/semiconductors/smics-third-gen-7nm-node-shows-smaller-metal-pitch-than-intel-18a-higher-transistor-density-than-tsmc-n6-without-euv-analysis-of-n-3-shows-significant-advancement-for-chinese-semi-manufacturing?utm_source=chatgpt.com "SMIC's third-gen 7nm node shows smaller metal pitch than Intel 18A, higher transistor density than TSMC N6 without EUV - analysis of N+3 shows significant advancement for Chinese semi manufacturing"
[5]: https://www.reuters.com/world/asia-pacific/huawei-proposes-new-path-chip-development-amid-us-sanctions-2026-05-25/?utm_source=chatgpt.com "China's Huawei reveals chip design breakthrough amid US sanctions"