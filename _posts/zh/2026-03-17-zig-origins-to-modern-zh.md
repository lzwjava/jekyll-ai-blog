---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Zig：从起源到现代时代
translated: true
type: note
---

**Zig 编程语言的历史**

Zig 是一个现代的、通用的、静态类型、编译型系统编程语言，旨在作为 **C** 的更安全、更易维护、更明确的替代品，同时保留低级控制、性能和简单性。

### 起源 (2015–2016)
- Andrew Kelley 在 **2015年末** 开始将 Zig 作为个人项目开发。
- 他暂停了 Genesis Digital Audio Workstation 的开发，转而创建一个新语言，以解决他认为现有系统语言（尤其是 C 及其预处理器、未定义行为、隐藏控制流以及糟糕的安全工具）中的根本缺陷。
- 在 **2016年2月8日**，Andrew 通过一篇题为 **"Introduction to the Zig Programming Language"** 的博客文章正式公布了 Zig——这一天被广泛认可为该语言的“首次亮相”。
- 早期原型已展示核心理念：无隐藏控制流、comptime（编译时执行）、优秀的 C 互操作性，以及对简单性和鲁棒性的强烈关注。

### 早期开发 (2016–2019)
- 由于其 **"better C"** 理念，Zig 迅速吸引了系统编程和游戏开发社区的关注。
- 关键早期里程碑包括：
  - 实现 **comptime**（任意代码在编译时的执行）——这一特性最初被一些语言专家视为不切实际，但后来成为 Zig 最强大且深受喜爱的功能之一。
  - 开箱即用的优秀跨编译支持。
  - 完全放弃 C 预处理器，并用更干净、更可预测的机制取代之。
- 在 **2019年5月**，Andrew 在一次会议上发表了影响深远的演讲 **"The Road to Zig 1.0"**，解释了动机、设计权衡以及长期愿景。该演讲显著提升了 Zig 的知名度。

### 增长与社区阶段 (2020–2023)
- Zig 在嵌入式系统、游戏引擎、工具以及需要强大 C 互操作的项目中稳步获得采用。
- 流行的学习资源出现：
  - **Ziglings**（通过修复损坏代码来学习 Zig 的练习）——于 2020年末启动。
  - 各种“Zig by example”网站和书籍。
- 该语言仍处于 1.0 前的版本，频繁进行破坏性变更——这是有意为之，以允许在无遗留负担的情况下进行激进改进。
- **Zig Software Foundation (ZSF)** 作为一个非营利组织成立，以提供可持续资金和治理（Andrew 和核心贡献者最终可获得资金）。

### 自托管编译器与成熟期 (2023–2025)
- 最大的技术成就之一是 **self-hosted compiler**：
  - Zig 0.11.0 (2023) 移除了旧的 C++/LLVM 引导编译器，转而采用 Zig 编写的前端 + 自托管后端。
  - 后续版本使用 **WebAssembly** 引导，实现更干净、更便携的构建。
- 重点转向：
  - 增量编译（最长期且最雄心勃勃的目标之一）。
  - 编译器性能改进。
  - 错误修复（1.0 前针对超过 1,200 个问题）。
  - 对第三方项目的更好支持。

### 最近状态 (2025–2026)
- 截至 2026年中，Zig 仍处于 **0.x** 版本（最近约为 0.15.x / 0.16 开发周期）。
- 定期路线图更新（例如 **Zig Roadmap 2024**、**Zig Roadmap 2026**）显示向 **1.0** 的持续进展，强调质量、错误消除和编译器速度，而不是匆忙设定日期。
- 在 **2025年末**，项目将其主要仓库从 GitHub 迁移至 **Codeberg**（一个非营利、开源友好的代码托管平台）。
- Zig 在多个细分领域达到了临界质量：嵌入式、音频、游戏开发工具、系统实用程序，以及替换性能关键 C/C++ 组件的项目。

### 总结时间线

- **2015年末** → Andrew Kelley 开始私有开发
- **2016年2月8日** → 公开公告 & 第一篇博客文章
- **2016–2019** → 早期采用，comptime 成为杀手级特性
- **2019年5月** → "The Road to Zig 1.0" 演讲
- **2020–2022** → Ziglings，社区增长
- **2023** → 自托管编译器转型（重大里程碑）
- **2024–2025** → 增量编译工作，重点打磨 & 错误修复
- **2025年11月** → 仓库迁移至 Codeberg
- **2026** → 向 1.0 持续进展（无固定日期，质量优先方法）

Zig 的历史反映了一种罕见的组合：一个单人业余项目成长为一个严肃的、有资金支持、社区支持的语言，并采取非常审慎、耐心通往稳定性的道路。

References:

- [https://en.wikipedia.org/wiki/Zig_(programming_language)](https://en.wikipedia.org/wiki/Zig_(programming_language))
- [https://andrewkelley.me/post/intro-to-zig.html](https://andrewkelley.me/post/intro-to-zig.html)
- [https://ziglang.org](https://ziglang.org) (official site – check /news for recent updates)
